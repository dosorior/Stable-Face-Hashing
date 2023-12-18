import numpy as np
from sklearn.cluster import AffinityPropagation
import pickle, os
import random

class AFQuantisation:

    def __init__(self, sub_spaces = 4):

        self.C = []

        self.sub_spaces = sub_spaces

    
    def train_model(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            aff_propagation = AffinityPropagation(random_state=0).fit(sub_features)

            self.C.append(aff_propagation)

    
    def __next_power_of_2(self, x):  

        return 1 if x == 0 else 2**(x - 1).bit_length()


    def encode(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        final_codes = None

        sub_space_lenght = []

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            aff_propagation = self.C[i]

            dim = self.__next_power_of_2(aff_propagation.cluster_centers_.shape[0])

            sub_space_lenght.append(dim)

            codes = np.zeros((n, dim))

            nearest = aff_propagation.predict(sub_features)

            for j in range(n):

                codes[j, nearest[j]] = 1

            final_codes = codes if final_codes is None else np.concatenate((final_codes, codes), axis=1)

        return final_codes, sub_space_lenght

        
    def save_model(self, output_path):

        with open(os.path.join(output_path, 'centers.pkl'), 'wb') as f:
            pickle.dump(self.C, f)

    def load_model(self, input_file):

        with open(os.path.join(input_file, 'centers.pkl'), 'rb') as f:
            self.C = pickle.load(f)



