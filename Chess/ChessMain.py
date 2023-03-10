import sys
import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8 #Chiều 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        #p.image.load: tải hình ảnh
        #p.transform.scale: thay đổi tỉ lệ hình ảnh
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock() #Đồng hồ đếm thời gian chuyển động
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Kiểm tra xem đã di chuyển quân cờ
    animate = False #Kiểm tra khi nào thì animate 1 nước đi

    loadImages()
    running = True
    sqSelected = () #Không có ô vuông nào được chọn, theo dõi ô vuông được nhấn (row, col)
    playerClicks = [] #Theo dõi thao tác click chuột của người chơi
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Xử lý chuột
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #(x,y) vị trí chuột
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col): #Nhấn lại ô vuông đó lần nữa
                        sqSelected = () #Bỏ chọn ô vuông
                        playerClicks = [] #Xóa bỏ thao tác người chơi
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #Ghi lại 2 lần nhấn để di chuyển quân
                    if len(playerClicks) == 2: #Sau khi nhấn lần 2
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMoved(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #Reset
                                playerClicks = [] #Reset
                        if not moveMade:
                            playerClicks = [sqSelected]
            #Xử lý phím
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMoved()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")

        p.display.flip()
        clock.tick(MAX_FPS) #Giới hạn fps
    p.quit()
    sys.exit()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #khi đến lượt nào chỉ quân màu đó được highlight
            #highlight ô được chọn
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #Làm mờ màu đi từ 0 -> 255
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight ô gợi ý
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #Vẽ ô vuông
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #Vẽ quân cờ

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r + c) % 2] #Màu ô vuông: chẵn là trắng, lẻ là đen
            p.draw.rect(screen, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #Vẽ hình lên screen

def drawPieces(screen, board):
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #Vẽ hình có sẵn lên screen

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #Khung hình để di chuyển trong 1 ô
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #Xóa quân ở ô đang đi đến
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #Vẽ quân bị bắt ở ô cuối
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #Vẽ quân đang di chuyển
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 64, True, False)
    textObject = font.render(text, 0, p.Color('Blue'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()