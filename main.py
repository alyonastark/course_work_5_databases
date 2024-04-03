from src.HHData import HHData
from src.DBManager import DBManager


def user_interaction():
    choice = input("Для взаимодействия введите:\n"
                   "0 - найти работодателя;\n"
                   "1 - работать с базой данных\n")
    db_manager = DBManager()
    if choice == '0':
        while True:
            keyword = input("Введите поисковый запрос:\n"
                            "(нажмите 0, чтобы завершить работу программы)\n")
            if keyword == '0':
                break
            else:
                cls_object = HHData()
                employers = cls_object.get_employers(keyword)
                for emp in employers:
                    main_info = (f"{emp['name']}, {emp['alternate_url']},"
                                 f" количество открытых вакансий - {emp['open_vacancies']}")
                    print(main_info)
                    decision = input("Для взаимодействия введите:\n"
                                     "0 - добавить работодателя в базу данных;\n"
                                     "1 - продолжить поиск;\n"
                                     "2 - ввести новый поисковый запрос\n")
                    if decision == '0':
                        db_manager.add_employer(emp)
                        vacancies = cls_object.get_vacancies(emp)
                        db_manager.add_vacancies(vacancies)
                    elif decision == '1':
                        continue
                    elif decision == '2':
                        break
    elif choice == '1':
        while True:
            interaction = input("Для взаимодействия введите:\n"
                                "0 - получить список работодателей из бд;\n"
                                "1 - получить список всех вакансий из бд;\n"
                                "2 - получить вакансии с зп выше среднего;\n"
                                "3 - найти вакансии по ключевым словам;\n"
                                "4 - завершить работы программы\n")
            if interaction == '0':
                db_manager.get_companies_and_vacancies_count()
                continue
            elif interaction == '1':
                db_manager.get_all_vacancies()
                continue
            elif interaction == '2':
                avg_salary = db_manager.get_avg_salary()
                db_manager.get_vacancies_with_higher_salary(avg_salary)
                continue
            elif interaction == '3':
                search_query = input("Введите поисковый запрос: ").lower()
                db_manager.get_vacancies_with_keyword(search_query)
                continue
            else:
                db_manager.close_connection()
                break


if __name__ == '__main__':
    user_interaction()
