import sqlite3

conn = sqlite3.connect('pass.db')
c = conn.cursor()
c.execute("""CREATE TABLE database (
		website text,
		username text,
		password text
		)""")
conn.commit()
conn.close()