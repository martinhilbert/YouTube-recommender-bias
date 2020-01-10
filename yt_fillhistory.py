#Author: Billy Liu at the C^2 Lab of UC Davis (Prof. Hilbert), for 3 studies on YouTube recommender bias (Hilbert et al (2018) CMM; Hilbert et al (2019) CMM; Cho et al (2020) JBEM)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
from datetime import datetime
import csv
import sys
import os

#globals

emailandpass = []
searchterms = []

result_num = 1

all_csvs = os.listdir('/Users/billyliu/desktop/cmn198')
driver = webdriver.Chrome('/usr/bin/chromedriver') # To be used for just recommend video page.
second_driver = webdriver.Chrome('/usr/bin/chromedriver') # To be used to open up windows.
third_driver = webdriver.Chrome('/usr/bin/chromedriver') # To be used for alchemy.

# Writes the header in the csv..
def csv_header():
    iofile = open('/Users/billyliu/desktop/yt.csv','a')
    fields = ('N', 'Title', 'Hyperlink', 'Description', 'Transcript', 'CONCATENATE', '.', \
    'Title +/-', 'Description +/-', 'Transcript +/-', 'Concatenate +/-', \
    'Title_Anger', 'Title_Disgust', 'Title_Fear', 'Title_Joy', 'Title_Sadness', \
    'Desc_Anger', 'Desc_Disgust', 'Desc_Fear', 'Desc_Joy', 'Desc_Sadness', \
    'Trans_Anger', 'Trans_Disgust', 'Trans_Fear', 'Trans_Joy', 'Trans_Sadness', \
    'Concat_Anger', 'Concat_Disgust', 'Concat_Fear', 'Concat_Joy', 'Concat_Sadness')
    fob = csv.DictWriter(iofile, fields, lineterminator = '\n')
    fob.writeheader()

# Function to call to write a row in a csv.
def csv_write(N, title, href, description, transcript, concatenate, dot, \
 titlepnn, descriptionpnn, transcriptpnn, concatenatepnn, \
 Title_Anger, Title_Disgust, Title_Fear, Title_Joy, Title_Sadness, \
 Desc_Anger, Desc_Disgust, Desc_Fear, Desc_Joy, Desc_Sadness, \
 Trans_Anger, Trans_Disgust, Trans_Fear, Trans_Joy, Trans_Sadness, \
 Concat_Anger, Concat_Disgust, Concat_Fear, Concat_Joy, Concat_Sadness):
    iofile = open('/Users/billyliu/desktop/yt.csv','a')
    fields = ('N', 'Title', 'Hyperlink', 'Description', 'Transcript', 'CONCATENATE', '.', \
    'Title +/-', 'Description +/-', 'Transcript +/-', 'Concatenate +/-', \
    'Title_Anger', 'Title_Disgust', 'Title_Fear', 'Title_Joy', 'Title_Sadness', \
    'Desc_Anger', 'Desc_Disgust', 'Desc_Fear', 'Desc_Joy', 'Desc_Sadness', \
    'Trans_Anger', 'Trans_Disgust', 'Trans_Fear', 'Trans_Joy', 'Trans_Sadness', \
    'Concat_Anger', 'Concat_Disgust', 'Concat_Fear', 'Concat_Joy', 'Concat_Sadness')

    fob = csv.DictWriter(iofile, fields, lineterminator = '\n')

    fob.writerow({'N':N, 'Title':title, 'Hyperlink':href, 'Description':description, 'Transcript':transcript, 'CONCATENATE':concatenate, '.':dot, \
    	'Title +/-':titlepnn, 'Description +/-':descriptionpnn, 'Transcript +/-':transcriptpnn, 'Concatenate +/-':concatenatepnn, \
    	'Title_Anger':Title_Anger, 'Title_Disgust':Title_Disgust, 'Title_Fear':Title_Fear, 'Title_Joy':Title_Joy, 'Title_Sadness':Title_Sadness, \
    	'Desc_Anger':Desc_Anger, 'Desc_Disgust':Desc_Disgust, 'Desc_Fear':Desc_Fear, 'Desc_Joy':Desc_Joy, 'Desc_Sadness':Desc_Sadness, \
    	'Trans_Anger':Trans_Anger, 'Trans_Disgust':Trans_Disgust, 'Trans_Fear':Trans_Fear, 'Trans_Joy':Trans_Joy, 'Trans_Sadness':Trans_Sadness, \
    	'Concat_Anger':Concat_Anger, 'Concat_Disgust':Concat_Anger, 'Concat_Fear':Concat_Fear, 'Concat_Joy':Concat_Joy, 'Concat_Sadness':Concat_Sadness})

# Open browser for youtube and one for alchemy.
def open_browser():
    driver.get('http://www.youtube.com')
    third_driver.get('https://alchemy-language-demo.mybluemix.net/')

# Function used to stall the program. Useful when the script is going to fast and the requests are being made.
def stall(seconds):
    time.sleep(seconds)

# Scrapes the description from the videos.
def description_scraper(youtube_url):
    second_driver.get(youtube_url)

    description = second_driver.find_element_by_xpath('//*[@id="eow-description"]')

    return ((description.text).encode('ascii', 'ignore').decode('ascii'))

# Logs into youtube automatically. 
def login():

    # Open Chrome to YouTube.com and then log in.

    #email = str(raw_input("What is the email? "))
    #password = str(raw_input("What is your password? "))
    
    email = 'cmn...'
    password = '...'

    youtube_login_button = driver.find_element_by_xpath('//*[@id="yt-masthead-signin"]/div/button/span').click()
    stall(.25)
    youtube_email = driver.find_element_by_xpath('//*[@id="Email"]').send_keys(email)
    youtube_next_button = driver.find_element_by_xpath('//*[@id="next"]').click()
    stall(.25)
    youtube_password = driver.find_element_by_xpath('//*[@id="Passwd"]').send_keys(password)
    signinbutton = driver.find_element_by_xpath('//*[@id="signIn"]').click()

    # You are now signed in.


# Searches the selected term.    
def youtube_search():
    search_box = driver.find_element_by_xpath('//*[@id="masthead-search-term"]').send_keys('negative')
    magnifying_glass_button = driver.find_element_by_xpath('//*[@id="search-btn"]').click()
    stall(1)

    # Click and watch one video
    top_10_videos = driver.find_elements_by_css_selector('a.yt-uix-sessionlink.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.spf-link')

# Checks to see if there's a transcript. Returns the transcript as a string, if not, returns NA.
def is_transcript():

	# Try and except catches if there's a transcript or not.
    try:
        stall(.5)
        dots_button = second_driver.find_element_by_xpath('//*[@id="action-panel-overflow-button"]')
        dots_button.click()
        stall(.5)
        transcript_button = second_driver.find_element_by_css_selector('#action-panel-overflow-menu > li:nth-child(2) > button')
        transcript_button.click()
        stall(.75)

        # The transcript are split by time on each line. Fix the broken transcript by concatenating them.
        broken_transcripts = second_driver.find_elements_by_css_selector('div.caption-line-text')

        # Checks to see if the broken transcript is not zero because sometimes it returns zero for some reason.
        trans_len = len(broken_transcripts)
        if trans_len != 0:
                tmp_list = []
                for i in range(trans_len):
                        tmp_list.append((broken_transcripts[i].text).encode('ascii', 'ignore').decode('ascii'))
                        tmp_list.append(' ')
                list_b = ''.join(tmp_list)
        return list_b
    # No transcript found.
    except:
        return 'NA'

# Scrapes the youtube.com/feed/recommended page. Gets the first 100 and writes all the info to a csv.
def recommended_scraper():
    driver.get('https://www.youtube.com/feed/recommended')

    # Load More Videos Button
    load_more_button = driver.find_element_by_xpath('//*[@id="browse-items-primary"]/button/span').click()
    stall(1)

    recommended_videos = driver.find_elements_by_css_selector('a.yt-uix-sessionlink.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.spf-link')

    # Run through all the 100 videos and collect their sentiment and emotions.
    for i in range(100):

    	# Grabs the title, hyperlink, description
        title = recommended_videos[i].get_attribute('title').encode('ascii', 'ignore').decode('ascii')
        href = recommended_videos[i].get_attribute('href').encode('ascii', 'ignore').decode('ascii')
        description = description_scraper(recommended_videos[i].get_attribute('href'))

        # Check the sentiment and emotion for the title.
        title_sentiment = positive_negative_neutral(str(title))
        title_emotions = emotions(str(title))

        # Check the sentiment and emotion for the description.
        description_sentiment = positive_negative_neutral(str(description))
        description_emotions = emotions(str(description))

        # Check the sentiment and emotion for the transcript.
        # Check if there's a transcript
        transcript = str(is_transcript())
        if transcript == 'NA':
        	# There's no transcript to be found.
        	transcript_sentiment = '-'
        	transcript_emotions = '-'
        	concatenate = str(title) + ' ' + str(description)
        else:
        	# There is a transcript
        	transcript_sentiment = positive_negative_neutral(transcript)
        	transcript_emotions = emotions(transcript)
        	concatenate = str(title) + ' ' + str(description) + ' ' + str(transcript)

        # Check the sentiment and emotion for the concatenated.
        concatenate_sentiment = positive_negative_neutral(str(concatenate))
        concatenate_emotions = emotions(str(concatenate))

        # If there's no transcript, there's no emotions, so mark that row empty for transcript emotions.
        if transcript == 'NA':
			csv_write(i, title, href, description, transcript, concatenate, '.', \
        	title_sentiment, description_sentiment, transcript_sentiment, concatenate_sentiment, \
        	title_emotions[1], title_emotions[3], title_emotions[5], title_emotions[7], title_emotions[9], \
        	description_emotions[1], description_emotions[3], description_emotions[5], description_emotions[7], description_emotions[9], \
        	'-', '-', '-', '-', '-', \
        	concatenate_emotions[1], concatenate_emotions[3], concatenate_emotions[5], concatenate_emotions[7], concatenate_emotions[9])
		# There is a transcript, so write the whole row.
        else:
        	csv_write(i, title, href, description, transcript, concatenate, '.', \
        	title_sentiment, description_sentiment, transcript_sentiment, concatenate_sentiment, \
        	title_emotions[1], title_emotions[3], title_emotions[5], title_emotions[7], title_emotions[9], \
        	description_emotions[1], description_emotions[3], description_emotions[5], description_emotions[7], description_emotions[9], \
        	transcript_emotions[1], transcript_emotions[3], transcript_emotions[5], transcript_emotions[7], transcript_emotions[9], \
        	concatenate_emotions[1], concatenate_emotions[3], concatenate_emotions[5], concatenate_emotions[7], concatenate_emotions[9])


# Returns either the word: positive, neutral, or negative.
def positive_negative_neutral(paragraph):

    reset_button = third_driver.find_element_by_xpath('/html/body/div[2]/article/div[2]/div/span/button')
    reset_button.click()

    text_box = third_driver.find_element_by_xpath('//*[@id="panel1"]/textarea')
    text_box.clear()
    text_box.send_keys(str(paragraph))

    stall(4)

    analyze_button = third_driver.find_element_by_xpath('//*[@id="submitbutton"]')
    analyze_button.click()

    time.sleep(1.5)

    document_sentiment = third_driver.find_element_by_xpath('//*[@id="t7"]')
    document_sentiment.click()

    time.sleep(1.25)

    sentiment_table = third_driver.find_elements_by_css_selector('tbody.base--tbody.sentiment-table')
    senti_list = str(sentiment_table[0].text)

    stop_index = 0
    for i in range(len(senti_list)):
        if str(senti_list[i]) == " ":
            stop_index = i
            break

    plus_neg_neu = [senti_list[0:stop_index],senti_list[stop_index+1:]]
    return plus_neg_neu[0]

# Takes in any string and returns emotions and their values in a list.
def emotions(paragraph):

    # Finds the document emotion table. This is what we want. We now need to parse out the data.
    document_emotion = third_driver.find_element_by_xpath('//*[@id="t6"]')
    document_emotion.click()

    time.sleep(1.25)
    
    # Variables

    Anger = []
    Disgust = []
    Fear = []
    Joy = []
    Sadness = []

    # Variable declarations to be used to parse out document emotion string.

    tmp1 = 'null'
    tmp2 = 'null'
    tmp3 = 'null'
    tmp4 = 'null'
    tmp5 = 'null'
    tmp6 = 'null'
    tmp7 = 'null'
    tmp8 = 'null'
    tmp9 = 'null'
    tmp10 = 'null'
    
    emotion_table = third_driver.find_elements_by_css_selector('tbody.base--tbody.emotion-table')
    emo_list = str(emotion_table[0].text)

    stop_index = 0
    # Gets the word Anger.
    for i in range(len(emo_list)):
        if emo_list[i] == " ":
            stop_index = i
            Anger.append(emo_list[:stop_index])
            tmp1 = emo_list[stop_index+1:]
            break
    
    # Gets number associated with Anger.
    for i in range(len(tmp1)):
        if tmp1[i] == "\n":
            stop_index = i
            Anger.append(tmp1[0:stop_index])
            tmp2 = tmp1[stop_index+1:]
            break

    # Gets the word Disgust.
    for i in range(len(tmp2)):
        if tmp2[i] == " ":
            stop_index = i
            Disgust.append(tmp2[0:stop_index])
            tmp3 = tmp2[stop_index+1:]
            break
    # Gets number associated with Digust.
    for i in range(len(tmp3)):
        if tmp3[i] == "\n":
            stop_index = i
            Disgust.append(tmp3[0:stop_index])
            tmp4 = tmp3[stop_index+1:]
            break

    # Gets the word Fear.
    for i in range(len(tmp4)):
        if tmp4[i] == " ":
            stop_index = i
            Fear.append(tmp4[0:stop_index])
            tmp5 = tmp4[stop_index+1:]
            break

    # Gets number associated with Fear.
    for i in range(len(tmp5)):
        if tmp5[i] == "\n":
            stop_index = i
            Fear.append(tmp5[0:stop_index])
            tmp6 = tmp5[stop_index+1:]
            break
                            
    # Gets the word Joy.
    for i in range(len(tmp6)):
        if tmp6[i] == " ":
            stop_index = i
            Joy.append(tmp6[0:stop_index])
            tmp7 = tmp6[stop_index+1:]
            break

    # Gets number associated with Joy.
    for i in range(len(tmp7)):
        if tmp7[i] == "\n":
            stop_index = i
            Joy.append(tmp7[0:stop_index])
            tmp8 = tmp7[stop_index+1:]
            break

        # Gets the word Sadness.

    # Gets number associated with Sadness.
    for i in range(len(tmp8)):
        if tmp8[i] == " ":
            stop_index = i
            Sadness.append(tmp8[0:stop_index])
            tmp9 = tmp8[stop_index+1:]
            break
    Sadness.append(tmp9[0:])

    # If emo_list is empty, that means an error happened and the alchemy couldn't process it.
    if len(emo_list) == 0:
        tmp = ['Anger', '-', 'Disgust', '-', 'Fear', '-', 'Joy', '-', 'Sadness', '-']
        return tmp
    else:
    	tmp = ['Anger', Anger[1], 'Disgust', Disgust[1], 'Fear', Fear[1], 'Joy', Joy[1], 'Sadness', Sadness[1]]
        return tmp

if __name__ == '__main__':
    
    open_browser()
    login()
    youtube_search()
    csv_header()
    recommended_scraper()

    driver.close()
    second_driver.close()
    third_driver.close()


