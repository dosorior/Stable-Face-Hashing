import time
import random
import pickle
import threading
import seal 
from seal import ChooserEvaluator,Ciphertext, Decryptor,Encryptor, \
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

import argparse
import os
import sys
import numpy as np

def print_parameters(context):
	print("/ Encryption parameters:")
	print("| poly_modulus: " + context.poly_modulus().to_string())

	# Print the size of the true (product) coefficient modulus
	print("| coeff_modulus_size: " + (str)(context.total_coeff_modulus().significant_bit_count()) + " bits")

	print("| plain_modulus: " + (str)(context.plain_modulus().value()))
	print("| noise_standard_deviation: " + (str)(context.noise_standard_deviation()))


def distance(encrypt_vect_probe, encrypt_vect_enroll, context, galos_keys, reli_keys, cleaner_vector, size_vector):
    
    #Creating Context
    # path_load_params = input_feat_emb + '/' + "params" + '/' + "params_encryption_bfv.bin"
    # params = pickle.load(open(path_load_params, "rb"))
    # context = SEALContext(params)
    # qualifiers = context.qualifiers()
    print_parameters(context)

    evaluator = Evaluator(context)

    encrypted_result_matrix = Ciphertext(encrypt_vect_probe)

    evaluator.sub(encrypted_result_matrix, encrypt_vect_enroll)

    evaluator.square(encrypted_result_matrix)

    evaluator.relinearize(encrypted_result_matrix, reli_keys)

    encrypted_squared_diff = Ciphertext(encrypted_result_matrix)

    for i in range(0,size_vector):

        evaluator.rotate_rows(encrypted_squared_diff, 1, galos_keys)

        evaluator.add(encrypted_result_matrix, encrypted_squared_diff)

    evaluator.multiply_plain(encrypted_result_matrix, cleaner_vector)
    # evaluator.multiply(encrypted_result_matrix, cleaner_vector)

    return encrypted_result_matrix


def euclidean_distance(evaluator, encrypt_vect_probe, encrypt_vect_enroll, galos_keys, reli_keys, cleaner_vector, size_vector):

    encrypted_result_matrix = Ciphertext(encrypt_vect_probe)

    evaluator.sub(encrypted_result_matrix, encrypt_vect_enroll)

    evaluator.square(encrypted_result_matrix)

    evaluator.relinearize(encrypted_result_matrix, reli_keys)

    encrypted_squared_diff = Ciphertext(encrypted_result_matrix)

    for i in range(0,size_vector):

        evaluator.rotate_rows(encrypted_squared_diff, 1, galos_keys)

        evaluator.add(encrypted_result_matrix, encrypted_squared_diff)

    evaluator.multiply_plain(encrypted_result_matrix, cleaner_vector)
    # evaluator.multiply(encrypted_result_matrix, cleaner_vector)

    return encrypted_result_matrix