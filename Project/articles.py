'''
	Author: Robert Cabral
	File Name: Post_Module.py
	Purpose: To create an Article Post into the database that has the Article Title and Article URL properties
		       associated with the Article Post.
	Date:	2/16/2013
'''
import datastore
import webapp2
import cgi
from google.appengine.api import users

form = """
<html>
	<body>
		<form method="post">
			<div><h1>Post Page</h1></div>
			<div>Title:</div>
			<div><textarea name="link_title" rows="2" cols="60"></textarea></div>
			<div>Location/URL:<br></div>
			<div><textarea name="link_url" rows="2" cols="60"></textarea></div>
			<div><input type="submit" value="Post"></div>
		</form>
	</body>
</html>
"""

def escape_html(s):
		return cgi.escape(s, quote = True)
		
class PostPage(webapp2.RequestHandler):
	def write_form(self, error="", title="", url=""):
		self.response.out.write(form %{"error": error,
                                       "link_title": escape_html(title),
                                       "link_url": escape_html(url)})
	def get(self):
		#We should check to see if the user is logged in here instead of after our POST.
		if users.get_current_user():
		    self.write_form()
		else:
		    self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user() 
		user_link_url = self.request.get('link_url')
		user_link_title = self.request.get('link_title')
		user_name = user.nickname()
		datastore.Post_Article(user_link_url,user_link_title,user_name)
		self.redirect("/")