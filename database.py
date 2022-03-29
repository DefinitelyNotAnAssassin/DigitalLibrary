import sqlite3


conn = sqlite3.connect("library.db")
c = conn.cursor()

#c.execute('''CREATE TABLE libraryfiles(
 # booktitle text,
#  filename text,
#  author text
  
  
#  )''')

result = c.fetchall()
print(result)