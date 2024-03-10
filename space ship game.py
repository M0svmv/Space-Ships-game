import pygame
import os
pygame.font.init()
pygame.mixer.init()
wide, high = 900, 500
window = pygame.display.set_mode((wide, high))
pygame.display.set_caption("first game!")
Lightsky_Blue = (135, 206, 250)
black = (0, 0, 0)
redc = (255, 0, 0)
yellowc = (255, 255, 0)
border = pygame.Rect(wide/2, 0, 10, high)
bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
spaceship_width, spaceship_height = 55, 40
FPS = 60
vel = 5
bullet_vel = 7
max_bullets = 10
health_font = pygame.font.SysFont('comicsans', 40)
win_font = pygame.font.SysFont('comicsans', 100)
space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (wide, high))
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2
yellow_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)),90)
red_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 270)


def movement(keys_pressed, red, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:  # left
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x + vel < (wide/2 - 40):  # right
        yellow.x += vel
    if keys_pressed[pygame.K_s] and yellow.y + vel < high-55:  # down
        yellow.y += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0:  # up
        yellow.y -= vel
    if keys_pressed[pygame.K_LEFT] and red.x - vel > (wide/2 + 10):  # left
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel < wide-40:  # right
        red.x += vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel < high-55:  # down
        red.y += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0:  # up
        red.y -= vel


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    window.blit(space, (0, 0))
    pygame.draw.rect(window, black, border)
    red_health_text = health_font.render("HEALTH : " + str(red_health), 1, Lightsky_Blue)
    yellow_health_text = health_font.render("HEALTH : " + str(yellow_health), 1, Lightsky_Blue)
    window.blit(red_health_text, (wide - red_health_text.get_width()-10, 10))
    window.blit(yellow_health_text, (10, 10))
    window.blit(yellow_spaceship, (yellow.x, yellow.y))
    window.blit(red_spaceship, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(window, redc, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(window, yellowc, bullet)
    pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > wide:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = win_font.render(text, 1, Lightsky_Blue)
    window.blit(draw_text,(wide/2 - draw_text.get_width()/2, high/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    yellow = pygame.Rect(80, 230, spaceship_width, spaceship_height)
    red = pygame.Rect(800, 230, spaceship_width, spaceship_height)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + spaceship_width, yellow.y + spaceship_height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x, red.y + spaceship_height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()
            if event.type == red_hit:
                bullet_hit_sound.play()
                red_health -= 1
            if event.type == yellow_hit:
                bullet_hit_sound.play()
                yellow_health -= 1



        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        movement(keys_pressed, red, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health)
    main()



main()


