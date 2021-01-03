import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_purple.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
PURPLE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_purple.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space background.png")), (WIDTH, HEIGHT))

# Fonts
spaceinv_font = pygame.font.Font('GAME ROBOT.otf', 64)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
    
    def collision2(self, objj):
        return collide(self, objj)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def shoot2(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        global enemies_killed
                        enemies_killed += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Player2(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PURPLE_SPACE_SHIP
        self.laser_img = PURPLE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        global enemies_killed
                        enemies_killed += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar2(window)
    
    def healthbar2(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1




def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main_2plyr():
    run = True
    FPS = 60
    level = 0
    global enemies_killed
    enemies_killed = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    win_font = pygame.font.SysFont("comicsans", 55)
    final_score_font = pygame.font.SysFont("comicsans", 70)


    enemies = []
    wave_length = 1
    enemy_vel = 1
    enemy_laser_vel = 2

    player_vel = 5
    player2_vel = 6
    laser_vel = 4

    player = Player(500, 600)
    player2 = Player2(150, 600)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    win = False
    win_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,0,0))
        level_label = main_font.render(f"Level: {level}", 1, (0,255,0))
        enemies_killed_label = main_font.render(f"Enemies Killed: {enemies_killed}", 1, (0, 0,255))
        final_score_label = final_score_font.render(f"Final Score: {enemies_killed} enemies killed", 1, (255, 99, 3))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(enemies_killed_label, (240, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        player2.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            WIN.blit(final_score_label, (WIDTH/2 - final_score_label.get_width()/2, 400))


        if win:
            win_label = win_font.render("YOU WON!! You defeated the enemies!", 1, (0,255,0))
            WIN.blit(win_label, (WIDTH/2 - win_label.get_width()/2, 350))
            WIN.blit(final_score_label, (WIDTH/2 - final_score_label.get_width()/2, 400))


        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0 or player2.health <=0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue
        
        if level >= 6:
            win = True
            win_count += 1
        
        if win:
            if win_count > FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel - 40 > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 30 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_f]:
            player.shoot()
        
        if keys[pygame.K_LEFT] and player2.x - player2_vel > 0: # left2
            player2.x -= player2_vel
        if keys[pygame.K_RIGHT] and player2.x + player2_vel + player.get_width() < WIDTH: # right
            player2.x += player2_vel
        if keys[pygame.K_UP] and player2.y - player2_vel - 40 > 0: # up
            player2.y -= player2_vel
        if keys[pygame.K_DOWN] and player2.y + player2_vel + player2.get_height() + 30 < HEIGHT: # down
            player2.y += player2_vel
        if keys[pygame.K_SPACE]:
            player2.shoot2()
        

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 3*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                enemies_killed += 1
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player2)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player2):
                player2.health -= 10
                enemies.remove(enemy)
                enemies_killed += 1
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player2.move_lasers(-laser_vel, enemies)

def main_1plyr():
    run = True
    FPS = 60
    level = 0
    global enemies_killed
    enemies_killed = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    win_font = pygame.font.SysFont("comicsans", 55)
    final_score_font = pygame.font.SysFont("comicsans", 70)


    enemies = []
    wave_length = 1
    enemy_vel = 2

    player_vel = 6
    laser_vel = 4

    player = Player(325, 600)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    win = False
    win_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,0,0))
        level_label = main_font.render(f"Wave: {level}", 1, (0,255,0))
        enemies_killed_label = main_font.render(f"Enemies Killed: {enemies_killed}", 1, (255, 99, 3))
        final_score_label = final_score_font.render(f"Final Score: {enemies_killed} enemies killed", 1, (255, 99, 3))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(enemies_killed_label, (240, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            WIN.blit(final_score_label, (WIDTH/2 - final_score_label.get_width()/2, 400))
        
        if win:
            win_label = win_font.render("YOU WON!! You defeated the enemies!", 1, (0,255,0))
            WIN.blit(win_label, (WIDTH/2 - win_label.get_width()/2, 350))
            WIN.blit(final_score_label, (WIDTH/2 - final_score_label.get_width()/2, 400))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 4:
                run = False
            else:
                continue
        
        if level >= 6:
            win = True
            win_count += 1
        
        if win:
            if win_count > FPS * 4:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel - 40 > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 30 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_f]:
            player.shoot()
        

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                enemies_killed += 1
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


            

def main_menu():
    regular_font = pygame.font.SysFont("comicsans", 35)
    spaceinv_font = pygame.font.Font('GAME ROBOT.otf', 80)
    white = (255, 255, 255)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        SPACE_INVADER = spaceinv_font.render("SPACE SHOOTERS", 1, (255,255,255))
        objective = regular_font.render("Mission Objective: Hold out against the enemy ships for as", 1, (white))
        objective2 = regular_font.render("long as posible.", 1, (white))
        p1controls = regular_font.render("Player One (Orange) Controls:", 1, (235, 171, 52))
        p1controls_w = regular_font.render("W - Up", 1, (235, 171, 52))
        p1controls_a = regular_font.render("A - Left", 1, (235, 171, 52))
        p1controls_s = regular_font.render("S - Down", 1, (235, 171, 52))
        p1controls_d = regular_font.render("D - Right", 1, (235, 171, 52))
        p1controls_shoot = regular_font.render("F - Shoot", 1, (235, 171, 52))
        p2controls = regular_font.render("Player Two (Purp) Controls:", 1, (131, 43, 186))
        p2controls_up = regular_font.render("Up Arrow Key - Up", 1, (131, 43, 186))
        p2controls_left = regular_font.render("Left Arrow Key - Left", 1, (131, 43, 186))
        p2controls_down = regular_font.render("Down Arrow Key - Down", 1, (131, 43, 186))
        p2controls_right = regular_font.render("Right Arrow Key - Right", 1, (131, 43, 186))
        p2controls_shoot = regular_font.render("SPACE - Shoot", 1, (131, 43, 186))
        howtoplay = regular_font.render("How to play: Shoot as many enemy spaceships as possible!", 1, (white))
        rules = regular_font.render("Rules:", 1, (white))
        rules1 = regular_font.render("1. Each user has 100hp. -10 each time you get hit by an enemy", 1, (white))
        rules1_1 = regular_font.render("bullet, or hit an enemy ship with your ship", 1, (white))
        rules2 = regular_font.render("2. Collective you have 5 lives. -1 each time an enemy passes", 1, (white))
        rules2_2 = regular_font.render("the bottom of your screen and gets to your base", 1, (white))
        rules3 = regular_font.render("3. You lose when EITHER SHIP has 0 hp, OR you have 0 lives", 1, (white))
        rules4 = regular_font.render("4. The game restarts automatically a few seconds afer losing", 1, (white))
        player1 = regular_font.render("Press [1] for single player", 1, (235, 171, 52))
        player2 = regular_font.render("Press [2] for double player", 1, (131, 43, 186))
        howtowin = regular_font.render("How to win: Clear all 5 waves of enemies", 1, (255,20,0))
        WIN.blit(SPACE_INVADER, (WIDTH/2 - SPACE_INVADER.get_width()/2, 50))
        WIN.blit(objective, (15, 150))
        WIN.blit(objective2, (15, 175))
        WIN.blit(p1controls, (15, 250))
        WIN.blit(p1controls_w, (15, 275))
        WIN.blit(p1controls_a, (15, 300))
        WIN.blit(p1controls_s, (15, 325))
        WIN.blit(p1controls_d, (15, 350))
        WIN.blit(p1controls_shoot, (15, 375))
        WIN.blit(p2controls, (415, 250))
        WIN.blit(p2controls_up, (415, 275))
        WIN.blit(p2controls_left, (415, 300))
        WIN.blit(p2controls_down, (415, 325))
        WIN.blit(p2controls_right, (415, 350))
        WIN.blit(p2controls_shoot, (415, 375))
        WIN.blit(howtoplay, (15, 410))
        WIN.blit(rules, (15, 450))
        WIN.blit(rules1, (15, 475))
        WIN.blit(rules1_1, (15, 500))
        WIN.blit(rules2, (15, 525))
        WIN.blit(rules2_2, (15, 550))
        WIN.blit(rules3, (15, 575))
        WIN.blit(rules4, (15, 600))
        WIN.blit(player1, (15, 700))
        WIN.blit(player2, (415, 700))
        WIN.blit(howtowin, (150, 650))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_1plyr()
                if event.key == pygame.K_2:
                    main_2plyr()
               
    pygame.quit()


main_menu()