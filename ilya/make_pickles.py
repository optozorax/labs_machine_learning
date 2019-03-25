import numpy as np
import os
import cv2
import random
import pickle

def create_pickle(datadir, categories, size, name):
    training_data = []
    for category in categories:
        path = os.path.join(datadir, category)
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (size, size))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
    random.shuffle(training_data)    
        
    X = []
    y = []
    
    for features, label in training_data:
        X.append(features)
        y.append(label)
        
    X = np.array(X).reshape(-1, size, size, 1)
    
    # Нормализуем данные
    X = X/255.0
    
    pickle_out = open(datadir + "/X_" + name + ".pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()
    
    pickle_out = open(datadir + "/y_" + name + ".pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()

categories = ["cats", "dogs"]
datadir = "D:/My/programs/labs_machine_learning/ilya"
imgsize = 100
create_pickle(datadir + "/processed", categories, imgsize, "train")
create_pickle(datadir + "/test", categories, imgsize, "test")