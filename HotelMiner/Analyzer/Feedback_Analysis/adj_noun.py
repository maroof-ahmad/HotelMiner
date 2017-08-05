import json
from pprint import pprint
from operator import itemgetter
import re
import operator


def worker3():
    with open('reviews.txt') as data_file:
        data = data_file.read()

		# data_file.close()
	# data = sorted(data, key=itemgetter('_id'))

	# list to store final result
	res = []

	# open the noun keywords file and store the keywords in an array.
	with open('nouns_final_list.txt') as nounlistFile:
		nouns = nounlistFile.read().splitlines()

	data_text = []
	with open('extracted_text.txt') as file:
		for line in file:
			x= json.loads(line)
			data_text.append(x)
	# data_text = sorted(data_text, key=itemgetter('_id'))

	# print "len ", len(data_text)

	# data = sorted(data, key=itemgetter('_id'))

	no_nouns = len(nouns)

	# noun_dict = dict((i+1,noun) for i,noun in zip(range(no_nouns),nouns))
	# noun_dict = {k: [] for k in nouns}


	# for review, ta in zip(data, data_text):
    review = data
    ta = data_text[0]
    # print review
    # print ta
    # reviewBody = review['reviewBody']
    noun_dict = {k: [] for k in nouns}
    for word in ta["tokens"]:
        # print noun_dict
        # print word["text"]
        tag = word["tag"]
        # print tag
        if tag == "ADJ":
            dep_word_index = word["headTokenIndex"]
            # print dep_word_index
            dep_word = ta["tokens"][dep_word_index]
            # print dep_word
            content = dep_word["content"]
            # print content
            if content in noun_dict:
                noun_dict[content].append(word["content"])

    res.append(noun_dict)

    with open('ans.json', 'w') as f:
        json.dump(res, f, indent=4)
        f.close()
        # exit()

