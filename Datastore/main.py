import webapp2
import datastore

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
	datastore.Create_User('thisguy@lol.com','butts')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
