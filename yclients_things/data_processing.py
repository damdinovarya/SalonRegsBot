from yclients import YClientsAPI


class DataProcessor:
    """
    Класс для получения и обработки данных из API YClients.
    """
    def __init__(self, api: YClientsAPI):
        """
        Инициализация объекта DataProcessor.

        :param api:
        """
        self.api = api
        self.staff_data_list = []
        self.services_data_list = []
        self.get_start_data()

    def get_start_data(self):
        """
        Загружает начальные данные сотрудников и услуг из API.
        """
        self.staff_data_list = self.api.get_staff()['data']
        fake_services_data_list = self.api.get_services()['data']['services']

        # Получаем id всех услуг
        all_services_id = [service['id'] for service in fake_services_data_list]

        services_data_list = []
        for service_id in all_services_id:
            services_data_list.append(self.api.get_service_info(service_id)['data'])
        self.services_data_list = services_data_list

    def get_staff_dates(self, staff_id):
        """
        Возвращает список доступных дней для записи к указанному сотруднику.

        :param staff_id: ID сотрудника.
        :return: Список дат, доступных для записи.
        """
        return self.api.get_available_days(staff_id)['data']['booking_dates']

    def get_service_id_by_name(self, service_name):
        """
        Получает ID услуги по её названию.

        :param service_name: Название услуги.
        :return: ID услуги.
        """
        for service in self.services_data_list:
            if service['title'] == service_name:
                return service['id']

    def get_service_price_by_name(self, service_name):
        """
        Получает цену услуги по её названию.

        :param service_name: Название услуги.
        :return: Минимальная цена услуги.
        """
        for service in self.services_data_list:
            if service['title'] == service_name:
                return service['price_min']

    def get_staff_dates_times(self, staff_id, service_name, day):
        """
        Получает список доступного времени для записи к сотруднику на указанную дату.

        :param staff_id: ID сотрудника.
        :param service_name: Название услуги.
        :param day: Дата.
        :return: Список времени.
        """
        service_id = self.get_service_id_by_name(service_name)
        return [time['time'] for time in self.api.get_available_times(staff_id, service_id, day)['data']]

    def get_all_services_titles(self):
        """
        Получает список названий всех услуг и их минимальных цен.

        :return: Кортеж из двух списков: названия услуг и их минимальные цены.
        """
        self.get_start_data()
        titles = []
        titles_prices = []
        for service in self.services_data_list:
            titles.append(service['title'].lower())
            titles_prices.append(service['price_min'])
        return titles, titles_prices

    def get_staff_by_id(self, staff_id):
        """
        Получает данные о сотруднике по его ID.

        :param staff_id: ID сотрудника.
        :return: Словарь с данными сотрудника.
        """
        self.get_start_data()
        for worker in self.staff_data_list:
            if worker['id'] == staff_id:
                return worker

    def get_staff_for_service(self, service_title):
        """
        Функция для получения имён сотрудников, которые занимаются определенной услугой.

        :param service_title: Название услуги, для которой нужно найти сотрудников
        :return: Список имён сотрудников, которые занимаются данной услугой
        """
        # Находим услугу по её названию
        self.get_start_data()
        for service in self.services_data_list:
            if service['title'].lower() == service_title:
                service_staff = []
                for staff in service['staff']:
                    for worker in self.staff_data_list:
                        if worker['id'] == staff['id']:
                            service_staff.append(worker)
                return service_staff


    def get_all_staffs(self):
        """
        Функция для получения всех сотрудников.

        :return: Список сотрудников, которые занимаются данной услугой
        """
        self.get_start_data()
        return self.staff_data_list

    def booking(self, staff_id, service_id, date_time):
        """
        Осуществляет запись клиента на услугу.

        :param staff_id: ID сотрудника.
        :param service_id: ID услуги.
        :param date_time: Дата и время записи.
        """
        booked, message = self.api.book(booking_id=0,
                                        fullname='челикс',
                                        phone='53425345',
                                        email='myemail@gmail.com',
                                        service_id=service_id,
                                        date_time='2024-12-07T18:00:00+03:00',
                                        staff_id=staff_id,
                                        comment='some_comment')
        print(booked)
        print(message)


