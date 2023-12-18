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

def generate_keys(descomposition_bit_count, input_feat_emb, context):
    save_params = os.path.join(input_feat_emb, 'keys')
    os.makedirs(save_params, exist_ok=True)
    file_params_keys_public = os.path.join(save_params, "keys_public_encryption_bfv.txt")
    file_params_keys_secret = os.path.join(save_params, "keys_secret_encryption_bfv.txt")
    file_params_keys_galos = os.path.join(save_params, "keys_galos_encryption_bfv.bin")
    file_params_keys_rel = os.path.join(save_params, "keys_rel_encryption_bfv.bin")
    #load params
    # path_load_params = input_feat_emb + '/' + "params" + '/' + "params_encryption_bfv.bin"
    # params = pickle.load(open(path_load_params, "rb"))
    print_parameters(context)

    # Generate key_secret and key_public
    keygen = KeyGenerator(context)
    public_key = keygen.public_key()
    print(type(public_key))
    secret_key = keygen.secret_key()
    print(type(secret_key))
    # Generate key_secret and key_galos
    gal_keys = GaloisKeys()
    keygen.generate_galois_keys(descomposition_bit_count, gal_keys)
    print(type(gal_keys))

    # Generate key_secret and key_rel
    ev_keys = EvaluationKeys()
    keygen.generate_evaluation_keys(descomposition_bit_count, ev_keys)
    print(type(ev_keys))

    #Saving keys
    pickle.dump(public_key, open(file_params_keys_public, "wb"))
    pickle.dump(secret_key, open(file_params_keys_secret, "wb"))
    # public_key.save(file_params_keys_public)
    # secret_key.save(file_params_keys_secret)
    gal_keys.save(file_params_keys_galos)
    ev_keys.save(file_params_keys_rel)
    return public_key, secret_key, gal_keys, ev_keys

def generate_keys1(keygen, descomposition_bit_count, input_feat_emb):
    # save_params = os.path.join(input_feat_emb, 'keys')
    os.makedirs(input_feat_emb, exist_ok=True)
    file_params_keys_public = os.path.join(input_feat_emb, "keys_public_encryption_bfv.txt")
    file_params_keys_secret = os.path.join(input_feat_emb, "keys_secret_encryption_bfv.txt")
    file_params_keys_galos = os.path.join(input_feat_emb, "keys_galos_encryption_bfv.bin")
    file_params_keys_rel = os.path.join(input_feat_emb, "keys_rel_encryption_bfv.bin")

    # Generate key_secret and key_public
    public_key = keygen.public_key()

    secret_key = keygen.secret_key()
    # Generate key_secret and key_galos
    gal_keys = GaloisKeys()

    keygen.generate_galois_keys(descomposition_bit_count, gal_keys)
    
    # Generate key_secret and key_rel
    ev_keys = EvaluationKeys()

    keygen.generate_evaluation_keys(descomposition_bit_count, ev_keys)

    #Saving keys
    pickle.dump(public_key, open(file_params_keys_public, "wb"))
    pickle.dump(secret_key, open(file_params_keys_secret, "wb"))
    # public_key.save(file_params_keys_public)
    # secret_key.save(file_params_keys_secret)
    gal_keys.save(file_params_keys_galos)
    ev_keys.save(file_params_keys_rel)

    return public_key, secret_key, gal_keys, ev_keys

    



















