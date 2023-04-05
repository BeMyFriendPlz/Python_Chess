import sys
import pygame as p
from Menu import Button
import ChessEngine,SmartMoveFinder
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH= 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # Chiều 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

class Piece_Button:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos
        self.piece = p.Surface((SQ_SIZE, SQ_SIZE))
        self.rect = self.piece.get_rect()
        self.rect.topleft = (self.pos[0] - self.piece.get_width() / 2 + 306, 
                             self.pos[1] - self.piece.get_height() / 2 + 218.5)
        self.clicked = False

    def draw(self, Screen):
        # p.draw.rect(self.piece, "light gray", (0, 0, self.piece.get_width(), self.piece.get_height()), 0, 0)
        # p.draw.rect(self.piece, "dark gray", (0, 0, self.piece.get_width(), self.piece.get_height()), 5, 0)
        p.draw.rect(self.piece, "purple", (0, 0, self.piece.get_width(), self.piece.get_height()))
        self.piece.blit(self.image, (0, 0))
        Screen.blit(self.piece, (self.pos[0] - self.piece.get_width() / 2, 
                                      self.pos[1] - self.piece.get_height() / 2))
    
    def check_clicked(self):
        if self.rect.collidepoint(p.mouse.get_pos()):
            if p.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if p.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked

class ChessMain:
    def loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            # p.image.load: tải hình ảnh
            # p.transform.scale: thay đổi tỉ lệ hình ảnh
            IMAGES[piece] = p.transform.scale(p.image.load("Chess/Pieces_Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    def choosePawnPromotion(self, gs, move, Screen):
        run = True
        while run:
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
            surf = p.Surface((300, 275))
            p.draw.rect(surf, "purple", (0, 0, surf.get_width(), surf.get_height()), 0, 0)
            p.draw.rect(surf, "dark gray", (0, 0, surf.get_width(), surf.get_height()), 5, 0)
            font = p.font.SysFont("freesansbold.ttf", 35)
            text = font.render("Promote pawn to:", True, "black")
            surf.blit(text, (10, 10))
            
            Queen_Button = Piece_Button(IMAGES[move.pieceMoved[0] + 'Q'], (75, 100))
            Queen_Button.draw(surf)
            Rook_Button = Piece_Button(IMAGES[move.pieceMoved[0] + 'R'], (75, 200))
            Rook_Button.draw(surf)
            Bishop_Button = Piece_Button(IMAGES[move.pieceMoved[0] + 'B'], (225, 100))
            Bishop_Button.draw(surf)
            Knight_Button = Piece_Button(IMAGES[move.pieceMoved[0] + 'N'], (225, 200))
            Knight_Button.draw(surf)
            
            if Queen_Button.check_clicked():
                gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
                run = False
            elif Rook_Button.check_clicked():
                gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'R'
                run = False
            elif Bishop_Button.check_clicked():
                gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'B'
                run = False
            elif Knight_Button.check_clicked():
                gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'N'
                run = False

            self.gameScreen.blit(surf, (self.gameScreen.get_width() / 2 - surf.get_width() / 2,
                                         self.gameScreen.get_height() / 2 - surf.get_height() / 2))
            Screen.blit(self.gameScreen, (75, 100))
            p.display.flip()
            # for event in p.event.get():
            #     if(event.type == p.KEYDOWN):
            #         if(event.key == p.K_q):
            #             gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
            #             run=False
            #         elif(event.key == p.K_r):
            #             gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'R'
            #             run=False
            #         elif(event.key == p.K_b):
            #             gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'B'
            #             run=False
            #         elif(event.key == p.K_k):
            #             gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'N'
            #             run=False

    def __init__(self, singlePlayer, Screen):
        p.init()
        self.gameScreen = p.Surface((BOARD_WIDTH+MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
        clock = p.time.Clock()  # Đồng hồ đếm thời gian chuyển động
        self.gameScreen.fill(p.Color("white"))
        moveLogFont = p.font.SysFont("Arial",12, False,False)
        gs = ChessEngine.GameState()
        validMoves = gs.getValidMoves()
        moveMade = False  # Kiểm tra xem đã di chuyển quân cờ
        animate = False  # Kiểm tra khi nào thì animate 1 nước đi

        f = open("Chess/audio_sound.txt", "r")
        self.audio_check = f.read().split()
        f.close()

        self.loadImages()
        sqSelected = ()  # Không có ô vuông nào được chọn, theo dõi ô vuông được nhấn (row, col)
        playerClicks = []  # Theo dõi thao tác click chuột của người chơi
        gameOver = False
        if singlePlayer:
            playerOne = True # nếu người chơi màu trắng thì sẽ đúng, nếu AI đang chơi thì sai
            playerTwo = False # giống trên nhưng với màu đen
        else:
            playerOne = True # nếu người chơi màu trắng thì sẽ đúng, nếu AI đang chơi thì sai
            playerTwo = True # giống trên nhưng với màu đen
        AIThingking = False
        moveFinderProcess = None
        moveUndone = False

        #Tạo Button
        Back_button = Button("BACK", (200, 50), 100, 40)
        NewGame_button = Button("NEW", (450, 50), 100, 40)
        Undo_button = Button("UNDO", (700, 50), 100, 40)

        #Thêm game sound
        move_sound = p.mixer.Sound("Chess/Audio/move_sound.mp3")
        # move_sound.set_volume(0.25)
        capture_sound = p.mixer.Sound("Chess/Audio/capture_sound.mp3")
        # capture_sound.set_volume(0.25)
        check_sound = p.mixer.Sound("Chess/Audio/check_sound.mp3")
        # check_sound.set_volume(0.25)
        checkmate_sound = p.mixer.Sound("Chess/Audio/checkmate_sound.mp3")
        # checkmate_sound.set_volume(0.25)
        stalemate_sound = p.mixer.Sound("Chess/Audio/stalemate_sound.mp3")
        # stalemate_sound.set_volume(0.25)

        while True:
            Back_button.draw(Screen)
            NewGame_button.draw(Screen)
            Undo_button.draw(Screen)
            if Back_button.check_clicked():
                break

            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # Xử lý chuột
                elif e.type == p.MOUSEBUTTONDOWN:
                    #Kiểm tra Button
                    if Undo_button.check_clicked():
                        gs.undoMoved()
                        moveMade = True
                        animate = False
                        gameOver = False
                        if AIThingking:
                            moveFinderProcess.terminate()
                            AIThingking = False
                        moveUndone = True
                        Undo_button.clicked = False
                    elif NewGame_button.check_clicked():
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        if AIThingking:
                            moveFinderProcess.terminate()
                            AIThingking = False
                        moveUndone = False
                        NewGame_button.clicked = False

                    if not gameOver and humanTurn:
                        location = p.mouse.get_pos()  # (x,y) vị trí chuột
                        col = (location[0] - 75) // SQ_SIZE
                        row = (location[1] - 100) // SQ_SIZE
                        if col < 0 or col > 7: continue
                        if row < 0 or row > 7: continue
                        if sqSelected == (row, col) or col >= 8 :  # Nhấn lại ô vuông đó lần nữa
                            sqSelected = ()  # Bỏ chọn ô vuông
                            playerClicks = []  # Xóa bỏ thao tác người chơi
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)  # Ghi lại 2 lần nhấn để di chuyển quân
                        if len(playerClicks) == 2:  # Sau khi nhấn lần 2
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMoved(validMoves[i])
                                    if move.isPawnPromotion:
                                        if humanTurn:
                                            self.choosePawnPromotion(gs, move, Screen)
                                        else:
                                            gs.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()  # Reset
                                    playerClicks = []  # Reset
                            if not moveMade:
                                playerClicks = [sqSelected]
                # Xử lý phím
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gs.undoMoved()
                        moveMade = True
                        animate = False
                        gameOver = False
                        if AIThingking:
                            moveFinderProcess.terminate()
                            AIThingking = False
                        moveUndone = True

                    if e.key == p.K_r:
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        if AIThingking:
                            moveFinderProcess.terminate()
                            AIThingking = False
                        moveUndone = False

            #Chuyển động của AI
            if not gameOver and not humanTurn and not moveUndone:
                if not AIThingking:
                    AIThingking = True
                    print("Thingking...")
                    returnQueue = Queue()#Truyền dữ liệu giữa các luồng
                    moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args=(gs, validMoves, returnQueue))
                    moveFinderProcess.start() # gọi findBestMove(gs, validMoves, returnQueue)
                if not moveFinderProcess.is_alive():
                    print("done thingking")
                    AIMove = returnQueue.get()
                    if AIMove is None:
                        AIMove = SmartMoveFinder.findRandomMove(validMoves)
                    gs.makeMoved(AIMove)
                    moveMade = True
                    animate = True
                    AIThingking = False

            if moveMade:
                if animate:
                    self.animateMove(gs.moveLog[-1], Screen, gs.board, clock)
                validMoves = gs.getValidMoves()

                if not moveUndone and self.audio_check[3] == "ON" and self.audio_check[0] == "ON":
                    if gs.checkmate:
                        checkmate_sound.play()
                    elif gs.stalemate:
                        stalemate_sound.play()
                    elif gs.inCheck():
                        check_sound.play()
                    elif (not humanTurn and AIMove.pieceCaptured != "--") or (humanTurn and move.pieceCaptured != "--"):
                        capture_sound.play()
                    else:
                        move_sound.play()

                moveMade = False
                animate = False
                moveUndone = False

            self.drawGameState(self.gameScreen, gs, validMoves, sqSelected, moveLogFont)
            Screen.blit(self.gameScreen, (75, 100))

            if gs.checkmate or gs.stalemate:
                gameOver = True
                self.drawEndGameText(Screen,'Stalement' if gs.stalemate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')
            p.display.flip()
            clock.tick(MAX_FPS)  # Giới hạn fps
    
    def drawGameState(self, screen, gs, validMoves, sqSelected, moveLogFont):
        self.drawBoard(screen)  # Vẽ ô vuông
        self.highlightSquares(screen, gs, validMoves, sqSelected)
        self.drawPieces(screen, gs.board)  # Vẽ quân cờ
        self.drawMoveLog(screen,gs,moveLogFont)

    def drawBoard(self, screen):
        global colors
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[(r + c) % 2]  # Màu ô vuông: chẵn là trắng, lẻ là đen
                p.draw.rect(screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Vẽ hình lên screen

    def highlightSquares(self, screen, gs, validMoves, sqSelected):
        if sqSelected != ():
            r, c = sqSelected
            if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # khi đến lượt nào chỉ quân màu đó được highlight
                # highlight ô được chọn
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # Làm mờ màu đi từ 0 -> 255
                s.fill(p.Color('blue'))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
                # highlight ô gợi ý
                s.fill(p.Color('green'))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
        #Highlight vua nếu bị chiếu
        if gs.inCheck():
            r, c = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # Làm mờ màu đi từ 0 -> 255
            s.fill(p.Color('red'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


    def drawPieces(self, screen, board):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece != '--':
                    screen.blit(IMAGES[piece], (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Vẽ hình có sẵn lên screen

    def drawMoveLog(self, screen,gs,font):
        moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
        p.draw.rect(screen, p.Color("black"),moveLogRect)
        moveLog= gs.moveLog
        moveTexts = []
        for i in range(0,len(moveLog),2):
            moveString = str(i//2 + 1)+". "+ str(moveLog[i])+" "
            if i + 1 < len(moveLog): # đảm bảo quân đen đã thực hiện 1 nước đi
                moveString += str(moveLog[i+1])+"   "
            moveTexts.append(moveString)

        movesPerRow = 3

        padding = 5
        textY = padding
        lineSpacing = 2
        for i in range(0, len(moveTexts), movesPerRow):
            text = ""
            for j in range(movesPerRow):
                if i + j < len(moveTexts):
                    text += moveTexts[i+j]
            textObject = font.render(text, True, p.Color('white'))
            textLocation = moveLogRect.move(padding,textY)
            screen.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing

    def animateMove(self, move, Screen, board, clock):
        global colors
        dR = move.endRow - move.startRow
        dC = move.endCol - move.startCol
        framesPerSquare = 10  # Khung hình để di chuyển trong 1 ô
        frameCount = (abs(dR) + abs(dC)) * framesPerSquare
        for frame in range(frameCount + 1):
            r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
            self.drawBoard(self.gameScreen)
            self.drawPieces(self.gameScreen, board)
            # Xóa quân ở ô đang đi đến
            color = colors[(move.endRow + move.endCol) % 2]
            endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(self.gameScreen, color, endSquare)
            # Vẽ quân bị bắt ở ô cuối
            if move.pieceCaptured != '--':
                if move.isEnpassantMove:
                    enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                    endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                self.gameScreen.blit(IMAGES[move.pieceCaptured], endSquare)
            # Vẽ quân đang di chuyển
            if move.pieceMoved != '--':
                self.gameScreen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            Screen.blit(self.gameScreen, (75, 100))
            p.display.flip()
            clock.tick(60)

    def drawEndGameText(self, Screen, text):
        font = p.font.SysFont("Helvitca", 32, True, False)
        textObject = font.render(text, 0, p.Color('Gray'))
        textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                        BOARD_HEIGHT / 2 - textObject.get_height() / 2)
        self.gameScreen.blit(textObject, textLocation)
        textObject = font.render(text, 0, p.Color('Black'))
        self.gameScreen.blit(textObject, textLocation.move(2, 2))
        Screen.blit(self.gameScreen, (75, 100))
