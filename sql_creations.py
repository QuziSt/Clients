
class Sql:
    def __init__(self):
        self.database_name = ''
        self.username = ''
        self.password = ''

    def create_tables(self, conn):
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(30) NOT NULL,
                        surname VARCHAR(30) NOT NULL,
                        email VARCHAR(60) UNIQUE);''')
            conn.commit()
            cur.execute('''CREATE TABLE IF NOT EXISTS numbers(
                        id SERIAL,
                        user_id int REFERENCES users(id),
                        number VARCHAR(11) UNIQUE);
                        ''')
            conn.commit()