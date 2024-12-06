class DataProcessor:
    def __init__(self, staff_data_list, services_data_list):
        """
        Конструктор класса для обработки данных сотрудников и услуг.

        :param staff_data_list: Список сотрудников
        :param services_data_list: Список услуг
        """
        self.staff_data_list = staff_data_list
        self.services_data_list = services_data_list

    async def get_all_services_titles(self):
        """
        Функция для получения списка названий всех услуг.

        :return: Список названий услуг
        """
        return [service['title'] for service in self.services_data_list]

    async def get_staff_for_service(self, service_title):
        """
        Функция для получения имён сотрудников, которые занимаются определенной услугой.

        :param service_title: Название услуги, для которой нужно найти сотрудников
        :return: Список имён сотрудников, которые занимаются данной услугой
        """
        # Находим услугу по её названию
        service = next((s for s in self.services_data_list if s['title'] == service_title), None)

        if service is None:
            # Если услуга не найдена, возвращаем пустой список
            return []

        # Получаем список сотрудников, которые оказывают эту услугу
        service_staff_ids = [staff_member['id'] for staff_member in service['staff']]

        # Находим сотрудников по их id
        staff_names = [
            staff['name']
            for staff in self.staff_data_list
            if staff['id'] in service_staff_ids and staff['specialization'] == service_title
        ]

        return staff_names
