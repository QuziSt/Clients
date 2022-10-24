import os
from psycopg2 import sql
from pick import pick


class Table:
    def __init__(self):
        pass

    def show_all(self, conn):
        os.system('cls || clear')
        with conn.cursor() as cur:
            cur.execute('''SELECT name, surname FROM users''')
            for user in cur.fetchall():
                print(user[0], user[1],  end='\n')
            while input('Для выхода нажмите Enter') != '':
                continue
            return

    def pick_one(self, conn):
        os.system('cls || clear')
        search_by = {
                    'Имя': ['name', 'имя'],
                    'Фамилия': ['surname', 'фамилию'],
                    'E-mail': ['email', 'e-mail'],
                    'Номер Телефона': ['number', 'номер телефона']}
        keys = [key for key in search_by.keys()]
        ask = 'По какому параметру найти пользователя(ей)?'
        search, index = pick(keys, ask, indicator='=>')
        param = input(f'Введите {search_by[search][1]} абонента:\n')
        while param == '':
            print('Ошибка ввода.')
            param = input(f'Введите {search_by[search][1]} абонента:\n')
        try:
            info = self.get_user_info(conn, search_by[search][0], param)
            users = []
            for person in info:
                users += {f'{person[0]} {person[1]} {person[2]}': None}
            picked_user, index = pick(users, 'Выберите пользователя:', indicator='=>')
            menu = {'Посмотреть номер(а) абонента': self.get_user_numbers,
                    'Добавить номер': self.add_number,
                    'Изменить данные': self.edit_user_info,
                    'Удалить номер(а)': self.delete_number,
                    'Удалить абонента': self.delete_user,
                    }
            action, index = pick([key for key in menu], f'{picked_user}\nВыберите действие:', indicator='=>')
            menu[action](picked_user.split()[-1], conn)
        except ValueError:
            print('Ошибка')
            while input('Для возврата в главное меню нажмите Enter') != '':
                input('Для возврата в главное меню нажмите Enter')

    def get_user_info(self, conn, search_param, param):
            with conn.cursor() as cur:
                search = sql.SQL('''
                SELECT name, surname, email 
                FROM users u
                LEFT JOIN numbers n ON n.user_id = u.id
                WHERE {search_param}={param}
                GROUP BY name, surname, email
                                    ''').format(search_param=sql.Identifier(search_param),
                                                param=sql.Literal(param))
                cur.execute(search)
                info = cur.fetchall()
                return info

    def get_user_numbers(self, param, conn):
        os.system('cls || clear')
        with conn.cursor() as cur:
            cur.execute('''
            SELECT number FROM numbers n
            JOIN users u ON n.user_id = u.id
            WHERE email=%s
            ''', (param, ))
            result = cur.fetchall()
            numbers = [number[0] for number in result]
        if len(numbers) == 0:
            print('Нет номеров')
        else:
            print(*numbers, sep='\n')
        while input('Для выхода в главное меню нажмите Enter') != '':
            input('Для выхода в главное меню нажмите Enter')

    def get_id(self, conn, email):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT id FROM users u 
            WHERE email=%s
                        ''', (email, ))
            return cur.fetchone()[0]

    def add_number(self, email, conn):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT number FROM numbers n
            JOIN users u ON n.user_id = u.id
            WHERE email=%s
                        ''', (email,))
            result = cur.fetchall()
        while True:
            number = input('Введите номер телефона в формате: 79998887766\n'
                           'Если не хотите добавлять номер, нажмите Enter\n')
            if number == '':
                break
            elif not number.isdigit() or len(number) != 11 or number[0] != '7':
                print('Неверный формат номера')
                continue
            elif number in result:
                print('Номер занят')
            else:
                break
        user_id = self.get_id(conn, email)
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO numbers(user_id,number)
            VALUES(%s,%s)
            ''', (user_id, number))
        conn.commit()

    def edit_user_info(self, email, conn):
        changes = {'Имя': ['name', 'имя'],
                  'Фамилию': ['surname', 'фамилию'],
                  'E-mail': ['email', 'email'],
                   }
        change, index = pick([key for key in changes], 'Что вы хотели бы изменить?', indicator='=>')
        new_data = input(f'Введите {changes[change][1]}')
        user_id = self.get_id(conn, email)
        with conn.cursor() as cur:
            edit = sql.SQL('''
            UPDATE users SET {param}={new_data}
            WHERE id={user_id}
            ''').format(param=sql.Identifier(changes[change][0]), new_data=sql.Literal(new_data),
                        user_id=sql.Literal(user_id))
            cur.execute(edit)
        conn.commit()

    def delete_number(self, email, conn):
        user_id = self.get_id(conn, email)
        with conn.cursor() as cur:
            cur.execute('''
            SELECT number from numbers
            WHERE user_id = %s''', (user_id, ))
            result = cur.fetchall()
            numbers = [number[0] for number in result]
        number, index = pick(numbers, 'Выберите номер для удаления:', indicator='=>')
        with conn.cursor() as cur:
            cur.execute('''
        DELETE FROM numbers WHERE user_id=%s and number=%s
        ''', (user_id, number))
        conn.commit()

    def delete_user(self, email, conn):
        user_id = self.get_id(conn, email)
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM numbers 
            WHERE user_id=%s
            ''', (user_id,))
            cur.execute('''
            DELETE FROM users u 
            WHERE id=%s
            ''', (user_id,))
            conn.commit()


