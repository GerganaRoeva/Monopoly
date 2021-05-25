import os
import importlib
import random
import pygame

from data import buttons
from data import gamespaces
from data import audio
from data import colors
from data import fonts

pygame.init()

winHeight = 1000
winWidth = 1000

screen = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Monopoly")

board = pygame.image.load(os.path.join('data', 'Assets', 'board.png'))
board = pygame.transform.scale(board, (1000, 1000))

# не са във функцията, за да са статик
current_player = 0
dice = [0, 0]
players = list()
mouse_pos = (0, 0)
audio_on = True
checked = False
buying = False
building = False
restoring = False
mortgaging = False
selling = False


class Player:
    def __init__(self, id, money=2000, stepped_on=gamespaces.go):
        self.id = id
        self.stepped_on = stepped_on
        self.money = money
        self.is_in_jail = False
        self.jail_counter = 0
        self.loser = False
        self.owning = []
        self.monopolist = False


def is_monopolist(player, group):
    duplicates = []

    for space in player.owning:
        if space.group == "brown" or space.group == "purple":
            need = 2
        else:
            need = 3

        for another_space in player.owning:
            if space.group == another_space.group and space.group == group and space is not another_space:
                duplicates.append(another_space)

                if len(duplicates) == need:
                    for i in duplicates:
                        i.can_build = True
                    player.monopolist = True
                    duplicates.clear()
                    return True

    return False


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
                if not gamespace.mortgaged:
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


def choose_build(player):
    can_build = []
    from_one_color = []
    groups = ['blue', 'brown', 'pink', 'orange', 'red', 'yellow', 'green', 'purple']

    for group in groups:
        if is_monopolist(player, group):
            from_one_color.append(group)

    for i in gamespaces.spaces:
        if i.type == "Property" and i.can_build:
            can_build.append(i)

    for color in from_one_color:
        for i in range(len(can_build)):
            for j in range(len(can_build)):
                if can_build[i].group == color and can_build[j].group == color:
                    if can_build[i].houses > can_build[j].houses:
                        can_build[i].can_build = False

    return can_build

def choose_sell(player):
    can_sell = []
    from_one_color = []
    # count_houses = []

    for space in player.owning:
        if space.houses > 0:
            for i in range(len(player.owning)):
                if player.owning[i].group == space.group:
                    from_one_color.append(player.owning[i])

            if len(from_one_color) == 2:
                if(from_one_color[0].houses == from_one_color[1].houses):
                    can_sell.append(from_one_color[0])
                    can_sell.append(from_one_color[1])
                if(from_one_color[0].houses > from_one_color[1].houses):
                    can_sell.append(from_one_color[0])
                else:
                    can_sell.append(from_one_color[1])

            if len(from_one_color) == 3:
                if(from_one_color[0].houses > from_one_color[1].houses or from_one_color[0].houses > from_one_color[2].houses):
                    can_sell.append(from_one_color[0])
                if(from_one_color[1].houses > from_one_color[0].houses or from_one_color[1].houses > from_one_color[2].houses):
                    can_sell.append(from_one_color[1])
                if(from_one_color[2].houses > from_one_color[0].houses or from_one_color[2].houses > from_one_color[1].houses):
                    can_sell.append(from_one_color[2])
                if(from_one_color[0].houses == from_one_color[1].houses and from_one_color[2].houses == from_one_color[1].houses):
                    can_sell.append(from_one_color[0])
                    can_sell.append(from_one_color[1])
                    can_sell.append(from_one_color[2])

        from_one_color.clear()

    return can_sell          


def turn_displayer(player):
    global building
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
    screen.blit(moneytxt, (175, 800))
    playertxt = fonts.calibri.render('Player: ' + str(player.id), True, colour)
    screen.blit(playertxt, (425, 800))
    # montxt = fonts.calibri.render('Build: ' + str(building), True, colour)
    # screen.blit(montxt, (650, 740))
    pass


def property_info(gamespace):
    colour = colors.white
    if gamespace.is_hovering(mouse_pos):
        info_bg = pygame.image.load(os.path.join('data', 'Assets', 'info_bg.png'))
        info_bg = pygame.transform.scale(info_bg, (230, 400))
        info4 = fonts.ariel.render("", True, colors.white)
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
        if gamespace.mortgaged:
            info4 = fonts.ariel.render("ИПОТЕКИРАН", True, colors.white)
        screen.blit(info1, (630, 450))
        screen.blit(info2, (630, 490))
        screen.blit(info3, (630, 530))
        screen.blit(info4, (630, 600))



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
    # if rolled and bought:
    #     buttons.mortgage_button.show_button(screen, colors.black, fonts.smaller_calibri)

    # Проверява дали играта е почнала или сме в менюто
    if not gamestart:
        buttons.two_players_button.show_button(screen, colors.black, fonts.calibri)
        buttons.three_players_button.show_button(screen, colors.black, fonts.calibri)
        buttons.four_players_button.show_button(screen, colors.black, fonts.calibri)

    # Проверява дали играта е почнала или сме в менюто
    if gamestart:
        for i in gamespaces.spaces:
            if i.type == "Property":
                property_info(i)
                i.show_houses(screen)

        # Проверява дали играче е в затвора
        if player_list[current_player].is_in_jail:
            buttons.pay_jail_button.show_button(screen, colors.black, fonts.calibri)
        if ((not buying) and player_list[current_player].monopolist and (not building)):
            buttons.build_button.show_button(screen, colors.black, fonts.calibri)
        if building:
            buttons.stop_build_button.show_button(screen, colors.black, fonts.calibri)
        # Проверява дали зарчето е хвърлено
        if not rolled and not buying and not building:
            buttons.dice_button.show_button(screen, colors.black, fonts.smaller_calibri)
        if rolled and not buying and not building:
            buttons.end_turn_button.show_button(screen, colors.black, fonts.calibri)

        can_mortgage = False
        for space in player_list[current_player].owning:
            if not space.mortgaged and space.houses == 0:
                can_mortgage = True
        if rolled and can_mortgage and not mortgaging:
            buttons.mortgage_button.show_button(screen, colors.black, fonts.smaller_calibri)

        can_restor = False
        for space in player_list[current_player].owning:
            if space.mortgaged:
                can_restor = True
        if can_restor and rolled and not restoring:
            buttons.restor_button.show_button(screen, colors.black, fonts.smaller_calibri)

        can_sell = False
        for space in player_list[current_player].owning:
            if space.houses:
                can_sell = True
        if can_sell and rolled and not building: 
            buttons.sell_button.show_button(screen, colors.black, fonts.smaller_calibri)
        


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
    global building
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
    restoring = False
    mortgaging = False
    selling = False
    # losers = []
    audio.themes[current_music].play(-1)

    while running:

        # Проверява дали сме минали всички играчи и се връща на първия
        if gamestart:
            max_check()
            groups = ['blue', 'brown', 'pink', 'orange', 'red', 'yellow', 'green', 'purple']

            for group in groups:
                is_monopolist(players[current_player], group)

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
                    if players[current_player].monopolist and not building and not buying:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.build_button.is_hovering(mouse_pos):
                                building = True

                    if event.type == pygame.MOUSEBUTTONDOWN and buttons.restor_button.is_hovering(mouse_pos):
                        restoring = True

                    if event.type == pygame.MOUSEBUTTONDOWN and buttons.sell_button.is_hovering(mouse_pos):
                        selling = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons.mortgage_button.is_hovering(mouse_pos):
                            mortgaging = True

                    if building and not buying:
                        for i in gamespaces.spaces:
                            if (i.type == "Property" and (i in choose_build(players[current_player])) and i.can_build and i.houses < 5):
                                if i.is_hovering(mouse_pos):
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        players[current_player].money -= i.house_price
                                        i.houses += 1

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.stop_build_button.is_hovering(mouse_pos):
                                building = False

                    if players[current_player].owning and mortgaging:
                        for gamespace in players[current_player].owning:
                            if gamespace.is_hovering(mouse_pos) and not gamespace.houses :
                                if event.type == pygame.MOUSEBUTTONDOWN and not gamespace.mortgaged:
                                    gamespace.mortgaged = True
                                    players[current_player].money += gamespace.price/2
                                    mortgaging = False
                    if selling:
                        for space in players[current_player].owning:
                            if space.is_hovering(mouse_pos):
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if space in choose_sell(players[current_player]):
                                        space.houses -= 1
                                        players[current_player].money += space.house_price/2
                                        selling = False
                        
                    if players[current_player].owning and restoring:
                        for gamespace in players[current_player].owning:
                            if gamespace.is_hovering(mouse_pos) and gamespace.mortgaged:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    gamespace.mortgaged = False
                                    players[current_player].money -= (gamespace.price/2 + (gamespace.price/2)*10/100)
                                    restoring = False

                    if buying and not players[current_player].is_in_jail:
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

                    if event.type == pygame.MOUSEBUTTONDOWN and buttons.restor_button.is_hovering(mouse_pos):
                        restoring = True

                    if event.type == pygame.MOUSEBUTTONDOWN and buttons.sell_button.is_hovering(mouse_pos):
                        selling = True
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons.mortgage_button.is_hovering(mouse_pos):
                            mortgaging = True
                            
                    if players[current_player].monopolist and not building and not buying:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.build_button.is_hovering(mouse_pos):
                                building = True

                    if building and not buying:
                        for i in gamespaces.spaces:
                            if (i.type == "Property" and (i in choose_build(players[current_player])) and i.can_build and i.houses < 5):
                                if i.is_hovering(mouse_pos):
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        players[current_player].money -= i.house_price
                                        i.houses += 1

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons.stop_build_button.is_hovering(mouse_pos):
                                building = False
                    if selling:
                        for space in players[current_player].owning:
                            if space.is_hovering(mouse_pos):
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if space in choose_sell(players[current_player]):
                                        space.houses -= 1
                                        players[current_player].money += space.house_price/2
                                        selling = False                        

                    if players[current_player].owning and mortgaging:
                        for gamespace in players[current_player].owning:
                            if gamespace.is_hovering(mouse_pos) and not gamespace.houses:
                                if event.type == pygame.MOUSEBUTTONDOWN and not gamespace.mortgaged:
                                    gamespace.mortgaged = True
                                    players[current_player].money += gamespace.price/2
                                    mortgaging = False
                    
                    if players[current_player].owning and restoring:
                        for gamespace in players[current_player].owning:
                            if gamespace.is_hovering(mouse_pos) and gamespace.mortgaged:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    gamespace.mortgaged = False    
                                    players[current_player].money -= (gamespace.price/2 + (gamespace.price/2)*10/100)
                                    restoring = False 

                    if buying and not players[current_player].is_in_jail:
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
                    # при добавяне на имоти ще има действия които се изпълняват между хвърления
                    # Което ще оправи порблема
                    gamespace_check(players[current_player].stepped_on, players[current_player])
                    player_check(players[current_player], event, throws)
                    if players[current_player].loser:
                        players.remove(players[current_player])
                        if len(players) == 1:
                            running = False 

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons.end_turn_button.is_hovering(mouse_pos):
                            current_player += 1
                            rolled = False


            buttons.mouse_hovering(event, mouse_pos)
