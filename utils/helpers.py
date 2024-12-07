def rus_to_eng(word):
    """
    Преобразует строку с русскими буквами в строку, закодированную латинскими символами или цифрами.
    Русские буквы сопоставляются уникальным латинским символам или цифрам.

    :param word: Строка на русском языке, которую нужно преобразовать.
    :return: Преобразованная строка, состоящая из латинских символов и цифр.
    """
    data_rus = "абвгдеёжзийклмопрстуфхцчшщъыьэюя"
    data_eng = "0123456789abcdefghiklmnopqrstvwx"
    mapping_dict = {k: v for k, v in zip(data_rus, data_eng)}
    s = ''
    for letter in word:
        s += mapping_dict[letter]
    return s


def eng_to_rus(word):
    """
    Преобразует строку, закодированную латинскими символами или цифрами, обратно в русские буквы.
    Латинские символы и цифры сопоставляются оригинальным русским буквам.

    :param word: Строка, закодированная латинскими символами или цифрами.
    :return: Преобразованная строка, состоящая из русских букв.
    """
    data_rus = "абвгдеёжзийклмопрстуфхцчшщъыьэюя"
    data_eng = "0123456789abcdefghiklmnopqrstvwx"
    mapping_dict = {k: v for k, v in zip(data_eng, data_rus)}
    s = ''
    for letter in word:
        s += mapping_dict[letter]
    return s

