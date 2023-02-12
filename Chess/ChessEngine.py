class GameState():
    def __init__(self):
        #Bàn cờ 8x8 với ma trận 2 chiều
        #'--' là chỗ trống để các quân di chuyển
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True #Trắng đi trước
        self.moveLog = [] #Nhật ký bàn cờ ghi lại các nước cờ di chuyển

    def makeMoved(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #Ghi lại các nước cờ
            self.whiteToMove = not self.whiteToMove #Chuyển người chơi

    def undoMoved(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range (len(self.board)):
            for c in range (len(self.board[r])):
                turn = self.board[r][c][0] #Quân trắng hay quân đen
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #Tốt trắng di chuyển
            if r-1 >= 0 and self.board[r-1][c] == '--': #1 ô phía trước trống?
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 ô phía trước trống?
                    moves.append(Move((r, c), (r-2, c), self.board))
            if r-1 >= 0 and c-1 >= 0: #Tốt bắt trái
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if r-1 >= 0 and c+1 <= 7: #Tốt bắt phải
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: #Tốt đen di chuyển
            if r+1 <= 7 and self.board[r+1][c] == '--': #1 ô phía trước trống?
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--': #2 ô phía trước trống?
                    moves.append(Move((r, c), (r+2, c), self.board))
            if r+1 <= 7 and c-1 >= 0: #Tốt bắt trái
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if r+1 <= 7 and c+1 <= 7: #Tốt bắt phải
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #Lên, trái, xuống, phải
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #Trên bàn cờ
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #Ô trống được đi
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Ăn quân địch
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Quân mình thì bị chặn không đi được
                        break
                else: #Ngoài bàn cờ
                    break

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #Trên bàn cờ
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Ô trống hoặc quân địch
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #Trên bàn cờ
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #Ô trống được đi
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Ăn quân địch
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Quân mình thì bị chặn không đi được
                        break
                else: #Ngoài bàn cờ
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range (8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #Trên bàn cờ
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Ô trống hoặc quân địch
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
