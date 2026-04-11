import sqlite3

con = sqlite3.connect("db/test.db")
cur = con.cursor()

# cur.execute('CREATE TABLE fruit(name, colour)')
# cur.execute("INSERT INTO fruit VALUES('banana', 'yellow'),('strawberry', 'red')")
# con.commit()

data = [
    ('tomato', 'red'),
    ('cucumber', 'green')
]

cur.executemany("INSERT INTO fruit VALUES(?, ?)", data)

con.commit()

res = cur.execute("SELECT name FROM fruit")
result = res.fetchall()
print(result)