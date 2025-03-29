import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('PRAGMA foreign_keys = ON')

#таблица "Магазин"
cursor.execute('''
CREATE TABLE IF NOT EXISTS shops (
    shop_id TEXT PRIMARY KEY,
    district TEXT NOT NULL,
    address TEXT NOT NULL
)
''')


with open('shopss.txt', 'r') as file:
    next(file)
    for line in file:
        data = [item.strip() for item in line.split('\t')]
        if len(data) == 3:
            cursor.execute('INSERT INTO shops (shop_id, district, address) VALUES (?, ?, ?)',
                          (data[0], data[1], data[2]))


# таблица "Товар"
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    article INTEGER PRIMARY KEY,
    department TEXT NOT NULL,
    product_name TEXT NOT NULL,
    unit TEXT NOT NULL,
    package_quantity REAL NOT NULL,
    supplier TEXT NOT NULL
)''')


with open('tovarr.txt', 'r') as file:
    next(file)
    for line in file:
        data = [item.strip() for item in line.split('\t')]
        if len(data) == 6:
            package_quantity = data[4].replace(',', '.')
            cursor.execute('''
            INSERT INTO products (article, department, product_name, unit, package_quantity, supplier)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (int(data[0]), data[1], data[2], data[3], float(package_quantity), data[5]))


#таблица "Движение товаров"
cursor.execute('''
CREATE TABLE IF NOT EXISTS operations (
    operation_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    store_id TEXT NOT NULL,
    article INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    operation_type TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (store_id) REFERENCES shops(shop_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (article) REFERENCES products(article)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)''')



with open('move_goods.txt', 'r') as file:
    next(file)
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 7:
            operation_id = int(parts[0])
            date = parts[1]
            store_id = parts[2]
            article = int(parts[3])
            quantity = int(parts[4])
            operation_type = parts[5]
            price = float(parts[6])
            cursor.execute('''
            INSERT INTO operations (operation_id, date, store_id, article, quantity, operation_type, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (operation_id, date, store_id, article, quantity, operation_type, price))

# запрос для решения задачи
cursor.execute('''
SELECT ROUND(SUM(o.quantity * p.package_quantity), 1) AS total_liters
FROM operations o
JOIN products p ON o.article = p.article
JOIN shops s ON o.store_id = s.shop_id
WHERE p.product_name = 'Smetana 15%'
    AND s.district = 'Oktabrskiy'
    AND o.date BETWEEN '01.06.2021' AND '10.06.2021'
    AND o.operation_type = 'Sale'
''')


result = cursor.fetchone()
print(f"Продано сметаны 15% в Октябрьском районе: {result[0] } л")




