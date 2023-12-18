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


# def Encrypt_batching(feat, input_feat_emb, name_sub, context, public_key):
    
#     #Creating Context
#     # path_load_params = input_feat_emb + '/' + "params" + '/' + "params_encryption_bfv.bin"
#     # params = pickle.load(open(path_load_params, "rb"))
#     # context = SEALContext(params)
#     # qualifiers = context.qualifiers()
#     print_parameters(context)


#     #Loading keys(public and secret)
#     # path_pub = input_feat_emb + '/' + "keys" + '/' + "keys_public_encryption_bfv.txt"
#     # public_key = pickle.load(open(path_pub, "rb"))

#     #Creating Encrypter
#     encryptor = Encryptor(context, public_key)
#     # decryptor = Decryptor(context, secret_key)
#     crtbuilder = PolyCRTBuilder(context)
#     slot_count = (int)(crtbuilder.slot_count())
#     print(slot_count)
#     # First we use PolyCRTBuilder to compose the matrix into a plaintext.
#     plain_matrix_feat = Plaintext()
#     crtbuilder.compose(feat, plain_matrix_feat)
#     # Next we encrypt the plaintext as usual.
#     encrypted_matrix = Ciphertext()
# 	# print("Encrypting: ")
#     encryptor.encrypt(plain_matrix_feat, encrypted_matrix)
#     # decryptor.invariant_noise_budget(encrypted_matrix)
#     save_feat_encrypt = input_feat_emb + '/' 
#     os.makedirs(save_feat_encrypt, exist_ok=True)
#     file_params = os.path.join(save_feat_encrypt, name_sub + '.txt')
#     # encrypted_matrix.save(file_params)
#     # Serialize it using Pickle
# 	# filename1 = "encrypted1.txt"
#     print("Dumping plaintext '{}' to file '{}'".format(plain_matrix_feat.to_string(), file_params ))
#     pickle.dump(encrypted_matrix, open(file_params, "wb"))
#     # file_params = os.path.join(save_feat_encrypt, "enc.npy")
#     # np.save(file_params, encrypted_matrix)

def Encrypt_batching(encryptor, crtbuilder, input_feat_emb):

    # First we use PolyCRTBuilder to compose the matrix into a plaintext.
    plain_matrix_feat = Plaintext()
    crtbuilder.compose(input_feat_emb, plain_matrix_feat)
    # Next we encrypt the plaintext as usual.
    encrypted_matrix = Ciphertext()
	# print("Encrypting: ")
    encryptor.encrypt(plain_matrix_feat, encrypted_matrix)
    # decryptor.invariant_noise_budget(encrypted_matrix)
    # pickle.dump(encrypted_matrix, open(output_path, "wb"))
    # file_params = os.path.join(save_feat_encrypt, "enc.npy")
    # np.save(file_params, encrypted_matrix)

    return encrypted_matrix

    
    


    
        




















