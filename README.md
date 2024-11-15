**Telegram-бот для записи в салон**

**Описание:**
Этот проект представляет собой Telegram-бота, предназначенного для записи клиентов в салон красоты с использованием API YClients. 

**Структура проекта:**

- yclients - содержит модули, связанные с интеграцией Yclients API: 
    - api_client.py: клиент для запросов к Yclients API (например, получение расписания мастеров). 
  - data_processing.py: модули для обработки данных, приходящих от Yclients (парсинг, приведение в нужный формат).

- bot - директория с основным кодом бота: 
  - main.py: основной файл запуска бота, инициализирует все хендлеры и сервисы. 
  - handlers/: папка с хендлерами для Телеграм-бота: 
     - client_handlers.py: хендлеры для клиентов, такие как запись к мастеру, уведомления и подтверждения. 
     - master_handlers.py: хендлеры для мастеров, отправка информации о записях и др. 
     - common_handlers.py: общие хендлеры, такие как команды "/start", "/help". 
  - services/: папка с логикой для различных сервисов, поддерживающих работу бота: 
     - schedule_service.py: загрузка и обработка расписания мастеров. 
     - notification_service.py: отправка уведомлений клиентам о предстоящих записях. 
     - calendar_service.py: логика для интеграции с Google и Apple календарями. 
     - statistics_service.py: логика сбора и обработки статистики по записям. 
  - utils/: вспомогательные функции и утилиты для обработки данных: 
     - validation.py: валидация данных, получаемых от клиентов. 
     - formatters.py: функции для форматирования текста, дат и других данных. 
     - helpers.py: другие вспомогательные функции. 

- reports - папка для отчетов и статистики: 
    excel_reports/ и csv_reports/: здесь будут храниться отчеты для салона в разных форматах. 

- requirements.txt - файл для установки зависимостей проекта.

- README.md - описание и структура проекта.

**Архитектура:**

1. **База данных:**
   - **Клиенты:** хранит данные о клиентах (ID, ФИО, номер телефона).
   - **Мастера:** хранит данные о мастерах (ID, ФИО, номер телефона, специализация, стаж, график работы).
   - **Записи:** информация о записях (ID, дата, время, услуга, мастер, клиент, комментарий, статус заявки).
   - **Статистика:** собирает статистику салона (число записей за день/месяц, эффективность мастера, доход)

2. **Основной функционал:**
   - **Запись к мастерам:** Подгрузка графиков через YClients и управление записями.
   - **Уведомления:** Уведомления перед мероприятием и после записи.
   - **Google/Apple календари:** Возможность интеграции записей в пользовательские календари.
   - **Функционал для мастеров:** Обзор и уведомления о предстоящих событиях.
   - **Аналитика:** Сбор и визуализация данных по посещениям и эффективности.
