import os
from scipy import ndarray
from skimage.transform import resize, rotate, AffineTransform,ProjectiveTransform, warp
from skimage import util
from skimage import io
import numpy

picsSize = 100
rotationDegree = 30

# Разворот на градус
def rotation(image_array: ndarray, degree:float):
    return rotate(image_array, degree)


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

'''
# Сдвиг изображения
def shift(image_array: ndarray):
    generator = numpy.matrix('1,0,10; 0,1,20; -0.0007,0.0005,1')
    homography = ProjectiveTransform(matrix=generator); 
    mapping = lambda img: warp(image_array, homography)
    return mapping
    #shifted = warp(image_array, transform, mode='wrap', preserve_range=True)

    #shifted = shifted.astype(image_array.dtype)

def projection(self, tile: HipsTile):
    im = Image.open("One.png")
transparent_area = (tmp_s.param11,tmp_s.param12,tmp_s.param13,tmp_s.param14)
mask=Image.new('L', im.size, color=255)
draw=ImageDraw.Draw(mask)
draw.rectangle(transparent_area, fill=0)
im.putalpha(mask)
out = im.transform(im.size,Image.PERSPECTIVE ,(persp1),getattr(Image, 'BICUBIC'))
out.save("two.png", "PNG")
'''

# Генерация изображения из папки и сохранение с щаблонным названием
def data_augmentation(folder_path, new_folder_path, pattern):
    
    folder_path+=pattern
    # Все файлы в директории
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    newFilesCount = 0               # Счётчик получанных изображений
    numOfImages = len(images)       # Число исходных файлов
    
    print('\nОбрабатывется папка %s' %folder_path)
    for i in range(numOfImages):
        
        print("\rЗавершено: %d процента" % int(i * 100 / numOfImages), end='')
        
        # Берём i-е изображение
        image_path = images[i]

        # Считываем изображение как двумерный массив пикселей
        image_to_transform = io.imread(image_path)
        # Зададим ему фиксированный размер
        image_to_transform = resize(image_to_transform, (picsSize, picsSize), mode='constant', anti_aliasing=True)

        # Наложение шума в одном из 7 режимов
        noise_types = ['gaussian', 'localvar', 'poisson', 'salt', 'pepper', 's&p', 'speckle']
        for mode in noise_types:
                transformed_image = add_noise(image_to_transform, mode)

                new_file_path = '%s/%s/%s%d.jpg' % (new_folder_path, pattern, pattern, newFilesCount)
                newFilesCount += 1
                # Сохраняем изображение на диск
                io.imsave(new_file_path, transformed_image)

        # Поворот изображения в диапазоне [-20, 20] градусов
        for degree in range(-rotationDegree, rotationDegree, 10):
                transformed_image = rotation(image_to_transform, degree)
                new_file_path = '%s/%s/%s%d.jpg' % (new_folder_path, pattern, pattern, newFilesCount)
                newFilesCount += 1
                # Сохраняем изображение на диск
                io.imsave(new_file_path, transformed_image)
        
        # Зеркальное изображение
        #transformed_image = horizontal_flip(image_to_transform)
        #new_file_path = '%s/%s/%s%d.jpg' % (new_folder_path, pattern, pattern, newFilesCount)
        #newFilesCount += 1
        # Сохраняем изображение на диск
        #io.imsave(new_file_path, transformed_image)
        image_to_transform = horizontal_flip(image_to_transform)

        # Поворот изображения в диапазоне [-20, 20] градусов
        for degree in range(-rotationDegree, rotationDegree, 10):
                transformed_image = rotation(image_to_transform, degree)
                new_file_path = '%s/%s/%s%d.jpg' % (new_folder_path, pattern, pattern, newFilesCount)
                newFilesCount += 1
                # Сохраняем изображение на диск
                io.imsave(new_file_path, transformed_image)
                
        '''
        transformed_image = shift(image_to_transform)
        new_file_path = '%s/%s/%s%d.jpg' % (new_folder_path, pattern, pattern, newFilesCount)
        newFilesCount += 1
        # Сохраняем изображение на диск
        io.imsave(new_file_path, transformed_image)
        '''
        

data_augmentation('source_train/', 'train', 'cats')
data_augmentation('source_train/', 'train', 'dogs')

data_augmentation('source_test/', 'test', 'cats')
data_augmentation('source_test/', 'test', 'dogs')

data_augmentation('source_test_David/', 'test_David', 'cats')
data_augmentation('source_test_David/', 'test_David', 'dogs')

data_augmentation('source_test_Ilya/', 'test_Ilya', 'cats')
data_augmentation('source_test_Ilya/', 'test_Ilya', 'dogs')


print('\nГотово')
