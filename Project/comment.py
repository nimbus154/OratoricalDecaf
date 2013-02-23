import cgi
import datetime
import urllib
import webapp2
import datastore

from google.appengine.ext import db
from google.appengine.api import users

class RequestHandler(webapp2.RequestHandler):
  def get(self, article_id):
        self.response.out.write('<html><body>')

        #article_key = self.request.get('article_key')

	my_article = datastore.Articles().get_by_id(ids = int(article_id))
	article_name = my_article.text

	#user login check
	user = users.get_current_user()
	if not user:
		self.redirect(users.create_login_url(self.request.uri))

	#article name
	self.response.out.write('Article Name: <b>%s</b>' % article_name)
	self.response.out.write('<br><a href="/">Back</a>')

	#comment query
	comment_list = datastore.Comments().all().filter("article_id =",int(article_id))

	#comment submission form
	self.response.out.write("""
		<form method="post">
		<div><textarea name="comment_text" rows="3" cols="60"></textarea></div>
		<div><input type="submit" value="Post"></div>
		</form>""")


	for comments in comment_list:
		#sub-note - comments will always have an author
		self.response.out.write('<b>%s</b> wrote:' % comments.comment_owner)
		self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(comments.comment_text))

        self.response.out.write("""</body></html>"""  )

  def post(self, article_id):

	comment_text = self.request.get('comment_text')
	datastore.Post_Comment(int(article_id),users.get_current_user().email(),cgi.escape(comment_text))

        self.redirect('/comment/%s'% (article_id))