class DataProcessor:
    def __init__(self, staff_data_list, services_data_list):
        """
        Конструктор класса для обработки данных сотрудников и услуг.

        :param staff_data_list: Список сотрудников
        :param services_data_list: Список услуг
        """
        self.staff_data_list = staff_data_list
        self.services_data_list = services_data_list

    def get_all_services_titles(self):
        """
        Функция для получения списка названий всех услуг.

        :return: Список названий услуг
        """
        return [service['title'].lower() for service in self.services_data_list]

    def get_staff_by_id(self, staff_id):
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
        for service in self.services_data_list:
            if service['title'].lower() == service_title:
                service_staff = []
                for staff in service['staff']:
                    for worker in self.staff_data_list:
                        if worker['id'] == staff['id']:
                            service_staff.append(worker)
                return service_staff
