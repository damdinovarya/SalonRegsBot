# Telegram-бот для записи в салон - SalonRegsBot
Этот проект представляет собой Telegram-бота, предназначенного для записи клиентов в салон красоты с использованием API YClients. 

## Структура проекта:

- analytics/ - директория с файлами, связанная с аналитикой и визуализацией данных
  - streamlit.py - приложение на базе Streamlit для показа основных статистик салона с графиками

- database/ - директория с файлами, связанная с локальной базой данных
  - db_admin_requests.py - работа с таблицей админов
  - db_claim_requests.py - работа с таблицей заявок
  - db_user_requests.py - работа с таблицей пользователей
  - db_connection.py - подключение к базе данных и создание необходимых таблиц

- handlers/ - директория с хендлерами для Телеграм-бота
  - images/ - директория с шаблонами банеров позиций
  - client_handlers_admin - хендлеры для админов
  - client_handlers_claims - хендлеры для клиентов, такие как просмотр и отправка заявок
  - client_handlers_profile.py - хендлеры для клиентов, такие как создание и редактирование профиля
  - client_handlers_services.py - хендлеры для клиентов, такие как запись к мастеру
  - keyboard.py - Шаблоны клавиатур для взаимодействия
  - master_handlers.py - хендлеры для мастеров, отправка информации о записях и др

- reports/ - директория с отчетами и статистикой

- services/ - директория с дополнительными сервисами для бота
  - schedule_service.py: загрузка и обработка расписания мастеров
  - notification_service.py: отправка уведомлений клиентам о предстоящих записях
  - calendar_service.py: логика для интеграции с Google и Apple календарями
  - statistics_service.py: логика сбора и обработки статистики по записям

- utils/ - директория с вспомогательными функциями
  - helpers.py - вспомогательные функции 

- yclients_things/ - директория с файлами, связанные с интеграцией Yclients API
  - api_client.py - подключение к API YClients
  - data_processing.py - получение и обработка нужных данных, приходящих от Yclients

- main.py: основной файл запуска бота, инициализирует все хендлеры и сервисы
- requirements.txt - файл для установки зависимостей проекта
- README.md - описание и структура проекта

## Основной функционал

- **Запись к мастерам:** Подгрузка графиков c YClients и управление записями.
- **Админ панель:** Интерфейс для управления записями, пользователями и сотрудниками.
- **Панель для мастера:** Интерфейс для просмотра заявок (подвержение/отклонение).
- **Уведомления:** Уведомления перед мероприятием и после записи.
- **Google календарь:** Возможность интеграции записей в пользовательские календари.
- **Функционал для мастеров:** Обзор и уведомления о предстоящих событиях.
- **Аналитика:** Сбор и визуализация данных по посещениям и эффективности.

## Команда проекта

- Колчин Семен
  - Разработка UI ТГ-бота
  - Реализация уведомлений о предстоящих записях.
  - Реализация основного функционала ТГ-бота
- Дамдинов Арья
  - Интеграция с Yclients API для получения данных о мастерах и их расписании.
  - Разработка функционала по записи к мастеру (подгрузка графика, постановка записи в системе).
- Гуч Вячеслав
  - Обработка запросов на подтверждение записи.
  - Сбор и предоставление данных для визуализации статистики салона.
- Ляпин Никита
  - Создание базы данных для хранения информации о записях, мастерах и расписаниях.
  - Реализация функционала подгрузки записи в гугл/эпл календарь.
