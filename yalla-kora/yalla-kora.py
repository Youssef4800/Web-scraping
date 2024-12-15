import requests
from bs4 import BeautifulSoup
import csv
import lxml
import os

date = input("Please enter a Date in: YYYY-MM-DD: ")

page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#")

matches_details = []


def get_match_info(championships):
    
    championship_title = championships.contents[1].find('h2').text.strip()
    all_matches = championships.contents[3].find_all("div", {'class' : 'item finish liItem'})
    
    for match in all_matches:
        # get teams names
        team_A = match.find("div", {'class' : 'teamA'}).text.strip()
        team_B = match.find("div", {'class' : 'teamB'}).text.strip()

        # get score
        match_result = match.find("div", {'class' : 'MResult'}).find_all("span", {'class' : 'score'})
        score = f'{match_result[0].text.strip()} - {match_result[1].text.strip()}'

        # get time
        match_time = match.find("div", {'class' : 'MResult'}).find("span", {'class' : 'time'}).text.strip()
        
        # save matches info
        matches_details.append({'championship_title' : championship_title,
                                'team-A' : team_A,
                                'team-b' : team_B,
                                'score' : score,
                                'time' : match_time,
                                'date' : date})


def main(page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")

    championships = soup.find_all("div", {'class' : 'matchCard'})

    for i in range(len(championships)):
        get_match_info(championships[i])
    
    keys = matches_details[0].keys()

    file_name = 'matches.csv'
    file_exists = os.path.exists(file_name)

    
    with open('matches.csv','a') as output:
        dict_writer = csv.DictWriter(output, keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("DONE")

main(page)                                                                                                        