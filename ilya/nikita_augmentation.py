import keras
import numpy as np

import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter

from skimage import io
import matplotlib.pyplot as plt

def elastic_transform(image, alpha, sigma, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
    """
    assert len(image.shape)==3

    if random_state is None:
        random_state = np.random.RandomState(None)
    r=image[:,:,0]
    g=image[...,1]
    b=image[...,2]
    
    shape = r.shape

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    x, y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
    indices = np.reshape(x+dx, (-1, 1)), np.reshape(y+dy, (-1, 1))
    res = np.copy(image)
    res[...,0] = map_coordinates(r, indices, order=1).reshape(shape)
    res[...,1] = map_coordinates(g, indices, order=1).reshape(shape)
    res[...,2] = map_coordinates(b, indices, order=1).reshape(shape)
    
    return res 

datadir = "D:/My/programs/labs_machine_learning/"
categories = ["cats", "dogs"]
count = 460
j = count

for c in categories:
    j = count
    for i in range(1, count+1):
        img = keras.preprocessing.image.load_img(datadir + f"ilya/processed/{c}/{i}.png", target_size=(200, 200))
        img = keras.preprocessing.image.img_to_array(img)/255
    
        t = 100
        sigma = 10.6
        img1 = elastic_transform(img, t, sigma)
        img2 = elastic_transform(img, t, sigma)
        
        j = j + 1;
        keras.preprocessing.image.save_img(datadir + f"ilya/processed/{c}/{j}.jpg", img1)
        j = j + 1;
        keras.preprocessing.image.save_img(datadir + f"ilya/processed/{c}/{j}.jpg", img2)