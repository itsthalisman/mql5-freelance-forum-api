import keyboard
import sys
import subprocess
import requests
from bs4 import BeautifulSoup
import time

#This script is meant to be run on windows, macOS and linux terminals. The core functions of this API will run just fine, however, this script will not be able to clear screen if you run it through any python interpreter

def clscr(): # This function enables this script to clear the user's terminal according to his respective operating system. It first detects the user's OS and, depending on the OS, will throw the correct command to clear the user's terminal

    os_type = sys.platform

    if os_type == 'win32' or os_type == 'cygwin':
        subprocess.call('cls', shell=True)

    elif os_type == 'linux' or os_type == 'darwin' or os_type == 'aix':
        subprocess.call('clear', shell=True)

def mql5_api():

    clscr() # Though this might seem redundant at first, the function "mql5_api()" will restart everytime a new forum post is fetched so it can load the newest forum post and print it to the terminal

    url = 'https://www.mql5.com/en/job?tab=new'

    content_list = [] # This will load and reload all of the forum posts and its attributes. It is responsible for holding info about the last forum post, info that will later be compared to the info gathered about the latest forum post by url requests. If the information about the latest post caught by the requests is the same as the information stored in this list, the script will do nothing, however, if the information between the requests and the list do not match, this script will clear everything in the terminal and then print all of the latest forum posts again.

    response = requests.get(url) # GET Requests to the URL
    soup = BeautifulSoup(response.content, "html.parser") # The following lines are an instance and functions of the BeautifulSoup module that will search and fetch, from the HTML data scraped by the GET request, relevant information about the forum posts such as dates, texts, titles, urls, and budgets from each post.
    script_date_soup = soup.find_all('time', class_='job-item__date')
    script_time_soup = soup.find_all('time', class_='job-item__date')
    script_text_soup = soup.find_all('div', class_='job-item__text')
    script_title_soup = soup.find_all('div', class_='job-item__title')
    script_link_soup = soup.find_all('div', class_='job-item__title')
    script_budget_soup = soup.find_all('span', class_='budget')

    print("Disclaimer: some links from the forum posts may not be accessible since some of them are private gigs |  Hold Q to stop running the script" + "\n" * 2)

    try:

        with open('mql5api_results.txt', 'r+', encoding='utf-8') as itch:  # Upon first executing this script, a file containing all of the relevant info from all gathered forum posts will be written to this file. Every time that this script detects a new forum post, it will restart and rewrite all of the new forum posts gathered previously along with the newest forum post found.

            itch.truncate(0)
            itch.close()

    except:

        pass

    for i in range(0, len(script_title_soup)): # This section here prints all of the info scraped and it also writes that info to the txt file

        last_title = "Title: " + script_title_soup[i].get_text(strip=True) + " | " + script_budget_soup[i].text + "\n"
        last_text = "Summary: " + script_text_soup[i].text[12:len(script_text_soup[i].text)]
        last_date = "Datetime: " + script_date_soup[i]['datetime'][0:10] + " | " + script_time_soup[i]['title'] + "\n"
        last_url = "URL: " + "https://www.mql5.com/en/job" + str(script_link_soup[i].find_all_next('a')[0]['href'])

        content_list.append(last_title)

        with open('mql5api_results.txt', 'a+', encoding='utf-8') as itch:

            itch.write(last_title + "\n" + last_date + "\n" + last_url + "\n" * 2)
            itch.close()

        print(last_title)
        print(last_text)
        print(last_date)
        print(last_url)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
		
    while keyboard.is_pressed('q') is not True: # This section analyses if the latest forum post is the same as the latest forum post stored on the list "content_list". If the latest forum post doesn't match with what is stored in "content_list", this script will end this function and restart it. I have coded this while loop to allow the user to terminate this entire script by pressing "W"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        script_title_soup = soup.find_all('div', class_='job-item__title')
        script_budget_soup = soup.find_all('span', class_='budget')
		
        for i in range(0, 1): # For loop for comparing "content_list" info to the latest request info

            last_title = "Title: " + script_title_soup[i].get_text(strip=True) + " | " + script_budget_soup[i].text + "\n"

            if last_title not in content_list:

                return 0 # Stops the function so it will be restarted leading to the new forum post to be printed in the terminal

        for i in range(0, 25): # For loop that ensures that the script won't break by pressing "W" while the "time.sleep()" method is activated and also guaranteeing that a new URL get request will be made every 5 seconds if the button "W" is not pressed by the user

            if keyboard.is_pressed('q') is not True:
                time.sleep(0.2)
			
            else:
                break
def main():

    while keyboard.is_pressed('q') is not True: # Necessary loop argument to ensure the function "mql5_api()" will not be executed again if the user presses "W" while mql5_api()'s while loop is running

        try: # Sometimes, the API might not be able to perform a get request due to lack of internet connection. Once this happens, unless managed with try/except statements, the API will keep mass requesting to the url's server which will lead to a Maximum Retries error and abruptly stop the script. This try/except statement prevents this from happening by making sure the "mql5_api()" function will load once every 3 seconds if connection issues ever get in the way of the GET requests

            mql5_api()

        except:

            print("\n" + "A connection error occurred! Restarting...")
            time.sleep(3)

if __name__ == '__main__':
    main()