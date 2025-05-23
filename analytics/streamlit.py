import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

DB_NAME = "data.db"


def create_connection(db_file=DB_NAME):
    """
    Создаёт соединение с SQLite базой.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.error(f"Ошибка при подключении к базе данных: {e}")
    return conn


@st.cache_data
def load_users_data(_conn):
    """
    Загружает данные из таблицы `users`.
    """
    query = """
    SELECT id, id_telegram, fullname, tnumber
    FROM users
    """

    print(query)
    return pd.read_sql_query(query, _conn)


@st.cache_data
def load_claims_data(_conn):
    """
    Загружает данные из таблицы `claims`.
    """
    query = """
    SELECT id, user_id, master_id, service, date, time, state
    FROM claims
    """
    return pd.read_sql_query(query, _conn)


@st.cache_data
def load_workers_data(_conn):
    """
    Загружает данные из таблицы `workers`.
    """
    query = """
    SELECT id, user_id, username, staff_id
    FROM workers
    """
    return pd.read_sql_query(query, _conn)


@st.cache_data
def load_admins_data(_conn):
    """
    Загружает данные из таблицы `admins`.
    """
    query = """
    SELECT id, user_id, state
    FROM admins
    """
    return pd.read_sql_query(query, _conn)


def refresh_data():
    """
    Функция для обновления данных в session_state.
    """
    conn = create_connection()
    if conn:
        st.session_state["users"] = load_users_data(conn)
        st.session_state["claims"] = load_claims_data(conn)
        st.session_state["workers"] = load_workers_data(conn)
        st.session_state["admins"] = load_admins_data(conn)
        conn.close()
    else:
        st.error("Не удалось подключиться к базе данных.")


def main():
    st.set_page_config(page_title="Аналитика Бота", layout="wide")
    st.title("Аналитика по данным из SQLite")

    # Инициализация session_state для хранения данных
    if "users" not in st.session_state:
        refresh_data()

    # Кнопка обновления данных
    if st.button("Обновить данные"):
        refresh_data()

    # Загружаем данные из session_state
    users_df = st.session_state["users"]
    claims_df = st.session_state["claims"]
    workers_df = st.session_state["workers"]
    admins_df = st.session_state["admins"]

    # --- Общая статистика ---
    st.subheader("Общая статистика")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего пользователей", len(users_df))
    with col2:
        st.metric("Всего заявок", len(claims_df))
    with col3:
        st.metric("Всего мастеров", len(workers_df))
    with col4:
        st.metric("Всего админов", len(admins_df))

    st.markdown("---")

    # --- График: Распределение заявок по услугам ---
    st.subheader("Распределение заявок по услугам")

    if not claims_df.empty:
        service_counts = claims_df["service"].value_counts().reset_index()
        service_counts.columns = ["service", "count"]

        chart_service = (
            alt.Chart(service_counts)
            .mark_bar()
            .encode(
                x=alt.X("service", sort="-y", title="Услуга"),
                y=alt.Y("count", title="Количество заявок"),
                tooltip=["service", "count"],
            )
            .properties(width=700, height=400, title="Количество заявок по услугам")
        )
        st.altair_chart(chart_service, use_container_width=True)
    else:
        st.info("Нет данных о заявках в таблице claims.")

    st.markdown("---")

    # --- График: Заявки по датам (линейный график) ---
    st.subheader("Заявки по датам")

    if not claims_df.empty:
        # Преобразуем поле date в формат даты
        claims_df["date"] = pd.to_datetime(claims_df["date"], errors="coerce")

        # Группируем заявки по дате
        daily_claims = claims_df.groupby("date")["id"].count().reset_index()
        daily_claims.columns = ["date", "count"]

        if not daily_claims.empty:
            chart_date = (
                alt.Chart(daily_claims)
                .mark_line(point=True)
                .encode(
                    x=alt.X("date:T", title="Дата"),
                    y=alt.Y("count:Q", title="Количество заявок"),
                    tooltip=["date:T", "count:Q"],
                )
                .properties(width=700, height=400, title="Заявки по датам")
            )
            st.altair_chart(chart_date, use_container_width=True)

            # Фильтр по интервалу дат
            min_date = daily_claims["date"].min()
            max_date = daily_claims["date"].max()

            if min_date == max_date:
                st.warning("Все заявки имеют одну и ту же дату. Фильтр недоступен.")
            else:
                min_date = min_date.date()
                max_date = max_date.date()

                st.write("Фильтр по дате:")
                start_date, end_date = st.slider(
                    "Выберите интервал дат",
                    min_value=min_date,
                    max_value=max_date,
                    value=(min_date, max_date),
                    format="YYYY-MM-DD",
                )

                filtered_df = daily_claims[
                    (daily_claims["date"] >= pd.Timestamp(start_date))
                    & (daily_claims["date"] <= pd.Timestamp(end_date))
                ]
                st.dataframe(filtered_df)
        else:
            st.info("Даты заявок не преобразовались или отсутствуют.")
    else:
        st.info("Нет данных о заявках для анализа по датам.")

    st.markdown("---")

    # --- График: Распределение заявок по статусам ---
    st.subheader("Распределение заявок по статусам")

    if not claims_df.empty:
        state_counts = claims_df["state"].value_counts().reset_index()
        state_counts.columns = ["state", "count"]

        chart_state = (
            alt.Chart(state_counts)
            .mark_bar()
            .encode(
                x=alt.X("state:O", sort="-y", title="Статус заявки"),
                y=alt.Y("count:Q", title="Количество"),
                tooltip=["state", "count"],
            )
            .properties(width=700, height=400, title="Количество заявок по статусам")
        )
        st.altair_chart(chart_state, use_container_width=True)
    else:
        st.info("Нет данных о заявках для анализа статусов.")

    st.markdown("---")

    # --- График: Количество заявок по мастерам (master_id) ---
    st.subheader("Количество заявок по мастерам")

    if not claims_df.empty:
        master_counts = claims_df["master_id"].value_counts().reset_index()
        master_counts.columns = ["master_id", "count"]

        if not workers_df.empty:
            workers_map = workers_df.set_index("user_id")["username"].to_dict()
            master_counts["username"] = (
                master_counts["master_id"].map(workers_map).fillna("Неизвестно")
            )
        else:
            master_counts["username"] = master_counts["master_id"]

        chart_master = (
            alt.Chart(master_counts)
            .mark_bar()
            .encode(
                x=alt.X("username:N", sort="-y", title="Мастер"),
                y=alt.Y("count:Q", title="Количество заявок"),
                tooltip=["username", "count"],
            )
            .properties(width=700, height=400, title="Количество заявок по мастерам")
        )
        st.altair_chart(chart_master, use_container_width=True)
    else:
        st.info("Нет данных о мастерах или заявках.")

    st.markdown("---")

    # --- Последние 10 заявок ---
    st.subheader("Последние 10 заявок")
    if not claims_df.empty:
        st.write(
            claims_df.sort_values(by="id", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
    else:
        st.info("Нет данных о заявках.")

    st.markdown("---")

    # --- Данные о пользователях ---
    st.subheader("Полный список пользователей")
    st.dataframe(users_df)


if __name__ == "__main__":
    main()
