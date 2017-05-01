from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime


def get_scores():
	url = 'http://www.cbssports.com/nba/scoreboard/'
	text = requests.get(url).text
	soup = BeautifulSoup(text, 'html.parser')
	scores = []
	games = soup.find_all(class_='live-update')
	scores = []
	for game in games:
	    time_data = game.find(class_='game-status').text
	    m = re.match(r'(\d)[\w]{2} (\d+:\d+)', time_data)
	    if m:
	        quarter = int(m.group(1))
	        time = m.group(2) # time left in quarter
	        live = True
	    else: # Game is already over
	        live = False
	        quarter = 4
	        time = 0 # Have to reset these variables somehow
	    team_data = game.select('a.team')
	    away, home = [el.text for el in team_data]
	    scoreboard = game.find_all('td')
	    away_score = int(scoreboard[5].text) 
	    home_score = int(scoreboard[11].text)
	    score = {'away' : away,
	            'home' : home, 
	            'away_score' : away_score, 
	            'home_score' : home_score, 
	            'live' : live   
	            }
	    if live:
	        score['quarter'] = quarter
	        score['time'] = time
	    scores.append(score)

return scores

def get_streams(url):
	text = requests.get(url).text
	soup = BeautifulSoup(text, 'html.parser')
	modComment = soup.find('div', {'data-author':'StreamsBotMod'})
	rows = modComment.find('table').find_all('tr')[1:]
	return [row.find_all('a')[1] for row in rows] # return links
    
def get_threads(home, away):
	url = 'https://www.reddit.com/r/nbastreams/'
	text = requests.get(url).text
	soup = BeautifulSoup(text, 'html.parser')
	threads = soup.select('a.title')
	for thread in threads:
	    regex = away + ' @ ' + home
	    if re.search(regex, thread.text):
        	return get_streams(thread['href'])

def get_times(date): # Maybe we can pass in a date?
	formatted_date = date.strftime('%m%d')
	url = 'http://www.cbssports.com/nba/schedules/day/{}/post'.format(today)

	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, 'html.parser')
	schedules = soup.find_all(class_='data')
	fulldate = date.strftime('%A, %B %-d, %Y')
	times = []
	for schedule in schedules:
	    curr_date = schedule.find(class_='title').find('td').text.strip()
	    if date == fulldate:
	        # Extract schedule
	        rows = schedule.find_all('tr', class_=lambda x: x != 'title' and x != 'label')
	        for row in rows:
	            el = row.find(class_='gmtTime')
	            gmt_time = int(el['data-gmt'])
	            start_time = datetime.fromtimestamp(gmt_time)
	            times.append(start_time)
    			print(start_time)
    return times

def main():
	scores = get_scores()
	for score in scores:
		get_threads(score['home'], score['away'])




