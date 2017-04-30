from bs4 import BeautifulSoup
import re
import requests


def get_scores():
	teams = ["", "Atlanta Hawks","Boston Celtics","New Orleans Pelicans","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","Brooklyn Nets","New York Knicks","Orlando Magic","Philadelphia 76ers"," Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Oklahoma City Thunder","Utah Jazz","Washington Wizards","Toronto Raptors","Memphis Grizzlies","Charlotte Hornets"]
	f = open('espn.html')
	text = f.read()
	# url = 'www.espn.com/nba/scores'
	# r = requests,get(url)
	# text = r.text
	soup = BeautifulSoup(text, 'html.parser')
	scores = []
	for scoreboard in soup.find_all('article', class_=['live']): # If I put basketball and scoreboard as classes, bs4 doesn't pick up on live. Displays finshed games
	    datetime = scoreboard.find(class_='date-time').text
	    m = re.match(r'(\d+:\d+) - (\d)', datetime)
	    time = m.group(1) # time left in quarter
	    quarter = int(m.group(2))
	    away = teams[int(scoreboard['data-awayid'])]
	    home = teams[int(scoreboard['data-homeid'])]
	    away_score = int(scoreboard.find(class_='away').find(class_='total').text)
	    home_score = int(scoreboard.find(class_='home').find(class_='total').text)
	   	scores.push({'away' : away, 'home' : home, 'away_score' : away_score, 'home_score' : home_score, 'time': time, 'quarter' : quarter})
	   	print(away, home, away_score, home_score, time, quarter)
	return scores

def get_streams(home, away):
	# Some code here to extract redditurl
	redditurl = 'https://www.reddit.com/r/nbastreams/comments/686srv/game_thread_los_angeles_clippers_utah_jazz_223000/?st=j244m1mm&sh=f1098fb4'
	r = requests.get(redditurl).text
	soup = BeautifulSoup(r, 'html.parser')
	modComment = soup.find('div', {'data-author':'StreamsBotMod'})
	rows = modComment.find('table').find_all('tr')[1:]
	links = [row.find_all('a')[1] for row in rows]
    