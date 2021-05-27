import pygame
import os
from data import fonts
from data import colors


# Клас за игрално поле
class GameSpace:
    def __init__(self, id, x, y, sp_type=''):
        self.id = id
        self.type = sp_type
        self.x = x
        self.y = y


# За бъдеще
class Property(GameSpace):
    def __init__(self, id, x, y, group, name, tier=0):
        GameSpace.__init__(self, id, x, y, "Property")
        self.owned_by = None
        self.houses = 0
        self.group = group
        self.price = 0
        self.rent = 0
        self.name = name
        self.can_build = False
        self.can_sell = False
        self.mortgaged = False
        self.hitbox = pygame.Rect(x, y, 0, 0)
        if group == "brown":
            self.hitbox = pygame.Rect(x - 35, y - 65, 70, 130)
            self.house_price = 50
            self.price = 60
            if tier:
                self.rent = [4, 20, 60, 180, 320, 450]
            else:
                self.rent = [2, 10, 30, 90, 160, 250]
        elif group == "blue":
            self.hitbox = pygame.Rect(x - 35, y - 65, 70, 130)
            self.house_price = 50
            if tier:
                self.price = 120
                self.rent = [8, 40, 100, 300, 450, 600]
            else:
                self.price = 100
                self.rent = [6, 30, 90, 270, 400, 550]
        elif group == "pink":
            self.hitbox = pygame.Rect(x - 65, y - 35, 130, 70)
            self.house_price = 100
            if tier:
                self.price = 160
                self.rent = [12, 60, 180, 500, 700, 900]
            else:
                self.price = 140
                self.rent = [10, 50, 150, 450, 625, 750]
        elif group == "orange":
            self.hitbox = pygame.Rect(x - 65, y - 35, 130, 70)
            self.house_price = 100
            if tier:
                self.price = 200
                self.rent = [16, 80, 220, 600, 800, 1000]
            else:
                self.price = 180
                self.rent = [14, 70, 200, 550, 700, 900]
        elif group == "red":
            self.hitbox = pygame.Rect(x - 35, y - 65, 70, 130)
            self.house_price = 150
            if tier:
                self.price = 240
                self.rent = [20, 100, 300, 750, 925, 1100]
            else:
                self.price = 220
                self.rent = [18, 90, 250, 700, 875, 1050]
        elif group == "yellow":
            self.hitbox = pygame.Rect(x - 35, y - 65, 70, 130)
            self.house_price = 150
            if tier:
                self.price = 280
                self.rent = [24, 120, 360, 850, 1025, 1200]
            else:
                self.price = 260
                self.rent = [22, 110, 330, 800, 975, 1150]
        elif group == "green":
            self.hitbox = pygame.Rect(x - 65, y - 35, 130, 70)
            self.house_price = 200
            if tier:
                self.price = 320
                self.rent = [28, 150, 450, 1000, 1200, 1400]
            else:
                self.price = 300
                self.rent = [26, 130, 390, 900, 110, 1275]
        elif group == "purple":
            self.hitbox = pygame.Rect(x - 65, y - 35, 130, 70)
            self.house_price = 200
            if tier:
                self.price = 400
                self.rent = [50, 200, 600, 1400, 1700, 2000]
            else:
                self.price = 350
                self.rent = [35, 175, 500, 1100, 1300, 1500]

    def show_houses(self, screen):
        rotate_angle = 0
        hx = self.x
        hy = self.y
        bhx = 0
        bhy = 0

        if self.group == "brown" or self.group == "blue":
            rotate_angle = 0
            hx -= 35
            hy -= 65
            bhx = 15
        elif self.group == "pink" or self.group == "orange":
            rotate_angle = 270
            hx += 35
            hy -= 35
            bhy = 15
        elif self.group == "red" or self.group == "yellow":
            rotate_angle = 180
            hx -= 35
            hy += 35
            bhx = 15
        elif self.group == "green" or self.group == "purple":
            rotate_angle = 90
            hx -= 65
            hy -= 35
            bhy = 15

        for i in range(self.houses):
            if self.houses < 5:
                house = pygame.image.load(os.path.join('data', 'Assets', 'house.png'))
                house = pygame.transform.scale(house, (20, 30))
                house = pygame.transform.rotate(house, rotate_angle)
                screen.blit(house, (hx, hy))
                hx += bhx
                hy += bhy
            else:
                house = pygame.image.load(os.path.join('data', 'Assets', 'hotel.png'))
                house = pygame.transform.scale(house, (40, 30))
                house = pygame.transform.rotate(house, rotate_angle)
                screen.blit(house, (hx, hy))

    def is_hovering(self, pos):
        if self.hitbox.collidepoint(pos):
            return True
        else:
            return False


class Station(GameSpace):
    pass


class Chance(GameSpace):
    def __init__(self, id, x, y, cards):
        GameSpace.__init__(self, id, x, y, "Chest")
        self.cards = cards


class Card:
    def __init__(self, text, effect):
        self.text = text
        self.effect = effect

# Всички карти
chest_cards = [Card] * 16
chance_cards = [Card] * 16
card1 = Card("Продължи към начало!", 1)
chest_cards[0] = card1
chance_cards[0] = card1
card2 = Card("Банкова грешка в твоя полза. Вземи 200!", 2)
chest_cards[1] = card2
card3 = Card("Сметки за доктор. Плати 50!", 3)
chest_cards[2] = card3
card4 = Card("Крипто валутите най-накрая се отплатиха! Вземи 50!", 4)
chest_cards[3] = card4
card5 = Card("Отиди в затвора!", 5)
chest_cards[4] = card5
chance_cards[7] = card5
card6 = Card("Припомняш си за стари дългове. Вземи 50 от всеки играч!", 6)
chest_cards[5] = card6
card7 = Card("Спечели в казиното! Вземи 100!", 7)
chest_cards[6] = card7
card8 = Card("Възстановяване на данък върху дохода. Вземи 20!", 8)
chest_cards[7] = card8
card9 = Card("Днес е твоят рожден ден! Вземи 10 от всеки играч!", 9)
chest_cards[8] = card9
card10 = Card("Застраховката се отплаща! Вземи 150!", 10)
chest_cards[9] = card10
card11 = Card("Болнични сметки. Плати 50!", 3)
chest_cards[10] = card11
card12 = Card("Училищни сметки. Плати 50!", 3)
chest_cards[11] = card12
card13 = Card("Получаваш пари от просене! Вземи 25!", 11)
chest_cards[12] = card13
card14 = Card("Спечели състезание по надяждане! Вземи 10!", 12)
chest_cards[13] = card14
card15 = Card("Получаваш наследство! Вземи 100!", 7)
chest_cards[14] = card15
card16 = Card("Такси за ремонт! 40 за всяка къща и 115 за всеки хотел, които притежаваш!", 13)
chest_cards[15] = card16
chance_cards[1] = card16
card17 = Card("Продължи до Редута!", 14)
chance_cards[2] = card17
card18 = Card("Продължи до Студентски град!", 15)
chance_cards[3] = card18
card19 = Card("Ограбваш пияница. Вземи 50!", 4)
chance_cards[4] = card19
card20 = Card("Върни се с 3 места назад!", 16)
chance_cards[5] = card20
chance_cards[15] = card20
chance_cards[14] = card20
card21 = Card("Минувач те пребива нощем и те обира. Загуби 15!", 17)
chance_cards[6] = card21
card22 = Card("Продължи до Иван Вазов!", 18)
chance_cards[8] = card22
card23 = Card("Намираш банкоти на пода! Получи 25!", 11)
chance_cards[9] = card23
card24 = Card("Изтърка билетче и спечели малка награда! Получи 100!", 7)
chance_cards[10] = card24
card25 = Card("Скамна лапе през ОЛХ! Получи 150!", 10)
chance_cards[11] = card25
card26 = Card("Продължи до Люлин 5", 19)
chance_cards[12] = card26
card27 = Card("Скамнаха те в наргиле бар! Загуби 50!", 3)
chance_cards[13] = card27


# Всички полета:
spaces = [None] * 40
go = GameSpace(0, 925, 925)
spaces[0] = go
brown1 = Property(1, 825, 925, "brown", "Люлин 5")
spaces[1] = brown1
cchest1 = Chance(2, 740, 925, chest_cards)
spaces[2] = cchest1
brown2 = Property(3, 660, 925, "brown", "Дружба 1", 1)
spaces[3] = brown2
tax1 = GameSpace(4, 580, 925)
spaces[4] = tax1
station1 = GameSpace(5, 500, 925)
spaces[5] = station1
blue1 = Property(6, 420, 925, "blue", "Надежда 2")
spaces[6] = blue1
chance1 = Chance(7, 340, 925, chance_cards)
spaces[7] = chance1
blue2 = Property(8, 260, 925, "blue", "Кранса Поляна")
spaces[8] = blue2
blue3 = Property(9, 175, 925, "blue", "Хаджи Димитър", 1)
spaces[9] = blue3
jail = GameSpace(10, 75, 925)
spaces[10] = jail
pink1 = Property(11, 75, 825, "pink", "Подуене")
spaces[11] = pink1
elec = GameSpace(12, 75, 740)
spaces[12] = elec
pink2 = Property(13, 75, 660, "pink", "Овча Купел")
spaces[13] = pink2
pink3 = Property(14, 75, 580, "pink", "Студентски Град", 1)
spaces[14] = pink3
station2 = GameSpace(15, 75, 500)
spaces[15] = station2
orange1 = Property(16, 75, 420, "orange", "Гоце Делчев")
spaces[16] = orange1
cchest2 = Chance(17, 75, 340, chest_cards)
spaces[17] = cchest2
orange2 = Property(18, 75, 260, "orange", "Бъкстон")
spaces[18] = orange2
orange3 = Property(19, 75, 175, "orange", "Сердика", 1)
spaces[19] = orange3
free = GameSpace(20, 75, 75)
spaces[20] = free
red1 = Property(21, 175, 75, "red", "Слатина")
spaces[21] = red1
chance2 = Chance(22, 260, 75, chance_cards)
spaces[22] = chance2
red2 = Property(23, 340, 75, "red", "Красно Село")
spaces[23] = red2
red3 = Property(24, 420, 75, "red", "Редута", 1)
spaces[24] = red3
station3 = GameSpace(25, 500, 75)
spaces[25] = station3
yellow1 = Property(26, 580, 75, "yellow", "Гео Милев")
spaces[26] = yellow1
yellow2 = Property(27, 660, 75, "yellow", "Горна Баня")
spaces[27] = yellow2
water = GameSpace(28, 740, 75)
spaces[28] = water
yellow3 = Property(29, 825, 75, "yellow", "Център", 1)
spaces[29] = yellow3
go_to_jail = GameSpace(30, 925, 75)
spaces[30] = go_to_jail
green1 = Property(31, 925, 175, "green", "Яворов")
spaces[31] = green1
green2 = Property(32, 925, 260, "green", "Младост 2")
spaces[32] = green2
cchest3 = Chance(33, 925, 340, chest_cards)
spaces[33] = cchest3
green3 = Property(34, 925, 420, "green", "Изток", 1)
spaces[34] = green3
station4 = GameSpace(35, 925, 500)
spaces[35] = station4
chance3 = Chance(36, 925, 580, chance_cards)
spaces[36] = chance3
purple1 = Property(37, 925, 660, "purple", "Лозенец")
spaces[37] = purple1
tax2 = GameSpace(38, 925, 740)
spaces[38] = tax2
purple2 = Property(39, 925, 825, "purple", "Иван Вазов", 1)
spaces[39] = purple2
