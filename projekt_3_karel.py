"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Kryštof Karel
email: krystof.karel@gmail.com
"""

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import csv
import argparse
import sys
import validators

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "td" in response.text:
                return True
            else:
                print("První argument musí být platná URL.")
                sys.exit(1)
            return True
        else:
            print("První argument musí být platná URL.")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("První argument musí být platná URL.")
        sys.exit(1)

def validate_arguments(url, file):
    if not validators.url(url):
        print("První argument musí být platná URL.")
        sys.exit(1)
    if not file.endswith('.csv'):
        print("Druhý argument musí být název souboru s příponou .csv.")
        sys.exit(1)

def get_response(url):
    return requests.get(url)

def extract_links(response, url):
    soup = bs(response.text, features="html.parser")
    link_list = []
    for div in soup.find_all("td", class_="cislo"):
        for link in div.find_all("a"):
            href = link.get('href')
            if href:
                full_link = urljoin(url, href)
                link_list.append(full_link)
    return link_list

def extract_data(link):
    response = requests.get(link)
    soup = bs(response.text, features="html.parser")
    data = soup.find_all("td")
    table_data = []
    for data in data:
        table_data.append(data.get_text(strip=True))
    return table_data

def create_header(data, file):
    with open(file, mode = "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        literal_columns = [item for item in data if any(c.isalpha() and item != "X" for c in item)]
        header = [
            "Kód obce",
            "Název obce",
            "Voliči v seznamu",
            "Vydané obálky",
            "Platné hlasy"
        ] + literal_columns
        writer.writerow(header)

def get_town_name(link):
    response = requests.get(link)
    soup = bs(response.text, features="html.parser")
    data = soup.find_all("h3")
    for town in data:
        parts = town.get_text().split(":")
        if len(parts) > 1 and parts[0].strip() == "Obec":
            town_name = parts[1].strip()
            return town_name

def get_votes_number(link):
    data = extract_data(link)
    trimmed_data = data[9:]
    while trimmed_data and trimmed_data[-1] == '-':
        trimmed_data.pop()
    return trimmed_data[2::5]

def write_data(link, file):
    with open(file, mode = "a") as csv_file:
        writer = csv.writer(csv_file)
        votes_for_parties = get_votes_number(link)
        row = [
            link[-19:-12],
            get_town_name(link),
            extract_data(link)[3],
            extract_data(link)[4],
            extract_data(link)[7]
        ] + votes_for_parties
        writer.writerow(row)

def main(url, file):
    check_url(url)
    validate_arguments(url, file)
    response = get_response(url)
    link_list = extract_links(response, url)
    data = extract_data(link_list[0])
    create_header(data, file)
    for link in link_list:
        extract_data(link)
        write_data(link, file)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if not args.url or not args.file:
        print("Musíte zadat URL a název CSV souboru.")
        sys.exit(1)
    else:
        main(args.url, args.file)