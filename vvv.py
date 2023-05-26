import cv2
import numpy as np


template = cv2.imread('map/Screenshot_77.png')
template = cv2.blur(template, (5,5))[393:400, 500:507]
cv2.imwrite('valun.png',template)

template2 = cv2.imread('map/Screenshot_73.png')
template2 = cv2.blur(template2, (1,1))[582:589,1127:1134]
cv2.imwrite('water.png',template2)

color_palette = [
    [154,158,158],          
    [154,104,78],
    [216,201,182],
    [199,134,100],
    [217,157,116],
    [191,127,940],
    [93,155,205],
    [229,165,119],
    [152,102,77]
]



def reduce_colors(image):
    # Преобразование изображения в формат с плавающей запятой и диапазон [0, 1]
    float_image = image.astype(np.float32) / 255.0

    # Преобразование изображения в формат с пикселями-столбцами
    pixels = float_image.reshape((-1, 3))

    # Задание критерия остановки и максимального количества итераций
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Применение алгоритма кластеризации K-Means
    _, labels, _ = cv2.kmeans(pixels, len(color_palette), None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Создание изображения с палитрой цветов
    palette_image = np.array(color_palette)

    # Преобразование пикселей изображения в соответствие с палитрой цветов
    segmented_image = palette_image[labels.flatten()]

    # Восстановление исходного размера изображения
    segmented_image = segmented_image.reshape(image.shape)

    # Приведение значений пикселей к диапазону [0, 255] и преобразование в формат с целочисленными значениями
    segmented_image = (segmented_image * 255).astype(np.uint8)

    return segmented_image




def compare_chunks(image):
    chunk_size = 7
    template_height, template_width = template.shape[:2]
    image_height, image_width = image.shape[:2]
    maping = np.zeros((image_height // chunk_size, image_width // chunk_size))

    for y in range(maping.shape[0]):
        for x in range(maping.shape[1]):
            chunk = image[y*chunk_size:(y+1)*chunk_size, x*chunk_size:(x+1)*chunk_size]
            diff = cv2.absdiff(template, chunk)
            similarity = cv2.mean(diff)[0]
            maping[y][x] = int(similarity)

    return maping



def print_arr(arr):
    x = 0
    y = 0
    kof = 20
    for i in arr:
        x += 1
        y = 0
        for k in i:
            y += 1
            
            if (x==8 or x==7) and (y==8 or y==7):
                print("\033[32m", end=' ')
                print(int(k), end=' ')
                # print(0 if k>kof else 1, end=' ')
            else:
                print("\033[0m", end=' ')
                print(int(k), end=' ')
                # print(0 if k>kof else 1, end=' ')
            

        
        
        print()

for i in range(46, 74):
    image = cv2.imread(f'map/Screenshot_{i}.png')[558:656, 1090:1188]
    result_image = cv2.blur(image, (3,3))
    result_image = reduce_colors(result_image)#
    cv2.imwrite('ff.png', result_image)
    cv2.imshow('Reduced Colors', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # result = compare_chunks(image)
    # print_arr(result)
    # print(result[6][6])

# Загрузка изображения
# image = cv2.imread(f'map/Screenshot_73.png')[558:656, 1090:1188]

# # Уменьшение количества цветов на изображении до 8
# result_image = reduce_colors(image, 8)

# # Отображение изображения


