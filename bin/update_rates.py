"""
1. Scrape web page
2. Take the number of works
3. Open CSV
4. Make yesterday's rate equal today's
5. Make today's rate equal value from 2.
"""

import urllib.request
import json
import re

pattern = "20 of (.*) Works in"
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

def get_rate(fics_yesterday, fics_today, yesterdays_rate, AVERAGE_NEW_FICS):
    todays_new_fics = fics_today - fics_yesterday
    relative_new_works = todays_new_fics / AVERAGE_NEW_FICS
    return(yesterdays_rate * relative_new_works) 


def main():
    url = "https://archiveofourown.org/tags/M*s*M/works"
    req = urllib.request.Request(url,headers=headers)
    resp = urllib.request.urlopen(req)
    file_content = resp.read().decode('utf-8')
    yaoi_fic_count = re.search(pattern, file_content).group(1)

    url = "https://archiveofourown.org/tags/F*s*F/works"
    req = urllib.request.Request(url,headers=headers)
    resp = urllib.request.urlopen(req)
    file_content = resp.read().decode('utf-8')
    yuri_fic_count = re.search(pattern, file_content).group(1)

    with open("./data/daily_rates.json", "r") as file:
        data = json.load(file)
        today_rate = data["yaoi_today"]
        tomorrow_rate = int(yaoi_fic_count.replace(',',''))
        data["yaoi_yesterday"] = today_rate
        data["yaoi_today"] = tomorrow_rate
        data["yaoi_rate"] = get_rate(today_rate, tomorrow_rate, data["yaoi_rate"], 2500)

        today_rate = data["yuri_today"]
        tomorrow_rate = int(yuri_fic_count.replace(',',''))
        data["yuri_yesterday"] = today_rate
        data["yuri_today"] = tomorrow_rate
        data["yuri_rate"] = get_rate(today_rate, tomorrow_rate, data["yuri_rate"],600)

        new_data = json.dumps(data)

    with open("./data/daily_rates.json", "w") as file:
        file.write(new_data)

if __name__ == "__main__":
    main()