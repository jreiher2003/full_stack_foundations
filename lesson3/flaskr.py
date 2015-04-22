from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	restaurant = session.query(Restaurant).all()
	output = ''
	for i in restaurant:
		output += i.name 
		output += '</br>'
	return output

@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenuItems(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  	output = ''
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output +='</br>'
		output +='</br>'
	return output
	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)