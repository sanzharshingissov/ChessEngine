"""
Responsible for storing all the information about current the current state of a chess game,
determining the valid moves at the current state, keeping a move log.
"""
class GameState():
    def __init__(self):
        """
        board is 8x8 2d list, each element has 2 characters, first character is color,
        second is type of the piece, "--" is empty space
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRockMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.stalemate = False
        self.checkmate = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #coordinates of the square where enpassant is possible
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    """
    Takes a move as a parameter amd executes it(this wont work for castling, pawn promotion and en passant)"""
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove #swap players
        #update King's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol )
        else:
            self.enpassantPossible = ()

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]#moves the rook
                self.board[move.endRow][move.endCol + 1] = '--' #erase the old rock
            else: #queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] #moves the rook
                self.board[move.endRow][move.endCol - 2] = '--'

        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    """Undo the last move made"""
    def undoMove(self):
        if len(self.moveLog) != 0:#make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update King's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
            self.currentCastlingRight = self.castleRightsLog[-1] #set current castle rights to the last one in the list
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:#kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else: #queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'



    '''
    Update castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False


    """
    All moves considering checks
    """

    def getValidMoves(self):

        moves = []
        self.inCheck, self.checks, self.pins = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # To block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # enemy piece causing the check
                validSquares = []  # squares that pieces can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)  # check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:  # once you get to the piece end checks
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K':  # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:  # move doesn't block check or capture piece
                                moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check, so all moves are fine
            moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)


        return moves


    '''
    Determine if the current player is in check
    '''

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])




    '''
    Determine if the enemy cn attack the square r, c
    '''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opp's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False

    """
    Returns if the player is in check, a list of pins, a list of checks
    """

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outward from king for pins and checks, keep track of pins
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else: #2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        #5 possibilities in this complex conditional
                        #1. orthogonally away from king and piece is a rock
                        #2. diagonally away from king and piece is a bishop
                        #3. 1 square diagonally away from king and piece is a pawn
                        #4. any direction and piece is a queen
                        #5. any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0<= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6<=j<=7) or (enemyColor == 'b' and 4<=j<=5))) or \
                                (type == 'Q') or (type == 'K' and i == 1):
                            if possiblePin == (): #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:#enemy piece not applying check
                            break
                else:
                    break #off board
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #enemy knight attacking king
                    inCheck = True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck, checks, pins


    """
    All moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves


    """
    Get all the pawn/rock/bishop/knight/king/queen moves for the pawn locacted at row, col and add these moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white pawns moves
            if self.board[r-1][c] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r, c),(r - 1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == "b": #capturing enemy piece
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == "b": #capturing enemy piece
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else: #black pawns moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r, c),(r + 1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                        moves.append(Move((r, c), (r + 2, c), self.board))

            if c-1 >= 0: #captures to the left
                if self.board[r+1][c-1][0] == "w": #capturing enemy piece
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))

            if c+1 <= 7: #captures to the right
                if self.board[r+1][c+1][0] == "w": #capturing enemy piece
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))


    def getRockMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #cant remove queen from pin on rock moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up,left,down,right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #max move-7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    if not piecePinned or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break # this break ends inner for loop, end forces program to check another direction
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  #(empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  #diagonal moves
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #max move-7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    if not piecePinned or pinDirection == (-d[0], -d[1]) or pinDirection == d:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break  # this break ends inner for loop, end forcs program to check another direction
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRockMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    # Place king in end square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    # Place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)


    """
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves
    """

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return #cant castle while in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)


    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))


    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

     ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
     rowsToRanks = {v: k for k, v in ranksToRows.items()}
     filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
     colsToFiles = {v: k for k, v in filesToCols.items()}

     def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove=False): #using optional parameter for en passant
         self.startRow = startSq[0]
         self.startCol = startSq[1]
         self.endRow = endSq[0]
         self.endCol = endSq[1]
         self.pieceMoved = board[self.startRow][self.startCol]
         self.pieceCaptured = board[self.endRow][self.endCol]
         self.castle = isCastleMove
         self.enpassant = isEnpassantMove
         #pawn promotion
         self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
         #en passant
         self.isEnpassantMove = isEnpassantMove
         if self.isEnpassantMove:
             self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'


         self.isCapture = self.pieceCaptured != '--'
         #castle move
         self.isCastleMove = isCastleMove

         self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


     """
     Overriding the equals method
     """

     def __eq__(self, other):
         if isinstance(other, Move):
             return self.moveID == other.moveID
         return False

     def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

     def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


     def __str__(self):
         #castle move
         if self.castle:
             return 'O-O' if self.endCol == 6 else 'O-O-O'

         endSquare = self.getRankFile(self.endRow, self.endCol)

         #pawn moves
         if self.pieceMoved[1] == 'p':
             if self.isCapture:
                 return self.colsToFiles[self.startCol] + 'x' + endSquare
             else:
                 return endSquare

         #piece moves
         moveString = self.pieceMoved[1]
         if self.isCapture:
             moveString += 'x'
         return moveString + endSquare






