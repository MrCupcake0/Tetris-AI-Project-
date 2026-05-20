import random
import wandb
import numpy as np
from DQN import DQN
from DQN_Agent import DQN_Agent
from Environment import Environment
from Replay_Buffer import ReplayBuffer
from Graphics import Graphics
from State import State
import pygame
import torch

MIN_BUFFER = 64


def main ():

    pygame.init()

    epochs = 2000
    learning_rate = 0.0001
    C = 300
    batch_size = 64

    epsilon_start = 1
    epsilon_final = 0.01
    epsilon_decay = 1000

    
    # path = "Data\DQN_PARAM.pth"

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    state = State()
    print(device)

    env = Environment(state=state, train = True)

    player = DQN_Agent(env, epsilon_start, epsilon_final, epsilon_decay, device=device)
    player_hat = DQN_Agent(env=env, device=device)
    graphics = Graphics()
    Q = player.Q
    player_hat.DQN = player.DQN.copy()
    Q_hat = player_hat.Q
    buffer = ReplayBuffer()
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)

    moves = 0
    score = 0
    best_score = 0
    loss = torch.tensor(0.0)
    start_epoch = 0

    project = "Tetris_AI"

    run = wandb.init(
        # Set the wandb entity where your project will be logged (generally your team name).
        entity="amitisraeli-",
        # Set the wandb project where this run will be logged.
        project= project,
        # Track hyperparameters and run metadata.
        config={
            "name": f"Tetris_AI",
            "epochs": epochs,
            "learning_rate": learning_rate,
            "C": C,
            "batch_size": batch_size,
            "start_epoch": start_epoch,
            "Model":str(player.DQN), 
            "device": str(device),
            "state": "state = np.array([height, bumpiness, holes]).astype(np.float32)",
            "reward": "reward = lines_cleared * 1 - holes * 0.5 - bumpiness * 0.05  - height * 0.03",
            "epsilon_start": epsilon_start,
            "epsilon_final": epsilon_final,
            "epsilon_decay": epsilon_decay
        },
    )


    for epoch in range(epochs):
        done = False
        while not done:
            
            
            pygame.event.pump()
            pygame.display.update()
            action, after_state = player.get_Action(state=state, epoch=epoch, train=True)
            state_dqn = state.get_state()
            done = env(state, action)
            after_state_dqn = state.get_state()
            reward = env.reward(state_dqn, after_state_dqn, done, state.board)
            moves += 1
            
            buffer.push(state_dqn, action, reward, after_state.copy(), after_state_dqn, done)
            

            if done:
                score = state.score
                if score > best_score:
                    best_score = score
                    torch.save(player.DQN.state_dict(), "Data/DQN_BEST.pth")
                env.restart(state)
                break
            
            if len(buffer) < MIN_BUFFER:
                continue


            _, _, rewards, next_states, next_states_dqn, dones = buffer.sample(batch_size) 
            next_states_dqn = torch.tensor(next_states_dqn, dtype=torch.float32, device=device)

            Q_values = Q(next_states_dqn)

            next_next_states_dqn = player.get_Actions(next_states)
            next_next_states_dqn = next_next_states_dqn.to(device)
            
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_next_states_dqn)
            
            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()




        if epoch % C == 0:
            player_hat.DQN.load_state_dict(player.DQN.state_dict())

            torch.save(player.DQN.state_dict(),"Data/DQN_PARAM.pth")
        run.log({"score": score, "loss": loss.item(), "moves": moves})

        print(f'epoch: {epoch} moves: {moves} loss: {loss:.7f}  score: {score}  best score: {best_score}')
    run.finish()


if __name__ == '__main__':
    main()