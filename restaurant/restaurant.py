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
		"""Handles all /url requests our webserver recieves to our local
		host port 8080/restaurant
		"""
		try:
			if self.path.endswith('/restaurant'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""	
				output += "<html><body><h3>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					# print restaurant.name
					output += restaurant.name + "</br>" 	
				# output += "</br></br></br>"	
				output += "</html></h3></body>"
				self.wfile.write(output)
				print output
				return


		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
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