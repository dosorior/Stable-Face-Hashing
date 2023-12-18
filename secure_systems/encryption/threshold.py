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


def threshold(context, distance, threshold_decision):

    print_parameters(context)
    evaluator = Evaluator(context)
    result = Ciphertext()
    evaluator.sub(distance, threshold_decision, result)
    evaluator.negate(result)
    return result

    





