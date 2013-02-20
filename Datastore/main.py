import webapp2
import os
import datastore
import config
import vote
import articles
import jinja2

# jinja2 file loading copied from 
# https://github.com/fRuiApps/cpfthw/blob/master/webapp2/views.py
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
j_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

# mock article
class Article():
    def __init__(self, id, link, text):
        self.id=id
        self.link=link
        self.text=text

# mock db retrieval
def get_articles():
    return [Article(i, 'http://%d' % i, 'The #%d article' % i) 
            for i in range(1, 10)]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = j_env.get_template(config.main_page)
        self.response.write(
            template.render(title=config.main_title,
                            articles = get_articles()))
                            

app = webapp2.WSGIApplication([
                    ('/', MainHandler),
                    ('/vote/(.*)', vote.RequestHandler),
                    ('/article', articles.PostPage)
                ], 
                debug=True)
