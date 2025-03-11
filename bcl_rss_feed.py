import requests
from bs4 import BeautifulSoup

URL = "https://www.championsleague.basketball/en/games" # Replace with actual schedule URL

def fetch_schedule():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    
    # You must adjust selectors based on BCL website structure.
    for game_row in soup.select(".game-row-selector"):  # <-- Adjust the selector
        round_num = game_row.select_one(".round-selector").text.strip()
        date = game_row.select_one(".date-selector").text.strip()
        home = game_row.select_one(".home-team-selector").text.strip()
        away = game_row.select_one(".away-team-selector").text.strip()
        time = game_row.select_one(".time-selector").text.strip()
        
        games.append((round_num, date, home, away, time))
    
    return games

def generate_html(games):
    html = '''
<style>
body {font-family: Arial; background-color: #111; color: #ddd; padding: 5px;}
table {width: 100%; border-collapse: collapse; font-size: 12px;}
th, td {padding: 4px 2px; text-align: center;}
th {background-color: #1a1a1a; color: #bbb;}
tr:nth-child(even) {background-color: #181818;}
tr:nth-child(odd) {background-color: #131313;}
.date-row {font-weight: bold; color: #aaa;}
</style>
<table>
<tr><th>ROUND</th><th>DATE</th><th>HOME</th><th>AWAY</th><th>TIME</th></tr>
'''

    last_date = ""
    last_round = ""
    for round_num, date, home, away, time in games:
        if date != last_date or round_num != last_round:
            html += f'<tr class="date-row"><td>{round_num}</td><td>{date}</td><td></td><td></td><td></td></tr>'
            last_date, last_round = date, round_num
        
        html += f'<tr><td></td><td></td><td>{home}</td><td>{away}</td><td>{time}</td></tr>'
    
    html += '</table>'
    return html

if __name__ == "__main__":
    games = fetch_schedule()
    widget_html = generate_html(games)
    with open("schedule_widget.html", "w", encoding="utf-8") as f:
        f.write(widget_html)

    print("Schedule widget updated.")
