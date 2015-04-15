from sqlalchemy import create_engine
# import sqlite

engine = create_engine("sqlite:///test.db")
# engine.execute("""CREATE TABLE employee (
# 	emp_id INTERGER PRIMARY KEY,
# 	emp_name VARCHAR(30)
# 	)""")

# engine.execute("insert into employee (emp_name) values (:name)", name='dilbert')
result = engine.execute("select * from employee")
print result.fetchall()
# print engine.fetchall()