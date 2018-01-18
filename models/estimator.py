import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import tensorflow as tf

class Estimator():

    def __init__(self, action_space, init_state):
        self.models = []

        self.action_space = action_space

        self.x = tf.placeholder('float', [None, len(init_state)])

        for _ in range(self.action_space):

            model = SGDRegressor(learning_rate='constant')
            #model = MLPRegressor(hidden_layer_sizes=500)

            model.partial_fit([init_state], [0])
            self.models.append(model)

    def load_data(self):

        f = 'train_model/model_'
        for i in range(len(self.models)):
            filename = f + str(i) + '.pkl'
            self.models[i] = joblib.load(filename)

    def predict(self, state):

        q_vals = np.ones(self.action_space)

        for i in range(len(self.models)):
            q_vals[i] = self.models[i].predict([state])[0]

        return q_vals

    def update(self, state, action, target):
        self.models[action].fit([state], [target])

    def save_data(self):

        s = 'train_model/model_'
        for i in range(len(self.models)):
            filename = s + str(i) + '.pkl'
            joblib.dump(self.models[i], filename)
