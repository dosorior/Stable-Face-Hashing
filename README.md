# Stable-Face-Hashing
The development of large-scale facial identification systems that provide privacy protection of the enrolled subjects represents an open challenge. In the context of privacy protection, several template protection schemes have been proposed in the past. However, these schemes appear to be unsuitable for indexing (workload reduction) in biometric identification systems. More precisely, they have been utilised in identification systems performing exhaustive searches, thereby leading to degradations of the computational efficiency. 

In this work, we propose a privacy-preserving face identification system which utilises a Product Quantisation-based hash look-up table for indexing and retrieval of protected face templates. These face templates are protected through fully homomorphic encryption schemes (FHE), thereby guaranteeing high privacy protection of the enrolled subjects. For the best configuration, the experimental evaluation carried out over closed-set and open-set settings shows the feasibility of the proposed technique for the use in large-scale facial identification systems: a workload reduction down to 0.1% of a baseline approach performing an exhaustive search is achieved together with a low pre-selection error rate of less than 1%. In terms of biometric performance, a False Negative Identification Rate (FNIR) in range of 0.0% - 0.2% is obtained for practical False Positive Identification Rate (FPIR) values on the FEI and FERET face databases. In addition, our proposal shows competitive performance on unconstrained databases, e.g., the LFW face database. To the best of the authors' knowledge, this is the first work presenting a competitive privacy-preserving workload reduction scheme which performs template comparisons in the encrypted domain.

# Citation

If you use this code in your research, please cite the following paper:

```{bibtex}

@article{OsorioRoig-StableHashFaceIdentification-TBIOM-2021,
 Author = {D. Osorio-Roig and C. Rathgeb and P Drozdowski and C. Busch},
 File = {:https\://cased-dms.fbi.h-da.de/literature/OsorioRoig-StableHashFaceIdentification-TBIOM-2021.pdf:URL},
 Groups = {TReSPAsS-ETN, ATHENE, NGBS},
 Journal = {Trans. on Biometrics, Behavior, and Identity Science ({TBIOM})},
 Keywords = {Face Recognition, Workload Reduction, Indexing, Data Privacy, Homomorphic Encryption},
 Month = {July},
 Number = {3},
 Pages = {333--348},
 Title = {Stable Hash Generation for Efficient Privacy-Preserving Face Identification},
 Volume = {4},
 Year = {2021}
}
```

# Contributions
1- A hash generation scheme based on a Product Quantisation (PQ) which generates stable hash codes from faces. These hashes are used for indexing a face database, i.e., to construct a hash look-up table. Facial references within the database are protected through FHE. At the time of authentication, face hashes are employed to speed up the retrieval, i.e., to return a candidate short-list. In contrast to existing works in the field, the retrieval of the candidate short-list does not require a one-to-many search, but can be directly obtained via the hash look-up table, i.e., exact matching with computational complexity of O(1). This is possible since obtained hash codes are highly stable, which further allows for a protection thereof using conventional cryptographic methods. Finally, FHE-based comparisons are carried out in the protected domain for a small fraction of facial references.  Thereby, the proposed approach reduces the overall computational workload of a face-based identification system while the indexing and retrieval is done in a privacy-preserving way.

2- A thorough analysis of several clustering techniques to obtain a stable hash generation scheme. The experimental results show the capability of graph- and density-based clustering algorithms to build a stable and compact hash code which can be successfully employed for face identification.  In addition, the search of different sub-spaces offered by the PQ- and clustering-based combination allows achieving a good trade-off between efficiency and biometric performance. Moreover, a detailed discussion on the protection of generated hash codes with conventional cryptographic methods is given.

3- A comprehensive performance evaluation based on standardised metrics of the ISO-IEC-19795-1-060401 carried out over challenging closed-set and open-set scenarios on three public face databases, i.e., FEI, FERET, and LFW. 

### Face Hashing

![Conceptual Overview of Indexing based on Face Hashing in the Encrypted Domain](images/overview_face_hashing.png)

# Installation

1- download database FEI in https://fei.edu.br/~cet/facedatabase.html 

2- pip install scikit-learn to work with:
- sklearn.cluster import AffinityPropagation (AP)
- sklearn.mixture import GaussianMixture (GMM)
- sklearn.cluster import KMeans (k-means)
- sklearn_extra.cluster import KMedoids (k-medoids)

3- pip install numpy

4- install and build the library seal in C++ for python. Seal builds to BFV as encoding scheme

5- import seal from python to work with homomorphic encryption

6- Details to build seal are in the folder Seal/README_build.md

# Pipeline

- Execute the pipeline according to the protocol used for each database (FEI, FERET, and LFW), code of example is available with the database FEI.

- Depending on type of unsupervised clustering technique utilised, the code should be executed in the unprotected or secure domain.

    1- Use FEI-open_set_affinity_256_unprotected.py or FEI-open_set_gmm_256_unprotected.py for unprotected domain

    2- Use FEI-open_set_affinity_256_secure.py or FEI-open_set_gmm_256_secure.py for protected domain with FHE

    3- For other clustering techniques such as K-means or K-medoids, use the classes KMeansQuantisation --> quantisation/kmean_quantisation.py and KMedoidsQuantisation --> quantisation/kmedoids_quantisation.py

# Description of parameters

- '-e', '--embeddings', help='path to the face embeddings extracted'
- '-p', '--params', help= 'set path to parameters corresponding to homomorphic encryption'
- '-q', '--precision', help= 'set value to parameters corresponding to homomorphic encryption'
- '-vm', '--value-modulus', help= 'set value to parameters corresponding to homomorphic encryption, polynomial computation'
- '-vc', '--value-coeff-modulus', help= 'set value to parameters corresponding to homomorphic encryption, security level, lowest--> more efficient'
- '-pm', '--plain-modulus', help='set value to parameters corresponding to homomorphic encryption'
- '-bit', '--descomp-bit-count', help='set value to parameters corresponding to homomorphic encryption'
- '-o', '--output', help='path to the output'
- '-n', '--name', help='name of the model to be generated in training'
- '-k', '--k-fold',  help='number of rounds to execute in k-folds'
- '-s', '--sub-spaces', help='number of sub-spaces to be set on the face embeddings, i.e. 1, 2, or 4'.
