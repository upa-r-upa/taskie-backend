import os
import psycopg2
from psycopg2 import sql
import csv
import random
from datetime import datetime, timedelta

# 요일을 나타내는 숫자 리스트 (0: 월, 1: 화, ..., 6: 일)
WEEK_DAYS = ["0", "1", "2", "3", "4", "5", "6"]


# 랜덤한 요일 문자열을 생성하는 함수
def generate_random_days():
    num_days = random.randint(1, 7)  # 1~7개의 요일을 선택
    random_days = random.sample(WEEK_DAYS, num_days)
    random_days.sort()  # 요일이 순서대로 정렬되도록
    return "".join(random_days)  # 예: '012' -> 월, 화, 수


# 데이터베이스 연결 설정
def connect_to_db():
    conn = psycopg2.connect(
        dbname="taskie_test_db",
        user="testuser",
        password="testpass",
        host="127.0.0.1",
        port="9000",
    )
    return conn


# CSV 파일로 대량의 랜덤 데이터 생성
def generate_csv_for_user(file_name, row_count):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "username",
                "password",
                "email",
                "profile_image",
                "nickname",
            ]  # id 및 created_at 제외
        )

        for i in range(1, row_count + 1):
            username = f"user_{i}"
            password = f"pass_{i}"
            email = f"user_{i}@example.com"
            profile_image = f"profile_{i}.png"
            nickname = f"nick_{i}"
            writer.writerow(
                [username, password, email, profile_image, nickname]
            )

    print(f"Generated {row_count} rows of data into {file_name}.")


def generate_csv_for_habit(file_name, row_count, user_count):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "title",
                "end_time_minutes",
                "start_time_minutes",
                "repeat_days",
                "repeat_time_minutes",
                "activated",
                "user_id",
                "created_at",
                "updated_at",
            ]  # id 및 created_at 제외
        )

        for i in range(1, row_count + 1):
            title = f"Habit {i}"
            end_time_minutes = random.randint(0, 1440)
            start_time_minutes = random.randint(0, 1440)
            repeat_days = generate_random_days()  # 랜덤한 요일 생성
            repeat_time_minutes = random.randint(0, 1440)
            activated = random.choice([True, False])
            user_id = random.randint(1, user_count)
            created_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            updated_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(
                [
                    title,
                    end_time_minutes,
                    start_time_minutes,
                    repeat_days,
                    repeat_time_minutes,
                    activated,
                    user_id,
                    created_at,
                    updated_at,
                ]
            )

    print(f"Generated {row_count} rows of data into {file_name}.")


def generate_csv_for_habit_log(file_name, row_count, habit_count):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["completed_at", "habit_id"])  # id 제외

        for i in range(1, row_count + 1):
            completed_at = (
                datetime.now() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d %H:%M:%S")
            habit_id = random.randint(1, habit_count)
            writer.writerow([completed_at, habit_id])

    print(f"Generated {row_count} rows of data into {file_name}.")


def generate_csv_for_routine(file_name, row_count, user_count):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "title",
                "start_time_minutes",
                "repeat_days",
                "user_id",
                "created_at",
                "updated_at",
            ]  # id 및 created_at 제외
        )

        for i in range(1, row_count + 1):
            title = f"Routine {i}"
            start_time_minutes = random.randint(0, 1440)
            repeat_days = generate_random_days()  # 랜덤한 요일 생성
            user_id = random.randint(1, user_count)
            created_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            updated_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(
                [
                    title,
                    start_time_minutes,
                    repeat_days,
                    user_id,
                    created_at,
                    updated_at,
                ]
            )

    print(f"Generated {row_count} rows of data into {file_name}.")


def generate_csv_for_routine_element(
    file_name, row_count, routine_count, user_count
):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "title",
                "order",
                "duration_minutes",
                "routine_id",
                "created_at",
                "updated_at",
                "user_id",
            ]  # id 및 created_at 제외
        )

        for i in range(1, row_count + 1):
            title = f"Routine Element {i}"
            order = random.randint(1, 10)
            duration_minutes = random.randint(1, 120)
            routine_id = random.randint(1, routine_count)
            created_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            updated_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            user_id = random.randint(1, user_count)

            writer.writerow(
                [
                    title,
                    order,
                    duration_minutes,
                    routine_id,
                    created_at,
                    updated_at,
                    user_id,
                ]
            )

    print(f"Generated {row_count} rows of data into {file_name}.")


def prepare_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    print(f"Preparing file: {file_name}")


def generate_csv_for_routine_log(
    file_name, row_count, routine_count, routine_element_count
):
    prepare_file(file_name)

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "duration_seconds",
                "completed_at",
                "is_skipped",
                "routine_id",
                "routine_element_id",
            ]  # id 제외
        )

        for i in range(1, row_count + 1):
            duration_seconds = random.randint(30, 3600)
            completed_at = (
                datetime.now() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d %H:%M:%S")
            is_skipped = random.choice([True, False])
            routine_id = random.randint(1, routine_count)
            routine_element_id = random.randint(1, routine_element_count)
            writer.writerow(
                [
                    duration_seconds,
                    completed_at,
                    is_skipped,
                    routine_element_id,
                    routine_id,
                ]
            )

    print(f"Generated {row_count} rows of data into {file_name}.")


# PostgreSQL에 CSV 파일을 사용해 대량 데이터 삽입
def copy_from_csv(conn, table_name, file_name, columns):
    cursor = conn.cursor()
    with open(file_name, "r") as file:
        cursor.copy_expert(
            sql.SQL(
                """
            COPY {} ({}) FROM STDIN WITH CSV HEADER
        """
            ).format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
            ),
            file,
        )
    conn.commit()
    cursor.close()


# 데이터베이스 테이블에 대량 데이터 삽입
def insert_large_data():
    conn = connect_to_db()

    # 각 테이블에 대한 CSV 파일 생성 및 데이터 삽입
    user_count = 1000000
    habit_count = 1000000
    habit_log_count = 500000
    routine_count = 5000000
    routine_element_count = 200000
    routine_element_log_count = 100000

    # 사용자 데이터 생성 및 삽입
    generate_csv_for_user("mock/user_data.csv", user_count)
    copy_from_csv(
        conn,
        "user",
        "mock/user_data.csv",
        ["username", "password", "email", "profile_image", "nickname"],
    )

    # 습관 데이터 생성 및 삽입
    generate_csv_for_habit("mock/habit_data.csv", habit_count, user_count)
    copy_from_csv(
        conn,
        "habit",
        "mock/habit_data.csv",
        [
            "title",
            "end_time_minutes",
            "start_time_minutes",
            "repeat_days",
            "repeat_time_minutes",
            "activated",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )

    # 습관 로그 데이터 생성 및 삽입
    generate_csv_for_habit_log(
        "mock/habit_log_data.csv", habit_log_count, habit_count
    )
    copy_from_csv(
        conn,
        "habit_log",
        "mock/habit_log_data.csv",
        ["completed_at", "habit_id"],
    )

    # 루틴 데이터 생성 및 삽입
    generate_csv_for_routine(
        "mock/routine_data.csv", routine_count, user_count
    )
    copy_from_csv(
        conn,
        "routine",
        "mock/routine_data.csv",
        [
            "title",
            "start_time_minutes",
            "repeat_days",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )

    # 루틴 요소 데이터 생성 및 삽입
    generate_csv_for_routine_element(
        "mock/routine_element_data.csv",
        routine_element_count,
        routine_count,
        user_count,
    )
    copy_from_csv(
        conn,
        "routine_element",
        "mock/routine_element_data.csv",
        [
            "title",
            "order",
            "duration_minutes",
            "routine_id",
            "created_at",
            "updated_at",
            "user_id",
        ],
    )

    # 루틴 로그 데이터 생성 및 삽입
    generate_csv_for_routine_log(
        "mock/routine_log_data.csv",
        routine_element_log_count,
        routine_count,
        routine_element_count,
    )
    copy_from_csv(
        conn,
        "routine_log",
        "mock/routine_log_data.csv",
        [
            "duration_seconds",
            "completed_at",
            "is_skipped",
            "routine_element_id",
            "routine_id",
        ],
    )

    # 연결 종료
    conn.close()
    print("Data inserted successfully.")


if __name__ == "__main__":
    insert_large_data()
