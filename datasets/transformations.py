"""
Module for defining the data set transformations for the data pipeline.
"""

__author__ = "Pedro Martins"

dataset_transformations = {
    'acute-inflammations-nephritis': { 'replace': { 'no': 0, 'yes': 1 } },
    'acute-inflammations-urinary': { 'replace': { 'no': 0, 'yes': 1 } },
    'balance-scale': { 'zero-index': range(5) },
    'banknote-authentication': { 'zero-index': [4] },
    'blood-transfusion-service': { 'zero-index': [4] },
    'breast-cancer-wisconsin': { 'zero-index': range(10) },
    'car-evaluation': { 'zero-index': [6], 'one-hot-encode': range(6) },
    'chess-kr-vs-kp': { 'zero-index': range(37), 'one-hot-encode': [14] },
    'climate-simulation-crashes': { 'zero-index': [20], 'drop-columns': [0,1] },
    'congressional-voting': { 'zero-index': range(17) },
    'connectionist-mines-vs-rocks': { 'zero-index': [60] },
    'contraceptive-method-choice': { 'zero-index': [1,2,4,5,6,7,8,9], 'one-hot-encode': [6] },
    'credit-approval': { 
        'replace': { 'a': 0, 'b': 1, 'f': 0, 't': 1 }, 
        'zero-index': [15],
        'one-hot-encode': [3,4,5,6,12],
        'drop-rows-with-values': ['?']
    },
    'cylinder-bands': {
        'replace': { 'NO': 0, 'YES': 1, 'KEY': 0, 'TYPE': 1, 'BAND': 0, 'NOBAND': 1 },
        'drop-columns': [0],
        'one-hot-encode': [1,2,3,7,8,9,10,12,14,15,16,17,18,19],
        'drop-rows-with-values': ['?']
    },
    'dermatology': { 'zero-index': list(range(33)) + [34] },
    'echocardiogram': { 'drop-columns': [9,10,11] },
    'fertility-diagnosis': { 'zero-index': [9], 'one-hot-encode': [0,5] },
    'habermans-survival': { 'zero-index': [3] },
    'hayes-roth': { 'zero-index': [4] },
    'heart-disease-cleveland': { 'zero-index': [1,2,13], 'one-hot-encode': [11,12], 'drop-rows': [87,166,192,266,287,302] },
    'hepatitis': { 
        'zero-index': list(range(1,13)) + [18,19],
        'drop-rows': [0,1,2,3,4,6,7,8,9,14,16,26,31,35,37,41,44,45,46,50,51,55,56,59,65,66,67,69,70,71,72,73,74,76,79,80,83,86,87,88,91,92,93,97,99,101,105,106,107,110,112,113,114,115,116,118,119,120,122,123,126,131,132,136,140,141,142,144,146,147,148,149,150,151,152]
    },
    'image-segmentation': { 'zero-index': [18] },
    'indian-liver-patient': { 'replace': { 'Female': 0, 'Male': 1  }, 'zero-index': [10], 'drop-rows-with-values': [0.947064]  },
    'ionosphere': { 'zero-index': [33] },
    'iris': { 'zero-index': [4] },
    'mammographic-mass': { 'zero-index': [5], 'one-hot-encode': [2,3], 'drop-rows-with-values': ['mean'] },
    'monks1': { 'zero-index': range(7), 'one-hot-encode': [1,2,4,5] },
    'monks2': { 'zero-index': range(7), 'one-hot-encode': [1,2,4,5] },
    'monks3': { 'zero-index': range(7), 'one-hot-encode': [1,2,4,5] },
    'optical-recognition': {},
    'ozone-eighthr': { 'zero-index': [72], 'drop-rows-with-values': ['mean'] },
    'ozone-onehr': { 'zero-index': [72], 'drop-rows-with-values': ['mean'] },
    'parkinsons': { 'zero-index': [22] },
    'pima-indians-diabetes': { 'zero-index': [8] },
    'planning-relax': { 'zero-index': [12] },
    'qsar-biodegradation': { 'zero-index': [41] },
    'seeds': { 'zero-index': [7] },
    'seismic-bumps': { 
        'replace': { 'a': 0, 'b': 1, 'c': 2, 'W': 0, 'N': 1 },
        'one-hot-encode': [1,7]
    },
    'soybean-small': { 'zero-index': [35] },
    'spambase': { 'zero-index': [57] },
    'spect-heart': {},
    'spectf-heart': {},
    'statlog-german-credit': {
        'zero-index': [0,2,3,5,6,8,9,11,13,14,16,18,19,20],
        'one-hot-encode': [0,2,3,5,6,8,9,11,13,14,16]
    },
    'statlog-landsat-satellite': { 'zero-index': [36] },
    'teaching-assistant-evaluation': { 'zero-index': list(range(4)) + [5], 'one-hot-encode': [1,2] },
    'thoracic-surgery': { 'zero-index': [0] + list(range(3,15)) + [16], 'one-hot-encode': [0,3,9] },
    'thyroid-ann': { 'zero-index': [21] },
    'thyroid-new': { 'zero-index': [5] },
    'tic-tac-toe': { 'zero-index': range(10), 'one-hot-encode': range(9) },
    'wall-following-robot-2': { 'zero-index': [2] },
    'wine': { 'zero-index': [13] }
}
