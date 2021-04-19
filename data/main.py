

import os
import importlib
import random
import pygame
# Направих ги на отделни файлове, защото е грозно
from data import buttons
from data import gamespaces
from data import audio
from data import colors
from data import fonts

pygame.init()

# За да може да ги сменяме и използваме по-лесно и да не е нужно да
# ги повтаряме по късно
winHeight = 1000
winWidth = 1000

screen = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Monopoly")

# Прекръстих го на поле да няма обърквания.
board = pygame.image.load(os.path.join('data', 'Assets', 'board.png'))
board = pygame.transform.scale(board, (1000, 1000))

# не са във функцията, защото искам да са статик
current_player = 0
dice = [0, 0]
players = list()
mouse_pos = (0, 0)
audio_on = True
checked = False
buying = False


# Клас за играч, по-късно ще будат добавени още неща като списък с имоти
class Player:
    def __init__(self, id, money=2000, stepped_on=gamespaces.go):
        self.id = id
        self.stepped_on = stepped_on
        self.money = money
        self.is_in_jail = False
        self.monopolist = False
        self.jail_counter = 0
        self.loser = False
        self.owning = []
        self.all_from_group = []


def is_monopolist(player):
    need = 3
    duplicates = []
    
    for space in player.owning:
        if space.group == "brown" or space.group == "purple":
            need = 2

        for another_space in player.owning:
            if(space.group == another_space.group):
                duplicates.append(another_space)
        
            if len(duplicates) == need:
                # monopolist = True
                if space.group not in player.all_from_group:
                    player.all_from_group.append(space.group)
                player.monopolist = True

def is_in_jail(player):
    if player.jail_counter == 3:
        player.is_in_jail = True
        player.jail_counter = 0

def went_bankrupt(player):
    if player.money < 0:
        player.loser = True

# Използва се за циклични проверки на състоянието на играча
def player_check(player, event, throws):
    
    is_in_jail(player)

    if player.is_in_jail:
        player.stepped_on = gamespaces.jail
        if throws == 3:
            player.is_in_jail = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttons.pay_jail_button.is_hovering(mouse_pos):
                player.money -= 50
                player.is_in_jail = False

    went_bankrupt(player)

    is_monopolist(player)

    



# Проверява какво представлява полето, на което играча е стъпил
# по - късно ще пълно пълни с различни действия за всички видове полета
def gamespace_check(gamespace, player):
    global checked
    global buying
    if gamespace.id == 30 or gamespace == gamespaces.go_to_jail:
        player.stepped_on = gamespaces.jail
        player.is_in_jail = True

    if not checked:
        if gamespace.id == 4 or gamespace == gamespaces.tax1:
            player.money -= 200
        elif gamespace.id == 38 or gamespace == gamespaces.tax2:
            player.money -= 100
        elif gamespace.type == "Property":
            if not gamespace.owned_by:
                buying = True
            else:
                player.money -= gamespace.rent[gamespace.houses]
                gamespace.owned_by.money += gamespace.rent[gamespace.houses]
    checked = True



# Изобразява подадения играч
def draw_player(player):
    if not player.loser:
        if player.id == 1:
            p1 = pygame.image.load(os.path.join('data', 'Assets', 'p1.png'))
            p1 = pygame.transform.scale(p1, (30, 30))
            screen.blit(p1, (player.stepped_on.x - 15, player.stepped_on.y - 15))
        elif player.id == 2:
            p2 = pygame.image.load(os.path.join('data', 'Assets', 'p2.png'))
            p2 = pygame.transform.scale(p2, (30, 30))
            screen.blit(p2, (player.stepped_on.x, player.stepped_on.y - 15))
        elif player.id == 3:
            p3 = pygame.image.load(os.path.join('data', 'Assets', 'p3.png'))
            p3 = pygame.transform.scale(p3, (30, 30))
            screen.blit(p3, (player.stepped_on.x - 15, player.stepped_on.y))
        elif player.id == 4:
            p4 = pygame.image.load(os.path.join('data', 'Assets', 'p4.png'))
            p4 = pygame.transform.scale(p4, (30, 30))
            screen.blit(p4, (player.stepped_on.x, player.stepped_on.y))
        pass

def choose_bild(player):
    can_bild = []
    from_one_color = []
    houses_in_group = 0

    for color in player.all_from_group:
        for space in gamespaces.spaces:
            if space.type == "Property":
                from_one_color.append(space)
                if(len(from_one_color) == 2 and (color == "brown" or color == "purple")):
                    break
                elif (len(from_one_color) == 3):
                    break

        for space in from_one_color:
            houses_in_group += space.houses
        
        if(color == "brown" or color == "purple"):
            can_bild.append(from_one_color[0])
            can_bild.append(from_one_color[1])

            if(can_bild[0].houses > can_bild[1].houses):
                can_bild.remove(can_bild[0])
            if(can_bild[0].houses < can_bild[1].houses):
                can_bild.remove(can_bild[1])
        else:
            can_bild.append(from_one_color[0])
            can_bild.append(from_one_color[1])
            can_bild.append(from_one_color[2])

            if(can_bild[0].houses > can_bild[1].houses):
                can_bild.remove(can_bild[0])
            if(can_bild[0].houses < can_bild[1].houses):
                can_bild.remove(can_bild[1])
            if(can_bild[1].houses < can_bild[2].houses):
                can_bild.remove(can_bild[1])
            if(can_bild[1].houses > can_bild[2].houses):
                can_bild.remove(can_bild[2])
            if(can_bild[2].houses < can_bild[0].houses):
                can_bild.remove(can_bild[2])
            if(can_bild[2].houses > can_bild[0].houses):
                can_bild.remove(can_bild[0])

    gamespace_to_bild = None
    flag = True

    while(flag != False):
        for gamespace in can_bild:
            if gamespace.is_hovering(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gamespace_to_bild = gamespace
                    flag = False

    rotate_angle = 0
    if gamespace_to_bild.group == "pink" or gamespace_to_bild.group == "orange":
        rotate_angle = 90
    if gamespace_to_bild.group == "red" or gamespace_to_bild.group == "yellow":
        rotate_angle = 180
    if gamespace_to_bild.group == "green" or gamespace_to_bild.group == "purple":
        rotate_angle = 270
            
    house = pygame.image.load(os.path.join('data', 'Assets', 'house.png'))
    house = pygame.transform.scale(house, (58, 77))

    house = pygame.transform.rotate(house, rotate_angle)
#         # new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    screen.blit(house, (170, 700))

    # for color in player.all_from_group:
    #     print(color)

    # house = pygame.image.load(os.path.join('data', 'Assets', 'house.png'))
    # house = pygame.transform.scale(house, (58, 77))
    # # house = pygame.transform.rotate(house, rotate_angle)
    # # new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    # screen.blit(house, (170, 700))
    # pygame.display.update()

    

    
def turn_displayer(player):
    colour = colors.black
    if player.id == 1:
        colour = colors.red
    elif player.id == 2:
        colour = colors.blue
    elif player.id == 3:
        colour = colors.yellow
    elif player.id == 4:
        colour = colors.dark_green
    moneytxt = fonts.calibri.render('Money: ' + str(player.money), True, colour)
    screen.blit(moneytxt, (175, 740))
    playertxt = fonts.calibri.render('Player: ' + str(player.id), True, colour)
    screen.blit(playertxt, (425, 740))
    pass


def property_info(gamespace):
    colour = colors.white
    if gamespace.is_hovering(mouse_pos):
        info_bg = pygame.image.load(os.path.join('data', 'Assets', 'info_bg.png'))
        info_bg = pygame.transform.scale(info_bg, (230, 400))
        screen.blit(info_bg, (620, 440))
        owner = "никой"
        if gamespace.owned_by:
            if gamespace.owned_by.id == 1:
                colour = colors.red
            elif gamespace.owned_by.id == 2:
                colour = colors.blue
            elif gamespace.owned_by.id == 3:
                colour = colors.yellow
            elif gamespace.owned_by.id == 4:
                colour = colors.dark_green
            owner = "Играч " + str(gamespace.owned_by.id)
        info1 = fonts.small_ariel.render("Имоти в " + str(gamespace.name), True, colors.white)
        info2 = fonts.small_ariel.render("Принадлежи на " + owner, True, colour)
        if not gamespace.owned_by:
            info3 = fonts.small_ariel.render("Цена: " + str(gamespace.price), True, colors.white)
        else:
            info3 = fonts.small_ariel.render("Наем: " + str(gamespace.rent[gamespace.houses]), True, colors.white)
        screen.blit(info1, (630, 450))
        screen.blit(info2, (630, 490))
        screen.blit(info3, (630, 530))


# Функция за изобразване за по-чист код и за да не се меша кода
def graphics(gamestart, player_list, rolled):
    global buying
    screen.fill(colors.white)

    # Dice roll и Money за момента се използват за дебъгване, по-късно
    # ще има различен, по-добър дисплей

    screen.blit(board, (0, 0))
    if gamestart:
        turn_displayer(player_list[current_player])

    # Изобразяване на зарчета
    if dice[0]:
        dice1txt = 'dice' + str(dice[0]) + '.png'
        dice1 = pygame.image.load(os.path.join('data', 'Assets', dice1txt))
        dice1 = pygame.transform.scale(dice1, (100, 100))
        screen.blit(dice1, (385, 390))
        dice2txt = 'dice' + str(dice[1]) + '.png'
        dice2 = pygame.image.load(os.path.join('data', 'Assets', dice2txt))
        dice2 = pygame.transform.scale(dice2, (100, 100))
        screen.blit(dice2, (495, 390))

    # Изобразява всички играчи
    for i in range(len(player_list)):
        draw_player(player_list[len(player_list) - 1 - i])

    # Изобрзаява бутоните
    buttons.quit_button.show_button(screen, colors.darker_red, fonts.calibri)
    buttons.audio_button.show_button(screen, colors.black, fonts.smaller_calibri)
    buttons.theme_button.show_button(screen, colors.black, fonts.smaller_calibri)
    if buying:
        buttons.buy_button.show_button(screen, colors.black, fonts.smaller_calibri)
        buttons.auction_button.show_button(screen, colors.black, fonts.smaller_calibri)
    # Проверява дали играта е почнала или сме в менюто
    if not gamestart:
        buttons.two_players_button.show_button(screen, colors.black, fonts.calibri)
        buttons.three_players_button.show_button(screen, colors.black, fonts.calibri)
        buttons.four_players_button.show_button(screen, colors.black, fonts.calibri)

    # Проверява дали играта е почнала или сме в менюто
    if gamestart:
        for i in range(40):
            if gamespaces.spaces[i].type == "Property":
                property_info(gamespaces.spaces[i])
        # Проверява дали играче е в затвора
        if player_list[current_player].is_in_jail:
            buttons.pay_jail_button.show_button(screen, colors.black, fonts.calibri)
        # Проверява дали зарчето е хвърлено
        if not rolled and not buying:
            buttons.dice_button.show_button(screen, colors.black, fonts.smaller_calibri)
        if rolled and not buying:
            if players[current_player].monopolist:
                buttons.bild_button.show_button(screen, colors.black, fonts.calibri)
            buttons.end_turn_button.show_button(screen, colors.black, fonts.calibri)
            

    # pygame.draw.circle(screen, colors.red, (75, 740), 2)
    # Използва се за намиране на кооринати

    pygame.display.update()


def max_check():
    global current_player
    global players
    if current_player == len(players):
        current_player = 0
    pass


def player_move(gamestart, rolled):
    global dice
    global current_player
    global players
    global audio_on
    global checked
    player = players[current_player]
    number = dice[0] + dice[1]
    while number > 0:
        if player.stepped_on.id + 1 == 40:
            player.stepped_on = gamespaces.go
            player.money += 200
            graphics(gamestart, players, rolled)
            if audio_on:
                audio.move_sound.play()
            number -= 1
            pygame.time.wait(300)
        player.stepped_on = gamespaces.spaces[player.stepped_on.id + 1]
        graphics(gamestart, players, rolled)
        if audio_on:
            audio.move_sound.play()
        number -= 1
        pygame.time.wait(200)
    checked = False


# Функция, за да може да се направи app init неща.
def run():
    # Променливи дефинирани извън цикъла
    frames_per_second = 60
    global dice
    global buying
    global current_player
    running = True
    clock = pygame.time.Clock()
    gamestart = False
    rolled = False
    global players
    global mouse_pos
    global audio_on
    throws = 0
    current_music = 0
    # losers = []
    audio.themes[current_music].play(-1)

    while running:

        # Проверява дали сме минали всички играчи и се връща на първия
        if gamestart:
            max_check()
        # Да има определен refresh rate, иначе цикъла ще върви колкото се
        # може повече и ще натоварва компютъра.
        clock.tick(frames_per_second)
        # Изобразява играта
        graphics(gamestart, players, rolled)
        # Координатите на мишката
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.quit_button.is_hovering(mouse_pos):
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.audio_button.is_hovering(mouse_pos):
                    if audio_on:
                        audio_on = False
                        pygame.mixer.pause()
                    else:
                        audio_on = True
                        pygame.mixer.unpause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.theme_button.is_hovering(mouse_pos):
                    if current_music == 4:
                        current_music = -1
                    current_music += 1
                    pygame.mixer.stop()
                    audio.themes[current_music].play(-1)

            # Проверява дали сме в менюто и прави определн брой играчи при
            # натискане на бутон
            if not gamestart:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons.two_players_button.is_hovering(mouse_pos):
                        player1 = Player(1)
                        player2 = Player(2)
                        players = [player1, player2]
                        gamestart = True
                    if buttons.three_players_button.is_hovering(mouse_pos):
                        player1 = Player(1)
                        player2 = Player(2)
                        player3 = Player(3)
                        players = [player1, player2, player3]
                        gamestart = True
                    if buttons.four_players_button.is_hovering(mouse_pos):
                        player1 = Player(1)
                        player2 = Player(2)
                        player3 = Player(3)
                        player4 = Player(4)
                        players = [player1, player2, player3, player4]
                        gamestart = True

            # Проверява дали играта е почнала. Това е секцията за хвърляне
            # на зар, местене на играча и действия при попаднало поле
            if gamestart:
                # Циклични проверки
                max_check()
                gamespace_check(players[current_player].stepped_on, players[current_player])
                player_check(players[current_player], event, throws)

                # Проверява дали зарчето е хвърлено
                if not rolled:
                    if buying:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.buy_button.is_hovering(mouse_pos):
                                players[current_player].stepped_on.owned_by = players[current_player]
                                players[current_player].owning.append(players[current_player].stepped_on)
                                players[current_player].money -= players[current_player].stepped_on.price
                                buying = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.auction_button.is_hovering(mouse_pos):
                                buying = False
                        
                                

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons.dice_button.is_hovering(mouse_pos):
                            rolled = True
                            # dice[0] = random.randint(1, 6)
                            # dice[1] = random.randint(1, 6)
                            dice[0] = 0
                            dice[1] = 1
                            # При чифт
                            if dice[0] == dice[1]:
                                rolled = False
                                if players[current_player].is_in_jail:
                                    players[current_player].is_in_jail = False
                                else:
                                    players[current_player].jail_counter += 1
                                player_move(gamestart, rolled)
                                gamespace_check(players[current_player].stepped_on, players[current_player])
                                player_check(players[current_player], event, throws)
                            else:
                                if players[current_player].is_in_jail:
                                    throws += 1
                                else:
                                    player_move(gamestart, rolled)
                                gamespace_check(players[current_player].stepped_on, players[current_player])
                                player_check(players[current_player], event, throws)
                                players[current_player].jail_counter = 0
                else:
                    if buying:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.buy_button.is_hovering(mouse_pos):
                                players[current_player].stepped_on.owned_by = players[current_player]
                                players[current_player].owning.append(players[current_player].stepped_on)
                                players[current_player].money -= players[current_player].stepped_on.price
                                buying = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.auction_button.is_hovering(mouse_pos):
                                buying = False
                    # Използва се за свършване на хода, налага се, защото в
                    # момента бутона се рефрешва при задържане на мишката. Ще бъде оправено по-късно
                    # Това не е функционален проблем, а по скоро графичен,
                    # придобавяне на имоти ще има действия които се изпълняват между хвърления
                    # Което ще оправи порблема
                    # gamespace_check(players[current_player].stepped_on, players[current_player])
                    # player_check(players[current_player], event, throws)
                    if players[current_player].loser:
                        players.remove(players[current_player])

                    if players[current_player].monopolist:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.bild_button.is_hovering(mouse_pos):
                                choose_bild(players[current_player])
                                # pass


                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons.end_turn_button.is_hovering(mouse_pos):
                            current_player += 1
                            rolled = False

            buttons.mouse_hovering(event, mouse_pos)
