import pygame


# Клас за игрално поле
class GameSpace:
    def __init__(self, id, x, y, sp_type=''):
        self.id = id
        self.type = sp_type
        self.x = x
        self.y = y


# За бъдеще
class Property(GameSpace):
    pass


class Station(GameSpace):
    pass


class CommunityChest(GameSpace):
    pass


class Chance(GameSpace):
    pass


# Всички полета:
spaces = [None] * 40
go = GameSpace(0, 925, 925)
spaces[0] = go
brown1 = GameSpace(1, 825, 925)
spaces[1] = brown1
cchest1 = GameSpace(2, 740, 925)
spaces[2] = cchest1
brown2 = GameSpace(3, 660, 925)
spaces[3] = brown2
tax1 = GameSpace(4, 580, 925)
spaces[4] = tax1
station1 = GameSpace(5, 500, 925)
spaces[5] = station1
blue1 = GameSpace(6, 420, 925)
spaces[6] = blue1
chance1 = GameSpace(7, 340, 925)
spaces[7] = chance1
blue2 = GameSpace(8, 260, 925)
spaces[8] = blue2
blue3 = GameSpace(9, 175, 925)
spaces[9] = blue3
jail = GameSpace(10, 75, 925)
spaces[10] = jail
pink1 = GameSpace(11, 75, 825)
spaces[11] = pink1
elec = GameSpace(12, 75, 740)
spaces[12] = elec
pink2 = GameSpace(13, 75, 660)
spaces[13] = pink2
pink3 = GameSpace(14, 75, 580)
spaces[14] = pink3
station2 = GameSpace(15, 75, 500)
spaces[15] = station2
orange1 = GameSpace(16, 75, 420)
spaces[16] = orange1
cchest2 = GameSpace(17, 75, 340)
spaces[17] = cchest2
orange2 = GameSpace(18, 75, 260)
spaces[18] = orange2
orange3 = GameSpace(19, 75, 175)
spaces[19] = orange3
free = GameSpace(20, 75, 75)
spaces[20] = free
red1 = GameSpace(21, 175, 75)
spaces[21] = red1
chance2 = GameSpace(22, 260, 75)
spaces[22] = chance2
red2 = GameSpace(23, 340, 75)
spaces[23] = red2
red3 = GameSpace(24, 420, 75)
spaces[24] = red3
station3 = GameSpace(25, 500, 75)
spaces[25] = station3
yellow1 = GameSpace(26, 580, 75)
spaces[26] = yellow1
yellow2 = GameSpace(27, 660, 75)
spaces[27] = yellow2
water = GameSpace(28, 740, 75)
spaces[28] = water
yellow3 = GameSpace(29, 825, 75)
spaces[29] = yellow3
go_to_jail = GameSpace(30, 925, 75)
spaces[30] = go_to_jail
green1 = GameSpace(31, 925, 75)
spaces[31] = green1
green2 = GameSpace(32, 925, 175)
spaces[32] = green2
cchest3 = GameSpace(33, 925, 260)
spaces[33] = cchest3
green3 = GameSpace(34, 925, 340)
spaces[34] = green3
station4 = GameSpace(35, 925, 420)
spaces[35] = station4
chance3 = GameSpace(36, 925, 500)
spaces[36] = chance3
purple1 = GameSpace(37, 925, 580)
spaces[37] = purple1
tax2 = GameSpace(38, 925, 660)
spaces[38] = tax2
purple2 = GameSpace(39, 925, 740)
spaces[39] = purple2
