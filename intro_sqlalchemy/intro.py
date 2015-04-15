from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")

# postgresql
# create_engine("postgresql + psycopg2://jeff:tiger@localhost/text")

result = engine.execute("select emp_id, emp_name from employee where emp_id=:emp_id", emp_id=3)
row = result.fetchone()
#print row
# (3, u'Fred')
# repr(row)
# (3,u'Fred')
# also like a dict
# row['emp_name']
# u'Fred'

result.close()