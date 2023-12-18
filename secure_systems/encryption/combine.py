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


def combine(list_distances_encrypted, context,galos_keys, total_count_distance):
    
    print_parameters(context)

    evaluator = Evaluator(context)

    combined_result = Ciphertext(list_distances_encrypted[0])

    for i in range(1,total_count_distance):

        current = Ciphertext(list_distances_encrypted[i])

        evaluator.rotate_rows(current, -i, galos_keys)

        evaluator.add(combined_result, current)

    return combined_result


def combine_distances(evaluator, list_distances_encrypted, galos_keys):
    
    distances = []  

    dist_label_combined = []              
    
    # [distances.append(list_distances_encrypted[i][0]) for i in range(len(list_distances_encrypted))]

    # combined_result = Ciphertext(distances[0])

    # dist_label_combined.append(list_distances_encrypted[0][1])

    combined_result = Ciphertext(list_distances_encrypted[0])

    for i in range(1,len(list_distances_encrypted)):

        current = Ciphertext(list_distances_encrypted[i])

        # current = Ciphertext(distances[i])

        evaluator.rotate_rows(current, -i, galos_keys)

        evaluator.add(combined_result, current)

        # dist_label_combined.append(list_distances_encrypted[i][1])


    return combined_result






