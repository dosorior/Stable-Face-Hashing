from secure_systems.encryptation import prepare_params_encryption as prepare_params
from secure_systems.encryptation import generate_keys as gk
from secure_systems.encryptation import Decrypt_batching as Decrypt_batching
from quantisation.affinity_propagation_quantisation import AFQuantisation
from secure_systems.SecureHashIdentificationSystem import SecureHashIdentificationSystem
from pathlib import Path
import math
import seal
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

import numpy as np
import os
import sys, random
import argparse



parser = argparse.ArgumentParser(description='AP-based hash quantisation',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-e', '--embeddings', help='path to the face embeddings extracted', type=str)

parser.add_argument('-p', '--params', help= 'set path to parameters corresponding to homomorphic encryption', type=str)

parser.add_argument('-q', '--precision', help= 'set value to parameters corresponding to homomorphic encryption', type=int, default='2500')

parser.add_argument('-vm', '--value-modulus', help= 'set value to parameters corresponding to homomorphic encryption, polynomial computation', type=int, default='4096')

parser.add_argument('-vc', '--value-coeff-modulus', help= 'set value to parameters corresponding to homomorphic encryption, security level, lowest--> more efficient', type=int, default='128')

parser.add_argument('-pm', '--plain-modulus', help='set value to parameters corresponding to homomorphic encryption', type=int, default='40961')

parser.add_argument('-bit', '--descomp-bit-count', help='set value to parameters corresponding to homomorphic encryption', type=int, default='30')

parser.add_argument('-o', '--output', help='path to the output' , type=str)

parser.add_argument('-n', '--name', help='name of the model to be generated in training', type=str, default='secure_affinity_resnet-100')

parser.add_argument('-k', '--k-fold',  help='number of rounds to execute in k-folds', type=int, default=5)

parser.add_argument('-s', '--sub-spaces', help='number of sub-spaces to be set on the face embeddings, i.e. 1, 2, or 4', type=int, default=1)

args = parser.parse_args()


#--------------------------------------------------------#

#Checking if exist params-->Loading
#--------------------------------------------------------#

save_params = os.path.join(args.params, "params_{}_{}_{}_{}".format(args.name, args.value_modulus, args.value_coeff_modulus, args.sub_spaces))

if os.path.isdir(save_params):

    print("Exist params, loading params")

    path_load_params = args.params + '/' + "params_{}_{}_{}_{}".format(args.name, args.value_modulus, args.value_coeff_modulus, args.sub_spaces) + '/' + "params_encryption_bfv.bin"

    parms = pickle.load(open(path_load_params, "rb"))
    
else:

    print("Not Exist params, creating params")

    parms = prepare_params.prepare_params_encryption(args.value_modulus, args.value_coeff_modulus, args.plain_modulus, save_params)

context = SEALContext(parms)

# print_parameters(context)

qualifiers = context.qualifiers()

#--------------------------------------------------------#

#Checking if exist keys-->Loading 
#--------------------------------------------------------#

output_key = os.path.join(args.params, "keys_{}_{}_{}_{}".format(args.name, args.value_modulus, args.value_coeff_modulus,  args.sub_spaces))

if os.path.isdir(output_key):
    
    print("Exist keys, loading keys")

    file_params_keys_public = os.path.join(output_key, "keys_public_encryption_bfv.txt")

    file_params_keys_secret = os.path.join(output_key, "keys_secret_encryption_bfv.txt")

    file_params_keys_galos = os.path.join(output_key, "keys_galos_encryption_bfv.bin")

    file_params_keys_rel = os.path.join(output_key, "keys_rel_encryption_bfv.bin")

    public_key = pickle.load(open(file_params_keys_public, "rb"))

    secret_key = pickle.load(open(file_params_keys_secret, "rb"))    

    gal_keys = GaloisKeys()

    ev_keys = EvaluationKeys() 

    gal_keys.load(file_params_keys_galos)

    ev_keys.load(file_params_keys_rel)    

else:

    keygen = KeyGenerator(context)

    #Creating keys

    public_key, secret_key, gal_keys, ev_keys = gk.generate_keys1(keygen, args.descomp_bit_count, output_key)

#--------------------------------------------------------#

# Creating Decryptor 
#--------------------------------------------------------#

decryptor = Decryptor(context, secret_key)

crtbuilder = PolyCRTBuilder(context)

#--------------------------------------------------------#

# Building Protocol-open-set-FEI 
#--------------------------------------------------------#

#loading hash
embeddings_path = list(Path(args.embeddings).glob('*.npy'))

embeddings_path.sort()

subjects = {}

for p in embeddings_path:

    l = p.stem.split('-')[0]

    if l in subjects:

        subjects[l].append(p)
    else:

        subjects[l] = [p]

average_comparisons = 0

total_false_negative = 0

hit_rate = 0

total_average_entities = 0

ave_rank = 0

fpath_txt_gen = os.path.join(args.output, "FEI_genuine_{}_{}.txt".format(args.name, args.sub_spaces))

fpath_txt_imp = os.path.join(args.output, "FEI_impostor_{}_{}.txt".format(args.name, args.sub_spaces))

with open(fpath_txt_gen, 'w') as f, open(fpath_txt_imp, 'w') as t: 

    for i in range(args.k_fold):

        total_entities = 0

        search_l = []

        enrol_l = []

        enrol_f = []

        search_f = []

        id_subjects = []
        
        id_subjects = list(subjects.keys())

        random.shuffle(id_subjects)

        id_subjects_impostors = id_subjects[: 10]

        id_subjects_genuines = id_subjects[10:]

        for key_imp in id_subjects_impostors:
            
            samples = subjects[key_imp]

            for e in samples:

                search_f.append(np.load(str(e)))

                search_l.append(e.stem)
        
        for key_gen in id_subjects_genuines:

            samples = subjects[key_gen]

            enrol_samples = samples[:10]

            search_samples = samples[10:]

            for e in enrol_samples:

                enrol_f.append(np.load(str(e)))

                enrol_l.append(e.stem)

            for e in search_samples:

                search_f.append(np.load(str(e)))

                search_l.append(e.stem)

        enrol_f = np.asarray(enrol_f)

        count_enrol = enrol_f.shape[0]

        search_f = np.asarray(search_f)

        count_search = search_f.shape[0]

        model = AFQuantisation(sub_spaces = args.sub_spaces)

        model.train_model(enrol_f)

        enroll_codes, bit_per_sub_spaces = model.encode(enrol_f)

        hash_codes_enroll = None

        for bit in bit_per_sub_spaces:

            sub_code = enroll_codes[:, 0: bit]

            hash_pos_enroll = np.asarray([np.where(sub_code[i, :])[0] for i in range(len(enrol_l))]) 

            tmp = np.asarray([list(map(lambda e: e % bit, hash_pos_enroll[i, :])) for i in range(len(enrol_l))])

            hash_codes_enroll = tmp if hash_codes_enroll is None else np.concatenate((hash_codes_enroll, tmp), axis = 1)

        #-------------------------------------------------------------------------------------------------------

        print('Starting encode process for search')

        search_codes, bit_per_sub_spaces = model.encode(search_f)

        hash_codes_search = None

        for bit in bit_per_sub_spaces:

            sub_code = search_codes[:, 0: bit]

            hash_pos_search = np.asarray([np.where(sub_code[i, :])[0] for i in range(len(search_l))]) 

            tmp = np.asarray([list(map(lambda e: e % bit, hash_pos_search[i, :])) for i in range(len(search_l))])

            hash_codes_search = tmp if hash_codes_search is None else np.concatenate((hash_codes_search, tmp), axis = 1)

        #-------------------------------------------------------------------------------------------------------
#--------------------------------------------------------#

# Building Secure Enrolment for Identification 
#--------------------------------------------------------#
        model_identification = SecureHashIdentificationSystem(context, public_key)

        print('Secure enrolment {}'.format(i))

        model_identification.enrol(hash_codes_enroll, enrol_f, enrol_l, args.precision)

#--------------------------------------------------------#

# Building Secure Search for Identification 
#--------------------------------------------------------#
        # search_f_one = search_f[0]

        print('Secure search {}'.format(i))
        
        candidate_list, candidate_labels = model_identification.search(hash_codes_search, search_f, gal_keys, ev_keys, args.precision)

        print('Check candidate list for K-fold {}'.format(i))

        for real, cand, c_labels in zip(search_l, candidate_list, candidate_labels):

            id_search = real.split('-')[0]

            label_filter = list(filter(lambda e: id_search in e and len(e.split('-')[0]) == len(id_search), enrol_l))

            if len(label_filter):

                if len(cand) > 0:

                    f.write(str(cand[0][0])+ '\n')
                
                else:

                    # f.write(str(sys.float_info.max) + '\n')

                    f.write(str(50000) + '\n')
            else:

                if len(cand) > 0:
                    
                    t.write(str(cand[0][0])+ '\n')
                
                else:

                    t.write(str(50000) + '\n')

    print('...done')