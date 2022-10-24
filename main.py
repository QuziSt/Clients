import psycopg2
import getpass
from sql_creations import *
from tables import *
from create_user import User


def start():
    while True:
        user = User()
        answers = {'Добавить абонента': user.create,
                   'Выбрать существующего абонента': tables_operations.pick_one,
                   'Показать список всех абонентов': tables_operations.show_all,
                   'Выйти': ''}
        title = 'Добро пожаловать в архив'
        answer, index = pick([key for key in answers], title,  indicator='=>')
        if answer == 'Выйти':
            return
        else:
            answers[answer](conn)


def authorization():
    sql.database_name = input('Введите имя базы данных для подключения:\n')
    sql.username = input('Введите логин:\n')
    sql.password = getpass.getpass('Введите пароль: ')
    return sql.database_name, sql.username, sql.password


if __name__ == "__main__":
    os.system('cls || clear')
    sql = Sql()
    tables_operations = Table()
    res = authorization()
    conn = psycopg2.connect(database=res[0], user=res[1], password=res[2])
    sql.create_tables(conn)
    start()
    conn.close()
    os.system('cls || clear')
    print('До свидания!')
