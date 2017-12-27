# 1. нужно преобразовать множество посчитанных
# с помощью path_creator точек в еще большее количество точек
# Количество точек будет тем больше, чем больше радиус поворота.
# 2. в процессе движения танка по траектории проводим перпендикуляр и
# смотрим, какой отрезок пути он пересекает
# получаем 2 параметра:
# А) длина перпендикуляра -т.е. наше отклонение
# от желаемого пути
# Б) угол между перпендикуляром и нашим вектором направления
# (должен стремиться к 90 градусам)
# далее мы ставим ПИД-регулятор и минимизируем эти два
# параметра с учетом коэффициентов, при том, что наши органы
# управления - поверни вправо, поверни влево, сбавь скорость, увеличь скорость

# итого задача делится на:
# 1) увеличение количество точек
# 2) проведение перпендикуляра к соответствующему отрезку пути,
# нахождение двух параметров: угол отклонения и расстояние до пути
# 3) построение ПИД-регулятора

# как преобразовать множество точек в какую-либо адекватную фигуру?
