from django.http import HttpResponse
from django.shortcuts import render
from Analyzer.Feedback_Analysis.feedback_analysis import worker
from textblob import TextBlob
import matplotlib.pyplot as plt
from pprint import pprint
import json
from pylab import *

plt.style.use('ggplot')



# Create your views here.

def index(request):

    if request.method == 'POST':
        hotel_url =  request.POST.get("hotelurl","")
        results = worker(hotel_url)


        final = dict()
        data_for_graph = dict()

        for key,value in results.iteritems():
            temp=dict()
            temp["good"]=[]
            temp["bad"]=[]
            graph_Y = 0
            for val in value:
                x = TextBlob(val)
                pl =  x.sentiment.polarity
                if pl<0:
                    temp["bad"].append(val)
                else:
                    temp["good"].append(val)
                graph_Y = graph_Y + pl

            final[key]=temp
            data_for_graph[key] = graph_Y

        # pprint(results)
        # # results = []
        # with open('temp.json', 'w') as f:
        #     json.dump(results, f, indent=4)
        #     f.close()

        # with open('temp.json', 'r') as f:
        #     results = json.load(f)
        #     f.close()

        sorted_data_for_graph = sorted(data_for_graph.items(), key=lambda x:x[1], reverse = True)

        y = []
        x = [7,6,5,4, 3, 2, 1, 0]

        y_1 = []

        label = []
        label_1 = []

        for item in sorted_data_for_graph[:8]:
            y.append(item[1])
            label.append(item[0])

        for item in sorted_data_for_graph[-8:]:
            y_1.append(item[1])
            label_1.append(item[0])

        plt.figure()
        plt.barh(x, y)
        plt.yticks(x,label)
        # plt.show()
        # plt.figure()
        plt.savefig('./static/graph.png')

        # print "Label 1 "+str(label_1[0])
        plt.figure()
        plt.barh(x, y_1)
        plt.yticks(x, label_1)
        # plt.show()
        # plt.figure()
        plt.savefig('./static/graph_1.png')


        context = {'res':final}
        return render(request, 'HotelMiner/results.html', context)



    return render(request, 'HotelMiner/index.html', {})



