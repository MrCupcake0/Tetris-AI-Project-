import pygame
from CONSTANTS import *

class Home_screen:
    def __init__(self,screen):
        self.font_title = pygame.font.SysFont("Arial", 36)
        self.font = pygame.font.SysFont("Arial", 24)
        temp = WIDTH / 5
        width = WIDTH - temp
        self.screen = screen

        self.human = pygame.Rect(temp /2, 120, width, 50)
        self.ai = pygame.Rect(temp /2, 190, width, 50)
        self.random = pygame.Rect(temp /2, 260, width, 50)


    def run(self):

        self.draw()

        run = True
        while(run):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.human.collidepoint(event.pos):
                        return "Human"

                    if self.ai.collidepoint(event.pos):
                        return "AI"
                    
                    if self.random.collidepoint(event.pos):
                        return "Random"

    def draw(self):

        self.screen.fill((30, 30, 30))

        title = self.font_title.render("Tetris", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        pygame.draw.rect(self.screen, (70, 130, 180), self.human)
        text1 = self.font.render("Human Player", True, BLACK)
        text_rect1 = text1.get_rect(center=self.human.center)


        pygame.draw.rect(self.screen, (180, 70, 70), self.ai)
        text2 = self.font.render("AI Player", True, BLACK)
        text_rect2 = text2.get_rect(center=self.ai.center)


        pygame.draw.rect(self.screen, (180, 70, 70), self.random)
        text3 = self.font.render("Random Player", True, BLACK)
        text_rect3 = text3.get_rect(center=self.random.center)
        
        self.screen.blit(text1,text_rect1)
        self.screen.blit(text2,text_rect2)
        self.screen.blit(text3,text_rect3)

        pygame.display.update()


    def death_animation(self):

        pygame.time.delay(2000)
        stop = False
        for i in range(1,ROWS+1):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stop = True
            if stop:
                break
            row = pygame.Rect(LINES_WIDTH,HEIGHT - i*(HEIGHT-LINES_WIDTH)/ROWS, WIDTH, SQUARE_SIZE)
            pygame.draw.rect(self.screen, GRAY, row)
            pygame.display.update()

            pygame.time.delay(200)

        pygame.time.delay(500)
        self.screen.fill(GRAY)
        pygame.display.flip()

        pygame.time.delay(500)

        

        text1 = self.font.render("Press Space To Continue", True, BLACK)

        rect1= text1.get_rect(center =(WIDTH /2,100))
        
        self.screen.blit(text1,rect1)
        pygame.display.update()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.QUIT:
                    return False

        
                

    def score(self,score):
        score = self.font.render(f"Score: {score}", True, (255,255,255))

        self.screen.blit(score, (20, 20))
        pygame.display.update()