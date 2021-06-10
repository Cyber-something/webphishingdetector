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