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

def prepare_params_encryption(value_modulus, value_coeff_modulus, plain_modulus, input_params):

    # save_params = os.path.join(input_params, "params")

    os.makedirs(input_params, exist_ok=True)

    file_params = os.path.join(input_params, "params_encryption_bfv.bin")

    parms = EncryptionParameters()

    parms.set_poly_modulus("1x^{} + 1".format(value_modulus))

    if value_coeff_modulus == 192:
        parms.set_coeff_modulus(seal.coeff_modulus_192(int(value_modulus)))
    else:
        parms.set_coeff_modulus(seal.coeff_modulus_128(int(value_modulus))) 

    # Note that 40961 is a prime number and 2*4096 divides 40960.
    parms.set_plain_modulus(int(plain_modulus))

    with open(file_params, 'wb') as f:
        pickle.dump(parms, f)

    return parms
    # context = SEALContext(parms)
    # print_parameters(context)
    # # We can see that batching is indeed enabled by looking at the encryption
    # # parameter qualifiers created by SEALContext.
    # qualifiers = context.qualifiers()
    # #print("Batching enable: " + boolalpha + qualifiers.enable_batching)
    # #print("Batching enable: " + qualifiers.enable_batching)
    # keygen = KeyGenerator(context)
    # public_key = keygen.public_key()                                                                                                                                                   
    # secret_key = keygen.secret_key()
    # # Here we use a moderate size decomposition bit count.
    # gal_keys = GaloisKeys()
    # keygen.generate_galois_keys(30, gal_keys)
    # # Since we are going to do some multiplications we will also relinearize.
    # # ev_keys = EvaluationKeys()
    # # keygen.generate_evaluation_keys(30, ev_keys)
    # encryptor = Encryptor(context, public_key)
    # i=3





















