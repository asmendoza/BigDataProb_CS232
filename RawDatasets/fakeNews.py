from twarc import Twarc
from urllib.request import urlopen

import json
import sys
import io

fileJSON = open("fileJSON.txt","w",encoding = "utf-8")
fileCSVFull = open("fileCSV_fullUrl.csv","w",encoding = "utf-8")
fileCSVShort = open("fileCSV_shortUrl.csv","w",encoding = "utf-8")

consumer_key = 'xnl5ibgxPxt9vMDuXiD80gQSP'
consumer_secret = 'bX8agc1w6MmNsOaP1ByMa1Vl1G6DU2esShTR5iF3rXhISbtooH'
access_token = '933448580253151232-jJEbQShtqPB8v5tp9JFZPQDw6mSuxxo'
access_token_secret = 'FsHOmzw4jZy56w3GxOZDUqUgTYyOA6yPagjFchSaIGIPr'


monthToNum = {'Jan' : '01','Feb' : '02','Mar' : '03','Apr' : '04','May' : '05', 'Jun' : '06', \
              'Jul' : '07','Aug' : '08','Sep' : '09','Oct' : '10','Nov' : '11', 'Dec' : '12'  }

t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

def getExpandedURL(urlList):
	intStartIndex = urlList.find("expanded_url") + 15
	intEndIndex = urlList.find(",",intStartIndex)

	expanded_url = urlList[intStartIndex:intEndIndex].replace("\'","")

	intCtr = 0
	while(len(expanded_url) > 2 and len(expanded_url) < 30):
		try:
			expanded_url = urlopen(expanded_url,timeout=1).geturl()
			print("urlopen was used")
		except:
			expanded_url = expanded_url
			break

		intCtr = intCtr + 1

		if (intCtr == 2):
			break

	return expanded_url
def getExpandedURLFromList(urlList):

	intStartIndex = urlList.find("expanded_url") + 15
	intEndIndex = urlList.find(",",intStartIndex)
	expanded_url = urlList[intStartIndex:intEndIndex].replace("\'","")

	return (expanded_url)

def isUrlNotEmpty(tweetOB):
	if("retweeted_status" in tweetOB):
		urlList = str(tweetOB["retweeted_status"]["entities"]["urls"])
		expanded_url = getExpandedURLFromList(urlList)
	else:
		urlList = str(tweetOB["entities"]["urls"])
		expanded_url = getExpandedURLFromList(urlList)
	if (len(expanded_url) < 2):
		return 0;
	else:
		return 1;
#yyyy-MM-dd HH:mm:ss
def convertDateFormat(strDate):

	strMonth = monthToNum[strDate[4:7]]
	strDay = strDate[8:10]
	strTime = strDate[11:19]
	strYear = strDate[26:30]
	return (strYear + "-" + strMonth + "-" + strDay + " " + \
			strTime)

def getMainDomainOfUrl(strURL):
	intStartIndex = strURL.find("//")
	intEndIndex = strURL.find("/",intStartIndex + 2)

	if(strURL.find("https") >= 0):
		return (strURL[intStartIndex-6:intEndIndex+1])
	else:
		return (strURL[intStartIndex-5:intEndIndex+1])

def writeCSVDATA(tweetOB):
	if ( isUrlNotEmpty(tweetOB)):
		userID = str(tweetOB["user"]["id"])
		userScreenName = tweetOB["user"]["screen_name"]
		userFollowersCount = tweetOB["user"]["followers_count"]
		userFriendsCount = tweetOB["user"]["friends_count"]
		userFavoritesCount = tweetOB["user"]["favourites_count"]
		tweetID = str(tweetOB["id"])
		dateCreated = convertDateFormat(tweetOB["created_at"])
		fullText = "\"" + tweetOB["full_text"].replace("\"","\'") + "\""
		userLocation = tweetOB["user"]["location"].replace(","," ").replace("  "," ")

		if ( "retweeted_status" in tweetOB):
			expanded_url = getExpandedURL(str(tweetOB["retweeted_status"]["entities"]["urls"]))
			isRetweet = "YES"
			originalTweetId = str(tweetOB["retweeted_status"]["id"])
		else:
			expanded_url = getExpandedURL(str(tweetOB["entities"]["urls"]))
			isRetweet = "NO"
			originalTweetId = ""

		mainURL = getMainDomainOfUrl(expanded_url)
		retweetCount = tweetOB["retweet_count"]
		favoriteCount = tweetOB["favorite_count"]


		if (len(expanded_url) >= 30):
			

			fileCSVFull.write(userID + "," + userScreenName + "," + str(userFollowersCount) + "," + str(userFriendsCount) + "," + \
						  str(userFavoritesCount) + "," + tweetID + "," + dateCreated + "," + fullText + "," + \
						  userLocation + "," + expanded_url + "," + mainURL + "," + str(retweetCount) + "," + \
						  str(favoriteCount) + "," + isRetweet + "," + originalTweetId + "\n")
			return 1,0;
		else:
			fileCSVShort.write(userID + "," + userScreenName + "," + str(userFollowersCount) + "," + str(userFriendsCount) + "," + \
						  str(userFavoritesCount) + "," + tweetID + "," + dateCreated + "," + fullText + "," + \
						  userLocation + "," + expanded_url + "," + mainURL + "," + str(retweetCount) + "," + \
						  str(favoriteCount) + "," + isRetweet + "," + originalTweetId + "\n")
			return 0,1;
	else:
		return 0,0;


def mainProgram():

	intIndex = 0
	intTotalProcessedFullUrl = 0
	intTotalProcessedShortUrl = 0
	fileCSVFull.write("userId,userScreenName,userFollowersCount,userFriendsCount,userFavoritesCount,tweetId,dateCreated," + \
		           "fullText,userLocation,expandedURL,mainURL,retweetCount,favoriteCount,isRetweet,originalTweetID\n")
	fileCSVShort.write("userId,userScreenName,userFollowersCount,userFriendsCount,userFavoritesCount,tweetId,dateCreated," + \
		           "fullText,userLocation,expandedURL,mainURL,retweetCount,favoriteCount,isRetweet,originalTweetID\n")
	strQuery = "Philippines filter:links"
	for tweet in t.search(strQuery):
		print ("Tweet# : " + str(intIndex))

		tweetString = str(tweet)
		tweetString = tweetString.replace("\'","\"")
		#fileJSON.write(tweetString + " \n\n" )

		isFullUrl,isShortUrl = writeCSVDATA(tweet)
		intTotalProcessedFullUrl += isFullUrl
		intTotalProcessedShortUrl += isShortUrl

		print ("Total data with full URL processed: " + str(intTotalProcessedFullUrl))
		print ("Total data with short URL processed: " + str(intTotalProcessedShortUrl))

		if (intIndex == 10000000):
			break
		
		intIndex = intIndex + 1
    
	print ("END OF PROCESSING! \n" + "Processed " + str(intTotalProcessedFullUrl + intTotalProcessedShortUrl) + " out of " + str(intIndex))
	return;

################################################################
################################################################
mainProgram()
