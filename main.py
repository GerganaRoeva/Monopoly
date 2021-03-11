import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

background = pygame.image.load('board.png')
background = pygame.transform.scale(background, (1000, 1000))

white_color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
# dark shade of the button 
color_dark = (100,100,100) 

width = screen.get_width()  
height = screen.get_height() 
  
front = pygame.font.SysFont('Corbel',35) 
  
# rendering a text written in this font 
text = front.render('Roll dice' , True , white_color)

button_dice = (width/5, height/3)

running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #checks if a mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the button roll dice
            if button_dice[0] <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                pass

    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if width/5 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/5,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/5,height/2,140,40]) 
      
    # superimposing the text onto our button 
    screen.blit(text , (width/5,height/2)) 

    pygame.display.update()
