from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

app.secret_key = 'some_secret'

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def oneItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return jsonify(MenuItem=[i.serialize for i in items][menu_id])

@app.route('/')
@app.route('/restaurant/')
def HelloWorld():
	restaurant = session.query(Restaurant).all()
	# output = ''
	# for i in restaurant:
	# 	output += i.name 
	# 	output += '</br>'
	return render_template('restaurants.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenuItems(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  	return render_template('menu.html', restaurant=restaurant, items=items)
 #  	output = ''
	# for i in items:
	# 	output += i.name
	# 	output += '</br>'
	# 	output += i.price
	# 	output += '</br>'
	# 	output += i.description
	# 	output +='</br>'
	# 	output +='</br>'
	# return output

#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'GET':
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
		
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash('You just successfully created and new menu item!')
		return redirect(url_for('restaurantMenuItems', restaurant_id=restaurant_id))
	
        

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	
	if request.method == 'GET':
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editedItem)
		
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash('You just successfully edited a menu item!')
		return redirect(url_for('restaurantMenuItems', restaurant_id=restaurant_id))
	

    

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'GET':
		return render_template('deletemenuitem.html',restaurant_id=restaurant_id, i=deleteItem)
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash('You just successfully deleted a menu item!')
		return redirect(url_for('restaurantMenuItems', restaurant_id=restaurant_id))

	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)