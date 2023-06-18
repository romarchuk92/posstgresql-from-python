import psycopg2


#1 Создание таблиц
def create_db (conn):
    
    with conn.cursor() as cur:
    
        cur.execute("""
        
        DROP TABLE Phone;
        DROP TABLE Client;

         """)   
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email VARCHAR(60) UNIQUE not null 
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES Client(client_id),
            phone VARCHAR(60) UNIQUE
        );
        """)
        conn.commit()

#2 Наполнение таблиц клиентами
def add_client (conn, first_name, last_name, email):

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Client(name, surname, email) VALUES(%s, %s, %s);
        """, (first_name, last_name, email))
        conn.commit()

#3  Добавление телефона для сущестующего клиента
def add_phone (conn, client_id, phone):

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Phone(client_id, phone) VALUES((SELECT client_id FROM Client WHERE client_id=%s), %s);
        """, (client_id, phone))
        conn.commit()

#4 Измененние даннфых о клиенте  
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):

    with conn.cursor() as cur:
        cur.execute("""
        UPDATE Client SET name=%s, surname=%s, email=%s 
        WHERE client_id=%s;
        """, (first_name, last_name, email, client_id))
        conn.commit()

        cur.execute("""
        UPDATE Phone SET phone=%s 
        WHERE client_id=%s;
        """, (phones, client_id))
        conn.commit()

#5 Удаление телефона существующего клиента 
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Phone 
        WHERE client_id=(SELECT client_id FROM Phone
        WHERE client_id=%s and phone=%s);
        """, (client_id, phone))
        conn.commit()
       
#6 Удаление существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Phone WHERE client_id=%s;
        """, (client_id,))

        cur.execute("""
        DELETE FROM Client WHERE client_id=%s;
        """, (client_id,))
        conn.commit() 

#7 Поиск клиента по его данным
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT name, surname, email, phone FROM Client
        LEFT JOIN Phone ON Client.client_id = Phone.client_id 
        WHERE Client.name=%s OR Client.surname=%s OR Client.email=%s OR Phone.phone=%s;
        """, (first_name, last_name, email, phone))
        return print(cur.fetchall())






with psycopg2.connect(database="clients_db", user="postgres", password="romarchuk") as conn:

    create_db(conn) 
    add_client(conn, 'Tom', 'Thomas', 'tt@mail.ru') 
    add_client(conn, 'Rom', 'Rhomas', 'rr@mail.ru')
    add_client(conn, 'Som', 'Shomas', 'ss@mail.ru')
    add_phone(conn, 1, '89081848176')
    add_phone(conn, 1, '89081848179')
    add_phone(conn, 2, '89081848180')
    add_phone(conn, 3, '89081848177')
    change_client (conn, 2, 'Romy', 'Rhomason', 'rrr@mail.ru', '89081848178')
    delete_phone (conn, 2, '89081848178')
    delete_client (conn, 2)
    find_client (conn, '', 'Shomas')

conn.close()
   






