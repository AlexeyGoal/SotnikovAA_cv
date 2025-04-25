import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

def group_hues(hue_dict, threshold=0.03):
    grouped = {}
    colors = sorted(hue_dict.keys())
        
    current_hue = colors[0]
    current_count = hue_dict[current_hue]
    
    for hue in colors[1:]:
        if abs(hue - current_hue) <= threshold:
            current_count += hue_dict[hue]
            current_hue = (current_hue * (current_count - hue_dict[hue]) + hue * hue_dict[hue]) / current_count
        else:
            grouped[round(current_hue, 2)] = current_count
            current_hue = hue
            current_count = hue_dict[hue]
    
    grouped[round(current_hue, 2)] = current_count
    return grouped


image = plt.imread('balls_and_rects.png')


gray = image.mean(axis=2)
binary = gray > 0  
labeled = label(binary)
regions = regionprops(labeled)


circle_colors = {}
rectangle_colors = {}

for region in regions:
    y, x = region.centroid
    color = round(rgb2hsv(image[int(y), int(x)])[0], 2)
    mask = region.image
    
    if np.all(mask):  
        rectangle_colors[color] = rectangle_colors.get(color, 0) + 1
        
    else:  
        circle_colors[color] = circle_colors.get(color, 0) + 1



print(f"Всего объектов:{np.max(labeled)}")
print(f"Всего кругов:{sum(circle_colors.values())}")
print(f"Всего прямоугольников:{sum(rectangle_colors.values())}")


groupted_circle = group_hues(circle_colors)
print(f"Круги по оттенкам:")
for hue, count in sorted(groupted_circle.items()):
        print(f"Оттенок {hue:.2f}: {count} шт.")

groupted_rectangle = group_hues(rectangle_colors)
print(f"Прямоугольники по оттенкам:")
for hue, count in sorted(groupted_rectangle.items()):
        print(f"Оттенок {hue:.2f}: {count} шт.")

