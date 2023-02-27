create table valute(
    id varchar(255) primary key,
    num_code integer,
    char_code varchar(255),
    nominal integer,
    name varchar(255)
);

create table valute_price(
    id integer primary key,
    value float,
    date date,
    valute_id varchar(255),
    FOREIGN KEY(valute_id) REFERENCES valute(id)
);