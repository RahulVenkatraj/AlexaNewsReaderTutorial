#!/usr/bin/python
# -*- coding: utf-8 -*-

#Borrows framework and components from Amazon's tutorail: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/alexa-skill-tutorial

import logging
import feedparser
from operator import itemgetter
import time

import speech_config

response_pack = speech_config.StandardResponses()
card_pack = speech_config.CardContents()
variables_pack = speech_config.RequiredVariables()

def build_speechlet_response(title, output, reprompt_text, should_end_session):
	'''
	More details on this here: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
	TO DO: Ensure outputSpeech does not exceed 8000 characters (check and take out complete sentences?)
	'''
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'card': {
			'type': 'Simple',
			'title': card_pack.COMPANY_NAME + title,
			'content': card_pack.COMPANY_NAME + output
		},
		'reprompt': {
			'outputSpeech': {
				'type': 'PlainText',
				'text': reprompt_text
			}
		},
		'shouldEndSession': should_end_session
	}


def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}

def parse_rss_feed(RSS_path):
	'''
	Uses RSS feedparser library (https://pypi.python.org/pypi/feedparser)
	Make sure you install this install library inside the same folder before you upload to S3
	"pip install feedparser -t ." 
	'''
	logging.info('%s >>-->> parsing RSS feed'%(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))))
	return feedparser.parse(RSS_path)

def get_daily_news_articles(allSports = variables_pack.ALL_SPORTS):
	'''
	Content-building function: Constructs the text content of a daily digest
	'''
	newsPiece = response_pack.NEWS_DIGEST_STARTER
	for eachGame in allSports:
		RSS_path = variables_pack.RSS_BASIC_PATH + eachGame
		logging.info('%s >>-->> Seeking RSS feed at %s'%(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())),RSS_path))
		content = parse_rss_feed(RSS_path)
		sortedEntries = sorted(content['entries'], key=itemgetter('published_parsed'), reverse=True)
		sortedEntriesShort = sortedEntries[0:variables_pack.NUM_PER_SPORT_IN_DIGEST]
		for eachEntry in sortedEntriesShort:
			try:
				newsPiece += "In " + str(eachGame) + ", " + str(eachEntry['title']) + ". "
			except Exception as e:
				logging.warning('%s >>-->> Error creating digest speech piece %s'%(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())),str(e)))
	return newsPiece
			

def get_specific_sport_articles(favorite_sport):
	'''
	Content-building function: Constructs the text content of specific sports news
	'''
	newsPiece = response_pack.SPECIFIC_SPORT_STARTER + favorite_sport + ". "
	RSS_path = 'https://sportscafe.in/rss/articles/' + favorite_sport
	logging.info('%s >>-->> Seeking RSS feed at %s'%(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())),RSS_path))
	content = feedparser.parse(RSS_path)
	sortedEntries = sorted(content['entries'], key=itemgetter('published_parsed'), reverse=True)
	sortedEntries = sortedEntries[0:variables_pack.NUM_ARTICLES_PER_SPORT]
	for eachEntry in sortedEntries:
		try:
			newsPiece += str(eachEntry['title']) + ". "
		except Exception as e:
			logging.warning('%s >>-->> Error creating sports news speech piece %s'%(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())),str(e)))
	return newsPiece
			

def get_welcome_response():
	'''
	Welcome greeting and Card contents (what appears on the mobile application) are defined here
	'''
	session_attributes = {}
	card_title = card_pack.WELCOME_CARD_TITLE
	speech_output = response_pack.WELCOME_MESSAGE
	reprompt_text = response_pack.WELCOME_REPROMPT
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
	'''
	End closure and Card contents (what appears on the mobile application) are defined here
	'''
	card_title = card_pack.END_CARD_TITLE
	speech_output = response_pack.END_SESSION_MESSAGE
	# Setting this to true ends the session and exits the skill.
	should_end_session = True
	return build_response({}, build_speechlet_response(
		card_title, speech_output, None, should_end_session))


def create_favorite_sport_attributes(favorite_sport):
	'''
	Helper function
	'''
	return {"favoriteSport": favorite_sport}


def get_daily_news_response(intent, session):
	'''
	Prepares, by calling the required content-building function, the speech response for Daily Digest
	'''
	card_title = intent['name']
	session_attributes = {}
	should_end_session = False

	try:
		speech_output = get_daily_news_articles()
		reprompt_text = response_pack.AFTER_NEWS_REPROMPT
	except:
		speech_output = response_pack.NEWS_DIDNOTGET_RESPONSE
		reprompt_text = response_pack.NEWS_DIDNOTGET_REPROMPT
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def get_news_by_sport(intent, session):
	'''
	Prepares, by calling the required content-building function, the speech response for Daily Digest
	'''

	card_title = intent['name']
	session_attributes = {}
	should_end_session = False

	if 'SportName' in intent['slots']:
		favorite_sport = intent['slots']['SportName']['value']
		session_attributes = create_favorite_sport_attributes(favorite_sport)
		speech_output = get_specific_sport_articles(favorite_sport)
		reprompt_text = response_pack.AFTER_NEWS_REPROMPT
	else:
		speech_output = response_pack.NEWS_DIDNOTGET_RESPONSE
		reprompt_text = response_pack.NEWS_DIDNOTGET_REPROMPT
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


# >>> --- >>> The following provide a basic framework that will help you build any Alexa skill
# >>> --- >>> The contents are nearly fully from: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/alexa-skill-tutorial

def on_session_started(session_started_request, session):
	'''
	Called when the session starts
	'''

	print("on_session_started requestId=" + session_started_request['requestId']
		  + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
	'''
	Called when the user launches the skill without specifying what they want
	'''

	print("on_launch requestId=" + launch_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# Dispatch to your skill's launch
	return get_welcome_response()


def on_intent(intent_request, session):
	'''
	Called when the user specifies an intent for this skill 
	'''

	print("on_intent requestId=" + intent_request['requestId'] +
		  ", sessionId=" + session['sessionId'])

	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']

	# Dispatch to your skill's intent handlers
	if intent_name == "GetNewsBySport":
		return get_news_by_sport(intent, session)
	elif intent_name == "GetDailyNewsDigest":
		return get_daily_news_response(intent, session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
	'''
	Called when the user ends the session. Is not called when the skill returns should_end_session=true
	'''
	print("on_session_ended requestId=" + session_ended_request['requestId'] +
		  ", sessionId=" + session['sessionId'])


def lambda_handler(event, context):
	'''
	 Route the incoming request based on type (LaunchRequest, IntentRequest, etc.) The JSON body of the request is provided in the event parameter.
	'''
	print("event.session.application.applicationId=" +
		  event['session']['application']['applicationId'])

	"""
	Uncomment this if statement and populate with your skill's application ID to
	prevent someone else from configuring a skill that sends requests to this
	function.
	"""
	# if (event['session']['application']['applicationId'] !=
	#         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
	#     raise ValueError("Invalid Application ID")

	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']},
						   event['session'])

	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])

