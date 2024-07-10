CREATE TABLE IF NOT EXISTS exam(
    id integer primary key autoincrement,
    title text,
    cfu integer,
    grade integer,
    passed boolean
);