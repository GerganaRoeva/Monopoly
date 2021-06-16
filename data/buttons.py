from data import colors
from data import fonts
import pygame


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
        # self.hitbox = pygame.Rect(x, y, width, height)  # Може да се използва ако искаме да използваме функции от pygame.Rect

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
quit_button = Button(colors.red, colors.darker_red, 280, 200, 100, 60, 'Quit')
two_players_button = Button(colors.gray, colors.black, 400, 530, 200, 100, 'Two Players')
three_players_button = Button(colors.gray, colors.black, 400, 640, 200, 100, 'Three Players')
four_players_button = Button(colors.gray, colors.black, 400, 750, 200, 100, 'Four Players')
dice_button = Button(colors.gray, colors.black, 390, 500, 200, 25, 'Roll Dice')
end_turn_button = Button(colors.gray, colors.black, 700, 780, 150, 75, 'End Turn')
pay_jail_button = Button(colors.gray, colors.black, 425, 530, 150, 75, 'Pay Escape')
audio_button = Button(colors.gray, colors.black, 150, 200, 120, 60, 'Audio ON/OFF')
theme_button = Button(colors.gray, colors.black, 740, 150, 120, 60, 'Change Music')
buy_button = Button(colors.gray, colors.black, 320, 680, 150, 50, 'Buy')
auction_button = Button(colors.gray, colors.black, 520, 680, 150, 50, 'Auction')
build_button = Button(colors.gray, colors.black, 420, 580, 150, 50, 'Build')
stop_build_button = Button(colors.gray, colors.black, 420, 680, 150, 50, 'Stop')
mortgage_button = Button(colors.gray, colors.black, 320, 610, 150, 50, 'Mortgage')
restore_button = Button(colors.gray, colors.black, 520, 610, 150, 50, 'Restore')
sell_button = Button(colors.gray, colors.black, 415, 740, 150, 50, 'Sell')
confirm_yes_button = Button(colors.gray, colors.black, 300, 450, 150, 75, 'YES')
confirm_no_button = Button(colors.gray, colors.black, 600, 450, 150, 75, 'NO')
okay_button = Button(colors.gray, colors.black, 420, 650, 150, 75, 'Okay')


# Функция за промяна на цвета на всички бутони
def mouse_hovering(event, pos):
    if event.type == pygame.MOUSEMOTION:
        if quit_button.is_hovering(pos):
            quit_button.color = colors.dark_red
        else:
            quit_button.color = colors.red

    if event.type == pygame.MOUSEMOTION:
        if two_players_button.is_hovering(pos):
            two_players_button.color = colors.dark_gray
        else:
            two_players_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if three_players_button.is_hovering(pos):
            three_players_button.color = colors.dark_gray
        else:
            three_players_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if four_players_button.is_hovering(pos):
            four_players_button.color = colors.dark_gray
        else:
            four_players_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if dice_button.is_hovering(pos):
            dice_button.color = colors.dark_gray
        else:
            dice_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if pay_jail_button.is_hovering(pos):
            pay_jail_button.color = colors.dark_gray
        else:
            pay_jail_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if end_turn_button.is_hovering(pos):
            end_turn_button.color = colors.dark_gray
        else:
            end_turn_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if audio_button.is_hovering(pos):
            audio_button.color = colors.dark_gray
        else:
            audio_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if theme_button.is_hovering(pos):
            theme_button.color = colors.dark_gray
        else:
            theme_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if buy_button.is_hovering(pos):
            buy_button.color = colors.dark_gray
        else:
            buy_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if auction_button.is_hovering(pos):
            auction_button.color = colors.dark_gray
        else:
            auction_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if build_button.is_hovering(pos):
            build_button.color = colors.dark_gray
        else:
            build_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if stop_build_button.is_hovering(pos):
            stop_build_button.color = colors.dark_gray
        else:
            stop_build_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if mortgage_button.is_hovering(pos):
            mortgage_button.color = colors.dark_gray
        else:
            mortgage_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if restore_button.is_hovering(pos):
            restore_button.color = colors.dark_gray
        else:
            restore_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if sell_button.is_hovering(pos):
            sell_button.color = colors.dark_gray
        else:
            sell_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if confirm_no_button.is_hovering(pos):
            confirm_no_button.color = colors.dark_gray
        else:
            confirm_no_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if confirm_yes_button.is_hovering(pos):
            confirm_yes_button.color = colors.dark_gray
        else:
            confirm_yes_button.color = colors.gray

    if event.type == pygame.MOUSEMOTION:
        if okay_button.is_hovering(pos):
            okay_button.color = colors.dark_gray
        else:
            okay_button.color = colors.gray



