from config import TEST_URL, TEST_KEY
from canvasapi import Canvas
from canvasapi.account import Account
from faker import Faker
from pandas import DataFrame, read_csv

canvas = Canvas(TEST_URL, TEST_KEY)
fake = Faker()

print("Fetching accounts...")
accounts: list[Account] = canvas.get_accounts()

accounts_dict: dict[int, Account] = {}

print("Accounts:")
for account in accounts:
    accounts_dict[account.id] = account
    print(f"ID: {account.id}\nName:{account.name}\n")

account_id_selection: int = input("Select account: ")

print(f"Select {accounts_dict[int(account_id_selection)].name}")


def generate_mock_student_sis_import(student_nr: int):
    student_details = []

    for i in range(1, student_nr):
        user_id = i
        rand_first_name = fake.first_name()
        rand_last_name = fake.last_name()
        rand_short_name = f"{rand_first_name} {rand_last_name}"
        rand_email = (
            f"{str.lower(rand_first_name)}.{str.lower(rand_last_name)}@student.vynk.co"
        )
        login_id = str.lower(rand_first_name[:3] + rand_last_name[:3] + str(user_id))
        password = login_id + login_id

        student_details.append(
            {
                "user_id": user_id,
                "login_id": login_id,
                "password": password,
                "first_name": rand_first_name,
                "last_name": rand_last_name,
                "short_name": rand_short_name,
                "email": rand_email,
                "status": "active",
                "declared_user_typ": "student",
            }
        )

    df_student_sis_import = DataFrame(student_details)

    df_student_sis_import.to_csv("./sis_files/students.csv", index=False)


# generate_mock_student_sis_import(10)

courses_accounts_df = read_csv(
    "./sis_files/courses_accounts.csv", encoding="utf-8", index_col=["Code"]
)

course_sample_size = int(
    input(f"How many courses should be loaded (0 to {len(courses_accounts_df)}): ")
)

course_sample_df = courses_accounts_df.head(course_sample_size)

print(course_sample_df)

accounts = course_sample_df["Subject"].unique()
print("Nr of accounts: " + str(len(accounts)))
