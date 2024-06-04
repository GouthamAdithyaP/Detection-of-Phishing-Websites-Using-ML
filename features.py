import re
import ipaddress
import whois
import urllib
import requests
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Function to extract domain from URL
def getDomain(url):
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain

# Function to check if URL contains IP address
def havingIP(url):
    try:
        ipaddress.ip_address(url)
        return 1
    except:
        return 0

# Function to check if URL contains "@" symbol
def haveAtSign(url):
    return 1 if "@" in url else 0

# Function to check URL length
def getLength(url):
    return 1 if len(url) >= 54 else 0

# Function to get depth of URL
def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = 0
    for segment in s:
        if segment:
            depth += 1
    return depth

# Function to check if URL redirects
def redirection(url):
    return 1 if url.rfind('//') > 6 else 0

# Function to check if URL uses HTTPS
def httpDomain(url):
    return 1 if 'https' in urlparse(url).netloc else 0

# Function to check if URL is from a known URL shortening service
def tinyURL(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                          r"tr\.im|link\.zip\.net"
    return 1 if re.search(shortening_services, url) else 0

# Function to check if URL contains prefix or suffix in domain
def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

# Function to check web traffic rank using Alexa
def web_traffic(url):
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1
    return 1 if rank < 100000 else 0

# Function to check domain age
def domainAge(url):
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        return 1
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if isinstance(creation_date, str) or isinstance(expiration_date, str):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if expiration_date is None or creation_date is None:
        return 1
    elif isinstance(expiration_date, list) or isinstance(creation_date, list):
        return 1
    else:
        age_of_domain = abs((expiration_date - creation_date).days)
        return 1 if (age_of_domain / 30) < 6 else 0

# Function to check domain expiration
def domainEnd(url):
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        return 1
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if expiration_date is None:
        return 1
    elif isinstance(expiration_date, list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        return 1 if (end / 30) < 6 else 0

# Function to check if HTML page contains iframe
def iframe(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return 1 if response == "" or re.findall(r"[<iframe>|<frameBorder>]", response.text) else 0

# Function to check if HTML page contains mouseover event
def mouseOver(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return 1 if response == "" or re.findall("<script>.+onmouseover.+</script>", response.text) else 0

# Function to check if HTML page contains right-click event
def rightClick(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return 1 if response == "" or re.findall(r"event.button ?== ?2", response.text) else 0

# Function to check if URL redirects multiple times
def forwarding(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return 1 if response == "" or len(response.history) > 2 else 0

# Function to perform feature extraction
def extract_features(url):
    features = [
       #getDomain(url),
        havingIP(url),
        haveAtSign(url),
        getLength(url),
        getDepth(url),
        redirection(url),
        httpDomain(url),
        prefixSuffix(url),
        tinyURL(url)
    ]
    # Address bar based features (9)

    # Domain based features (4)
    features.append(1 if domainAge(url) == 1 else 1)
    features.append(1 if domainEnd(url) == 1 else 1)

    # HTML & Javascript based features (4)
    features.append(iframe(url))
    features.append(mouseOver(url))
    features.append(rightClick(url))
    features.append(forwarding(url))
    features.append(forwarding(url))
    features.append(forwarding(url))

    return features
'''if __name__ == "__main__":
    url = 'http://www.facebook.com/home/service'
    features = extract_features(url)
    print(features)'''
