import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes as fill
from skimage.filters import sobel as edge_detect, threshold_otsu as otsu
from skimage.measure import label as segment, regionprops as analyze_regions

def pencil_shape(reg, dim):
    center_y, center_x = reg.centroid_local
    norm_x = center_x / reg.image.shape[1]
    norm_y = center_y / reg.image.shape[0]
    
    diagonal = (reg.image.shape[0]**2 + reg.image.shape[1]**2)**0.5
    perimeter_ratio = 0.25 * reg.perimeter / diagonal
    area_ratio = reg.area / (reg.perimeter ** 2)
    
    checks = [
        perimeter_ratio < 1.38,
        area_ratio < 0.03,
        dim/2 < diagonal < dim,
        perimeter_ratio > 0.62,
        abs(norm_x - 0.5) < 0.1,
        abs(norm_y - 0.5) < 0.1
    ]
    
    return all(checks)

def scan_images(total):
    count = 0
    
    for n in range(1, total+1):
        path = f"./images/img ({n}).jpg"
        img_data = plt.imread(path).mean(2)
        edge_map = edge_detect(img_data)
        
        cutoff = otsu(edge_map) * 0.5
        binary = (edge_map >= cutoff).view('uint8')
        processed = fill(binary, np.ones((3,3)))
        
        labeled = segment(processed)
        regions = sorted(analyze_regions(labeled), 
                        key=lambda x: x.perimeter)
        
        size_ref = min(labeled.shape)
        pencils = sum(1 for r in regions[-10:] 
                     if pencil_shape(r, size_ref))
        
        print(f'Изображение {n}: найдено {pencils} карандаш(ей)')
        count += pencils
    
    print(f'Итого обнаружено: {count} карандаш(ей)')

scan_images(12)
