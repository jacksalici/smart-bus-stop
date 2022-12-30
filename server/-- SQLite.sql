-- SQLite

-- demo table only!! 
CREATE TABLE users(
    id text PRIMARY key,
    email text ,
    credit real,
    name text,
    pw text
)

INSERT INTO users(id,email,credit,name,pw)
VALUES
    ('111-111-111', 'mail@mail.com', 5.0, 'John Doe', 'abcdef')


