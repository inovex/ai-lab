"""
AbstractBaseClass (Interface) for all RL Agents used in this Lab.
"""

from abc import ABC, abstractmethod


class AbstractAgent(ABC):

    @abstractmethod
    def act(self, state):
        """Selects the action to be executed based on the given state.
        
        Implements epsilon greedy exploration strategy, i.e. with a probability of
        epsilon, a random action is selected.
        
        Args:
            state [tuple]: Tuple of agent and target position, representing the state.
        
        Returns:
            action [int]
        """

    @abstractmethod
    def train(self, exploration):
        """Learns the Q-values based on experience.
        
        Args:
            experience [tuple]: Tuple of state, action, next state, reward, done.
        
        Returns:
            None
        """
