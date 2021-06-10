import os
import json
import argparse
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from difflib import SequenceMatcher
from difflib import get_close_matches

# Parameters
similarity_treshold = 90
subdomain_treshold = 60

db = []

generic_keywords = ["login", "log in", "authenticate", "sign in", "signin"]

def similar_domain_ratio(source, target):
    return round(SequenceMatcher(None, source, target).ratio() * 100)

def is_subdomain(source, target):
    a = SequenceMatcher(None, source, target).find_longest_match(0,len(source),0,len(target))
    extracted = target[a.b:(a.b + a.size)]
    similarity = similar_domain_ratio(source, extracted)
    if similarity >= subdomain_treshold:
        return extracted
    return None

def process_url(x):
    if not x.startswith('http'):
        # BUG for urlparse to ensure netloc can be extracted
        x = "http://" + x
    d = urlparse(x).netloc
    return d

def get_root_domain(x):
    return '.'.join(x.split('.')[-2:-1])

def get_root_tld(x):
    return '.'.join(x.split('.')[-2:])

def analyze_domain(d):
    rd = get_root_tld(d)

    # Process domain similarity
    max = 0
    hit = "debug"
    for i in db:
        x = similar_domain_ratio(i['domain'], rd)
        if x > max:
                max = x
        if x > similarity_treshold:
            hit = i['domain']

    if max > similarity_treshold:
        print("[+] {} is {}% similar to {}".format(rd,max,hit))
    
    if max < subdomain_treshold:
        for i in db:
            r = is_subdomain(i['domain'], d)
            if r:
                print("[+] {} is a subdomain of {}".format(i['domain'],d))


def list_domains(url):
    domain = get_root_domain(url)
    banner = "Similarity report for: {}".format(domain)
    print(banner)
    print("-" * len(banner))
    for i in db:
        x = similar_domain_ratio(i['domain'], domain)
        print("{}% Match for {}".format(str(x),i['domain']))

def analyze_local_file(path):
    try:
        if os.path.isfile(path):
            with open(path,'r') as f:
                content = f.read()
                analyze_content(content)
        else:
            print("[!] Something is wrong with the path")
    except:
        print("[!] Cannot analyze file")

def analyze_content(content):

    #flags
    tile_match = False
    password_input = False
    auth_keywords = False

    soup = BeautifulSoup(content, 'html.parser')

    # Check for similar title
    for u in db:
        x1 = round(SequenceMatcher(None, u['title'], soup.title.string).ratio() * 100)
        print("[+] Title match: {}% for {}".format(str(x1),u['domain']))
        if x1 > similarity_treshold:
            tile_match = True


    # Find if the website has a password input field
    x2 = soup.find('input',type='password')
    if x2:
        password_input = True
        print("[+] Found password input field")
    else:
        print("[-] No password field found")

    # Look for generic keywords within the contents
    x3 = str(soup.find('form')).lower()
    for s in generic_keywords:
        if x3.find(s) != -1:
            auth_keywords = True
            print("[+] Found keyword: {}".format(s))

    print("===============================================")
    if tile_match or password_input or auth_keywords:
        print("[+] The webpage is most likely a login page")
    else:
        print("[-] The web page is not a login page")


def load_websites():
    with open('config.json','r') as f:
        jfile = f.read()
    return json.loads(jfile)



if __name__ == '__main__':
    try:
        db = load_websites()
    except:
        print("[!] Cannot load config data")
        quit()

    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="Specify the domain that should be compared with the safe one")
    #parser.add_argument("-a", "--add", action="store_true", help="Add a new website to be library")
    parser.add_argument("-l", "--list", action="store_true", help="List similarities with the domains known by PhishDetect")
    parser.add_argument("-f", "--file", action="store_true", help="Scan a local html file")

    args = parser.parse_args()
    
    url = process_url(args.url)
    
    while True:
        if args.list:
            
            list_domains(url)
            break

        if args.file:
            analyze_local_file(args.url)
            break

        analyze_domain(url)
        break
