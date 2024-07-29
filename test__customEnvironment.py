import gymnasium
from gymnasium import spaces
import numpy as np

class CustomEnv(gymnasium.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()

        # Actions are to change the values of the elements in the paramList 


        # Define action and observation space
        self.action_space = spaces.Discrete(5)  # 5 discrete actions
        self.observation_space = spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)  # Single continuous observation

        # Initialize state
        self.state = 0  # Starting state

    def step(self, action):
        # Validate action
        assert self.action_space.contains(action), f"Invalid action {action}"

        # Perform action
        if action == 0:
            reward = 1
        elif action == 1:
            reward = 2
        elif action == 2:
            reward = 3
        elif action == 3:
            reward = 0
        elif action == 4:
            reward = -1

        # Update state (for illustration purposes, state just increments by 1 each step)
        self.state += 1

        # Check if done
        done = False
        if self.state >= 100:  # Arbitrary condition for termination
            done = True

        # Return observation, reward, done, info
        return np.array([self.state]), reward, done, {}

    def reset(self):
        # Reset state to initial state
        self.state = 0
        return np.array([self.state])

    def render(self, mode='human'):
        # Optional: render environment
        pass

    def close(self):
        # Clean-up environment
        pass
