#!/usr/bin/python
# -*- coding: utf-8 -*-

class StandardResponses():
	'''
	Contains speech responses. Edit these to get Alexa to say something different.
	'''
	def __init__(self):
		self.WELCOME_MESSAGE = "Sports cafe Fan Club, brings the latest sports news for Indian fans. This is an unofficial skill was developed by a Sports cafe fan. " \
					"Ask for news on your favorite sport, like cricket. " \
					"Or ask for the daily news digest. " \
					"We cover five sports. Cricket, football, badminton, tennis and hockey."
		self.WELCOME_REPROMPT = "You can ask for cricket news by saying, " \
					"get me Cricket news."
		self.END_SESSION_MESSAGE = "Goodbye. " \
					"Have a nice day! "
		self.AFTER_NEWS_REPROMPT = "Do you want news from any other sport?"
		self.NEWS_DIDNOTGET_RESPONSE = "I'm not sure what you are saying " \
						"Please try saying the name of a sport"
		self.NEWS_DIDNOTGET_REPROMPT = "Friend! I am not sure what you are trying to ask. " \
						"Please try saying cricket or hockey"
		self.NEWS_DIGEST_STARTER = "Here is today's news digest. "
		self.SPECIFIC_SPORT_STARTER = "Here is the latest on "
		   

		
		

class CardContents():
	'''
	Contains card contents. Edit these to get a different card displayed on the Alexa mobile application
	'''
	def __init__(self):
		self.WELCOME_CARD_TITLE = "Welcome"
		self.END_CARD_TITLE = "Good Bye"
		self.COMPANY_NAME = "Fans of Sportscafe"


class RequiredVariables():
	'''
	Configuration variables to define news contents
	'''
	def __init__(self):
		self.ALL_SPORTS = ['cricket', 'football', 'badminton', 'tennis', 'hockey']
		self.RSS_BASIC_PATH = 'https://sportscafe.in/rss/articles/'
		self.NUM_PER_SPORT_IN_DIGEST = 1
		self.NUM_ARTICLES_PER_SPORT = 4