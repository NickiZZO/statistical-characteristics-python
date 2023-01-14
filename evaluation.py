import math
from functools import reduce

# метод получения оценки статистических данных
def get_statistical_characteristics (filename):
    # открываем файл
    file = open(filename, "r", encoding="utf8")

    # получаем текст файла в виде строки
    text = file.read()

    # закрываем файл
    file.close()

    # формируем список символов в алфавите
    alphabet = list(set(text))

    # формируем список вероятности символов в алфавите
    probabilities = list(map(lambda symbol: get_probability(symbol, text), alphabet))

    # вычисляем максимальную энтропию
    h_max = math.log2(len(alphabet))

    # вычисляем реальную энтропию
    h_real = reduce(lambda acc, probability: acc - probability * math.log2(probability), probabilities)

    # вычисляем абсолютною избыточность
    r_abs = h_max - h_real

    # вычисляем относительную избыточность
    r_rel = 1 - h_real / h_max

    # вычисляем значения собственной информации символов алфавита
    self_informations = list(map(lambda symbol: get_self_information(symbol, text), alphabet))
    zipped_alphabet = list(zip(alphabet, self_informations))
    sorted_zipped_alphabet = sorted(zipped_alphabet, key=lambda item: item[1])

    # символ с наибольшей собственной информацией
    s_max = sorted_zipped_alphabet[-1]

    # символ с наименьшей собственной информацией
    s_min = sorted_zipped_alphabet[0]

    # возвращаем полученные данные
    return {
        "text_length": len(text),
        "alphabet_length": len(alphabet),
        "symbols": alphabet,
        "probabilities": probabilities,
        "h_max": h_max,
        "h_real": h_real,
        "r_abs": r_abs,
        "r_rel": r_rel,
        "s_max": s_max,
        "s_min": s_min,
    }

# метод получения вероятности
def get_probability (symbol, text):
    occurrence = text.count(symbol)
    probability = occurrence / len(text)
    return probability

# метод получения собственной информации
def get_self_information (symbol, text):
    probability = get_probability(symbol, text)
    self_information = math.log2(1 / probability)
    return self_information
