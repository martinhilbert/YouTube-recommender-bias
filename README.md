# YouTube-recommender-bias
Versions of this code has been used in 3 complementary studies about the social effects of YouTube's recommender engine 
Two scripts are included, which have been used in three publications at the Computational Communication Research Lab (C^2) at UC Davis under Prof. Hilbert (http://c2.ucdavis.edu/). 
The code was used to collect data to study the behavior and social effects of the YouTube recommender engine. 
1.	Hilbert M, Ahmed S, Cho J, Liu B, Luu J. Communicating with Algorithms: A Transfer Entropy Analysis of Emotions-based Escapes from Online Echo Chambers. Communication Methods and Measures. 2018;12(4):260-275. doi:10.1080/19312458.2018.1479843
2.	Hilbert M, Liu B, Luu J, Fishbein J. Behavioral Experiments With Social Algorithms: An Information Theoretic Approach to Input–Output Conversions. Communication Methods and Measures. 2019;0(0):1-20. doi:10.1080/19312458.2019.1620712
3.	Cho J, Ahmed S, Hilbert M, Liu B, Luu J "Do Search Algorithms Endanger Democracy? An Experimental Investigation of Algorithm Effects on Political Polarization", Journal of Broadcasting & Electronic Media.

The code led by Billy Liu (yt_fillhistory) automates the process to bias a YouTube search history. 
It searches for given search terms in YouTube, then watches the video for a few seconds (moving it into the watch history), collects the transcript of the video, repeats this with a determined number of videos, and then collects the information from the YouTube recommended page.
It then evaluates the resulting emotions through a sentiment analysis online service, which was called https://alchemy-language-demo.mybluemix.net through a web-browsing automation. It was later converted into https://natural-language-understanding-demo.ng.bluemix.net/ (https://www.ibm.com/watson/services/alchemy-language-migration/).

The code led by Jonathan Luu (AnalyzeText) focuses on collecting sentiments from the (back then incipient versions) of the IBM Watson API for natural language understanding.
back in 2016 still under ‘Alchemy’, (https://en.wikipedia.org/wiki/AlchemyAPI).
