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

def Decrypt_batching(secret_Keys, context, result_encrypted, list_size):  

    print_parameters(context)

    plain_result = Plaintext()
    decryptor = Decryptor(context, secret_Keys)
    crtbuilder = PolyCRTBuilder(context)
    # slot_count = (int)(crtbuilder.slot_count())
    decryptor.decrypt(result_encrypted, plain_result)
    # print("Result before decompose: '{}'".format(plain_result.to_string()))
    crtbuilder.decompose(plain_result)
    
    result = list([plain_result.coeff_at(i) for i in range(list_size)])
    # print("Result is: '{}'".format(plain_result.to_string()))

    return result

def Decrypt_batching1(decryptor, crtbuilder, result_encrypted, list_size):  

    plain_result = Plaintext()
    # slot_count = (int)(crtbuilder.slot_count())
    decryptor.decrypt(result_encrypted, plain_result)
    # print("Result before decompose: '{}'".format(plain_result.to_string()))
    crtbuilder.decompose(plain_result)
    
    result = list([plain_result.coeff_at(i) for i in range(list_size)])
    # print("Result is: '{}'".format(plain_result.to_string()))

    return result


    
    
    
    
    
    # #Creating Context
    # path_load_params = input_feat_emb + '/' + "params" + '/' + "params_encryption_bfv.bin"
    # params = pickle.load(open(path_load_params, "rb"))
    # context = SEALContext(params)
    # qualifiers = context.qualifiers()

    # #Loading keys(public and secret)
    # path_sec = input_feat_emb + '/' + "keys" + '/' + "keys_secret_encryption_bfv.txt"
    # #path_pub = input_feat_emb + '/' + "keys" + '/' + "keys_public_encryption_bfv.txt"
    # secret_key = pickle.load(open(path_sec, "rb"))
    # #public_key = pickle.load(open(path_pub, "rb"))

    # decryptor = Decryptor(context, secret_key)
    # crtbuilder = PolyCRTBuilder(context)
    # slot_count = (int)(crtbuilder.slot_count())

    # #loading encrypted feature
    # path_encrypted = input_feat_emb + '/' + "encrypted_feat" + '/' + "enc.txt"
    # pickle_encrypted = pickle.load(open(path_encrypted, "rb"))
    # decrypted = Plaintext()
    # decryptor.decrypt(pickle_encrypted, decrypted)
    # print("Read serialized ciphertext back in and decrypt to: '{}'".format(decrypted.to_string()))
    # crtbuilder.decompose(decrypted)

    # #Saving decrypted feature
    # path_decrypted_out = input_feat_emb + '/' + "decrypted_out" 
    # os.makedirs(path_decrypted_out, exist_ok=True)
    # file_save_decrypted = os.path.join(path_decrypted_out, "dec.txt")
    # pickle.dump(decrypted, open(file_save_decrypted, "wb"))



    
    


    
        




















