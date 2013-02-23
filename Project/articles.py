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
import config
from google.appengine.api import users


def escape_html(s):
		return cgi.escape(s, quote = True)
		
class PostPage(webapp2.RequestHandler):
    def write_form(self, error="", title="", url=""):
        template=config.templates.get_template(config.article_post_page)
        self.response.out.write(template.render(
                                            { 
                                                "user": users.get_current_user(),
                                                "error": error,
                                                "title": title,
                                                "url": url
                                            }))

    def get(self):
        # We should check to see if the user is logged in here 
        # instead of after our POST.
        if users.get_current_user():
		    self.write_form()
        else:
		    self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user() 
        user_link_url = self.request.get('link_url')
        user_link_title = self.request.get('link_title')
        user_name = user.nickname()
        datastore.post_article(user_link_url,user_link_title,user_name)
        self.redirect("/")
