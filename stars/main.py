import numpy as np 
import matplotlib.pyplot as plt
from skimage.measure import label,regionprops

image = np.load("stars.npy")


labeled = label(image)

reg = regionprops(labeled)

result = 0
for i in reg:
    if i.solidity < 1:
        result+=1

print(result)
