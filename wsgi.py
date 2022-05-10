from app import db, Books, Category
import random




data = [Books(f"BOOK{i}", f"FILE{i}") for i in range(100000)]

print("Data done")
db.session.bulk_save_objects(data, return_defaults=True)
print("Saving done")

print("Appending")
for i in data:
  var = Category.query.get(random.randint(1,10))
  var.booklist.append(i)

print("Commiting")
db.session.commit()
print("Success!!")