create table classification(cf_num numeric(3,0) primary key, cf_name char(5));
create table books(book_id numeric(8,0), author varchar(15), title varchar(15), publisher varchar(10), publish_year numeric(4,0), ISBN numeric(13,0), cf_num numeric(3,0) references classification, primary key(book_id));
create table member(id varchar(8) primary key, name varchar(20));
create table department(dept varchar(20) primary key, workplace varchar(20));
create table worker(id varchar(8) references member, name varchar(20), dept varchar(20) references department, salary numeric(8,2), primary key(id));
create table borrow(book_id numeric(8,0) references books, id varchar(8) references member, borrow date, return date, primary key(book_id, id));
