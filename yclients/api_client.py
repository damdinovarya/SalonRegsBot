# TOKEN = "b238a6679665f570af0f1a21ce183d7b"
# CID = 1186779
# FID = 1301768

from yclients import YClientsAPI


class APIClient:
    def __init__(self, token, company_id, form_id, login, password):
        self.token = token
        self.company_id = company_id
        self.form_id = form_id
        self.login = login
        self.password = password
        self.api = self.get_api_connection()

    def get_api_connection(self):
        """
        Функция для подключения к API YClients.
        Возвращает объект API, готовый к использованию.
        """
        # Создаем объект API
        api = YClientsAPI(token=self.token, company_id=self.company_id, form_id=self.form_id)

        # Получаем токен пользователя
        user_token = api.get_user_token(self.login, self.password)
        api.update_user_token(user_token)

        return api

    def get_data_from_api(self):
        """
        Функция для получения данных с API.
        Возвращает данные о сотрудниках и услугах.
        """
        # Получаем данные
        staff_data_list = self.api.get_staff()['data']
        fake_services_data_list = self.api.get_services()['data']['services']

        # Получаем id всех услуг
        all_services_id = [service['id'] for service in fake_services_data_list]

        services_data_list = []
        for service_id in all_services_id:
            services_data_list.append(self.api.get_service_info(service_id)['data'])

        return staff_data_list, services_data_list


TOKEN = "nzdj6eabmyj9kd3mbmjk"
CID = 1186779
FID = 1301768

login = "hooooogrideeer@gmail.com"
password = "zh33ek"

api = APIClient(TOKEN, CID, FID, login, password)
