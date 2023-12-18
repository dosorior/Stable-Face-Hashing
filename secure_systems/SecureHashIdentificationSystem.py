import numpy as np
from scipy.spatial import distance
from secure_systems.encryption import distance_encrypted as distance_encrypted
from secure_systems.encryption import Decrypt_batching as Decrypt_batching
from secure_systems.encryption import Encrypt_batching
from secure_systems.encryption import combine as combine
import seal, time
import csv
import pickle
from seal import ChooserEvaluator,\
Ciphertext, \
Decryptor, \
Encryptor, \
EncryptionParameters, \
Evaluator, \
IntegerEncoder, \
FractionalEncoder, \
KeyGenerator, \
MemoryPoolHandle, \
Plaintext, \
SEALContext, \
EvaluationKeys, \
GaloisKeys, \
PolyCRTBuilder, \
ChooserEncoder, \
ChooserEvaluator, \
ChooserPoly



class SecureHashIdentificationSystem:

    def __init__(self, context, public_key):

        self.hash_table = {}

        self.encrypter = Encryptor(context, public_key)

        self.crtbuilder = PolyCRTBuilder(context)

        self.evaluator = Evaluator(context)

    
    def enrol(self, hash, features, labels, precision):

        for h, f, l in zip(hash, features, labels):

            h_tmp = ''.join(str(e) for e in h)

            #Making quantisation of the features
            # quantisation_f = self.__feature_quantisation(f, precision)
            quantisation_f = self.__quantisation_by_threshold(f)

            #Encrypting features
            encrypted_feature = Encrypt_batching.Encrypt_batching(self.encrypter, self.crtbuilder, quantisation_f)

            #Encrypting labels
            # byte_label = np.array(str.encode(l))

            # encrypted_label = Encrypt_batching.Encrypt_batching(self.encrypter, self.crtbuilder, byte_label)

            if h_tmp in self.hash_table:

                self.hash_table[h_tmp].append((encrypted_feature, l))
            
            else:

                self.hash_table[h_tmp] = [(encrypted_feature, l)]


    def search(self, hash, features, gal_keys, ev_keys, precision):

        slot_count = (int)(self.crtbuilder.slot_count())

        cleaner = [0]*slot_count

        cleaner[0] = 1

        cleaner_plain_text = Plaintext()

        self.crtbuilder.compose(cleaner, cleaner_plain_text)

        result, labels = [], []

        for h, f in zip(hash, features):

            h_tmp = ''.join(str(e) for e in h)

            if h_tmp in self.hash_table:

                # quantisation_f = self.__feature_quantisation(f, precision)

                quantisation_f = self.__quantisation_by_threshold(f)

                encrypted_f = Encrypt_batching.Encrypt_batching(self.encrypter, self.crtbuilder, quantisation_f)

                dists = []

                lab = []

                init_time = time.time()

                entry =  self.hash_table[h_tmp]

                end_time = time.time()

                print('Indexing time: {} ms'.format((end_time - init_time)*1000))

                for e, l in entry: # f is feat_probe_encrypt and e is feat_enrol_encrypt

                    init_time = time.time()

                    encrypted_value = distance_encrypted.euclidean_distance(self.evaluator, encrypted_f, e, gal_keys, ev_keys, cleaner_plain_text, len(f))

                    end_time = time.time()

                    print('Encryption time: {} ms'.format((end_time - init_time)*1000))

                    # result = Decrypt_batching.Decrypt_batching1(decryptor, self.crtbuilder, encrypted_value, 10)
                    
                    # print(result)

                    dists.append(encrypted_value)

                    lab.append(l)

                combined_result = combine.combine_distances(self.evaluator, dists, gal_keys)

                # result_final_decrypted = Decrypt_batching.Decrypt_batching1(decryptor, self.crtbuilder, combined_result, len(dists))

                # print(result_final_decrypted)

                # [distance_combined_label.append((result_final_decrypted[i], label_final[i])) for i in range(len(result_final_decrypted))]
                
                # distance_combined_label.sort(key=lambda tup: tup[0])

                result.append(combined_result)

                labels.append(lab)

            else:

                result.append([])

                labels.append([])

        return result, labels
    

    def __quantisation_by_threshold(self, features):

        with open("th_FERET_512.csv", mode="r", newline="\n") as f:
            thresholds = [tuple(map(float, el)) for el in csv.reader(f, delimiter=',')]

        return [(0 if (value < thresholds[i][0]) else (1 if (value < thresholds[i][1]) else (2 if (value < thresholds[i][2]) else 3))) for i, value in enumerate(features)]
            
    

    def __feature_quantisation(self, features, precision):

        multi_data_feat = features * precision

        return multi_data_feat.astype(int)

    
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
                        
                        print ("Colissioned candidates for {}".format(str(e[1])))


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

        






                



