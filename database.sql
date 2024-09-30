DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url;

CREATE TABLE urls(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE url(
    id SERIAL PRIMARY KEY,
    url_id SERIAL REFERENCES urls (id),
    status_code INT,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);
