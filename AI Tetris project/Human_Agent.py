import pygame

class Human_Agent:
    def __init__(self):
        self.held_down = False
        # self.held_left = False
        # self.held_right = False
    
    def get_Action(self, events = None ,state = None):

        action = 0
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action =  1 
                if event.key == pygame.K_RIGHT:
                    action =  2
                if event.key == pygame.K_DOWN:
                    action =  3
                if event.key == pygame.K_z:
                    action =  4
                if event.key == pygame.K_x:
                    action =  5
                if event.key == pygame.K_SPACE:
                    action =  11
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    action =  6
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            action =  7
        keys = pygame.KEYUP
        return action , None

        
    