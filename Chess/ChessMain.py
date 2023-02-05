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

    loadImages()
    running = True
    sqSelected = () #Không có ô vuông nào được chọn, theo dõi ô vuông được nhấn (row, col)
    playerClicks = [] #Theo dõi thao tác click chuột của người chơi
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Xử lý chuột
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    if move in validMoves:
                        gs.makeMoved(move)
                        moveMade = True
                    sqSelected = () #Reset
                    playerClicks = [] #Reset
            #Xử lý phím
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMoved()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        p.display.flip()
        clock.tick(MAX_FPS) #Giới hạn fps
    p.quit()
    sys.exit()

def drawGameState(screen, gs):
    drawBoard(screen) #Vẽ ô vuông
    drawPieces(screen, gs.board) #Vẽ quân cờ

def drawBoard(screen):
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

if __name__ == "__main__":
    main()