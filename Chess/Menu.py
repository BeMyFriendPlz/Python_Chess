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
        self.cl_sound = p.mixer.Sound("Chess/Audio/click_sound.mp3")
        # self.cl_sound.set_volume(0.25)
        self.audio_check = "ON"

    def draw(self, Screen):
        font = p.font.SysFont("freesansbold.ttf", 30)
        p.draw.rect(self.button, "light gray", (0, 0, self.button.get_width(), self.button.get_height()), 0, 0)
        p.draw.rect(self.button, "dark gray", (0, 0, self.button.get_width(), self.button.get_height()), 5, 0)
        text = font.render(self.text, True, "black")
        self.button.blit(text, (self.button.get_width() / 2 - text.get_width() / 2, 
                                self.button.get_height() / 2 - text.get_height() / 2))
        Screen.blit(self.button, (self.pos[0] - self.button.get_width() / 2, 
                                      self.pos[1] - self.button.get_height() / 2))
        f = open("Chess/audio_sound.txt", "r")
        self.audio_check = f.read().split()
        f.close()
    
    def check_clicked(self):
        if self.rect.collidepoint(p.mouse.get_pos()):
            if p.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if self.audio_check[2] == "ON" and self.audio_check[0] == "ON":
                    self.cl_sound.play()
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

def drawOptions():
    font_txt = p.font.SysFont("arial", 40, True, False)
    display_text(Screen, "Total Sound:", (SCREEN_WIDTH / 2 - 356 + 100, SCREEN_HEIGHT / 7 - 23 + 80), font_txt, 'white')
    display_text(Screen, "Music Sound:", (SCREEN_WIDTH / 2 - 356 + 100, SCREEN_HEIGHT / 7 - 23 + 180), font_txt, 'white')
    display_text(Screen, "Menu Sound:", (SCREEN_WIDTH / 2 - 356 + 100, SCREEN_HEIGHT / 7 - 23 + 280), font_txt, 'white')
    display_text(Screen, "Game Sound:", (SCREEN_WIDTH / 2 - 356 + 100, SCREEN_HEIGHT / 7 - 23 + 380), font_txt, 'white')

    Total_Sound_button.draw(Screen)
    Music_Sound_button.draw(Screen)
    Menu_Sound_button.draw(Screen)
    Game_Sound_button.draw(Screen)

    Back_button = Button("BACK", (95, 65), 100, 40)
    Back_button.draw(Screen)
    if Back_button.check_clicked():
        Options_button.clicked = False
        return 0
    else:
        return 3

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

    f = open("Chess/audio_sound.txt", "r")
    Total_sound, Music_sound, Menu_sound, Game_sound = f.read().split()
    f.close()

    Total_Sound_button = Button(Total_sound, (SCREEN_WIDTH / 2 - 356 + 550, SCREEN_HEIGHT / 7 - 23 + 103), 100, 40)
    Music_Sound_button = Button(Total_sound if Total_sound == "OFF" else Music_sound, (SCREEN_WIDTH / 2 - 356 + 550, SCREEN_HEIGHT / 7 - 23 + 203), 100, 40)
    Menu_Sound_button = Button(Total_sound if Total_sound == "OFF" else Menu_sound, (SCREEN_WIDTH / 2 - 356 + 550, SCREEN_HEIGHT / 7 - 23 + 303), 100, 40)
    Game_Sound_button = Button(Total_sound if Total_sound == "OFF" else Game_sound, (SCREEN_WIDTH / 2 - 356 + 550, SCREEN_HEIGHT / 7 - 23 + 403), 100, 40)

    #Thêm music background
    bg_music = p.mixer.Sound("Chess/Audio/background_music.mp3")
    if Music_sound == "ON" and Total_sound == "ON":
        bg_music.play(loops=-1)
        bg_music.set_volume(0.2)

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
                menu_command = drawOptions()
            elif menu_command == 4:
                menu_command = drawAbout()
            elif menu_command == 5:
                run = False
        
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if Total_Sound_button.check_clicked():
                    Total_sound = "OFF" if Total_sound == "ON" else "ON"
                    Total_Sound_button.text = Total_sound
                    Music_Sound_button.text = Total_sound if Total_sound == "OFF" else Music_sound
                    if Music_sound == "ON" and Total_sound == "ON":
                        bg_music.play(loops=-1)
                    else:
                        bg_music.stop()
                    Menu_Sound_button.text = Total_sound if Total_sound == "OFF" else Menu_sound
                    Game_Sound_button.text = Total_sound if Total_sound == "OFF" else Game_sound
                    Total_Sound_button.clicked = False
                elif Music_Sound_button.check_clicked():
                    Music_sound = "OFF" if Music_sound == "ON" else "ON"
                    Music_Sound_button.text = Music_sound
                    if Music_sound == "ON" and Total_sound == "ON":
                        bg_music.play(loops=-1)
                    else:
                        bg_music.stop()
                    Music_Sound_button.clicked = False
                elif Menu_Sound_button.check_clicked():
                    Menu_sound = "OFF" if Menu_sound == "ON" else "ON"
                    Menu_Sound_button.text = Menu_sound
                    Menu_Sound_button.clicked = False
                elif Game_Sound_button.check_clicked():
                    Game_sound = "OFF" if Game_sound == "ON" else "ON"
                    Game_Sound_button.text = Game_sound
                    Game_Sound_button.clicked = False
                f = open("Chess/audio_sound.txt", "w")
                f.write("{} {} {} {}".format(Total_sound, Music_sound, Menu_sound, Game_sound))
                f.close()
        
        p.display.flip()

    p.quit()
    sys.exit()