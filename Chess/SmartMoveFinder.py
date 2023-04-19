import random

'''
Gắn giá trị điểm cho từng quân cờ
K: nhà vua, Q: quân hậu, R: quân xe, N: quân mã, p: quân tốt
'''


pieceScore = {"K": 0, "Q":10, "R":5, "N":3, "B":3, "p":1}

knightScore=[[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 2, 2, 2, 2, 2, 2, 1],
             [1, 2, 3, 3, 3, 3, 2, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 2, 3, 3, 3, 3, 2, 1],
             [1, 2, 2, 2, 2, 2, 2, 1],
             [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores =[[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rootScores=[[4, 3, 4, 4, 4, 4, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores =[[0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 0, 0, 1, 1, 1],
                  [1, 1, 2, 3, 3, 2, 1, 1],
                  [1, 2, 3, 4, 4, 3, 2, 1],
                  [2, 3, 3, 5, 5, 3, 3, 2],
                  [5, 6, 6, 7, 7, 6, 6, 5],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8]]
piecePositionScores ={"N": knightScore, "Q": queenScores, "B":bishopScores , "R":rootScores,
                      "bp":blackPawnScores, "wp":whitePawnScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


'''
Lấy và trả về bước đi ngẫu nhiên
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]#các bước đi hợp lệ

'''
Phương thức trợ giúp để thưc hiện lời gọi đệ quy đầu tiên
'''
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMoved(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMoved()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMoved(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMoved()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter +=1
    if depth ==0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMoved(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves,depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMoved()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #sắp xếp thứ tự di chuyển - thực hiện sau
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMoved(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves,depth-1,-beta,-alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move,score)
        gs.undoMoved()
        if maxScore > alpha: #nơi quá trình cắt tỉa xảy ra
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

'''
Một điểm số tích cực thì tốt cho quân trắng, quân trắng thắng, điểm trừ thì tốt cho quân đen
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE # quân đen thắng
        else:
            return CHECKMATE # quân trắng thắng
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #diem theo vi tri
                piecePositionScore = 0
                if square[1] !="K": #không có bảng vi trí cho vua
                    if square[1] == 'p': # cho quan tot
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: #quan co khac
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * .1

    return score


'''
Chấm điểm dựa trên material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
