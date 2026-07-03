import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
''')

cur.execute('''
INSERT INTO employees (name, department, salary) VALUES
('Aathi', 'Engineering', 90000),
('Priya', 'Engineering', 85000),
('Rahul', 'Marketing', 75000),
('Sneha', 'HR', 65000),
('Vikram', 'Marketing', 72000)
''')

conn.commit()

print("Database created!")
cur.execute("SELECT * FROM employees")
print(cur.fetchall())

conn.close()
