from api_client import get_data_from_api
from data_processing import get_all_services_titles, get_staff_for_service

# Usage exapmle
# staff_data_list, services_data_list = get_data_from_api()
#
# # Получаем все названия услуг
# all_services_titles = get_all_services_titles(services_data_list)
# print("Все услуги:", all_services_titles)
#
# service_title = "стрижка"
# staff_for_service = get_staff_for_service(service_title, services_data_list, staff_data_list)
# print(f"Сотрудники, которые занимаются услугой '{service_title}':", staff_for_service)
