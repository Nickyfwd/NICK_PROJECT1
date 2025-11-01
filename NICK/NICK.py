
import pygame, random, time, sys

pygame.init()
pygame.mixer.init()

# шрифт
f = pygame.font.Font('ofont.ru_FindSans Pro.ttf', 30)

# окно и базовые объекты
W, H = 1000, 1000
s = pygame.display.set_mode((W, H))
pygame.display.set_caption("Игра")
f = pygame.font.Font('ofont.ru_FindSans Pro.ttf', 30)
clock = pygame.time.Clock()

# звуки и музыка
try:
    pygame.mixer.music.load("Yan Cook — Inferno [PRRUKBLK056] (www.lightaudio.ru).mp3")
    pygame.mixer.music.play(-1)  # фоновая музыка играет бесконечно
except:
    print(" (Yan Cook — Inferno [PRRUKBLK056] (www.lightaudio.ru).mp3)")

try:
    coin_sound = pygame.mixer.Sound("mixkit-arcade-game-jump-coin-216.wav")
    hit_sound = pygame.mixer.Sound("mixkit-martial-arts-fast-punch-2047.wav")
except:
    coin_sound = hit_sound = None
    print("(mixkit-arcade-game-jump-coin-216.wav, mixkit-martial-arts-fast-punch-2047.wav)")

# игрок, враг и настройки
player = pygame.Rect(180, 180, 40, 40)
enemy = pygame.Rect(400, 100, 30, 30)
SPEED = 5
ex, ey = 4, 3
lives = 3
score = 0

# таймер
TIME_LIMIT = 60
end_time = time.time() + TIME_LIMIT

# монетки
COIN_TYPES = [((255, 215, 0), +1),
              ((0, 200, 0), +3),
              ((200, 50, 50), -2),
              ((0, 0, 255), +2),
              ((0, 0, 0), -5)]


def new_coin():
    (r, g, b), value = random.choice(COIN_TYPES)
    return {"pos": (random.randint(20, W - 20), random.randint(20, H - 20)),
            "color": (r, g, b),
            "value": value}


coins = [new_coin() for _ in range(3)]


# меню
def show_menu():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return  # начинаем игру

        s.fill((0, 0, 0))
        title = f.render("Собери монетки", True, (255, 255, 255))
        subtitle = f.render("Нажми ENTER для старта", True, (255, 255, 255))
        s.blit(title, (400, 360))
        s.blit(subtitle, (350, 400))
        pygame.display.flip()
        clock.tick(30)


# функция игры
def run_game():
    global score, lives, ex, ey
    score = 0
    lives = 3
    end_time = time.time() + TIME_LIMIT
    player.x, player.y = 180, 180
    enemy.x, enemy.y = 100, 100
    run = True
    reason = "time"

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # управление
        k = pygame.key.get_pressed()
        if k[pygame.K_a]:  player.x -= SPEED
        if k[pygame.K_d]: player.x += SPEED
        if k[pygame.K_w]:    player.y -= SPEED
        if k[pygame.K_s]:  player.y += SPEED

        # границы
        player.x = max(0, min(W - player.w, player.x))
        player.y = max(0, min(H - player.h, player.y))

        # движение врага
        enemy.x += ex
        enemy.y += ey
        if enemy.left <= 0 or enemy.right >= W: ex *= -1
        if enemy.top <= 0 or enemy.bottom >= H: ey *= -1

        # столкновение с врагом
        if player.colliderect(enemy):
            lives -= 1
            if hit_sound: hit_sound.play()
            player.x, player.y = 180, 180
            pygame.time.wait(300)
            if lives <= 0:
                reason = "lives"
                break

        # сбор монеток
        for c in coins:
            if player.collidepoint(c["pos"]):
                score += c["value"]
                if coin_sound: coin_sound.play()
                nc = new_coin()
                c["pos"], c["color"], c["value"] = nc["pos"], nc["color"], nc["value"]

        # отрисовка
        s.fill((30, 30, 30))
        pygame.draw.rect(s, (0, 200, 255), player)
        pygame.draw.rect(s, (255, 80, 80), enemy)
        for c in coins:
            pygame.draw.circle(s, c["color"], c["pos"], 10)

        t_left = max(0, int(end_time - time.time()))
        s.blit(f.render(f"Очки: {score}", True, (255, 255, 255)), (10, 10))
        s.blit(f.render(f"Жизни: {lives}", True, (255, 180, 180)), (10, 40))
        s.blit(f.render(f"Время: {t_left}", True, (200, 220, 255)), (10, 70))
        pygame.display.flip()
        clock.tick(60)

        if t_left == 0:
            break

    # плавное затухание музыки при завершении
    pygame.mixer.music.fadeout(1500)

    # экран завершения
    s.fill((20, 20, 20))
    msg = "GAME OVER" if reason == "lives" else "Время вышло!"
    s.blit(f.render(msg, True, (255, 120, 120)), (420, 390))
    s.blit(f.render(f"Очки: {score}", True, (255, 255, 255)), (450, 420))
    s.blit(f.render("Нажми ENTER для меню", True, (180, 200, 255)), (350, 450))
    pygame.display.flip()

    # ждём нажатия
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                waiting = False

    # возвращаем музыку
    try:
        pygame.mixer.music.play(-1)
    except:
        pass


# запуск
show_menu()
while True:
    run_game()
    show_menu()