import os

from db_manager.abstract_db_manager import AbstractDBManager
import psycopg2
from dotenv import load_dotenv



class DBManager(AbstractDBManager):

   def __init__(self, database, user, password, host, port):
       self.conn = psycopg2.connect(database=database,
                                    user=user,
                                    password=password,
                                    host=host,
                                    port=port)


    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employer (
                id int PRIMARY KEY,
                name varchar(100),
                url varchar(100)            
                )
                """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                id int PRIMARY KEY,
                name varchar(100),
                url varchar(100)            
                )
            """)


        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass


    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'."""


load_dotenv()
db = DBManager(
        dbname='',
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
)
