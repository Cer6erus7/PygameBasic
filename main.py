import pygame


class Game:
    IS_GAME = True
    RIGHT_WALK = True
    LEFT_WALK = False
    IS_JUMP = False
    PLAYER_SPEED = 5
    JUMP_COUNT = 10

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        self.icon = pygame.image.load("images//game.png").convert_alpha()
        self.bg = pygame.image.load("images//background.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.bg_sound = pygame.mixer.Sound("sounds//comic5-25269.mp3")
        self.bg_sound.play(loops=True)

        pygame.display.set_caption("My First Pygame!")
        pygame.display.set_icon(self.icon)

        self.walk_left = [
            pygame.image.load("images//player_left//Lstep1.png").convert_alpha(),
            pygame.image.load("images//player_left//Lstep2.png").convert_alpha(),
            pygame.image.load("images//player_left//Lstep3.png").convert_alpha(),
            pygame.image.load("images//player_left//Lstep4.png").convert_alpha()
        ]

        self.walk_right = [
            pygame.image.load("images//player_right//Rstep1.png").convert_alpha(),
            pygame.image.load("images//player_right//Rstep2.png").convert_alpha(),
            pygame.image.load("images//player_right//Rstep3.png").convert_alpha(),
            pygame.image.load("images//player_right//Rstep4.png").convert_alpha()
        ]

        self.health_bars = [
            pygame.image.load("images//healthbar//health1.png").convert_alpha(),
            pygame.image.load("images//healthbar//health2.png").convert_alpha(),
            pygame.image.load("images//healthbar//health3.png").convert_alpha(),
            pygame.image.load("images//healthbar//health4.png").convert_alpha(),
            pygame.image.load("images//healthbar//health5.png").convert_alpha()
        ]

        self.blood_frame = pygame.image.load("images//blood_frame.png").convert_alpha()
        self.blood_frame = pygame.transform.scale(self.blood_frame, (1350, 950))
        self.is_blood_frame = False
        self.blood_frame_timer = 10

        self.gradient = True

        self.enemies = []

        self.ghost = pygame.image.load("images//ghost.png").convert_alpha()
        self.ghost = pygame.transform.scale(self.ghost, (46, 56))

        self.portal = pygame.image.load("images//portal.png").convert_alpha()
        self.portal = pygame.transform.scale(self.portal, (120, 130))

        self.hp_index = 0
        self.enemy_touch = 2
        self.damage_timer = 15

        self.animation_count = 1
        self.bg_x = 0
        self.player_x = 200
        self.player_y = 600

        self.clock = pygame.time.Clock()

    def walk(self):
        """
        Method for left or right walking, using static variable for this
        :return: None
        """
        if Game.RIGHT_WALK:
            self.screen.blit(self.walk_right[self.animation_count], (self.player_x, self.player_y))
        elif Game.LEFT_WALK:
            self.screen.blit(self.walk_left[self.animation_count], (self.player_x, self.player_y))

        if self.animation_count == len(self.walk_right) - 1:
            self.animation_count = 0
        else:
            self.animation_count += 1

    def pressed_keys(self):
        """
        Player movement when holds the keys.
        :return:
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.player_x > 50:
                self.player_x -= Game.PLAYER_SPEED
                Game.RIGHT_WALK = False
                Game.LEFT_WALK = True

        elif keys[pygame.K_d]:
            if self.player_x < 400:
                self.player_x += Game.PLAYER_SPEED
                Game.LEFT_WALK = False
                Game.RIGHT_WALK = True

    def bg_movement(self):
        """
        Method for moving background while player is walking, using static variables for this
        :return:
        """
        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg_x + 1200, 0))
        self.screen.blit(self.portal, (1000, 530))

        if self.bg_x == -1200:
            self.bg_x = 0
        else:
            self.bg_x -= 2

    def jump(self):
        """
        Player jumps when "w" has been pressed. Used Static variables and some formula for the smoother jump
        :return:
        """
        keys = pygame.key.get_pressed()

        if not Game.IS_JUMP and keys[pygame.K_w]:
            Game.IS_JUMP = True

        elif Game.IS_JUMP:
            if Game.JUMP_COUNT >= -10:
                if Game.JUMP_COUNT > 0:
                    self.player_y -= (Game.JUMP_COUNT ** 2) / 2
                else:
                    self.player_y += (Game.JUMP_COUNT ** 2) / 2
                Game.JUMP_COUNT -= 1
            else:
                Game.IS_JUMP = False
                Game.JUMP_COUNT = 10

    def health_bar(self):
        """
        Health bar that shows how many lives the player have.
        :return:
        """
        if self.hp_index == 5:
            Game.IS_GAME = False
        else:
            self.health_bars[self.hp_index] = pygame.transform.scale(self.health_bars[self.hp_index], (400, 100))
            self.screen.blit(self.health_bars[self.hp_index], (30, 30))

    def enemy(self):
        """
        Enemy for the game, they spawn on the map and walk to the player. If player
        crashed with enemies it loses its hp.
        :return:
        """
        player_rect = self.walk_left[0].get_rect(topleft=(self.player_x, self.player_y))

        if self.enemies:
            for i, enemy in enumerate(self.enemies):
                self.screen.blit(self.ghost, enemy)
                enemy.x -= 5

                if enemy.x == -70:
                    self.enemies.pop(i)

                if player_rect.colliderect(enemy) and self.damage_timer == 15:
                    self.enemy_touch -= 1

    def take_damage(self):
        """
        When an enemy hit the player twice, it will take damage
        :return:
        """
        if self.enemy_touch <= 0 and self.damage_timer == 15:
            self.hp_index += 1
            self.enemy_touch = 2
            self.damage_timer = 0
            self.is_blood_frame = True

        self.blood_f()

        if 0 <= self.damage_timer < 15:
            self.damage_timer += 1

    def blood_f(self):
        """
        Bloody frame for taking a damage
        :return:
        """
        if self.is_blood_frame and self.blood_frame_timer > 0:
            self.screen.blit(self.blood_frame, (-75, -75))
            self.blood_frame_timer -= 1
        elif self.blood_frame_timer == 0:
            self.blood_frame_timer = 10
            self.is_blood_frame = False

    def game_over(self):
        """
        Game over screen, gradient for this, restart button and exit button.
        :return:
        """
        mouse = pygame.mouse.get_pos()

        black_gradient = pygame.image.load('images//black_gradient.png').convert_alpha()
        black_gradient = pygame.transform.scale(black_gradient, (1200, 1400))

        if self.gradient:
            self.screen.blit(black_gradient, (0, 0))
            self.gradient = False

        label_gm = pygame.font.Font("fonts//Lato-Black.ttf", 120)
        label_gm = label_gm.render("Game Over", False, (94, 17, 209))
        self.screen.blit(label_gm, (300, 190))

        l_restart = pygame.font.Font("fonts//Lato-Black.ttf", 70)
        l_restart = l_restart.render(">Restart<", False, (186, 17, 212))
        rect_restart = l_restart.get_rect(topleft=(440, 360))
        self.screen.blit(l_restart, rect_restart)

        l_exit = pygame.font.Font("fonts//Lato-Black.ttf", 60)
        l_exit = l_exit.render(">Exit<", False, (150, 17, 57))
        rect_exit = l_exit.get_rect(topleft=(510, 480))
        self.screen.blit(l_exit, rect_exit)

        if rect_restart.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.enemies.clear()
            self.hp_index = 0
            self.player_x = 200
            self.player_y = 600
            self.is_blood_frame = False
            self.gradient = True
            Game.IS_GAME = True
        elif rect_exit.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            exit()

    def run_game(self):
        """
        Loop for the game. A whole game works when this loop is working.
        :return:
        """
        ghost_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(ghost_timer, 2500)

        runner = True
        while runner:

            if Game.IS_GAME:
                self.bg_movement()
                self.health_bar()
                self.pressed_keys()
                self.walk()
                self.jump()
                self.enemy()
                self.take_damage()
            else:
                self.game_over()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
                    quit()

                if event.type == ghost_timer:
                    self.enemies.append(self.ghost.get_rect(topleft=(1000, 580)))

            self.clock.tick(30)


if __name__ == "__main__":
    g = Game()
    g.run_game()
