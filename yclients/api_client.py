# TOKEN = "b238a6679665f570af0f1a21ce183d7b"
# CID = 1186779
# FID = 1301768

from yclients import YClientsAPI

TOKEN = "nzdj6eabmyj9kd3mbmjk"
CID = 1186779
FID = 1301768

login = "hooooogrideeer@gmail.com"
password = "zh33ek"


def get_api_connection():
    """
    Функция для подключения к API YClients.
    Возвращает объект API, готовый к использованию.
    """
    # Создаем объект API
    api = YClientsAPI(token=TOKEN, company_id=CID, form_id=FID)

    # Получаем токен пользователя
    user_token = api.get_user_token(login, password)
    api.update_user_token(user_token)

    return api


def get_data_from_api():
    """
    Функция для получения данных с API.
    Возвращает данные о клиентах, сотрудниках и услугах.
    """
    api = get_api_connection()

    # Получаем данные
    staff_data_list = api.get_staff()['data']
    fake_services_data_list = api.get_services()['data']['services']

    all_services_id = [service['id'] for service in fake_services_data_list]

    services_data_list = []
    for service_id in all_services_id:
        services_data_list.append(api.get_service_info(service_id)['data'])

    return staff_data_list, services_data_list
