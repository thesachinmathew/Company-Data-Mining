import requests
from bs4 import BeautifulSoup

url = "https://www.zaubacorp.com/search"

ck = "ZCSESSID=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiIiwiYW5vbnltb3VzX3V1aWQiOiJkNDhiNGZmZS1jMTc0LTRiOWItOWM3Yi1iYTczYjkzOWZiNzciLCJleHAiOjE3NDAzMjM1ODV9.VfFqES9DzJOBW8bqtlIZ03rFWtdYwyakXyncC5v8arE; _ga=GA1.1.1771896780.1739718785; cf_clearance=mO8NcJsa.kVSvWcHcmfLO_LZsn.oHejvXyVvEIHJ3rs-1740413838-1.2.1.1-aDstrdEizVZJPHE.lhL0fY5_XtjNQp1h1yAC6pCseNpnR4yQF7Rl3_1rDberfS4E.SJWhfjc7Q.r.0GLlh6TSHlJWEgybvgUHee1T3P5st78qQk_M3Ty53Npzr9LvvoekugPqtJS3U04XqB1FLzzRnM9H_5l53YBtE7Bo2YGAKfCcfAj2ui1tG0vBsk5uqIYInHmk6qrEoKPPjsf35oDJyIZVk.GBtHKbE2SoNrJaXKMxDnsXry3o0_9d6LJpZhi.H_2gk0GL9yXHXSuFoMXKD66Xz0_25SlnbdEuFOBocgGNGFGCArjg56o3CQJ_w.VM7fDy9uYLG_FAV8YKzM5cA; _ga_VVR3BV80B8=GS1.1.1740413838.23.0.1740413838.60.0.0"

data = {
    "cd": "company",
    "searchvalue": "fafafa"
}
f = open("names.txt", "r", encoding='cp1252')

company_names = f.readlines()

unique_links = set()
from datetime import datetime
for company in company_names:
    company = company.replace("\n","")
    print(f"On Postfix : {company}")
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
    data = {"cd": "company", "searchvalue": company}
    response = requests.post(url, headers=headers, data=data, verify=False)

    
    soup = BeautifulSoup(response.text, "html.parser")
    if "records" not in soup.prettify():
        current_datetime = datetime.now()
        datetime_int = int(current_datetime.strftime("%Y%m%d%H%M%S"))
        with open(f"links{datetime_int}.txt", "w") as lf:
            for link in unique_links:
                lf.write(link + "\n")
        ic = input("New cookie : ")
        if ic != "":
            ck = ic
    for link in soup.select("#results tbody tr td a"):     
        href = link.get("href")
        if href and "zaubacorp.com" in href:
            unique_links.add(href)
  

with open("links.txt", "a") as lf:
    for link in unique_links:
        lf.write(link + "\n")

f.close()  
