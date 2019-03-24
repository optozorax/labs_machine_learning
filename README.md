# Общий репозиторий для работы над машинным обучением в рамках дисциплины "Проектная деятельность"

# Скачать готовый датасет с кошками и собаками

[https://www.microsoft.com/en-us/download/details.aspx?id=54765](https://www.microsoft.com/en-us/download/details.aspx?id=54765). Можно взять оттуда картинки мордочек. 

# Установка tensorflow

На Linux всё очень плохо, поэтому ставьте на Windows. Сначала устанавливаете Anaconda 3, затем с помощью [этой статьи](https://www.asozykin.ru/deep_learning/2017/09/07/Keras-Installation-TensorFlow.html) ставите tensorflow и keras, а так же для GPU.

# Ссылка на отчёт
[Отчёт на docs.google](https://docs.google.com/document/d/1l64QFcJGvTqRiP2qpEo5nNQ7DZtgBXln25ZfL_Iuqfs/edit)

# Таблица ресурсов

|Ресурс|Краткое описание области применения, архитектура|Автор записи|
|-|-|-|
|[Онлайн приложение](https://quickdraw.withgoogle.com/#)|Распознавание нарисованных вами объектов за 20 секунд. Архитектура: вроде GAN (не уверен) (много интересной инфы написано [тут](https://hackernoon.com/catgan-cat-face-generation-using-gans-f44663586d6b)), [github датасетов](https://github.com/googlecreativelab/quickdraw-dataset) |Утюганов|
|[Онлайн приложение](https://greenscreen-ai.boorgle.com/), [Архитектура](https://towardsdatascience.com/background-removal-with-deep-learning-c4f2104b3157)|Удаление фона оригинальных изображений (датасет мордочек не подходит). Внимание: хорошо работает либо при высоком контрасте фона и объекта, либо если фон занимает значительную часть изображения|Кожекин|
|[Видео](https://www.youtube.com/watch?v=4VAkrUNLKSo) [Код](https://github.com/HackerPoet/FaceEditor)|Генерация лиц при помощи выставления признаков. Архитектура: автокодировщик + метод главных компонент.|Шепрут|

# Согласования об именовании файлов

Пока договорились о таком именовании:

`(cat/dog)_<первая буква имени>_nnnn.jpg`, например: `cat_d_0001.jpg`, `dog_t_1000.jpg`.

# Методы генерации изображений

* Отразить по вертикали, горизонтали
* Добавить шума
* Повернуть
* Приблизить определенную часть изображения
* Сделать наклон изображения в трехмерном пространстве
* Менять фон
* Менять раскраску кошек и собак

Полезный код: [Исходники](https://github.com/eborboihuc/rotate_3d) - наклон изображения в трехмерном пространстве при помощи матрицы поворота и проекции из openCV. (с) Кожекин.

# Интересные статьи

* [https://youtu.be/HP9S1Az8Tuw](https://youtu.be/HP9S1Az8Tuw), [AlphaGo Zero совсем на пальцах / Хабр](https://habr.com/ru/post/343590/)
* [Внезапный диван леопардовой расцветки / Хабр](https://habr.com/post/259191/)
* [Достижения в глубоком обучении за последний год / Блог компании Mail.ru Group / Хабр](https://habr.com/company/mailru/blog/338248/)
* [Четыре способа обмануть нейросеть глубокого обучения / Блог компании Mail.Ru Group / Хабр](https://habr.com/company/mailru/blog/348140/)
* [Китайские ученые научили нейросеть понимать, что видит человек по сканам активности мозга / Geektimes](https://geektimes.ru/post/288955/)
* [Переобученные нейросети в дикой природе и у человека / Geektimes](https://geektimes.ru/post/290005/)
* [Глубинное обучение: критическая оценка / Geektimes](https://geektimes.ru/post/297309/)
* [Перцептрон — Википедия](https://ru.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D1%86%D0%B5%D0%BF%D1%82%D1%80%D0%BE%D0%BD)

# Отголоски прошлого

[https://docs.google.com/document/d/1rDFRdYlVDlD-fRylP0KfjZPc2WAQF1X50st5cYEVthY/edit](https://docs.google.com/document/d/1rDFRdYlVDlD-fRylP0KfjZPc2WAQF1X50st5cYEVthY/edit)
