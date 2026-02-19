import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Создаем таблицу клиентов
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT,
    company TEXT,
    email TEXT,
    status TEXT
)
''')

# Создаем таблицу заявок
cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    client_id INTEGER,
    issue TEXT,
    priority TEXT,
    created_at DATE,
    FOREIGN KEY(client_id) REFERENCES clients(id)
)
''')

# Заполняем данными
cursor.executemany('INSERT INTO clients (name, company, email, status) VALUES (?,?,?,?)', [
    ('Иван Иванов', 'ООО Ромашка', 'ivan@romashka.ru', 'VIP'),
    ('Петр Петров', 'ЗАО ГазМяс', 'petr@gaz.ru', 'Active'),
    ('Анна Сидорова', 'ИП Сидорова', 'anna@ip.ru', 'Blocked')
])

cursor.executemany('INSERT INTO tickets (client_id, issue, priority, created_at) VALUES (?,?,?,?)', [
    (1, 'Не работает вход в личный кабинет', 'High', '2023-10-25'),
    (1, 'Хочу продлить подписку', 'Low', '2023-10-26'),
    (2, 'Ошибка 404 при оплате', 'Critical', '2023-10-27')
])

conn.commit()
conn.close()
print("База данных crm.db создана!")