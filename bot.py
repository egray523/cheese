# ============================================================================
# - https://github.com/egray523/cheese
# - https://twitter.com/unjourunfromage
#
# An enormous thanks to the talented Alix Chagué, who both inspired me to
# create this twitter bot, and then graciously helped in the redaction and 
# testing of this monument to one of France's finest products. Her work can 
# be found at:
# - https://github.com/alix-tz
# ============================================================================


import tweepy
import csv
import random
import requests

from secrets import *

#CREATING TWEET #####################################################################################

def generate_img(url):
	""" Turn url of image into image that can be loaded into twitter"""
	#url = todayscheese[1]
	r = requests.get(url = url)
	return r.content # this is a png file

def save_image_file(img):
    """save the image in a temporary file"""
    with open("temp.png", "wb") as fh:
        fh.write(img)


def build_text_for_tweet(cheesename):
	"""Create the textual  content of the future tweet"""
	message = "Aujourd'hui, le bot vous propose: \n{} \n#wikidata #cheesebot\n".format(cheesename)
	return message

def create_tweet(source):
	""" defines textual and image content for tweet"""
	message = build_text_for_tweet(todayscheese[0])
	image = generate_img(todayscheese[1])
	return image, message


# TWEETING ##########################################################################################

def tweet(message):
	"""Post a tweet"""
	from secrets import C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET

	# Twitter authentication
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
	api = tweepy.API(auth) 

	# posting
	try:
		uploaded = api.media_upload(filename = "temp.png")
	except tweepy.error.TweepError as e:
		print(e)
		uploaded = None

	try:
		api.update_status(status = message, media_ids = [uploaded.media_id])
	except tweepy.error.TweepError as e:
		print(e.message)

list_cheese = []

with open('UnJourUnFromage.csv', newline='') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		list_cheese.append(row)
todayscheese= random.choice(list_cheese)
print("Aujourd'hui, le bot vous propose", todayscheese[0], todayscheese[1])

if __name__ == "__main__":
	source = "./data/classes_of_entity.json"
	image, message = create_tweet(source)
	save_image_file(image)
	tweet(message) 