from scraper import*
from databaseFunctions import*

##Given a particular wikilink this uses functions from scraper.py to collect metaData for a link 
def getMetadata(link,flag):# flag is True if link is a Telenav link 
    soup = converter(link)
    name  =  title(soup,flag)
    date = time(soup,flag)
    attachmentsData = (attachments(soup,flag))
    return name,date,attachmentsData


## Input list of links into function, returns a 2d list with relevant metaData ##[[link,name,date,attachments]]

def convert(links):
    flag = False # this flag is used to check if a link is related to Telenav 
    newLinks =[]
    for link in links:
        if link.find("telenav")!=-1 and link.find("Telenav")!=1:
            flag = True 
            # if link is https://www.google.com then flag = False, no need to scrape/fetch MetaData 
        
        
        try:
            name,date,attachments = getMetadata(link,flag)
            
        except:
            name,date,attachments = link,"None","None"
     
        newLink = [link,str(name),date,attachments]
        flag = False 
        newLinks.append(newLink)
        
   
    return newLinks


    

###use this to debug 
#print(convert(["https://spaces.telenav.com:8443/display/svr/infogroup"]))
#addToNodes(conn(),"FKA","D",convert(["https://spaces.telenav.com:8443/display/svr/infogroup","https://spaces.telenav.com:8443/display/svr/infogroup"]))
    

 

##These functions are not used anymore can be used in the future 
#####Not using these fucntion currently 

def convertLinks(list):
    if list!= None:
        links = dict()
        
        for link in list:
            links[link]=linkToText(link)
        return links
        
#it is a simple function to convert https:string to a few keywords 
def linkToText(link):

    if link.find("title=") !=- 1:
        startIndex = link.find("title=")+6
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
    
    elif link.find("svr") !=- 1:
        startIndex = link.find("svr")+4
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
    elif link.find("syse")!= -1:
        startIndex = link.find("syse")+5
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
    else:
        return link
        pass
        