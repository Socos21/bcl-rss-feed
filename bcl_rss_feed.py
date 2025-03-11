import requests
from bs4 import BeautifulSoup
import feedgenerator

# URL of the BCL schedule page (Replace with actual URL)
BCL_SCHEDULE_URL = "https://www.championsleague.basketball/2024/schedule"

# Fetch schedule data
def get_bcl_schedule():
    response = requests.get(BCL_SCHEDULE_URL)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []
    
    # Example: Assuming the website has 'game-date' and 'game-title' classes
    for game in soup.find_all("div", class_="game-listing"):
        date = game.find("span", class_="game-date").text.strip()
        teams = game.find("span", class_="game-title").text.strip()
        games.append({"date": date, "teams": teams})
    
    return games

# Generate RSS feed
def create_rss_feed():
    feed = feedgenerator.Rss201rev2Feed(
        title="BCL Schedule RSS Feed",
        link=BCL_SCHEDULE_URL,
        description="Latest Basketball Champions League Games",
        language="en"
    )
    
    for game in get_bcl_schedule():
        feed.add_item(
            title=f"{game['teams']} - {game['date']}",
            link=BCL_SCHEDULE_URL,
            description=f"Matchup: {game['teams']} on {game['date']}"
        )
    
    return feed.writeString('utf-8')

# Save RSS to a file
with open("bcl_schedule.xml", "w", encoding="utf-8") as f:
    f.write(create_rss_feed())

print("RSS feed generated: bcl_schedule.xml")
