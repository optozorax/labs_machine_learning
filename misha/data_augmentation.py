import os
from scipy import ndarray
from skimage import transform
from skimage import util
from skimage import io

pattern = 'cat'
folder_path = '/home/user/NSTU/ML/cats2'
new_folder_path = 'new_cats'

# Все файлы в директории
images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


numOfImages = len(images)       # Число исходных файлов
numOfGradations = 10            # Число градаций каждого преобразования
newFilesCount = 0               # Счётчик получанных изображений



# Разворот на градус
def rotation(image_array: ndarray, degree:float):
    return transform.rotate(image_array, degree)


# Применяем один из видов наложения шума
# 'gaussian'
# 'localvar'
# 'poisson'
# 'salt'
# 'pepper'
# 's&p'
# 'speckle'
def add_noise(image_array: ndarray, new_mode: str):
    return util.random_noise(image_array, new_mode)


# Зеркальное отражение относительно оси OY
def horizontal_flip(image_array: ndarray):
    return image_array[:, ::-1]



for i in range(numOfImages):

        # Берём i-е изображение
        image_path = images[i]

        # Считываем изображение как двумерный массив пикселей
        image_to_transform = io.imread(image_path)

        # Наложение шума в одном из 7 режимов
        noise_types = ['gaussian', 'localvar', 'poisson', 'salt', 'pepper', 's&p', 'speckle']
        for mode in noise_types:
                print(mode)
                transformed_image = add_noise(image_to_transform, mode)

                new_file_path = '%s/%s%d.jpg' % (new_folder_path, pattern, newFilesCount)
                newFilesCount += 1
                # Сохраняем изображение на диск
                io.imsave(new_file_path, transformed_image)


        # Зеркальное изображение
        transformed_image = horizontal_flip(image_to_transform)
        new_file_path = '%s/%s%d.jpg' % (new_folder_path, pattern, newFilesCount)
        newFilesCount += 1
        # Сохраняем изображение на диск
        io.imsave(new_file_path, transformed_image)


        # Поворот изображения в диапазоне [-20, 20] градусов
        for degree in range(-20, 20, 4):
                transformed_image = rotation(image_to_transform, degree)
                new_file_path = '%s/%s%d.jpg' % (new_folder_path, pattern, newFilesCount)
                newFilesCount += 1
                # Сохраняем изображение на диск
                io.imsave(new_file_path, transformed_image)
