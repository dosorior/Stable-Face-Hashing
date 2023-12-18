import numpy as np
from scipy.spatial import distance
import time



class TripleHashIdentificationSystem:

    def __init__(self):

        self.hash_table = {}

        self.dataset = []

    
    def enrol(self, g_hash, g_features, labels):

        for h, f, l in zip(g_hash, g_features, labels):

            h_tmp = ''.join(str(e) for e in h)

            if h_tmp in self.hash_table:

                self.hash_table[h_tmp].append((f, l))
            
            else:

                self.hash_table[h_tmp] = [(f, l)]

    def enrol_exhaustive(self, g_features, labels):

        for f, l in zip(g_features, labels):

            self.dataset.append((f, l))


    def search(self, q_hash, q_features):

        result = []

        for h, f in zip(q_hash, q_features):

            h_tmp = ''.join(str(e) for e in h)

            if h_tmp in self.hash_table:

                entry =  self.hash_table[h_tmp]

                dist = []

                for e, l in entry:

                    value = distance.sqeuclidean(f, e)

                    # dist.append((-np.inner(f, e), l))

                    dist.append((value, l))

                
                dist.sort(key=lambda tup: tup[0])

                result.append(dist)
                
            else:

                result.append([])            
    
        return result
    
    def search_exhaustive(self, q_features):

        result = []

        for q in q_features:

            dist = []

            for element_e in self.dataset:

                feat_e = element_e[0]

                label_feat_e = element_e[1]

                value = distance.sqeuclidean(q, feat_e)

                dist.append((value, label_feat_e))
            
            # dist.sort(key=lambda tup: tup[0])

            result.append(dist)
        
        return result




    def find_label_lost(self, label):

        for g_hash in self.hash_table:

            elements_colissions = self.hash_table[g_hash]

            for value in elements_colissions:

                v = value[0]

                l = value[1]

                if label == value[1]:

                    found = True

                    print ("Found in hashtable {}".format(str(g_hash)))

                    list_elements = self.hash_table[g_hash]

                    for e in list_elements:
                        
                        print ("Collision of candidates for {}".format(str(e[1])))


    def counting_samples(self):

        average = 0

        count_entry = 0

        count_feat = 0

        for g_hash in self.hash_table:

            count_entry +=1

            elements_colissions = self.hash_table[g_hash]

            count_feat += len(elements_colissions)
        
        average = count_feat / count_entry

        return average
    

    def getting_keys_hash_table(self):

        count_entities = 0

        count_entities = len(self.hash_table)

        return count_entities

        






                



