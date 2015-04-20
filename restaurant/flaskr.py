from flask import Flask 
app = Flask(__name__)

# step 1 sqla db code import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def helloWorld():
	# return "Hello World"
	# restuarant = session.query(Restaurant).first()
	# items = session.query(MenuItem).filter_by(restaurant_id=restuarant.id)
	# output = ""
	# for i in items:
	# 	output += i.name 
	# 	output += '</br>'
	# return output
	restuarants = session.query(Restaurant).all()
	output = ''
	for restauant in restuarants:
		output += restauant.name +'<br>'
		output += "<a href='#'>Edit</a><br>"
		output += "<a href='#'>Delete</a><br><br>"
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)