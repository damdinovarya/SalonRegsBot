from datetime import datetime, timedelta
from urllib.parse import quote

import pytz


def rus_to_eng(word):
    """
    Преобразует строку с русскими буквами в строку, закодированную латинскими символами или цифрами.
    Русские буквы сопоставляются уникальным латинским символам или цифрам.

    :param word: Строка на русском языке, которую нужно преобразовать.
    :return: Преобразованная строка, состоящая из латинских символов и цифр.
    """
    data_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    data_eng = "0123456789abcdefghiklmnopqrstvwxyz"
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
    data_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    data_eng = "0123456789abcdefghiklmnopqrstvwxyz"
    mapping_dict = {k: v for k, v in zip(data_eng, data_rus)}
    s = ''
    for letter in word:
        s += mapping_dict[letter]
    return s


def create_google_calendar_link(date_object, time_object, worker, claim_name, price):
    datetime_combined = datetime.combine(date_object, time_object)

    # Добавление временной зоны
    timezone = pytz.timezone('Europe/Moscow')  # Укажите ваш часовой пояс
    datetime_combined_local = timezone.localize(datetime_combined)

    # Перевод в UTC
    datetime_combined_utc = datetime_combined_local.astimezone(pytz.utc)
    end_datetime_utc = (datetime_combined_utc + timedelta(hours=1))

    # Форматирование начала и конца события
    formatted_start = datetime_combined_utc.strftime("%Y%m%dT%H%M%SZ")
    formatted_end = end_datetime_utc.strftime("%Y%m%dT%H%M%SZ")

    description = (
        f"Сотрудник: {' '.join(worker.split())}\n"
        f"Выбранная услуга: {claim_name.capitalize()}\n"
        f"Стоимость услуги: {price}₽"
    )

    encoded_description = quote(description, safe='')

    event_url = (f"https://calendar.google.com/calendar/r/eventedit?text={claim_name.capitalize()}"
                 f"&dates={formatted_start}/{formatted_end}"
                 f"&details={encoded_description}"
                 f"&location=")
    return event_url
