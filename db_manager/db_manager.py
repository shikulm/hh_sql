import os
import sys

# from db_manager.abstract_db_manager import AbstractDBManager
from db_manager.abstract_db_manager import AbstractDBManager
import psycopg2


# sys.path.append(os.path.join(BASE_DIR.parent.parent, ""))


class PostgreDBManager(AbstractDBManager):

    def __init__(self, database, user, password, host, port):
        self.conn = psycopg2.connect(database=database,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)

    def create_tables(self):
        """Метод для создания таблиц"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employer (
                id_employer int PRIMARY KEY,
                name_employer varchar(100),
                url varchar(100)
                )
                """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                id_vacancy int PRIMARY KEY,
                name_vacancy varchar(150),
                id_employer int REFERENCES employer ON DELETE CASCADE,
                city varchar(100),
                salary_from numeric(10,2) NULL,
                salary_to numeric(10,2) NULL,
                url varchar(100),
                requirement text,
                responsibility text
                )
            """)

        self.conn.commit()

    def drop_tables(self):
        """Метод для удаления таблиц из БД"""
        with self.conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS vacancies
                """)

            cur.execute("""
                DROP TABLE IF EXISTS employer
                """)

        self.conn.commit()

    def filling_employer(self, data):
        """Заполнение таблицы filling_employer данными из словаря data"""
        with self.conn.cursor() as cur:
            for empl in data:
                cur.execute("""
                    INSERT INTO employer (id_employer, name_employer, url)
                    VALUES (%s, %s, %s);
                    """, (empl['id_employer'], empl['name_employer'], empl['url'])
                            )

        self.conn.commit()

    def filling_vacancies(self, data):
        """Заполнение таблицы filling_employer данными из словаря data"""
        with self.conn.cursor() as cur:
            for vac in data:
                cur.execute("""
                    INSERT INTO vacancies (id_vacancy, name_vacancy, id_employer, city, salary_from, salary_to, url, requirement, responsibility)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (vac['id_vacancy'], vac['name_vacancy'], vac['id_employer'], vac['city'], vac['salary_from'],
                          vac['salary_to'],
                          vac['url'], vac['requirement'], vac['responsibility'])
                            )

        self.conn.commit()

    def filling_tables(self, data_employer: list[dict], data_vacancies: list[dict]) -> None:
        """Заполнение таблиц базы данных"""
        self.drop_tables()
        self.create_tables()

        self.filling_employer(data_employer)
        # print(hh.get_vacancies())
        self.filling_vacancies(data_vacancies)

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id_employer, name_employer, e.url, count(*) as cnt
	                FROM public.employer AS e JOIN vacancies USING(id_employer)
	                GROUP BY id_employer, name_employer, e.url;
	                """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute("""
                 SELECT e.name_employer, v.name_vacancy, 
                    CONCAT(COALESCE('от '||salary_from::varchar(50), ''), COALESCE(' до '||salary_to::varchar(50), '')) AS salary, v.url
                    FROM public.employer AS e JOIN vacancies AS v USING(id_employer);
        	                """)
            return cur.fetchall()


    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT v.name_vacancy, avg(COALESCE(salary_from, salary_to))::NUMERIC(10,2) as avg_salary
                    FROM vacancies AS v
                    GROUP BY v.name_vacancy;
        	                """)
            return cur.fetchall()


    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT v.name_vacancy, 
                    CONCAT(COALESCE('от '||salary_from::varchar(50), ''), COALESCE(' до '||salary_to::varchar(50), '')) AS salary
                    FROM vacancies AS v
                    WHERE COALESCE(salary_from, salary_to) > 
                        (SELECT avg(COALESCE(salary_from, salary_to)) FROM vacancies)
                    ORDER BY COALESCE(salary_from, salary_to) desc
        	                """)
            return cur.fetchall()


    def get_vacancies_with_keyword(self, word: str):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                 SELECT e.name_employer, v.name_vacancy, 
                    CONCAT(COALESCE('от '||salary_from::varchar(50), ''), COALESCE(' до '||salary_to::varchar(50), '')) AS salary, v.url
                    FROM public.employer AS e JOIN vacancies AS v USING(id_employer)
                    WHERE upper(name_vacancy) LIKE '%{word.upper()}%' 
                    ORDER BY COALESCE(salary_from, salary_to) desc;
        	                """)
            return cur.fetchall()



