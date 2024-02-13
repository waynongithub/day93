from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import random

nc = "\033[0;97m"
red = "\033[0;91m"
green = "\033[0;92m"
blue = "\033[0;96m"
yellow = "\033[0;93m"
lilac = "\033[0;95m"

'''
Instead of manually copying video title, date and url from telegram, this script scrapes the data from the 
coinburo website.
First scrapes the video url, title and date from the list of videos and outputs to a textfile.

Second reads the urls from said text file and scrapes the video descriptions.
'''

def scrape_page(nr):
    url = f"https://www.coinbureau.com/videos/?page={nr}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # get the div that contains the cards. each card is an 'a'-tag without classes or id
    cards = soup.find(class_="Video_cardDiv__AiH6_")

    videolist = []
    for card in cards.find_all('a', recursive=False):
        print(f"{card}\n")

        # the link to the video on the CB site
        videolink = card.get('href')

        # each card has 2 or 3 <img> tags. Need to find the one that has the video title in the alt-attribute,
        # and the ID of the youtube video in the src-attribute
        imgs = card.find_all('img')
        title = ""
        youtube_id = ""

        for img in imgs:
            # get video title from a non-empty alt
            alt = img.get('alt')
            if alt != "":
                title = alt

            # select the src that contains ".jpg" because it has the ID of the youtube video
            src = img.get('src')
            regex = "\.jpg"
            match = re.search(regex, src)

            if match:
                regex = "(.*\.com%2F)(.*)(\.jpg.*)"
                match = re.search(regex, src)
                youtube_id = match.group(2)

        fullvideolink = f"https://www.coinbureau.com/videos/{videolink}"
        youtubelink = f"https://www.youtube.com/watch?v={youtube_id}"

        # get the div that contains the publication date in "Dec 27, 2023" format
        date = card.find(class_="Video_publishedDate__NIS8s")
        date_str = date.text
        # change date format
        datetime_object = datetime.strptime(date_str, '%b %d, %Y')
        date = datetime_object.strftime('%Y-%m-%d')
        # print(f"fullvideolink={videolink}")
        print(f"title={title}")
        # print(f"youtube_id={youtube_id}")
        # print(f"youtubelink={youtubelink}")
        # print(f"date={date}")
        videolist.append([fullvideolink, title, youtubelink, date])
    return videolist


def get_all_videos(first_page, last_page):
    all_videos = []
    for page_nr in range(first_page, last_page + 1):
        new_quotes = scrape_page(page_nr)
        all_videos += new_quotes
        time.sleep(random.choice(range(5, 15)))

    with open("/media/datax/downloads/coinburovideos.txt", "w") as f:
        for video in reversed(all_videos):
            f.write(f"{video[3]}  {video[1]}\n{video[2]}\n{video[0]}\n\n")



# get_all_videos(1,2)

def get_descriptions():
    out = ""
    now = datetime.now().strftime("%H%M")
    outputfile = f"/media/datax/coding/python/100_days_of_python/day098_custom-automation/videosout-{now}.txt"

    with open('/media/datax/coding/python/100_days_of_python/day098_custom-automation/videos.txt') as f:
        for line in f:
            print(line.strip())
            out += line
            if line.find("https://www.coinbureau.com") > -1:
                out += "\n"
                # remove the newline character
                url = line.strip()
                # print(f"url={yellow}{url}{nc}")
                response = requests.get(url)
                # print(f"response={response}")
                soup = BeautifulSoup(response.text, 'html.parser')
                desc = soup.find(class_="titleAndDescription_descriptionDiv__szynY")
                if desc is None:
                    print(f"{yellow}desc is None, this should not happen{nc}")
                    return
                # find the paragraph tags in the description block
                pees = desc.find_all("p")
                for pee in pees:
                    if pee.text.find("Disclaimer") > -1:
                        break
                    if pee.text.find("~~~") > -1:
                        continue
                    if pee.text.find("📝 Overview 📝") > -1:
                        continue
                    if pee.text.find("🚨 New Video Alert!! 🚨") > -1:
                        continue
                    if pee.text.find("Helpful Links") > -1:
                        continue
                    if pee.text.find("Useful Links") > -1:
                        continue
                    if pee.text.find("https://") > -1:
                        continue
                    # print(f"{green}{pee.text}{nc}")
                    out += f"{pee.text}\n"
                out += f"\n\n------------------------------------------------------------"
                with open(outputfile, mode="a") as outfile:
                    outfile.write(out)
                out = ""
                time.sleep(random.choice(range(5, 10)))
                # time.sleep(random.choice(range(1, 5)))


get_descriptions()


def get_desc():
    out = ""
    url = "/media/datax/coding/python/100_days_of_python/day098_custom-automation/Fetch.ai Review_ Should you Consider FET_ - Coin Bureau.html"
    # print(f"url={blue}{url}{nc}")
    # print('dummy')

    with open(url) as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')
    # get the div that contains the cards. each card is an 'a'-tag without classes or id
    desc = soup.find(class_="titleAndDescription_descriptionDiv__szynY")
    pees = desc.find_all("p")

    for pee in pees:
        if pee.text.find("~~~") > -1:
            continue
        if pee.text.find("Disclaimer") > -1:
            break
        if pee.text.find("Helpful Links") > -1:
            continue
        if pee.text.find("https://") > -1:
            continue
        print(f"{green}{pee.text}{nc}")
        out += f"{pee.text}\n\n"
    out += f"------------------------------------------------------------\n\n"
    # print(desc)
    with open('/media/datax/coding/python/100_days_of_python/day098_custom-automation/videosout.txt', mode="w") as f:
        f.write(out)

# get_desc()


