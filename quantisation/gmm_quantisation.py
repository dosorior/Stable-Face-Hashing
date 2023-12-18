import numpy as np
from sklearn.mixture import GaussianMixture
import pickle, os

class GMMQuantisation:

    def __init__(self, K = 256, sub_spaces = 4):

        self.C = []

        self.K = K

        self.sub_spaces = sub_spaces

    
    def train_model(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            gmm = GaussianMixture(n_components=self.K, random_state=0).fit(sub_features)

            self.C.append(gmm)

    
    def encode(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        codes = np.zeros((n, self.K*self.sub_spaces))

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            gmm = self.C[i]

            nearest = gmm.predict(sub_features)

            nearest = nearest + i*self.K

            for j in range(n):

                codes[j, nearest[j]] = 1

        return codes

        
    def save_model(self, output_path):

        with open(os.path.join(output_path, 'centers.pkl'), 'wb') as f:
            pickle.dump(self.C, f)

    def load_model(self, input_file):

        with open(os.path.join(input_file, 'centers.pkl'), 'rb') as f:
            self.C = pickle.load(f)



