from bs4 import BeautifulSoup
import requests
import time

filepath = "transcript.txt"


def scrape_episode(url, filepath):
    """
    Scrapes episode transcript, and appends text to file
    
    url: Url of episode to scrape
    filepath: File to write to
    """
    
    response = requests.get(url)
    if response.status_code == 429:
        print(f"Rate limited, waiting 15s...")
        time.sleep(15)
        response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", class_="headerscontent")

    table = tables[1]
    rows = table.find_all("tr")

    title = rows[0].get_text(strip=True)
    print(title)

    rows = rows[2:len(rows)-1]

    with open(filepath, "a") as file:
        file.write("[START OF EPISODE: " + title + "]\n\n")

    for row in rows:

        tds = row.find_all("td")

        character = tds[0].get_text(strip=True)
        dialogue = tds[1].get_text(strip=True)

        with open(filepath, "a") as file:
            if character == "":
                file.write(dialogue + "\n" + "\n")
            else:
                file.write(character + ": " + dialogue + "\n" + "\n")

            # file.write("This text will be added to the end.\n")

    with open(filepath, "a") as file:
        file.write("[END OF EPISODE: " + title + "]\n\n")


with open(filepath, "w") as f:
    pass

main_url = "https://southpark.wiki.gg/wiki/Portal:Scripts"
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

seasons = soup.find_all(class_="gallery mw-gallery-traditional")[0]
seasons = seasons.find_all("li")

for season in seasons:
    link = season.find("a")['href']
    
    time.sleep(5)
    new_page = requests.get("https://southpark.wiki.gg/" + link)
    new_soup = BeautifulSoup(new_page.text, 'html.parser')

    episodes = new_soup.find_all(class_="gallery mw-gallery-traditional")[0]
    episodes = episodes.find_all("li")

    for episode in episodes:
        link = episode.find("a")['href']
        time.sleep(5)
        scrape_episode("https://southpark.wiki.gg/" + link, filepath)