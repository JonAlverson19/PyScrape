import tweepy
import json
import requests
import argparse
from math import floor
import time
import os


def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='handle', default="becc_aloha",
						help='Set twitter handle to scrape')
						
	parser.add_argument('-i', action='store_true', default=False,
						dest='save_image',
						help='Save the user profile image')
						
	parser.add_argument('-s', action='store_true', default=False,
						dest='save_data',
						help='Save the user profile information to {HANDLE}.json')
						
	parse_results = parser.parse_args()

#--------------------AUTHENTICATE--------------------
def authenticate():
	with open("twitter_credentials.json","r") as f:
		keys = json.load(f)

	auth = tweepy.OAuthHandler(keys["CONSUMER_KEY"],keys["CONSUMER_SECRET"])
	auth.set_access_token(keys["ACCESS_TOKEN"],keys["ACCESS_SECRET"])

	api = tweepy.API(auth)
	return api

#--------------------SCRAPE ACCOUNT--------------------
def scrape(api, Handle, Save_Image, Save_Data):
	if not os.path.exists("RateLimiter.txt"):
		#print("RateLimiter.txt does not exist. Creating it.")
		with open("RateLimiter.txt",'w') as f:
			f.write("")
			#print(str(time.time()))
	#exit()
	with open("RateLimiter.txt",'r+') as f:
		t = f.readline()
		now = time.time()
		#print(str(t))
		#print(float(t))
		if not t == "":
			if float(now) < (float(t) + 900):
				data = "Rate has been limited and requests will be ignored. \n"
				data += "Try again in " + str(floor((float(t)+900)-float(now))) + " seconds"
				return data
			else:
				f.write(str(time.time()))

	try:
		user = api.get_user(Handle)
		data = {}
		
		data["Name"] = user.name
		#print("Account Name: " + user.name)
		data["created_on"] = str(user.created_at)
		#print("Account created on: " + str(user.created_at))

		
		#fix weird url finding
		data["default_profile_image"] = user.default_profile_image
		imagetype = user.profile_image_url.split("normal")[1]
		url = user.profile_image_url.split("normal")[0] + "400x400" + imagetype
		response = requests.get(url)
		if response.status_code != 200:
			print("Error in loading larger profile image.")
			print("Continuing with normal image path.")
			
			response = requests.get(user.profile_image_url)
			if response.status_code != 200:
				print("Error in loading profile image.")
				print("Skipping profile image processing.")
				data["profile_image_url"] = ""
			else:
				data["profile_image_url"] = user.profile_image_url
		else:
			data["profile_image_url"] = url
				
		# try:
			# #print(user.profile_banner_url)
			# data["banner_url"] = user.profile_banner_url
		# except:
			# pass
			
		# if "banner_url" in data.keys():
			# response = requests.get(user.profile_banner_url)
			
			# if response.status_code != 200:
				# print("Error in loading profile banner image.")
				# print("Skipping profile banner image processing.")
			
			
			
			
		if Save_Image:
			if user.default_profile_image:
				print("Account uses default profile image so it will not be saved locally.")
			else:
				print("Profile image url: " + user.profile_image_url)
				


		if user.geo_enabled:
			data["location"] = user.location
			#print("Account location: " + user.location)
			
			
		data["followers_count"] = user.followers_count
		#print("Followers: " + str(user.followers_count))

		data["followers"] = []
		for page in tweepy.Cursor(api.followers, screen_name=user.screen_name, include_user_entities=False, skip_status=True, count=200).pages(1):
			for follower in page:
				data["followers"].append(follower.screen_name)
		
		
		data["following_count"] = user.friends_count
		#print("Following: " + str(user.friends_count))
		
		data["following"] = []
		for page in tweepy.Cursor(api.friends, screen_name=user.screen_name, include_user_entities=False, skip_status=True, count=200).pages(1):
			for followee in page:
				data["following"].append(followee.screen_name)
		
		
		data["statuses_count"] = user.statuses_count
		#print("Statuses: " + str(user.statuses_count))

		#for all statuses, use: spages = floor(user.statuses_count/20) + 1
		#pages start at 0
		spages = 0 
		iter = 0
		data["statuses"] = []
		while iter <= spages:
			statuses = api.user_timeline(screen_name=user.screen_name, count=200)
			for status in statuses:
				data["statuses"].append(status.id)
			iter += 1
		#print(len(data["statuses"]))
		#access status by id through: twitter.com/{HANDLE}/status/{STATUS_ID}
			
		if Save_Data:
			jsonfile = "{}.json"
			with open(jsonfile.format(user.screen_name,user.screen_name),'w') as f:
				json.dump(data,f)
		#else:
			#print(json.dumps(data))
			
	except tweepy.RateLimitError:
		print("Rate Limit Reached.")
		with open("RateLimiter.txt",'w') as f:
			f.write(str(time.time()))
	return data

#--------------------Testing--------------------
def get_input():
	s = input("User's name: ")
	print("Hello " + s)
	return s