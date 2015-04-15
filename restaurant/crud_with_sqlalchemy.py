
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

##### CREATE ######
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()


cheesepizza = menuItem(name="Cheese Pizza", 
					   description = "Made with all natural ingredients and fresh mozzarella", 
					   course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()

### READ ####
firstResult = sesson.query(Restaurant).first()
firstResult.name

items = session.query(MenuItem).all()
for item in items:
    print item.name


### UPDATE #####
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
	print veggieBurger.id, veggieBurger.price, veggieBurger.restaurant.name

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()
# # print UrbanVeggieBurger.price
# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
	if veggieBurger.price != '2.99':
		veggieBurger.price = '2.99'
		session.add(veggieBurger)
		session.commit()

##### DELETE #######
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
session.delete(spinach)
session.commit()