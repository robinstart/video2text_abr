# This code is from https://github.com/jadore801120/attention-is-all-you-need-pytorch/blob/master/transformer/Optim.py
'''A wrapper class for optimizer '''
import numpy as np


class ScheduledOptim():
    '''A simple wrapper class for learning rate scheduling'''

    def __init__(self, optimizer, d_model, n_warmup_steps):
        self._optimizer = optimizer
        self.n_warmup_steps = n_warmup_steps
        self.n_current_steps = 0
        self.init_lr = np.power(d_model, -0.5)

    def step(self):
        "Step with the inner optimizer"
        self._update_learning_rate()
        self._optimizer.step()

    def zero_grad(self):
        "Zero out the gradients by the inner optimizer"
        self._optimizer.zero_grad()

    def _get_lr_scale(self):
        return np.min([
            np.power(self.n_current_steps, -0.5),
            np.power(self.n_warmup_steps, -1.5) * self.n_current_steps])

    def _update_learning_rate(self):
        ''' Learning rate scheduling per step '''

        self.n_current_steps += 1
        lr = self.init_lr * self._get_lr_scale()

        for param_group in self._optimizer.param_groups:
            param_group['lr'] = lr
            
    def state_dict(self):
        state = self._optimizer.state_dict()
        state['init_lr'] = self.init_lr
        state['n_warmup_steps'] = self.n_warmup_steps
        state['n_current_steps'] = self.n_current_steps
        return state

    def load_state_dict(self, state):
        self._optimizer.load_state_dict(state)
        self.init_lr = state['init_lr']
        self.n_warmup_steps = state['n_warmup_steps']
        self.n_current_steps = state['n_current_steps']
