# Изтрих ти старите коментари, защото заедно с моите заемат много място

import os
import importlib
import random
# Направих ги на отделни файлове, защото е грозно
from buttons import *
from gamespaces import *

pygame.init()

# За да може да ги сменяме и използваме по-лесно и да не е нужно да
# ги повтаряме по късно
winHeight = 1000
winWidth = 1000

screen = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Monopoly")

# Прекръстих го на поле да няма обърквания.
board = pygame.image.load(os.path.join('Assets', 'board.png'))
board = pygame.transform.scale(board, (winWidth, winHeight))


# Клас за играч, по-късно ще будат добавени още неща като списък с имоти
class Player:
    def __init__(self, id, money):
        self.id = id
        self.stepped_on = go
        self.money = money
        self.is_in_jail = False
        self.jail_counter = 0
        self.jail_tries = 0
        self.loser = False


# Използва се за циклични проверки на състоянието на играча
def player_check(player, event, rolled):
    if player.jail_counter == 3:
        player.is_in_jail = True
        player.jail_counter == 0

    if player.is_in_jail:
        player.stepped_on = jail
        if player.jail_tries == 3:
            player.is_in_jail = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pay_jail_button.isHovering(mouse_pos):
                player.money -= 50
                player.is_in_jail = False

    if player.money < 0:
        player.loser = True


# Изобразява подадения играч
def draw_player(player):
    if player.id == 1:
        p1 = pygame.image.load(os.path.join('Assets', 'p1.png'))
        p1 = pygame.transform.scale(p1, (30, 30))
        screen.blit(p1, (player.stepped_on.x - 15, player.stepped_on.y - 15))
    elif player.id == 2:
        p2 = pygame.image.load(os.path.join('Assets', 'p2.png'))
        p2 = pygame.transform.scale(p2, (30, 30))
        screen.blit(p2, (player.stepped_on.x, player.stepped_on.y - 15))
    elif player.id == 3:
        p3 = pygame.image.load(os.path.join('Assets', 'p3.png'))
        p3 = pygame.transform.scale(p3, (30, 30))
        screen.blit(p3, (player.stepped_on.x - 15, player.stepped_on.y))
    elif player.id == 4:
        p4 = pygame.image.load(os.path.join('Assets', 'p4.png'))
        p4 = pygame.transform.scale(p4, (30, 30))
        screen.blit(p4, (player.stepped_on.x, player.stepped_on.y))
    pass


# Проверява какво представлява полето, на което играча е стъпил
# по - късно ще пълно пълни с различни действия за всички видове полета
def gamespace_check(gamespace, player):
    if gamespace.id == 30 or gamespace == go_to_jail:
        player.stepped_on = jail
        player.is_in_jail = True


# Функция за изобразване за по-чист код и за да не се меша кода
def graphics(gamestart, player_list, rolled):
    screen.fill((0, 0, 0))

    # Dice roll и Money за момента се използват за дебъгване, по-късно
    # ще има различен, по-добър дисплей
    movetxt = calibri.render('Dice roll: ' + str(move), True, blue)
    screen.blit(board, (0, 0))
    screen.blit(movetxt, (700, 740))
    if gamestart:
        moneytxt = calibri.render('Money: ' + str(player_list[current_player].money), True, red)
        screen.blit(moneytxt, (175, 740))

    # Изобразява всички играчи
    for i in range(len(player_list)):
        draw_player(player_list[len(player_list) - 1 - i])

    # Изобрзаява бутоните
    quit_button.show_button(screen, black, calibri)
    # Проверява дали играта е почнала или сме в менюто
    if not gamestart:
        two_players_button.show_button(screen, black, calibri)
        three_players_button.show_button(screen, black, calibri)
        four_players_button.show_button(screen, black, calibri)

    # Проверява дали играта е почнала или сме в менюто
    if gamestart:
        # Проверява дали играче е в затвора
        if player_list[current_player].is_in_jail:
            pay_jail_button.show_button(screen, black, calibri)
        # Проверява дали зарчето е хвърлено
        if not rolled:
            dice_button.show_button(screen, black, calibri)
        if rolled:
            end_turn_button.show_button(screen, black, calibri)

    # pygame.draw.circle(screen, red, (75, 740), 2)
    # Използва се за намиране на кооринати

    pygame.display.update()


# не са във функцията, защото искам да са статик
current_player = 0
move = 0
players = list()
losers = list()
mouse_pos = (0, 0)


# Функция, за да може да се направи app init неща.
def run():
    # Променливи дефинирани извън цикъла
    frames_per_second = 60
    global move
    global current_player
    running = True
    clock = pygame.time.Clock()
    gamestart = False
    rolled = False
    global players
    global mouse_pos
    # losers = []

    while running:

        # Проверява дали сме минали всички играчи и се връща на първия
        if gamestart:
            if current_player == len(players):
                current_player = 0
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
                if quit_button.isHovering(mouse_pos):
                    running = False

            # Проверява дали сме в менюто и прави определн брой играчи при
            # натискане на бутон
            if not gamestart:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if two_players_button.isHovering(mouse_pos):
                        player1 = Player(1, 2000)
                        player2 = Player(2, 2000)
                        players = [player1, player2]
                        gamestart = True
                    if three_players_button.isHovering(mouse_pos):
                        player1 = Player(1, 2000)
                        player2 = Player(2, 2000)
                        player3 = Player(3, 2000)
                        players = [player1, player2, player3]
                        gamestart = True
                    if four_players_button.isHovering(mouse_pos):
                        player1 = Player(1, 2000)
                        player2 = Player(2, 2000)
                        player3 = Player(3, 2000)
                        player4 = Player(4, 2000)
                        players = [player1, player2, player3, player4]
                        gamestart = True

            # Проверява дали играта е почнала. Това е секцията за хвърляне
            # на зар, местене на играча и действия при попаднало поле
            if gamestart:

                if current_player == len(players):
                    current_player = 0
                # Циклични проверки
                gamespace_check(players[current_player].stepped_on, players[current_player])
                player_check(players[current_player], event, rolled)

                # Проверява дали зарчето е хвърлено
                if not rolled:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if dice_button.isHovering(mouse_pos):
                            rolled = True
                            dice1 = 6
                            dice2 = 4
                            move = dice1 + dice2
                            # При чифт
                            if dice1 == dice2:
                                rolled = False
                                if players[current_player].is_in_jail:
                                    players[current_player].is_in_jail = False
                                else:
                                    players[current_player].jail_counter += 1
                                if players[current_player].stepped_on.id + move >= 40:
                                    move -= 40
                                    players[current_player].money += 200
                                players[current_player].stepped_on = spaces[players[current_player].stepped_on.id + move]
                            else:
                                if players[current_player].stepped_on.id + move >= 40:
                                    move -= 40
                                    players[current_player].money += 200
                                players[current_player].stepped_on = spaces[players[current_player].stepped_on.id + move]
                                gamespace_check(players[current_player].stepped_on, players[current_player])
                                players[current_player].jail_counter = 0
                else:
                    # Използва се за свършване на хода, налага се, защото в
                    # момента бутона се рефрешва при задържане на мишката. Ще бъде оправено по-късно
                    # Това не е функционален проблем, а по скоро графичен,
                    # придобавяне на имоти ще има действия които се изпълняват между хвърления
                    # Което ще оправи порблема
                    gamespace_check(players[current_player].stepped_on, players[current_player])
                    player_check(players[current_player], event, rolled)
                    if players[current_player].loser:
                        players.remove(players[current_player])
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_turn_button.isHovering(mouse_pos):
                            current_player += 1
                            rolled = False

            mouseHovering(event, mouse_pos)
