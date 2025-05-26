import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
url = "https://www.zaubacorp.com/search"
import warnings
warnings.filterwarnings("ignore")

cookies = open("cookies.txt","r")
ck = str(cookies.read()).strip()
f = open("links.txt", "r", encoding='utf8')
links = f.readlines()
try:
    with open("data/data.json", "r", encoding="utf-8") as json_file:
        details = json.load(json_file) 
        if not isinstance(details, list): 
            details = []
except (FileNotFoundError, json.JSONDecodeError):
    details = []

cf = open("count.txt","r")
count = int(cf.read())
cf.close()
for link in links[count:]:
    count+=1
    link = link.replace("\n","")
    print(f"{count} On link : {link}")
    headers = {
        "Host": "www.zaubacorp.com",
        "Cookie": ck,
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.zaubacorp.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.zaubacorp.com/",
    }
    company_data = {}
    
    response = requests.post(link, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    if "CIN" not in soup.prettify():
        current_datetime = datetime.now()
        print(f"-------------------------------Program Termnated on link {count} ---------------time{current_datetime}")
        break
        # datetime_int = int(current_datetime.strftime("%Y%m%d%H%M%S"))
        # with open(f"data/data{datetime_int}.txt", "w") as lf:
        #     for det in details:
        #         json.dump(det, lf, indent=4, ensure_ascii=False)
        # ic = input("New cookie : ")
        # if ic != "":
        #     ck = ic
    rows = soup.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) == 2:
            key = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            company_data[key] = value
    directors = []
    director_table = soup.find("div", id=lambda x: x and "director-information" in x.lower())
    if director_table:
        director_rows = director_table.find_all("tr")[1:]  # Skip header row
        for d_row in director_rows:
            d_columns = d_row.find_all("td")
            if len(d_columns) == 4:
                director = {
                    "DIN": d_columns[0].get_text(strip=True),
                    "Name": d_columns[1].get_text(strip=True),
                    "Designation": d_columns[2].get_text(strip=True),
                    "Appointment Date": d_columns[3].get_text(strip=True)
                }
                directors.append(director)
    company_data["Directors"] = directors
    
    tables = soup.find_all("div", class_="table-responsive tbl")
    for table_div in tables:
        caption = table_div.find("caption")
        if caption:
            key = caption.get_text(strip=True)
            directors = []
            table = table_div.find("table")
            if table:
                rows = table.find_all("tr")[1:]  # Skip header row
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) >= 4:
                        director = {
                            "DIN": columns[0].get_text(strip=True),
                            "Name": columns[1].get_text(strip=True),
                            "Designation": columns[2].get_text(strip=True),
                            "Appointment Date": columns[3].get_text(strip=True)
                        }
                        if len(columns) > 4:
                            director["Cessation"] = columns[4].get_text(strip=True)
                        directors.append(director)
            company_data[key] = directors


    details.append(company_data)

  

with open("data/data.json", "w", encoding='utf8') as lf:
    json.dump(details, lf, indent=4, ensure_ascii=False)
cf = open("count.txt","w")
cf.write(str(count))
f.close()
cf.close()
