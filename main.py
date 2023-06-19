import psycopg2


#1 Создание таблиц
def create_db (cur):
    
    
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

#2 Наполнение таблиц клиентами
def add_client (cur, first_name, last_name, email):

    cur.execute("""
    INSERT INTO Client(name, surname, email) VALUES(%s, %s, %s);
    """, (first_name, last_name, email))

#3  Добавление телефона для сущестующего клиента
def add_phone (cur, client_id, phone):

    cur.execute("""
    INSERT INTO Phone(client_id, phone) VALUES((SELECT client_id FROM Client WHERE client_id=%s), %s);
    """, (client_id, phone))

#4 Измененние данных о клиенте  
def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):

    if first_name is not None:
        cur.execute("""
        UPDATE Client SET name=%s 
        WHERE client_id=%s;
        """, (first_name, client_id))

    if last_name is not None:
        cur.execute("""
        UPDATE Client SET surname=%s 
        WHERE client_id=%s;
        """, (last_name, client_id))

    if email is not None:
        cur.execute("""
        UPDATE Client SET email=%s 
        WHERE client_id=%s;
        """, (email, client_id)) 

    if phones is not None:
        cur.execute("""
        UPDATE Phone SET phone=%s 
        WHERE client_id=%s;
        """, (phones, client_id))    


#5 Удаление телефона существующего клиента 
def delete_phone(cur, client_id, phone):
    cur.execute("""
    DELETE FROM Phone 
    WHERE client_id=(SELECT client_id FROM Phone
    WHERE client_id=%s and phone=%s);
    """, (client_id, phone))
       
#6 Удаление существующего клиента
def delete_client(cur, client_id):
    cur.execute("""
    DELETE FROM Phone WHERE client_id=%s;
    """, (client_id,))

    cur.execute("""
    DELETE FROM Client WHERE client_id=%s;
    """, (client_id,))

#7 Поиск клиента по его данным
def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if first_name != None and last_name != None and email != None and phone != None:
        cur.execute("""
        SELECT name, surname, email, phone FROM Client
        LEFT JOIN Phone ON Client.client_id = Phone.client_id 
        WHERE Client.name=%s AND Client.surname=%s AND Client.email=%s AND Phone.phone=%s;
        """, (first_name, last_name, email, phone))
        return print(cur.fetchall())

    elif first_name or last_name or email or phone is not None:
         cur.execute("""
         SELECT name, surname, email, phone FROM Client
         LEFT JOIN Phone ON Client.client_id = Phone.client_id 
         WHERE Client.name=%s OR Client.surname=%s OR Client.email=%s OR Phone.phone=%s;
         """, (first_name, last_name, email, phone))
         return print(cur.fetchall())   





conn = psycopg2.connect(database="clients_db", user="postgres", password="romarchuk")

if __name__ == "__main__":

    with conn.cursor() as cur:

        create_db(cur,) 
        add_client(cur, 'Tom', 'Thomas', 'tt@mail.ru') 
        add_client(cur, 'Rom', 'Rhomas', 'rr@mail.ru')
        add_client(cur, 'Som', 'Shomas', 'ss@mail.ru')
        add_phone(cur, 1, '89081848176')
        add_phone(cur, 1, '89081848179')
        add_phone(cur, 2, '89081848180')
        add_phone(cur, 3, '89081848177')
        change_client (cur, 2, 'Romy', 'Rhomason', None, '89081848190')
        delete_phone (cur, 2, '89081848178')
        delete_client (cur, 2)
        find_client (cur, 'Tom', 'Thomas',)
        conn.commit()

conn.close()
   






