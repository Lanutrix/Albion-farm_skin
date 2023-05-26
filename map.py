import cv2
import numpy as np


# template = cv2.imread('map/Screenshot_77.png')
# template = cv2.blur(template, (5,5))[393:400, 500:507]
# cv2.imwrite('valun.png',template)

# template2 = cv2.imread('map/Screenshot_73.png')
# template2 = cv2.blur(template2, (1,1))[582:589,1127:1134]
# cv2.imwrite('water.png',template2)

template = cv2.imread('dirt.png')
template2 = cv2.imread('water.png')

import cv2
import numpy as np

import cv2
import numpy as np

import cv2
import numpy as np

def reduce_colors(image, num_colors):
    # Преобразование изображения в пространство цветов BGR
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Преобразование изображения в формат с плавающей запятой
    float_image = np.float32(bgr_image) / 255.0

    # Преобразование изображения в формат с пикселями-столбцами
    pixels = float_image.reshape((-1, 3))

    # Задание критерия остановки и максимального количества итераций
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Применение алгоритма кластеризации K-Means
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Конвертация центров кластеров в формат с пикселями-строками
    segmented_pixels = centers[labels.flatten()].reshape((-1, 3))

    # Восстановление исходного размера изображения
    segmented_image = segmented_pixels.reshape(image.shape)

    # Преобразование изображения в пространство цветов RGB
    rgb_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

    # Приведение значений пикселей к диапазону 0-255
    rgb_image = np.clip(rgb_image * 255, 0, 255).astype(np.uint8)

    return rgb_image




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



def sum_2x2_blocks(arr):
    arr = np.array(arr)
    # Проверяем размерность массива
    if arr.shape[0] % 2 != 0 or arr.shape[1] % 2 != 0:
        raise ValueError("Размер массива должен быть кратен 2 по обоим измерениям.")
    
    # Вычисляем количество блоков по каждому измерению
    num_blocks_row = arr.shape[0] // 2
    num_blocks_col = arr.shape[1] // 2
    
    # Создаем новый массив для хранения сумм каждого блока
    result = np.zeros((num_blocks_row, num_blocks_col))
    
    # Вычисляем сумму в каждом блоке 2x2
    for i in range(num_blocks_row):
        for j in range(num_blocks_col):
            block = arr[i*2:(i+1)*2, j*2:(j+1)*2]
            result[i, j] = np.sum(block)//4
    
    return result.tolist()


def print_arr(arr):
    x = 0
    y = 0
    kof = 20
    for i in arr:
        x += 1
        y = 0
        for k in i:
            y += 1
            
            if (x==4) and (y==4):
                print("\033[32m", end=' ')
                print(int(k), end=' ')
                # print(0 if k>kof else 1, end=' ')
            else:
                print("\033[0m", end=' ')
                print(int(k), end=' ')
                # print(0 if k>kof else 1, end=' ')
            

        
        
        print()
# [[154,158,158],          
#  [154,104,78],
#  [216,201,182],
#  [199,134,100],
#  [217,157,116],
#  [191,127,940],
#  [93,155,205],
#  [229,165,119],
#  [152,102,77]]
for i in range(58, 59):
    image = cv2.imread(f'map/Screenshot_{i}.png')[558:656, 1090:1188]
    
    result_image = cv2.blur(image, (3,3))
    # result_image = reduce_colors(result_image, 16)#
    cv2.imwrite('ff.png', result_image)
    # cv2.imshow('Reduced Colors', result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    result = compare_chunks(image)
    print_arr(result)
    arr = sum_2x2_blocks(result)
    print()
    print_arr(arr)
    print(result[6][6])

# Загрузка изображения
# image = cv2.imread(f'map/Screenshot_73.png')[558:656, 1090:1188]

# # Уменьшение количества цветов на изображении до 8
# result_image = reduce_colors(image, 8)

# # Отображение изображения


