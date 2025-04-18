import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border


def extractor(region):
    norm_area = region.area / region.image.size
    norm_perimeter = region.perimeter / region.image.size
    width, height = region.image.shape[1], region.image.shape[0]
    cy, cx = region.centroid_local
    norm_cy = cy / height
    norm_cx = cx / width
    norm_hole_area = holeArea(region) / region.image.size
    
    return np.array([
        norm_area,                     
        norm_cy,                       
        norm_cx * 10,                  
        norm_perimeter*2,               
        region.eccentricity * 3,      
        (np.all(region.image, axis=0).sum() / width)*0.3,  
        min(width, height) / max(width, height),    
        norm_hole_area * 1.5,         
        region.solidity*1.2,              
        (region.euler_number - 1) / -2  
    ])


def norm_l1(v1, v2):
    return ((v1 - v2)**2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result


def holeArea(region):
    inv = ~region.image
    border = clear_border(inv)
    labeled = label(border)
    return sum(reg.area for reg in regionprops(labeled))



image = plt.imread('alphabet-small.png')
image = image[:, :, :-1]
gray = image.mean(axis=2)
binary = gray < 1
labeled = label(binary)
regions = regionprops(labeled)

templates = {'A': extractor(regions[2]),
             'B': extractor(regions[3]), 
             '8': extractor(regions[0]),
             '0': extractor(regions[1]),
             '1': extractor(regions[4]),
             'W': extractor(regions[5]), 
             'X': extractor(regions[6]), 
             '*': extractor(regions[7]),
             '-': extractor(regions[9]), 
             '/': extractor(regions[8])}

image2 = plt.imread('alphabet.png')[:, :, :-1]
gray = image2.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

symbolsCnt = {}

for region in regions:
    v = extractor(region)
    symbol = classificator(v, templates)  
    symbolsCnt[symbol] = symbolsCnt.get(symbol, 0) + 1


for symbol in sorted(symbolsCnt.keys()):
    print(f"{symbol}: {symbolsCnt[symbol]}")
