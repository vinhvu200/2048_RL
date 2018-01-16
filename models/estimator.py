import numpy as np
from sklearn.linear_model import SGDRegressor


class Estimator():

    def __init__(self, action_space, init_state):
        self.models = []

        self.action_space = action_space
        for _ in range(self.action_space):

            model = SGDRegressor(learning_rate='constant')

            model.partial_fit([init_state], [0])
            self.models.append(model)

    def predict(self, state):

        q_vals = np.ones(self.action_space)

        for i in range(len(self.models)):
            q_vals[i] = self.models[i].predict([state])[0]

        return q_vals

    def update(self, state, action, target):
        self.models[action].fit([state], [target])