# Phishing Website Detector
Leverage domain similarity and content analysis to detect phishing websites that are hosted on typosquated domains

## Usage
```code
python3 phishdetect.py -h
usage: phishdetect.py [-h] [-l] [-f] url

positional arguments:
  url         Specify the domain that should be compared with the safe one

optional arguments:
  -h, --help  show this help message and exit
  -l, --list  List similarities with the domains known by PhishDetect
  -f, --file  Scan a local html file
```

### Example #1
```code
python3 phishdetect.py www.googled.com
[+] googled.com is 95% similar to google.com
```

### Example #2
```code
python3 phishdetect.py -f demo_files/set_phish.html
[+] Title match: 100% for google.com
[+] Title match: 20% for accounts.google.com
[+] Found password input field
[+] Found keyword: login
[+] Found keyword: sign in
[+] Found keyword: signin
===============================================
[+] The webpage is most likely a login page
```