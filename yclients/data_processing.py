def get_all_services_titles(services_data_list):
    """
    Функция для получения списка названий всех услуг.

    :param services_data_list: Список всех услуг
    :return: Список названий услуг
    """
    return [service['title'] for service in services_data_list]


def get_staff_for_service(service_title, services_data_list, staff_data_list):
    """
    Функция для получения имён сотрудников, которые занимаются определенной услугой.

    :param service_title: Название услуги, для которой нужно найти сотрудников
    :param services_data_list: Список всех услуг
    :param staff_data_list: Список всех сотрудников
    :return: Список имён сотрудников, которые занимаются данной услугой
    """
    # Находим id услуги по названию
    service_staff_ids = []
    for service_data in services_data_list:
        if service_title == service_data['title']:
            service_staff_ids = [staff_member['id'] for staff_member in service_data['staff']]

    # Находим сотрудников по их id
    staff_names = [
        staff['name']
        for staff in staff_data_list
        if staff['id'] in service_staff_ids
    ]

    return staff_names
