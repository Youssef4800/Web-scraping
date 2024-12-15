import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

jop_name = input("Please enter a jop name to search: ")
result = requests.get(f'https://wuzzuf.net/search/jobs/?q={jop_name}&a=hpb')

jop_info = []

def get_jop_details(jop):
    
    jop_title = jop.find('a', {'class' : 'css-o171kl'}).text.strip()
    company_name = jop.find('a', {'class' : 'css-17s97q8'}).text.strip()
    company_name = company_name.rstrip(company_name[-1]) # to remove '-' at the end of the text  
    company_loc = jop.find('span', {'class' : 'css-5wys0k'}).text.strip()
    all_skills = jop.find_all('a', {'class' : 'css-5x9pm1'})
    skills = ''
    for skill in all_skills:
        skills += skill.text.strip()
    
    parent = jop.find('div', {'class' : 'css-y4udm8'})
    exp = parent.contents[1].find('span').text.strip()

    jop_info.append({'jop_title' : jop_title,
                     'company_name' : company_name,
                     'company_location' : company_loc,
                     'skills' : skills,
                     'years_of_exp' : exp})



def main():
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    jops = soup.find_all('div', {'class' : 'css-1gatmva e1v1l3u10'})
    for i in range(len(jops)):
        get_jop_details(jops[i])


    labels = jop_info[0].keys()

    with open(f'wuzzuf/{jop_name}.csv','w') as file:
        dict_writer = csv.DictWriter(file, labels)
        dict_writer.writeheader()
        dict_writer.writerows(jop_info)
        print("DONE")


main()


