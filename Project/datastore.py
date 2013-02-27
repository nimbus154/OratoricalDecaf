import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

'''
	DATASTORE CLASSES
'''
class Articles(db.Model):
	link = db.LinkProperty()
	text = db.StringProperty()
	votes = db.IntegerProperty(default=0)
	posted = db.DateTimeProperty(auto_now_add=True)
	owner = db.StringProperty()

	def time_since_post(self):
		return time_since(self.posted)

class Votes(db.Model):
	voter = db.EmailProperty()

class Comments(db.Model):
	comment_owner = db.StringProperty()
	comment_text = db.StringProperty(multiline=True)
	posted = db.DateTimeProperty()

	def time_since_post(self):
		return time_since(self.posted)

def article_list_key():
    return db.Key.from_path('ArticleList', 'default_list')

'''
	DATASTORE FUNCTIONS
'''
'''
	Function: Post Article
	Properties:
		input:
			link = URL link passed from script
			text = Article title text passed from script
		output:
			None
		required:
			None
'''
def post_article(link,text,owner):
	article_info = Articles(parent=article_list_key())

	# set the article data
	article_info.link = link
	article_info.text = text
	article_info.votes = 0
	article_info.owner = owner
	# store it!
	article_info.put()

'''
	Function: Get Article List
	Properties:
		input:
			None
		output:
			list of articles, ranked according to ranking algorithm
		required:
			None
'''
def get_articles():
    # sort by date posted, then by number of votes
	return rank(Articles.all().ancestor(article_list_key()))

'''
	Function: Retrieves requested article from datastore
	Input:
		id - id of article to retrieve
	Output:
		article with requested id
	Raises:
		LookupError when no article with requested id is found
'''
def get_article(id):
    # Retrieve parent article from db, so it can be vote's ancestor
	article = Articles.get_by_id(int(id), article_list_key())

	if article is None: 
		# article not found, can't proceed
		raise LookupError("Article not found")

	return article

'''
	Function: Post Comment
	Properties:
		input:
			article_id = entity id of article from script
			commentor = comment author (username)
			comment_text = comment text body passed from script
		output:
			None
		required:
			None
'''
def post_comment(article_id,commentor,comment_text):
	# note that article_id is actually an entity id which can be pulled when we load the comments
	article = get_article(article_id)
	new_comment = Comments(article.key())
	
	#setup the comment data
	new_comment.comment_owner = commentor
	new_comment.comment_text = comment_text
	new_comment.posted = datetime.datetime.now()
	new_comment.put()

def get_comments(article_id):
	article = get_article(article_id)
	return Comments.all().ancestor(article.key()).order('-posted')

''' Function: Article Vote
	Properties:
		input:
            article_id - id of article for which to vote
            vote - 1 (up), -1 (down)
            user - user who cast vote (GAE user object)
		output:
            updated number of votes for article

'''
def vote_article(article_id, vote, user):
	if vote != 1 and vote != -1:
		raise TypeError("Vote must be 1 or -1")

    # Retrieve parent article from db, so it can be vote's ancestor
	article = get_article(article_id)

	if not has_already_voted(user, article):
		# Cast vote
		new_vote = Votes(article.key())
		new_vote.voter = user.email()

		# update vote total
		article.votes += vote
		article.put()

		# save voter info to prevent double-voting
		new_vote.put()
	return article.votes

'''
Helper Functions
'''
'''
	Function: time_since
		Calculates how many hours/minutes/days have passed since time.
	input:
		time - reference point
	output:
		formatted string "[amount of time] [unit(s)] ago" e.g. "4 days ago"
	
'''
def time_since(time):
	# Print the time since a post
	hours = hours_since(time)

	if hours < 1:
		time = hours * 60
		unit = "minute"
	elif hours < 24:
		time = hours
		unit = "hour"
	else:
		time = hours / 24
		unit = "day"
	
	if int(time) != 1:
		unit = "%ss" % unit

	return "%d %s ago" % (time, unit)
'''
	Function: hours since
	input:
		time - time of an event
	output:
		number of hours since that event
'''
def hours_since(time):
	return ((datetime.datetime.now() - time).total_seconds()) / 3600

'''
	Function: has_already_voted
	Checks if a user has already voted for an article
	Properties:
		input:
            user - user to check
            article - article to check
		output:
            true if user has already voted
'''
def has_already_voted(user, article):
	# retrieve all votes for an article
	past_votes = Votes.all().ancestor(article.key())

	return not(past_votes is None \
		or past_votes.filter("voter =", user.email()).count() == 0)

'''
	Function: Ranks articles for display
	input:
		a list of articles
	output:
		the list of articles sorted by a scoring algorithm
'''
def rank(articles):
	return sorted(articles, key=lambda article: score(article), reverse=True)

'''
	Function: calculate the overall score for an article
	input:
		an article
	output:
		the overall score for an article
'''
def score(article):
	# This ranking algorithm is almost a direct rip-off of 
	# the Hacker News algorithm as explained here:
	# http://amix.dk/blog/post/19574 
	hours_since_post = hours_since(article.posted)
	return (article.votes) / pow(hours_since_post + 2, 1.8)

