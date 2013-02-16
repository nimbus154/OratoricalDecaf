import datetime
from google.appengine.ext import db
from google.appengine.api import users

'''
	DATASTORE CLASSES
'''
class Users(db.Model):
	username = db.EmailProperty()
	password = db.StringProperty()

class Articles(db.Model):
	link = db.StringProperty()
	text = db.StringProperty()
	votes = int
	posted = db.DateTimeProperty()
	owner = db.StringProperty()

class Votes(db.Model):
	user = db.EmailProperty()
	article_id = int

class Comments(db.Model):
	article_id = int
	comment_owner = db.EmailProperty()
	comment_text = db.Text()
	posted = db.DateTimeProperty()

'''
	DATASTORE FUNCTIONS
'''


'''
	Function: Create User
	Properties:
		input:
			username = email address passed in from other script
			password = password passed in from other script
		output:
			None
		required:
			None
'''
def Create_User(username,password):
	#NOTE - we should check to make sure the user doesn't already exists! NOT IMPLEMENTED YET
	user = Users()

	#set the username
	if users.get_current_user() is not None:
		user.username = users.get_current_user().email()
	else:
		user.username = username

	#set the password
	user.password = password

	#store it!
	user.put()


'''
	Function: Authenticate User
	Properties:
		input:
			username = email address passed in from other script
			password = password passed in from other script
		output:
			result:
				0 = failure
				1 = accepted
		required:
			None
'''
#def Authenticate_User(username,password):
	
	
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
	new_comment = Comments()
	
	#setup the comment data
	new_comment.article_id = article_id
	new_comment.comment_owner = commentor
	new_comment.comment_text = comment_text
	new_comment.posted = datetime.datetime.now()


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
	new_vote = Votes()
	article_add_vote = Articles()

	#check to see if we have already voted for this article!
	already_voted = False
	already_voted = Votes.all().filter("user ==",username)
	if already_voted is None:
		already_voted = True
	else:
		return 1

	new_vote.article_id = article_id

	if vote == 1:
		new_vote.vote = new_vote.vote+1
	elif vote == '-1':
		if new_vote.vote > 0:
			#make sure we actually have votes to negate
			new_vote.vote = new_vote.vote -1

	article_add_votes.get(article_id)
	if vote == 1:
		article_add_votes.votes = article_add_votes.votes +1
	elif vote == '-1':
		if article_add_votes.votes >0:
			article_add_votes.votes = article_add_votes.votes -1