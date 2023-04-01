import sys
import pygame as p
import Chess

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

class Button:
    def __init__(self, txt, pos, width, height):
        self.text = txt
        self.pos = pos
        self.button = p.Surface((width, height))
        self.rect = self.button.get_rect()
        self.rect.topleft = (self.pos[0] - self.button.get_width() / 2, 
                             self.pos[1] - self.button.get_height() / 2)
        self.clicked = False

    def draw(self, Screen):
        font = p.font.SysFont("freesansbold.ttf", 30)
        p.draw.rect(self.button, "light gray", (0, 0, self.button.get_width(), self.button.get_height()), 0, 0)
        p.draw.rect(self.button, "dark gray", (0, 0, self.button.get_width(), self.button.get_height()), 5, 0)
        text = font.render(self.text, True, "black")
        self.button.blit(text, (self.button.get_width() / 2 - text.get_width() / 2, 
                                self.button.get_height() / 2 - text.get_height() / 2))
        Screen.blit(self.button, (self.pos[0] - self.button.get_width() / 2, 
                                      self.pos[1] - self.button.get_height() / 2))
    
    def check_clicked(self):
        if self.rect.collidepoint(p.mouse.get_pos()):
            if p.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if p.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked

def display_text(surface, text, pos, font, color):
    collection = [word.split(" ") for word in text.splitlines()]
    space = font.size(' ')[0]
    x, y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= SCREEN_WIDTH - 20:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def drawMenu():
    Menu_Image = p.transform.scale(p.image.load("Chess/Menu_Images/Menu.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    Screen.blit(Menu_Image, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    #Vẽ chữ
    font = p.font.SysFont("Inkfree", 150, True, False)
    text = font.render("Chess", 0, p.Color('Red'))
    Screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                                  SCREEN_HEIGHT / 7 - text.get_height() / 2))
    #Vẽ button tùy chọn
    SinglePlayer_button.draw(Screen)
    MultiPlayer_button.draw(Screen)
    Options_button.draw(Screen)
    About_button.draw(Screen)
    Exit_button.draw(Screen)
    if SinglePlayer_button.check_clicked():
        return 1
    elif MultiPlayer_button.check_clicked():
        return 2
    elif Options_button.check_clicked():
        return 3
    elif About_button.check_clicked():
        return 4
    elif Exit_button.check_clicked():
        return 5
    return 0

def drawSinglePlayer():
    Screen.fill(p.Color('light blue'))
    Chess.ChessMain(True, Screen)
    SinglePlayer_button.clicked = False
    return 0 
    
def drawMultiPlayer():
    Screen.fill(p.Color('light blue'))
    Chess.ChessMain(False, Screen)
    MultiPlayer_button.clicked = False
    return 0 

def drawAbout():
    font_title = p.font.SysFont("Inkfree", 60, True, False)
    text = font_title.render("Bai Tap Lon Python - D20ATTT", 0, p.Color('white'))
    Screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                                  SCREEN_HEIGHT / 7 - text.get_height() / 2))
    font_txt = p.font.SysFont("arial", 40, True, False)
    display_text(Screen, "Nhom 06:", (SCREEN_WIDTH / 2 - 356, SCREEN_HEIGHT / 7 - 23 + 90), font_txt, 'white')
    message = """Dang Quoc Cuong    B20DCAT020\nNguyen Xuan Hieu    B20DCAT060\nLe Duc Long              B20DCAT112\nTran Xuan Tien          B20DCAT160"""
    display_text(Screen, message, (SCREEN_WIDTH / 2 - 356 + 200, SCREEN_HEIGHT / 7 - 23 + 90), font_txt, 'white')
    font = p.font.SysFont("arial", 26, True, False)
    introduce = "The Game of Chess:\n          Chess, one of the oldest and most popular board games, played by two opponents on a checkered board with specially designed pieces of contrasting colours, commonly white and black. White moves first, after which the players alternate turns in accordance with fixed rules, each player attempting to force the opponent’s principal piece, the King, into checkmate-a position where it is unable to avoid capture."
    display_text(Screen, introduce, (34, SCREEN_HEIGHT / 7 - 23 + 300), font, 'white')
    Back_button = Button("BACK", (75, 35), 100, 40)
    Back_button.draw(Screen)
    if Back_button.check_clicked():
        About_button.clicked = False
        return 0
    else:
        return 4

if __name__ == "__main__":
    p.init()
    Screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    p.display.set_caption('Chess Game')
    icon = p.image.load("Chess/Menu_Images/Icon.png")
    p.display.set_icon(icon)
    menu_command = 0

    #Khởi tạo nút
    SinglePlayer_button = Button("SINGLE PLAYER", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5), 260, 40)
    MultiPlayer_button = Button("MULTI PLAYER", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5 + 65), 260, 40)
    Options_button = Button("OPTIONS", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5 + 65 * 2), 260, 40)
    About_button = Button("ABOUT", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5 + 65 * 3), 260, 40)
    Exit_button = Button("EXIT", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5 + 65 * 4), 260, 40)

    run = True
    while run:
        Screen.fill(p.Color("black"))
        if menu_command == 0:
            menu_command = drawMenu()
        else:
            if menu_command == 1:
                menu_command = drawSinglePlayer()
            elif menu_command == 2:
                menu_command = drawMultiPlayer()
            elif menu_command == 3:
                Options_button.clicked = False
                pass
            elif menu_command == 4:
                menu_command = drawAbout()
            elif menu_command == 5:
                run = False
        
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
        
        p.display.flip()
    p.quit()
    sys.exit()