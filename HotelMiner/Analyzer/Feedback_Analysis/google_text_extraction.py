import json
from pprint import pprint
from operator import itemgetter
import re
import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


# open the reviews file for the hotel and read reviews in ascending order of date.




def mainfunc(mylist):
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('language', 'v1', credentials=credentials)

	templist = []
	service_request = service.documents().analyzeSyntax(
	  body={
	    'document': {
	      'type': 'PLAIN_TEXT',
	      'content': mylist,
	    }
	  }
	)
	response = service_request.execute()
	# pprint(response)
	return response

def worker2():
	# with open('reviews.json') as data_file:
	# 	data = json.load(data_file)
	# 	data_file.close()
	# data = sorted(data, key=itemgetter('_id'))
    #
	# res = []
	# l = len(data)
	# print l
	# i = 1
	# # for review in data:
	# # for review,x in zip(data,range(10)):
	# with open("extracted_text.txt", "w") as file:
	# 	for w in range(l):
	# 		review = data[w]
	# 		reviewBody = review['reviewBody']
	# 		print reviewBody
	# 		temp = mainfunc(reviewBody)
	# 		a = dict()
	# 		a["_id"] = review["_id"]
	# 		a["tokens"] = []
	# 		for word in temp["tokens"]:
	# 			temp2 = dict()
	# 			temp2["headTokenIndex"] = word["dependencyEdge"]["headTokenIndex"]
	# 			temp2["tag"] = word["partOfSpeech"]["tag"]
	# 			temp2["content"] = word["text"]["content"]
	# 			a["tokens"].append(temp2)
    #
	# 		json.dump(a, file)
	# 		file.write('\n')
	# 		print "counter ", i
	# 		i = i + 1

	with open('reviews.txt') as data_file:
		data = data_file.read()
	with open("extracted_text.txt", "w") as file:

		temp = mainfunc(data)
		a = dict()
		# a["_id"] = review["_id"]
		a["tokens"] = []
		for word in temp["tokens"]:
			temp2 = dict()
			temp2["headTokenIndex"] = word["dependencyEdge"]["headTokenIndex"]
			temp2["tag"] = word["partOfSpeech"]["tag"]
			temp2["content"] = word["text"]["content"]
			a["tokens"].append(temp2)

		json.dump(a, file)
		file.write('\n')



	


