import requests
from bs4 import BeautifulSoup




URL = 'https://spaces.telenav.com:8443/pages/viewpage.action?pageId=96177147'
LOGIN_URL = 'https://spaces.telenav.com:8443/login.action?'

session = requests.session()

login_data = {'initialURI': '/portal',
              'loginname': '',
              'loginpassword': '',
              'os_username': 'ishaanj@telenav.com',
              'os_password': 'Mehn@z2424'}
session.post(LOGIN_URL, data=login_data)


req = session.get(URL)
data = req.text
#h = req
soup = BeautifulSoup(data,"html.parser")

#for element in (soup.find_all('th')):
def tableHeaders(soup):
    for element in (soup.find_all('th')):
        print(element.string)
    #print(element.get('th'))
#print(soup.prettify())
#tableHeaders(soup)
def images(soup):

    for img in soup.find_all('img'):
    
        name = (img.get('alt'))
        if name!=None:
            print(name)

#images(soup)
#print(soup.find_all('img'))
def title(soup):
    name = soup.title.string
    print("path="+name)
    pos = name.find("-")
    if pos!=-1:
        return name[0:pos]
    else:
        return name
    
print("title="+title(soup))
def linksOnPage(soup):

    for link in soup.find_all('a'):
        print(link.get('href'))
#linksOnPage(soup)
#samples = soup.find_all("a", "item-title")
#print(soup)
#print(data)

