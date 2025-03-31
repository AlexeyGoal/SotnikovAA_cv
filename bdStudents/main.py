import  sqlite3

connection = sqlite3.connect("baza.db")
cursor = connection.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS level_education (
            id_level INTEGER PRIMARY KEY,
            name_education TEXT NOT NULL
        )
        """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS directions (
            id_direction INTEGER PRIMARY KEY,
            name_direction TEXT NOT NULL
        )
        """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS types_training (
            id_type INTEGER PRIMARY KEY,
            name_training TEXT NOT NULL
        )
        """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id_student INTEGER PRIMARY KEY AUTOINCREMENT,
            id_level INTEGER NOT NULL,
            id_direction INTEGER NOT NULL,
            id_type_direction INTEGER NOT NULL,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            patronymic TEXT,
            avr_score INTEGER NOT NULL,
            FOREIGN KEY (id_level) REFERENCES level_education (id_level),
            FOREIGN KEY (id_direction) REFERENCES directions (id_direction),
            FOREIGN KEY (id_type_direction) REFERENCES types_training (id_type)
        )
        """)


with open('levelEducaton.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 2:
                cursor.execute(
                    "INSERT INTO level_education VALUES (?, ?)",
                    (int(parts[0]), parts[1])
                )

with open('direction.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 2:
                cursor.execute(
                    "INSERT INTO directions VALUES (?, ?)",
                    (int(parts[0]), parts[1])
                )

with open('type_training.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 2:
                cursor.execute(
                    "INSERT INTO types_training VALUES (?, ?)",
                    (int(parts[0]), parts[1])
                )

with open('students.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 8:
                cursor.execute(
                    "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (int(parts[0]), int(parts[1]), int(parts[2]),
                     int(parts[3]), parts[4], parts[5], parts[6], int(parts[7]))
                )

connection.commit()

#1 запрос
cursor.execute("SELECT COUNT(*) FROM students")
print(f"Всего студентов: {cursor.fetchone()[0]}")


#2 запрос
print("\n2. Количество студентов по направлениям:")
cursor.execute("""
SELECT d.name_direction, COUNT(*) as count 
FROM students s
JOIN directions d ON s.id_direction = d.id_direction
GROUP BY d.name_direction
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")


# 3 запрос
print("\n3. Количество студентов по формам обучения:")
cursor.execute("""
SELECT t.name_training, COUNT(*) as count 
FROM students s
JOIN types_training t ON s.id_type_direction = t.id_type
GROUP BY t.name_training
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")


# 4 запрос
print("\n4. Максимальный, минимальный, средний баллы студентов по направлениям:")
cursor.execute("""
SELECT 
    d.name_direction,
    MAX(s.avr_score) as max_score,
    MIN(s.avr_score) as min_score,
    AVG(s.avr_score) as avg_score
FROM students s
JOIN directions d ON s.id_direction = d.id_direction
GROUP BY d.name_direction
""")
for row in cursor.fetchall():
    print(f"{row[0]}: Макс. {row[1]}, Мин. {row[2]}, Ср. {row[3]:.1f}")


# 5 запрос
print("\n5. Средний балл студентов по направлениям, уровням и формам обучения:")
cursor.execute("""
SELECT 
    d.name_direction,
    l.name_education,
    t.name_training,
    AVG(s.avr_score) as avg_score
FROM students s
JOIN directions d ON s.id_direction = d.id_direction
JOIN level_education l ON s.id_level = l.id_level
JOIN types_training t ON s.id_type_direction = t.id_type
GROUP BY d.name_direction, l.name_education, t.name_training
ORDER BY d.name_direction, l.name_education, t.name_training
""")
for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}, {row[2]}): {row[3]:.1f}")


# 6 запрос
print("\n6. Топ-5 студентов Прикладной Информатики очной формы обучения:")
cursor.execute("""
SELECT s.surname, s.name, s.patronymic, s.avr_score
FROM students s
JOIN directions d ON s.id_direction = d.id_direction
JOIN types_training t ON s.id_type_direction = t.id_type
WHERE d.name_direction = 'Прикладная информатика' AND t.name_training = 'Очная'
ORDER BY s.avr_score DESC
LIMIT 5
""")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. {row[0]} {row[1]} {row[2]}: {row[3]}")


# 7 запрос
print("\n7. Количество однофамильцев:")
cursor.execute("""
SELECT surname, COUNT(*) as count
FROM students
GROUP BY surname
HAVING COUNT(*) > 1
ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")


# 8 запрос
print("\n8. Полные тезки (совпадают ФИО):")
cursor.execute("""
SELECT surname, name, patronymic, COUNT(*) as count
FROM students
GROUP BY surname, name, patronymic
HAVING COUNT(*) > 1
""")
tezki = cursor.fetchall()
if tezki:
    for row in tezki:
        print(f"{row[0]} {row[1]} {row[2] or ''}: {row[3]}")
else:
    print("Полных тезок нет")

connection.close()
