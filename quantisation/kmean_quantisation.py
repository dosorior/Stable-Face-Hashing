import numpy as np
from sklearn.cluster import KMeans
import pickle, os

class KMeansQuantisation:

    def __init__(self, K = 256, sub_spaces = 4, soft_assignment = 1):

        self.C = []

        self.K = K

        self.sub_spaces = sub_spaces

        if soft_assignment >= K:

            raise Exception('ERROR: assignment = {} is greater than the number of centers {}'.format(soft_assignment, K))

        self.soft_assignment = soft_assignment

    
    def train_model(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            kmeans = KMeans(n_clusters=self.K, random_state=0).fit(sub_features)

            self.C.append(kmeans)

    def __predict(self, features, centers):

        distance = np.asarray([np.linalg.norm(centers - f, axis=1) for f in features])

        result = []

        for dist in distance:

            index = np.arange(0, self.K)

            merge = list(zip(dist, index))

            merge.sort(key=lambda tup: tup[0])

            merge = merge[:self.soft_assignment]

            result.append([l for d,l in merge])

        return np.asarray(result)

    
    def encode(self, features):

        n, m = features.shape

        if m % self.sub_spaces != 0:

            print('feature dimension {} must be multiple of {}'.format(m, self.sub_spaces))

            return None

        num_sub_spaces = int(m/self.sub_spaces)

        codes = np.zeros((n, self.K*self.sub_spaces))

        for i in range(self.sub_spaces):

            sub_features = features[:, i*num_sub_spaces:(i + 1)*num_sub_spaces]

            kmeans = self.C[i]

            top_nearest = self.__predict(sub_features, kmeans.cluster_centers_)

            top_nearest += i*self.K

            # nearest = kmeans.predict(sub_features)

            # nearest = nearest + i*self.K

            for j in range(n):

                codes[j, top_nearest[j, :]] = 1

        return codes

        
    def save_model(self, output_path):

        with open(os.path.join(output_path, 'centers.pkl'), 'wb') as f:
            pickle.dump(self.C, f)

    def load_model(self, input_file):

        with open(os.path.join(input_file, 'centers.pkl'), 'rb') as f:
            self.C = pickle.load(f)



