import os
from get_api.get_api_hh import GetApiHh
from dotenv import load_dotenv
from utils import print_format
from db_manager.db_manager import PostgreDBManager

def sel_query(db) -> bool:
    while True:
        print('Выбрерите вариант запроса')
        print("1 - Получить список всех компаний и количество вакансий у каждой компании")
        print("2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
        print("3 - Получить среднюю зарплату по вакансиям")
        print("4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5 - Получает список всех вакансий, в названии которых содержатся переданные в метод слова")
        print("6 - Вернуться к предыдущему меню")
        print("7 - Завершить работу полностью")

        sel = input('> ').rstrip()
        print()
        if sel == '7':
            return False
        elif sel == '6':
            break
        elif sel == '1':
            print_format(('Код компании', 'Название компании', 'URL', 'Количество вакансий'), db.get_companies_and_vacancies_count())
        elif sel == '2':
            print_format(('Название компании', 'Название вакансии', 'Зарплата', 'URL вакансии'), db.get_all_vacancies())
        elif sel == '3':
            print_format(('Название вакансии', 'Средняя зарплата'), db.get_avg_salary())
        elif sel == '4':
            print_format(('Название вакансии', 'Средняя зарплата'), db.get_vacancies_with_higher_salary())
        elif sel == '5':
            print('Введте слово')
            wrd = input('> ').rstrip()
            print_format(('Название вакансии', 'Средняя зарплата'), db.get_vacancies_with_keyword(wrd))
        else:
            print('Таких вариантов нет. Попробуйте еще раз.')

    return True

def user_interface():
    load_dotenv()
    db = PostgreDBManager(
        database='work_db',
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )


    hh = GetApiHh()

    print("Здравствуйте! Познакомьтесь с системой для работы с вакансиями")
    while True:
        print('Выберите вариант:')
        print('1 - Заполнить БД значениями из HH')
        print('2 - Выполнить запросы к БД')
        print('3 - Завершить работу')

        sel = input('> ').rstrip()
        if sel == '3':
            break
        elif sel == '1':
            db.filling_tables(hh.get_employer(), hh.get_vacancies())
        elif sel == '2':
            res = sel_query(db)
            if not res:
                break
        else:
            print('Таких вариантов нет. Попробуйте еще раз.')


if __name__ == '__main__':
    user_interface()