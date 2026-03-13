import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Dastur konfiguratsiyasini saqlovchi klass.

    Ushbu klass `.env faylidan o'qilgan
    ma'lumotlar bazasi sozlamalarini saqlaydi.

    Atributlar:
        DB_USER (str): Database foydalanuvchi nomi
        DB_PASSWORD (str): Database paroli
        DB_HOST (str): Database host manzili
        DB_PORT (str): Database port raqami
        DB_NAME (str): Database nomi
    """

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")


config = Config()