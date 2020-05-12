drop database if exists sEmg;
create database sEmg;
use sEmg;

create table users(
    id varchar(255) primary key not null,
    psw varchar(255) not null,
    integral int default 0
);
insert into users(id, psw) values('sinscry', 'testpsw');
select * from users;