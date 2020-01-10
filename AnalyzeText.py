#Author: Jonathan Luu, at the C^2 Lab of UC Davis (Prof. Hilbert), for 3 studies on YouTube recommender bias (Hilbert et al (2018) CMM; Hilbert et al (2019) CMM; Cho et al (2020) JBEM)
#Email: jrluu@ucdavis.edu
#This script may have errors because either the request or alchemy api cannot handle extremely long text at one time.
#Future improvements may include splitting up the text

import requests
import csv
import sys
import time

def readRow(row):
	
    title= row[1]
    description = row[3] 
    transcript = row[4]
    all_text = title + ' ' +  description + ' ' + transcript
 
    searchTerms = [title, description, transcript, all_text]

    return searchTerms


def analyzeData(searchTerms, apikey):

	#Counter is the number of search terms - 1
    counter = 4
    result=searchTerms[:]
    result.insert(counter, ".")
    counter = counter + 1


	#Get Positive/Negative Sentiment
    for term in searchTerms:
        payload = { 'text': term, 'apikey': apikey, 'outputMode': 'json'}
	try:
	    	r = requests.get('http://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment', params = payload)

		try: 
			Sentiment = r.json()['docSentiment']['type']
			
		except:
			Sentiment = "Error"

		result.insert(counter, Sentiment)
		
	except requests.exceptions.ConnectionError:
		result.insert(counter, "Connection error")
 		
	counter = counter + 1
	time.sleep(1)

    #Get Emotions
    for term in searchTerms:
        payload = { 'text': term, 'apikey': apikey, 'outputMode': 'json'}
	try:
	    	r = requests.get('http://gateway-a.watsonplatform.net/calls/text/TextGetEmotion', params = payload)

		try: 
			anger =  r.json()['docEmotions']['anger']
			disgust = r.json()['docEmotions']['disgust']
			fear = r.json()['docEmotions']['fear']
			joy = r.json()['docEmotions']['joy']
			sadness = r.json()['docEmotions']['sadness']
			
		except:
			anger = "Error"
			disgust ="Error"
			fear = "Error"
			joy = "Error"
			sadness = "Error"

		result.insert(counter, anger)
		counter = counter + 1
		result.insert(counter, disgust)
		counter = counter + 1	
		result.insert(counter, fear)
		counter = counter + 1
		result.insert(counter, joy)
		counter = counter + 1
		result.insert(counter, sadness)

	except requests.exceptions.ConnectionError:
		result.insert(counter, "Connection error")
 		counter = counter + 1
		result.insert(counter, "Connection error")
 		counter = counter + 1
		result.insert(counter, "Connection error")
 		counter = counter + 1
		result.insert(counter, "Connection error")
 		counter = counter + 1
		result.insert(counter, "Connection error")
		print "Connection Error"

	counter = counter + 1	
    return result

def writeRow(csv_w, data):

	csv_w.writerow(data)


def main():

#Note these keys will not work (used 8/1/16)
#To get your own code, please see our readme or go to IBM's bluemix website for more details.
#    apikey = "..."
#    apikey = "..."
    apikey = "..."
    row_count = 0
	
    if len(sys.argv) < 2:
        print "Usage:"
        print "    python AnalyzeUrl.py <file_name>"
        sys.exit(1)
		
    csv_f = csv.reader(open(sys.argv[1], "rU"))
    csv_w = csv.writer(open('result.csv','wb'))

    #Print column titles for results.csv
    data = ['Title','Description','Transcript','CONCATENATE','.','Title +/-','Description +/-','Transcript +/-','Concatenate +/-','Title_Anger','Title_Disgust','Title_Fear','Title_Joy','Title_Sadness','Desc_Anger','Desc_Disgust','Desc_Fear','Desc_Joy','Desc_Sadness','Trans_Anger','Trans_Disgust','Trans_Fear','Trans_Joy','Trans_Sadness','Concat_Anger','Concat_Disgust','Concat_Fear','Concat_Joy','Concat_Sadness'] 
    writeRow(csv_w, data)

    #Skip first line of input file
    next(csv_f)


    for row in csv_f:
        print "Running on row " , row_count
        row_count = row_count + 1
        search_terms = readRow(row)
        data = analyzeData(search_terms, apikey)
        writeRow(csv_w, data)

if __name__ == "__main__":
    main()
