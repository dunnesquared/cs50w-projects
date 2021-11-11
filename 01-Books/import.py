"""Script that imports book data from 'books.csv'"""

import sys
import os
import csv

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Book table must exist before importing
try:
    books = db.execute("SELECT * FROM books")
except exc.ProgrammingError as err:
    print("Error: Cannot import book data.")
    print("Table 'books' does not exist. Please run SQL script 'schema.sql' before importing data.")
    sys.exit()

# Import data
try:
    with open('books.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header line
        next(reader, None)

        # To inform user of current of record being outputted
        count = 1

        # Insert data into database
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES \
                        (:isbn, :title, :author, :year)",
                        {"isbn": isbn,
                         "title": title,
                         "author": author,
                         "year": year})

            print(f"#{count}: Inserting record into table 'books': isbn = {isbn}")
            count += 1

        db.commit()

        print("Insertion of data from 'book.csv' into database complete.")

except OSError as err:
    print("OSError: {0}".format(err))
