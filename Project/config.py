# This file contains hardcoded strings and values
import jinja2
import os

# jinja2 file loading copied from 
# https://github.com/fRuiApps/cpfthw/blob/master/webapp2/views.py
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
templates = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

# Pages
article_post_page="post_article.html"
comments_page="comment_list.html"
main_page="article_list.html"

main_title="Oratorical Decaf"
