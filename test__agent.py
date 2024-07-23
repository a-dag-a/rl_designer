import gymnasium
import numpy as np
from test__customEnvironment import CustomEnv

# Define the environment (assuming CustomEnv class is defined as in the previous response)
env = CustomEnv()

# Reset environment to get initial observation
observation = env.reset()

# Run episodes
for episode in range(5):  # Run 5 episodes
    total_reward = 0
    done = False
    step = 0

    print(f"Episode {episode + 1}")
    while not done:
        # Choose a random action from the action space
        action = env.action_space.sample()

        # Perform the action in the environment
        next_observation, reward, done, _ = env.step(action)

        # Accumulate total reward
        total_reward += reward

        # Print out information (optional)
        print(f"Step {step}: Action taken - {action}, Reward - {reward}, Next State - {next_observation}")

        # Update observation for the next step
        observation = next_observation
        step += 1

    print(f"Total reward for episode {episode + 1}: {total_reward}")
    print("Episode completed\n")

# Close the environment
env.close()
