import numpy as np 
import matplotlib.pyplot as plt 
from skimage.measure import label 
from skimage.morphology import (binary_closing, binary_opening, binary_dilation, binary_erosion)


data = np.load("wires3npy.txt")

labeled = label(data)
def gaps(wire):
    countWires = np.max(labeled)
    countGaps =[]
    for i in range(wire.shape[0] - 1 ):
        count = 0
        if wire[i,0] ==  1:
            for j in range(wire.shape[1] - 1):
                if wire[i,j] == 0:
                    count+=1
            countGaps.append(count)
    if countWires != len(countGaps):
        countGaps.append("None")

    return countGaps




result = binary_erosion(data,np.ones(3).reshape(3,1))


print(f"Кол-во проводов:{np.max(labeled)}")

iteracia = 1
for i in gaps(result):
    if i == "None":
        print("Провод анигилирован")
        iteracia+=1
    else:
        print(f"{i} дырки в  {iteracia} проводе")
        iteracia+=1
 


plt.imshow(result)
plt.show()
