import mysql.connector
mycon=mysql.connector.connect(host="localhost",user="root",password="sql123")
cur=mycon.cursor()
cur.execute("create database bank")
mycon.commit()
cur.execute("use bank")
mycon.commit()
cur.execute(f'create table account(name char(20) not null,account_number varchar(10) primary key, dob date,address varchar(200),phone_number char(10) unique,opening_balance float,pwd varchar(10) not null)')
mycon.commit()
cur.execute(f'create table amount(t_no int,account_number varchar(10),t_date date,t_type char(1),t_amount float,balance float,primary key(t_no,account_number))')
mycon.commit()
cur.execute(f'create table admin(name varchar(10),pwd varchar(10))')
mycon.commit()
cur.execute(f'insert into admin values("admin1","abcde12345")')
cur.execute(f'insert into admin values("admin2","abcde12345")')
mycon.commit()
cur.execute(f'insert into account values("Person1","sb101","2005/12/1","4th street",9221222221,90000,"hi123")')
cur.execute(f'insert into account values("Person2","sb102","2005/12/2","5th street",9221222220,80000,"hi123")')
cur.execute(f'insert into account values("Person3","sb103","2005/12/3","6th street",9221222229,70000,"hi123")')
cur.execute(f'insert into account values("Person4","sb104","2005/12/4","12th street",9221222227,50000,"hi123")')
mycon.commit()
cur.execute(f'insert into amount values({1},"sb101","2023/2/9","D",90000,90000)')
cur.execute(f'insert into amount values({1},"sb102","2023/2/9","D",80000,80000)')
cur.execute(f'insert into amount values({1},"sb103","2023/2/9","D",70000,70000)')
cur.execute(f'insert into amount values({1},"sb104","2023/2/9","D",50000,50000)')
mycon.commit()
