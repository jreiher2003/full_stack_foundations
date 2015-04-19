from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		"""
		Handles all /url requests our webserver recieves to our local
		host port 8080/restaurants
		"""
		try:
			if self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""	
				output += "<html><body><h3>"
				output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>" + "</br></br>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					# print restaurant.name
					output += restaurant.name + "</br>"  
					output += "<a href='/restaurants/{0}/edit' style='color: #FFE284;'>Edit</a>".format(restaurant.id) + "</br>"  
					output += "<a href='/restaurants/{0}/delete' style='color: #9EFFEB;'>Delete</a>".format(restaurant.id)	
					output += "</br></br></br>"
				
				output += "</h3></body></html>"
				self.wfile.write(output)
				# print output
				return
				
			if self.path.endswith('/restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>\
						   <input type='text' name='newrestaurant' placeholder='new restaurant name'/>\
						   <input type='submit' value='Create'/> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				if self.path.endswith('/restaurants/{0}/edit'.format(restaurant.id)):
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/edit'".format(restaurant.id) +">"
					output += "<label>Bakery Bonanza</label>"
					output += "<input type='text' name='rename' placeholder='Rename Restaurant' />"
					output += "<input type='submit' value='Rename' />"
					output += "</form>"
					output += "</body></html>"
					self.wfile.write(output)
					return

				if self.path.endswith('/restaurants/{0}/delete'.format(restaurant.id)):
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete "
					output += "<span style='color: blue'>" + restaurant.name  + "</span></h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/delete'".format(restaurant.id) +">"
					output += "<input type='submit' name='delete_rest' value='DELETE' style='color: red'>"
					output += "</form>"
					output += "</body></html>"
					self.wfile.write(output)
					return



		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		""" 
		Finds form and parses out the value from the name of the input
		Then puts that value into the DB and makes a redirect back to /restaurants
		"""
		try:
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				# print ctype, pdict
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile,pdict)
					# print fields
				messagecontent = fields.get('newrestaurant')
				# print "this is messagecontent"
				# print messagecontent
				# Create new Restaurant object
				NewRestaurant = Restaurant(name=messagecontent[0])
				session.add(NewRestaurant)
				session.commit()

				# create a 301 redirect back to /restauarnts
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

			# edit post update
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				if self.path.endswith('/restaurants/{0}/edit'.format(restaurant.id)):
					ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile,pdict)

					messageupdate = fields.get('rename')

					updateName = session.query(Restaurant).filter_by(id = restaurant.id).one()
					updateName.name = messageupdate[0]
					session.add(updateName)
					session.commit()

					# create 301 redirect back to /restauants
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

					return

				# delete restaurant from db
				if self.path.endswith('/restaurants/{0}/delete'.format(restaurant.id)):
					ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)

					delete_rest = session.query(Restaurant).filter_by(id = restaurant.id).one()
					session.delete(delete_rest)
					session.commit()

					# create 301 redirect back to /restaunts after post
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

		except:
			pass





def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()