import os


class User:
    def __init__(self):
        self.numbers = []

    def create(self, conn):

        os.system('cls || clear')
        name = input('Введите имя:\n')
        while name == '':
            name = input('Введите имя:\n')
        self.first_name = name
        surname = input('Введите фамилию:\n')
        while surname == '':
            surname = input('Введите фамилию:\n')
        self.second_name = surname
        while True:
            email = input('Введите email:\n')
            if email == '' or email.find('@') == -1 or email.find('@') != email.rfind('@') or email.find('.') == -1\
                    or email.rfind('.') < email.rfind('@'):
                print('Не верный формат ввода, попробуйте еще раз.')
                continue
            elif email in self.get_all_emails(conn):
                print('Email занят.')
                continue
            else:
                break
        self.email = email
        while True:
            number = input('Введите номер телефона в формате: 79998887766\n'
        'Если не хотите добавлять номер, нажмите Enter\n')
            if number == '':
                break
            elif not number.isdigit() or len(number) != 11 or number[0] != '7':
                print('Неверный формат номера')
                continue
            elif number in self.numbers or number in self.get_all_numbers(conn):
                print('Номер занят.')
            else:
                self.numbers.append(number)
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO users(name, surname, email)
                        VALUES(%s, %s, %s);''', (self.first_name, self.second_name, self.email))

            for number in self.numbers:
                cur.execute('''
                            INSERT INTO numbers(user_id, number)
                            VALUES(%s, %s);''', (self.get_user_id(conn), number))
            conn.commit()

    def get_user_id(self, conn):
        with conn.cursor() as cur:
            cur.execute('''SELECT id FROM users WHERE email = %s;''', (self.email, ))
            return cur.fetchone()[0]

    def get_all_numbers(self, conn):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT number FROM numbers
            ''')
            numbers = [number[0] for number in cur.fetchall()]
            return numbers

    def get_all_emails(self, conn):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT email FROM users
            ''')
            emails = [email[0] for email in cur.fetchall()]
            return emails

    def get_all_names(self, conn):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT name FROM users
            ''')
            names = [name[0] for name in cur.fetchall()]
            return names

    def get_all_surnames(self, conn):
        with conn.cursor() as cur:
            cur.execute('''
            SELECT surname FROM users
            ''')
            surnames = [surname[0] for surname in cur.fetchall()]
            return surnames

