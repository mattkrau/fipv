# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 17:38:30 2015

@author: sbasht- Matthias Kraus
"""

from imgurpython import ImgurClient
import urllib2
import time
import RPi.GPIO as GPIO

#########################################
#HERE COMES THE PART WHERE YOU NEED TO CHANGE SOMETHING
#
#To get your client_id and client_secret you need to register
# at https://api.imgur.com/oauth2/addclient
##########################################
#
#
client_id = 'YOUR-CLIENT-ID'
client_secret = 'YOUR-CLIENT-SECRET'
username="YOUR-USERNAME"
DISPLAY_WIDTH = 24 #How many chars fit into one line of the display
#
#
#########################################


client = ImgurClient(client_id, client_secret)


#Initializing zerovalues, if IMGUR gives back a 502 as so often..
latest_post_points=0
best_post_points=0
latest_comment_points=0
best_comment_points=0
latest_galleryid="000000"
best_sub_id="000000"



def get_latest_submission_id(username):
    try:
        submissions = client.get_account_submissions(username, page=0)
        latest = submissions[0].link
        latest_galleryid = latest.split("/")[3].split(".")[0]
        if latest_galleryid == "a":
            latest_galleryid = latest.split("/")[4].split(".")[0]
        return latest_galleryid
    except:
        return latest_galleryid

def get_best_submission_id(username):
    try:
        url = "https://imgur.com/user/" + username + "/submitted/best"
        response = urllib2.urlopen(url);
        data = response.readlines()
        line = "<a href=\"/gallery/"
        for element in data:
            if  line in element:
                best_sub_id= element.split('"')[1].split("/")[2]
        return best_sub_id
    except:
        return best_sub_id
                

def get_gallery_votecount(galleryid):
    url = "http://imgur.com/gallery/"+galleryid
    response = urllib2.urlopen(url);
    data = response.readlines()
    line = "points-"+ galleryid 
    for element in data:
        if  line in element:
            revalue= element.split(">")[1].split("<")[0]
    return revalue
            
def get_reputation_status(username):
    try:    
        rep = client.get_account(username).reputation
    except:
        rep = 0
        
    if rep >= 20000:
        return ("Glorious", rep)
    elif rep >= 8000:
        return ("Renowned", rep)
    elif rep >= 4000:
        return ("Idolized", rep)
    elif rep >= 2000:
        return ("Trusted", rep)
    elif rep >= 1000:
        return ("Liked", rep)
    elif rep >= 400:
        return ("Accepted", rep)
    elif rep >= 0:
        return ("Neutral", rep)
    else :
        return ("Forever alone", rep)
        

def get_highest_rated_comment(username):
    try:
        highestid = client.get_account_comment_ids(username, sort="best", page=0)[0]  
        url = "https://imgur.com/user/" + username + "/index/best"
        response = urllib2.urlopen(url);
        data = response.readlines()
        line = "points-"+ str(highestid) 
        for element in data:
            if  line in element:
                best_comment_points= element.split(">")[1].split("<")[0]
        return best_comment_points
    except:
        return best_comment_points
    
def get_latest_comment(username):
    try:    
        highestid = client.get_account_comment_ids(username, sort="newest", page=0)[0]  
        url = "https://imgur.com/user/" + username + "/index/newest"
        response = urllib2.urlopen(url);
        data = response.readlines()
        line = "points-"+ str(highestid) 
        for element in data:
            if  line in element:
                latest_comment_points= element.split(">")[1].split("<")[0]
        return latest_comment_points
    except:
        return latest_comment_points
        
sleeptime=2            
            
##############
#PARTS OF THIS CODE ARE FROM http://schnatterente.net 
##############
def display_init():
	lcd_byte(0x33,DISPLAY_CMD)
	lcd_byte(0x32,DISPLAY_CMD)
	lcd_byte(0x28,DISPLAY_CMD)
	lcd_byte(0x0C,DISPLAY_CMD)  
	lcd_byte(0x06,DISPLAY_CMD)
	lcd_byte(0x01,DISPLAY_CMD)  

def lcd_string(message):
	message = message.ljust(DISPLAY_WIDTH," ")  
	for i in range(DISPLAY_WIDTH):
	  lcd_byte(ord(message[i]),DISPLAY_CHR)

def lcd_byte(bits, mode):
	GPIO.output(DISPLAY_RS, mode)
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x10==0x10:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x20==0x20:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x40==0x40:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x80==0x80:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)      
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x01==0x01:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x02==0x02:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x04==0x04:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x08==0x08:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)   

            
DISPLAY_RS = 7
DISPLAY_E  = 8
DISPLAY_DATA4 = 25 
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18
	
DISPLAY_LINE_1 = 0x80 	
DISPLAY_LINE_2 = 0xC0 	
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.00005
E_DELAY = 0.00005



def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DISPLAY_E, GPIO.OUT)
    GPIO.setup(DISPLAY_RS, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA6, GPIO.OUT)	
    GPIO.setup(DISPLAY_DATA7, GPIO.OUT)
    
    display_init()
    
    
    	
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string('        FIPV:')
    	
    lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
    lcd_string('FakeInternetPointViewer')
    time.sleep(sleeptime)
    while True:


		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string('Username: ' + username)
		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string('Rep: '+ str(get_reputation_status(username)[0])+ " (" + str(get_reputation_status(username)[1])+ ")")

		time.sleep(sleeptime)


		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string('Latest submission:')

		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string(get_gallery_votecount(str(get_latest_submission_id(username)))+ " points")

		time.sleep(sleeptime)
	
		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string('Best submission:')

		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string(get_gallery_votecount(str(get_best_submission_id(username)))+ " points")

		time.sleep(sleeptime)
  
		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string('Latest comment:')

		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string(str(get_latest_comment(username))+ " points")

		time.sleep(sleeptime)

		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string('Best comment:')

		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string(str(get_highest_rated_comment(username))+ " points")

		time.sleep(sleeptime)




if __name__ == '__main__':
	main()
