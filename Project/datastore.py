import datetime
from google.appengine.ext import db
from google.appengine.api import users

'''
	DATASTORE CLASSES
'''
class Articles(db.Model):
	link = db.LinkProperty()
	text = db.StringProperty()
	votes = db.IntegerProperty()
	posted = db.DateTimeProperty()
	owner = db.StringProperty()

class Votes(db.Model):
	article_id = db.IntegerProperty()
	users = db.ListProperty(db.Email)


class Comments(db.Model):
	article_id = db.IntegerProperty()
	comment_owner = db.EmailProperty()
	comment_text = db.StringProperty()
	posted = db.DateTimeProperty()

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
def Post_Article(link,text,owner):
	article_info = Articles()

	#set the article data
	article_info.link = link
	article_info.text = text
	article_info.votes = 0
	article_info.posted = datetime.datetime.now()
	article_info.owner = owner
	#store it!
	article_info.put()

'''
	Function: Get Article List
	Properties:
		input:
			None
		output:
			Articles -> list
				[0] = database index id
				[1] = article link (URL)
				[2] = article text
				[3] = article vote amount
		required:
			None
'''
def Get_Articles():
	articles = []
	result = []
	for i in Articles.all().order('-posted'):
		result = [i.key().id(),i.link,i.text,i.votes]
		articles.append(result)
	return(articles)

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
def Post_Comment(article_id,commentor,comment_text):
	#note that article_id is actually an entity id which can be pulled when we load the comments
	new_comment = Comments(Articles().get_by_id(ids = article_id).key())
	
	#setup the comment data
	new_comment.article_id = article_id
	new_comment.comment_owner = commentor
	new_comment.comment_text = comment_text
	new_comment.posted = datetime.datetime.now()
	new_comment.put()

'''
	Function: Article Vote
	Properties:
		input:

		output:

		required:

'''
def Vote_Article(username,article_id,vote):
	'''
		note, vote can only be -1 or 1, 0 IS NOT acceptable
		also note this is a two prong function, we must make sure the user has not voted prior; if they have not voted than
		we must add the vote to the Articles() table and then also add an entry to the Votes() table.
	'''
	new_vote = Votes().all().filter("article_id =",int(article_id))
	#we should always have an article that matches its ID, if not than we are in serious trouble!
	article_add_vote = Articles().get_by_id(ids = int(article_id))
	email_address = db.Email(username)

	#make sure the votes for this article exist, if not create a new entry for them.
	if new_vote.get() is None:
		#WARNING: we are redefining new_vote!
		new_vote = Votes(Articles().get_by_id(ids = int(article_id)).key())
		new_vote.article_id = int(article_id)
		new_vote.users = [email_address]
		
		article_add_vote.votes = int(vote)
		#add the vote to the article first
		article_add_vote.put()
		#now add the votes entity
		new_vote.put()
		return
	else:
		#check to see if we have already voted for this article!
		already_voted = Votes.all().filter("article_id =",article_id).filter("users in",[email_address]).get()
		if already_voted is None:
			return 1
		
		new_vote = Votes().all().filter("article_id =",int(article_id)).get()
		new_vote = Votes(Articles().get_by_id(ids = int(article_id)).key()).get_by_id(ids = new_vote.key().id())
		new_vote.users.append(email_address)
		
		article_add_vote.votes = int(article_add_vote.votes) + int(vote)
				
		new_vote.put()
		article_add_vote.put()