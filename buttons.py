from colors import *
from fonts import *


# Клас за бутон да не правим всеки бутон отделно
class Button:
    def __init__(self, color, text_color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.hitbox = pygame.Rect(x, y, width, height)  # Може да се използва ако искаме да използваме функции от pygame.Rect

    def show_button(self, screen, outline_color, font):
        # Прави бутона да се изборазява.
        pygame.draw.rect(screen, outline_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_hovering(self, pos):
        # Проверява дали мишката е върху бутона
        # Pos е координатите на мишката
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Бутони се създават тук:
quit_button = Button(red, darker_red, 340, 200, 100, 60, 'Quit')
two_players_button = Button(gray, black, 400, 520, 200, 100, 'Two Players')
three_players_button = Button(gray, black, 400, 630, 200, 100, 'Three Players')
four_players_button = Button(gray, black, 400, 740, 200, 100, 'Four Players')
dice_button = Button(gray, black, 400, 420, 200, 100, 'Roll Dice')
end_turn_button = Button(gray, black, 700, 780, 150, 75, 'End Turn')
pay_jail_button = Button(gray, black, 425, 600, 150, 75, 'Pay Escape')


# Функция за промяна на цвета на всички бутони
def mouse_hovering(event, pos):
    if event.type == pygame.MOUSEMOTION:
        if quit_button.is_hovering(pos):
            quit_button.color = dark_red
        else:
            quit_button.color = red

    if event.type == pygame.MOUSEMOTION:
        if two_players_button.is_hovering(pos):
            two_players_button.color = dark_gray
        else:
            two_players_button.color = gray

    if event.type == pygame.MOUSEMOTION:
        if three_players_button.is_hovering(pos):
            three_players_button.color = dark_gray
        else:
            three_players_button.color = gray

    if event.type == pygame.MOUSEMOTION:
        if four_players_button.is_hovering(pos):
            four_players_button.color = dark_gray
        else:
            four_players_button.color = gray

    if event.type == pygame.MOUSEMOTION:
        if dice_button.is_hovering(pos):
            dice_button.color = dark_gray
        else:
            dice_button.color = gray

    if event.type == pygame.MOUSEMOTION:
        if pay_jail_button.is_hovering(pos):
            pay_jail_button.color = dark_gray
        else:
            pay_jail_button.color = gray

    if event.type == pygame.MOUSEMOTION:
        if end_turn_button.is_hovering(pos):
            end_turn_button.color = dark_gray
        else:
            end_turn_button.color = gray
