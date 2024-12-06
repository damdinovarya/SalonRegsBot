def rus_to_eng(word):
    data_rus = "абвгдеёжзийклмопрстуфхцчшщъыьэюя"
    data_eng = "0123456789abcdefghiklmnopqrstvwx"
    mapping_dict = {k: v for k, v in zip(data_rus, data_eng)}
    s = ''
    for letter in word:
        s += mapping_dict[letter]
    return s


def eng_to_rus(word):
    data_rus = "абвгдеёжзийклмопрстуфхцчшщъыьэюя"
    data_eng = "0123456789abcdefghiklmnopqrstvwx"
    mapping_dict = {k: v for k, v in zip(data_eng, data_rus)}
    s = ''
    for letter in word:
        s += mapping_dict[letter]
    return s

