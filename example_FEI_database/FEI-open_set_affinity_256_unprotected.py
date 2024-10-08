import numpy as np
import os
import sys, random
import argparse
from quantisation.affinity_propagation_quantisation_testing import AFQuantisation
from secure_systems.TripleHashSystem import TripleHashIdentificationSystem
from pathlib import Path


parser = argparse.ArgumentParser(description='AP-based hash quantisation',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-e', '--embeddings', help='path to the face embeddings extracted', type=str)

parser.add_argument('-o', '--output', help='path to the output' ,type=str)

parser.add_argument('-n', '--name', help='name of the model to be generated in training',type=str,
                     default='affinity_resnet-100')

parser.add_argument('-k', '--k-fold', help='number of rounds to execute in k-folds' ,type=int, default=5)

parser.add_argument('-c', '--centers', help='number of centers defined according to the clustering technique used, AP does not employ this parameter', type=int, default=64)

parser.add_argument('-s', '--sub-spaces', help='number of sub-spaces to be set on the face embeddings, i.e. 1, 2, or 4', type=int, default=4)

args = parser.parse_args()


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

        id_subjects_impostors = id_subjects[:10]

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

        model.train_model(enrol_f, enrol_l)

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
    
        model_identification = TripleHashIdentificationSystem()

        print('Enrol features for K-fold {}'.format(i))

        model_identification.enrol(hash_codes_enroll, enrol_f, enrol_l)

        candidate_list = model_identification.search(hash_codes_search, search_f)

        print('Check candidate list for K-fold {}'.format(i))

        for real, cand in zip(search_l, candidate_list):

            id_search = real.split('-')[0]

            label_filter = list(filter(lambda e: id_search in e.split('-')[0] and len(e.split('-')[0]) == len(id_search), enrol_l))

            if len(label_filter):

                if len(cand) > 0:

                    f.write(str(cand[0][0])+ '\n')
                
                else:

                    # f.write(str(sys.float_info.max) + '\n')

                    f.write(str(2.0) + '\n')
            else:

                if len(cand) > 0:
                    
                        # t.write(str(cand[0][0])+ '\n' + cand[0][1] + '\n' + real + '\n')

                    t.write(str(cand[0][0])+ '\n')

                        # for c in range(0, len(cand)):

                        #     value = cand[c][0]

                        #     if value < 0.457:

                        #         t.write(str(value)+ '->' + cand[0][1] + '->' + real + '\n')





                
                else:

                    # t.write(str(2.0) + '\n' + real + '\n')

                    t.write(str(2.0) + '\n')

    print('...done')