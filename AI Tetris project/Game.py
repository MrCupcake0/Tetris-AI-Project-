import pygame
from CONSTANTS import *
from Graphics import Graphics
from DQN_Agent import DQN_Agent
from Human_Agent import Human_Agent
from Environment import Environment
from Random_Agent import Random_Agent
from State import State
import torch
from Home_screen import Home_screen

pygame.init()

clock = pygame.time.Clock()
state = State()
env = Environment(state=state)
home_screen = Home_screen(env.screen)


if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

player = DQN_Agent(env=env,device=device)
score = []


def main():

    def restart(first = False):
        if not first:
            off = home_screen.death_animation()
            if off is not None:
                return False
        player = home_screen.run()

        if player == "Human":
            player = Human_Agent()
        elif player == "AI":
            player = DQN_Agent(env = env,device=device)
            player.DQN.load_state_dict(torch.load("Data/DQN_BEST1.pth",weights_only=True))
            player.DQN.eval()
        elif player == "Random":
            player = Random_Agent(env=env)
        return player

    run = True

    player = restart(True)
    if player == False:
        run = False

    
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        action, __ = player.get_Action(events, state)
        done = env(state, action)
        
        if done:
            player = restart()
            if player == False:
                run = False
            else:
                env.restart(state)



        # elif(type(player) == DQN_Agent):
        #         pygame.time.delay(300)
            


        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



if __name__ == '__main__':
    main()
