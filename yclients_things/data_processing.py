from yclients import YClientsAPI


class DataProcessor:
    def __init__(self, api: YClientsAPI):
        """
        Конструктор класса для обработки данных сотрудников и услуг.
        """
        self.api = api
        self.staff_data_list = []
        self.services_data_list = []
        self.get_start_data()

    def get_start_data(self):
        self.staff_data_list = self.api.get_staff()['data']
        fake_services_data_list = self.api.get_services()['data']['services']

        # Получаем id всех услуг
        all_services_id = [service['id'] for service in fake_services_data_list]

        services_data_list = []
        for service_id in all_services_id:
            services_data_list.append(self.api.get_service_info(service_id)['data'])
        self.services_data_list = services_data_list

    def get_staff_dates(self, staff_id):
        return self.api.get_available_days(staff_id)['data']['booking_dates']

    def get_service_id_by_name(self, service_name):
        for service in self.services_data_list:
            if service['title'] == service_name:
                return service['id']

    def get_staff_dates_times(self, staff_id, service_name, day):
        service_id = self.get_service_id_by_name(service_name)
        return [time['time'] for time in self.api.get_available_times(staff_id, service_id, day)['data']]

    def get_all_services_titles(self):
        """
        Функция для получения списка названий всех услуг.

        :return: Список названий услуг
        """
        self.get_start_data()
        return [service['title'].lower() for service in self.services_data_list]

    def get_staff_by_id(self, staff_id):
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

    def booking(self, staff_id, service_id, date_time):
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


