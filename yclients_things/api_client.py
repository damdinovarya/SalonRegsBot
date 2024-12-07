from yclients import YClientsAPI


class APIClient:
    """
    Класс для управления подключением к API YClients.
    Обеспечивает авторизацию и возвращает объект API для выполнения запросов.
    """
    def __init__(self, token, company_id, form_id, login, password):
        """
        Инициализация клиента API YClients.

        :param token: API-токен.
        :param company_id: ID компании в YClients.
        :param form_id: ID формы в YClients.
        :param login: Логин пользователя в YClients.
        :param password: Пароль пользователя в YClients.
        """
        self.token = token
        self.company_id = company_id
        self.form_id = form_id
        self.login = login
        self.password = password
        self.api = self.get_api_connection()

    def get_api_connection(self):
        """
        Устанавливает соединение с API YClients.
        Получает пользовательский токен и обновляет авторизационные данные API.

        :return: Объект API YClients, готовый к использованию.
        """
        # Создаем объект API
        api = YClientsAPI(token=self.token, company_id=self.company_id, form_id=self.form_id)

        # Получаем токен пользователя
        user_token = api.get_user_token(self.login, self.password)
        api.update_user_token(user_token)

        return api
