import time
from itertools import count
import matplotlib.pyplot as plt
import torch

from training import *
from input_extraction import *
from training_loop import *
from result_csv import *

#
# Game here

pygame.init()
game = Game()
game.display_state()
done = game.if_game_over()
clock.tick(1)
#

result_csv = StatisticsDQN()


plt.figure()
plt.imshow(get_screen().cpu().squeeze(0).permute(1, 2, 0).numpy(),
           interpolation='none')
plt.title('Example extracted screen')
plt.show()



num_episodes = 300
for i_episode in range(num_episodes):
    # Initialize the environment and state

    print("game ", i_episode,", Score: ", game.score)
    start_time = time.time()
    game.reset()
    last_screen = get_screen()
    current_screen = get_screen()
    state = current_screen - last_screen
    for t in count():
        # Select and perform an action
        previous_score = game.score
        temp_state = state
        action = select_action(state)
        a = action.item()
        g1 = [game.ghosts[0].x,game.ghosts[0].y]
        g2 = [game.ghosts[1].x,game.ghosts[1].y]
        p = [game.pacman.x,game.pacman.y]
        if(num_episodes > 90):
            pygame.time.delay(50)
        done = game.run_for_dqn(action.item())
        game.display_state()
        pygame.display.update()
        reward = game.score - previous_score


        if(game.if_win==False):
            reward = -10

        reward = torch.tensor([reward], device=device)

        # Observe new state
        last_screen = current_screen
        current_screen = get_screen()
        if not done:
            next_state = current_screen - last_screen
        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        optimize_model()
        if done:
            episode_durations.append(t + 1)
            plot_durations()
            scores.append(game.score)
            break

    result_csv.add_statistics(i_episode, game.score,time.time() - start_time )

    # Update the target network, copying all weights and biases in DQN
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

print('Complete')
plt.ioff()
plt.clf()
plot_score()












#
#
#
#
# game = Game(1, 1, "alpha-beta")
# win = pygame.display.set_mode((game.display_info.display_width, game.display_info.display_height))
# pygame.init()
# game.display.draw_window(win, game.grid, game.display_info, game.pacman, game.ghosts, pygame, game.score, None,
#                                  None)
#
# plt.figure()
# plt.imshow(get_screen().cpu().squeeze(0).permute(1, 2, 0).numpy(),
#            interpolation='none')
# plt.title('Example extracted screen')
# plt.show()
#
#
# num_episodes = 100
# for i_episode in range(num_episodes):
#     # Initialize the environment and state
#     game.reset()
#     last_screen = get_screen()
#     current_screen = get_screen()
#     state = current_screen - last_screen
#
#
#     for t in count():
#         # Select and perform an action
#         print("here")
#         previous_score = game.score
#         action = select_action(state)
#
#         pygame.time.delay(180)
#         done = game.run_for_dqn(action.item(), win)
#
#         reward = game.score - previous_score
#         reward = torch.tensor([reward], device=device)
#
#         # Observe new state
#         last_screen = current_screen
#         current_screen = get_screen()
#         if not done:
#             next_state = current_screen - last_screen
#         else:
#             next_state = None
#
#         # Store the transition in memory
#         memory.push(state, action, next_state, reward)
#
#         # Move to the next state
#         state = next_state
#
#         # Perform one step of the optimization (on the policy network)
#         optimize_model()
#         if done:
#             episode_durations.append(t + 1)
#             plot_durations()
#             scores.append(game.score)
#             break
#         # Update the target network, copying all weights and biases in DQN
#     if i_episode % TARGET_UPDATE == 0:
#         target_net.load_state_dict(policy_net.state_dict())
#
# print('Complete')
# plt.ioff()
# plt.clf()
# plot_score()