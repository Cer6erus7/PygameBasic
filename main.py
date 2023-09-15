import pygame


class Game:
    RIGHT_WALK = False
    LEFT_WALK = False

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        self.icon = pygame.image.load("images//game.png")
        self.bg = pygame.image.load("images//background.png")
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.bg_sound = pygame.mixer.Sound("sounds//comic5-25269.mp3")

        self.clock = pygame.time.Clock()
        self.bg_sound.play()

        pygame.display.set_caption("My First Pygame!")
        pygame.display.set_icon(self.icon)

        self.walk_left = [
            pygame.image.load("images//player_left//Lstep1.png"),
            pygame.image.load("images//player_left//Lstep2.png"),
            pygame.image.load("images//player_left//Lstep3.png"),
            pygame.image.load("images//player_left//Lstep4.png")
        ]

        self.walk_right = [
            pygame.image.load("images//player_right//Rstep1.png"),
            pygame.image.load("images//player_right//Rstep2.png"),
            pygame.image.load("images//player_right//Rstep3.png"),
            pygame.image.load("images//player_right//Rstep4.png")
        ]

        self.standing_player = pygame.image.load("images//player_stand.png")
        self.standing_player = pygame.transform.scale(self.standing_player, (36, 46))

        self.animation_count = 1
        self.bg_x = 0

    def r_walk(self):
        """
        Method for right walking, using static variable for this
        :return: None
        """
        if Game.RIGHT_WALK:
            self.screen.blit(self.walk_right[self.animation_count], (600, 600))
            if self.animation_count == len(self.walk_right) - 1:
                self.animation_count = 0
            else:
                self.animation_count += 1

    def l_walk(self):
        """
        Method for left walking, using static variable for this
        :return: None
        """
        if Game.LEFT_WALK:
            self.screen.blit(self.walk_left[self.animation_count], (600, 600))
            if self.animation_count == len(self.walk_right) - 1:
                self.animation_count = 0
            else:
                self.animation_count += 1

    def bg_movement(self):
        """
        Method for moving background while player is walking, using static variables for this
        :return:
        """
        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg_x + 1200, 0))
        self.screen.blit(self.bg, (self.bg_x - 1200, 0))

        if Game.LEFT_WALK:
            if self.bg_x == 1200:
                self.bg_x = 0
            else:
                self.bg_x += 2

        elif Game.RIGHT_WALK:
            if self.bg_x == -1200:
                self.bg_x = 0
            else:
                self.bg_x -= 2

    def player_stand(self):
        """
        When player doesn't walk, it stands on place.
        :return:
        """
        if not Game.LEFT_WALK and not Game.RIGHT_WALK:
            self.screen.blit(self.standing_player, (600, 600))

    def run_game(self):
        runner = True
        while runner:

            self.bg_movement()
            self.player_stand()
            self.r_walk()
            self.l_walk()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        Game.LEFT_WALK = False
                        Game.RIGHT_WALK = True

                    elif event.key == pygame.K_a:
                        Game.RIGHT_WALK = False
                        Game.LEFT_WALK = True

                    elif event.key == pygame.K_s:
                        Game.RIGHT_WALK = False
                        Game.LEFT_WALK = False

            self.clock.tick(20)


if __name__ == "__main__":
    g = Game()
    g.run_game()