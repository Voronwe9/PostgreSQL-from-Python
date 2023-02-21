import psycopg2
from pprint import pprint

def create_db(connect, cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
            );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_book(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES accounts(client_id) ON DELETE CASCADE,
            phone CHAR(50)
            );
        """)

    conn.commit()
def delete_table(cursor):

    cursor.execute("""
            DROP TABLE accounts, phone_book CASCADE;
            """)
def add_accounts(cursor, first_name=None, last_name=None, email=None, phone=None):
    cursor.execute("""
            INSERT INTO accounts(first_name, last_name, email) 
            VALUES (%s, %s, %s)
            RETURNING client_id, first_name, last_name;
            """, (first_name, last_name, email))
    account = cur.fetchone()
    if phone is not None:
        cur.execute("""
                INSERT INTO phone_book(client_id, phone)
                VALUES (%s, %s)
                RETURNING phone;
                """, (account[0], phone))
        cur.fetchone()
    print('Клиент', *account[1:], 'добавлен(-а) в таблицу.')

def add_phone(cursor, client_id, phone):
    cursor.execute("""
            INSERT INTO phone_book(client_id, phone)
            VALUES (%s, %s)
            RETURNING client_id, phone;
            """, (client_id, phone))
    number = cur.fetchone()
    print(f'Для клиента с id {number[0]} добавлен номер телефона {number[1]}.')


def change_accounts(connect, cursor, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cursor.execute("""
            UPDATE accounts SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
            UPDATE accounts SET last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
    if email is not None:
        cur.execute("""
            UPDATE accounts SET email=%s WHERE client_id=%s;
            """, (email, client_id))
    if phone is not None:
        cur.execute("""
            UPDATE phone_book SET phone=%s WHERE client_id=%s;
            """, (phone, client_id))
    connect.commit()
    print(f'Данные клиента с id {client_id} изменены.')


def delete_phone(connect, cursor, client_id, phone):
    cursor.execute("""
            DELETE FROM phone_book WHERE client_id=%s AND phone=%s;
            """, (client_id, phone))
    connect.commit()
    print(f'Номер телефона {phone} для клиента с id {client_id} удален.')


def delete_account(connect, cursor, client_id):
    cursor.execute("""
            DELETE FROM accounts WHERE client_id=%s;
            """, (client_id,))
    connect.commit()
    print(f'Клиент с id {client_id} удален.')


def find_account(cursor, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cursor.execute("""
                SELECT a.client_id, a.first_name, a.last_name, a.email, p.phone FROM accounts AS a
                LEFT JOIN phone_book AS p ON a.client_id = p.client_id
                WHERE a.first_name LIKE %s""", (first_name,))
        pprint(cur.fetchall())
    if last_name is not None:
        cursor.execute("""
                SELECT a.client_id, a.first_name, a.last_name, a.email, p.phone FROM accounts AS a
                LEFT JOIN phone_book AS p ON a.client_id = p.client_id
                WHERE a.last_name LIKE %s""", (last_name,))
        pprint(cur.fetchall())
    if email is not None:
        cursor.execute("""
                SELECT a.client_id, a.first_name, a.last_name, a.email, p.phone FROM accounts AS a
                LEFT JOIN phone_book AS p ON a.client_id = p.client_id
                WHERE a.email LIKE %s""", (email,))
        pprint(cur.fetchall())
    if phone is not None:
        cursor.execute("""
                SELECT a.client_id, a.first_name, a.last_name, a.email, p.phone FROM accounts AS a
                LEFT JOIN phone_book AS p ON a.client_id = p.client_id
                WHERE p.phone LIKE %s""", (phone,))
        pprint(cur.fetchall())


def all_accounts(cursor):
    cursor.execute("""
            SELECT a.client_id, first_name, last_name, email, phone FROM accounts AS a
            LEFT JOIN phone_book AS p ON a.client_id = p.client_id
            ORDER BY client_id;
            """)
    pprint(cur.fetchall())

with psycopg2.connect(database="HW_db", user="postgres", password="1131") as conn:
    with conn.cursor() as cur:
        delete_table(cur)
        create_db(conn, cur)
        add_accounts(cur, 'София', 'Та', 'gfhtryhg@gmail.com', '+99554613246')
        add_accounts(cur, 'Ольга', 'Эта', 'tryjyhg@gmail.com')
        add_accounts(cur, 'Петр', 'Тот', 'safdfdgtr@gmail.com', '+99554613265')
        add_accounts(cur, 'Антон', 'Ничей', 'lkdhsflns3@gmail.com', '+9956546513465')
        all_accounts(cur)
        add_phone(cur, '1', '+99565413216')
        add_phone(cur, '2', '+99565684955')
        add_phone(cur, '3', '+99512154646')
        all_accounts(cur)
        change_accounts(conn, cur, '1', 'Леонид', None, 'dsfgffyh@gmail.com')
        change_accounts(conn, cur, '2', None, None, 'sadadfvds@gmail.com')
        change_accounts(conn, cur, '4', None, 'Зачем', None, '+99556332316')
        all_accounts(cur)
        delete_phone(conn, cur, 1, '+99554613246')
        delete_account(conn, cur, 2)
        all_accounts(cur)
        find_account(cur, 'София')
        find_account(cur, None, 'Та')
        find_account(cur, None, None, 'safdfdgtr@gmail.com')
        find_account(cur, None, None, None, '+995656849875')
        all_accounts(cur)
conn.close()





        







