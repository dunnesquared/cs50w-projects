DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS books; -- Comment this out to avoid having to reimport all the books again

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL
);

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL UNIQUE,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  opinion VARCHAR NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  book_id INTEGER REFERENCES books,
  user_id INTEGER REFERENCES users
);

-- Sample users
INSERT INTO users
  (name, password)
  VALUES ('admin', '123');

INSERT INTO users
  (name, password)
  VALUES ('borat', '999');

-- Sample reviews
-- INSERT INTO reviews
--   (opinion, rating, book_id, user_id)
--   VALUES ('The first book I ever read! Awesome!', 4, 1, 1);
--
-- INSERT INTO reviews
--   (opinion, rating, book_id, user_id)
--   VALUES ('The first book I ever read! Awesome!', 1, 1, 2);
