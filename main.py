import pygame


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        self.icon = pygame.image.load("images//game.png")
        self.screen.fill((34, 82, 66))

        pygame.display.set_caption("My First Pygame!")
        pygame.display.set_icon(self.icon)

    def blue_square(self):
        square = pygame.Surface((1000, 600))
        square.fill("Blue")
        self.screen.blit(square, (100, 100))

    def lollipop(self):
        image = pygame.image.load("images//lollipop.png")
        image = pygame.transform.scale(image, (100, 100))
        self.screen.blit(image, (550, 350))

    def pikachu(self):
        image = pygame.image.load("images//game.png")
        image = pygame.transform.scale(image, (100, 100))
        self.screen.blit(image, (550, 350))

    def text(self):
        myfont = pygame.font.Font("fonts//Lato-Black.ttf", 40)
        text_surface = myfont.render("Matvii Roker!!!", True, "red")
        self.screen.blit(text_surface, (480, 370))

    def run_game(self):
        runner = True
        while runner:

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.blue_square()
                    elif event.key == pygame.K_s:
                        self.lollipop()
                    elif event.key == pygame.K_d:
                        self.pikachu()
                    elif event.key == pygame.K_w:
                        self.text()

if __name__ == "__main__":
    g = Game()
    g.run_game()