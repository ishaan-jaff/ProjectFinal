import requests
from bs4 import BeautifulSoup
# need requests and beautiful soup on system to use 

def fetchMetaData(links):
    session = logIn()
    for link in links:
        soup = converter(session,link)
        print(title(soup))


## used to login and create a session for Telenav Servers 
def logIn():
    LOGIN_URL = 'https://spaces.telenav.com:8443/login.action?'
    
    session = requests.session()
    
    login_data = {'initialURI': '/portal',
                'loginname': '',
                'loginpassword': '',
                'os_username': 'ishaanj@telenav.com',
                'os_password': 'Mehn@z2424'}
    session.post(LOGIN_URL, data=login_data)
    
    return session
    
## Convert the webpage into html data and into a soup format, readable by Beautiful Soup
def converter(URL):
    session = logIn()
    req = session.get(URL)
    data = req.text
    soup = BeautifulSoup(data,"html.parser")
    return soup


##To get data about tables/table headers on link
def tableHeaders(soup):
    tableData = [ ]
    for element in (soup.find_all('th')):#table headers stored as "th" in html 
        title = str(element.string).replace("'","")
        if title !=None and title.replace(" ","")!="" :
            
            title = title.replace(u'\xa0', u' ')
            """ this was an exception, it is to prevent the  application from crashing, some tableHeaders have \xa0 which can not be inserted into the db  """
            
            
            #title should not be None or more than 60 characters
            if len(title)<=60 and title.strip()!="None":
                tableData.append(title)
    
    return tableData
  
  
## to get images from wikiLink
def images(soup):
    
    names = []
    links = []
    namesLinks = dict()
    for x in (soup.find_all('img')):# Images stores as img
        if (x.get('class')==['confluence-embedded-image']):# all images are mainly in this class
            link = (x.get('data-image-src'))
            namesLinks[link] = link
        
    # this for loop checks if images are stored in a different format 
    for i in soup.find_all('img'):
        name = (i.get('alt'))
        
        name = str(name).replace("'","")
        name =  name.replace(u'\xa0', u' ')
        """ this was an exception, it is to prevent the application from crashing, some tableHeaders have \xa0 which can not be inserted into the db  """
        
        
        if name!=None and name.find('User icon')==-1:# it is irrelevant if it is just a user icon
            link1 = ""
            link2 = str(i.get('src'))
            
            
            if (link2!=None):
                link = link1+link2 
            
                if name not in namesLinks:# prevent entering duplicates
                    namesLinks[name] = link 
    return namesLinks
       


## to get all attachment files and arrange then in format used in function, insertMetaData() in #databaseFunctions.py
def attachments(soup,flag):
    if flag == True:# if links is related to Telenav only then check for attachments 
        
        #dictionary with name of attachment and link 
        # {telenav.pdf: https://spaces.telenav.com:8443/download/attachments/}
        namesLinks = dict()
        
        
        serverUrl = ""
        for x in (soup.find_all('a')):# attachments are under class "a"
            if x.get('id')=="content-metadata-attachments":
                link = x.get('href')
                link = link.replace(u'\xa0', u' ')
                """ this was an exception, it is to prevent the application from crashing, some tableHeaders have \xa0 which can not be inserted into the db  """
                
                
                
                if link not in namesLinks:# to prevent duplicateData
                    namesLinks[link] = link
            
            if x.get('data-filename')!=None:# another method of getting attachments from html
                name = x.get('data-filename')
                name = name.replace("'","")
                name = name.replace(u'\xa0', u' ')
                #Same exception case as above 
                
                
                
                link = serverUrl + str(x.get('href'))
                link = link.replace(u'\xa0', u' ')
                #Same exception case as above 
                
                
                
                if name.find('image20') == -1:# do not want images inserted 
                    if name not in namesLinks:
                        namesLinks[name] = link # insert into dictionary 
        
        
        
        imgs = images(soup)
        tableData = tableHeaders(soup)
         
         
         
        """THE PROBLEM:
        The return statement is a workaround, in a json array it was not possible to have an element that was a two dimensional list, it led to issues because the strings/links needed to be entered wihtou quotation marks. When using commas to seperate elements it would not work when reading from db. 
        if metadata was entered as [{attachment:https://spaces.telenav,at:https:/www.},[1,2,3,Header],{img:imgLink}
        Since the lists and dictionaries had many elements seperated with "," within the returned list when the data was read and the string.split(",") was run the list returned was not formatted correctly 
        THE SOLUTION:
        Instead of using a "," the string "SPLITTER" is used, it is only on the back end. It is used because now a string.split("SPLITTER") can be called to create a lists of different elements in the attachmnets list. string.split("SPLITTER") is called in when the attcahments button is clicked in the UI.py file """

        return [namesLinks,"SPLITTER",tableData,"SPLITTER",(imgs)]
        
    else:
        return None 
        
        
def title(soup,flag):
    
    if flag == True :# only if it is a Telenav link 
        namesLinks = dict()
        name = soup.title.string        
      
        name = name.replace("-",",")       
        return name
    else:
        return soup.title.string
## get last modified, seen in the UI, last modified for each link 
def time(soup,flag):
    if flag==True:
        data = str(soup.find('a',class_ = 'last-modified'))
        data = (data.split(">")[1])
        data = (data.split("<")[0])
        data =  data.replace(",","-")
        return data 
    else:
        return "None" 
    
    
    
def linksOnPage(soup):

    for link in soup.find_all('a'):
        print(link.get('href'))


############ Use these functions if need to debug 
#URL = 'https://spaces.telenav.com:8443/pages/viewpage.action?spaceKey=svr&title=Search+Categories'
#soup = converter(URL)
#print(images(soup))

#print(soup.prettify())
#tableHeaders(soup)
#linksOnPage(soup)
#print(title(soup))
#time(soup)
#print(tableHeaders(soup))
#print(images(soup))
#print(attachments(soup,True))
#linksOnPage(soup)
