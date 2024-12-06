# TOKEN = "b238a6679665f570af0f1a21ce183d7b"
# CID = 1186779
# FID = 1301768

from yclients import YClientsAPI

if __name__ == '__main__':

    TOKEN = "nzdj6eabmyj9kd3mbmjk"
    CID = 1186779
    FID = 1301768

    login = "hooooogrideeer@gmail.com"
    password = "zh33ek"

    # Create api object
    api = YClientsAPI(token=TOKEN, company_id=CID, form_id=FID)
    user_token = api.get_user_token(login, password)
    api.update_user_token(user_token)

    api.show_debugging()

    clients_data_list = api.get_clients_data()
    staff_data_list = api.get_staff()['data']
    services_data_list = api.get_services()['data']['services']

    all_clients_id = [client['id'] for client in clients_data_list]
    client_visits = api.get_visits_for_client(CID)

    print(clients_data_list)
    print(staff_data_list)
    for i in services_data_list:
        print(i)

