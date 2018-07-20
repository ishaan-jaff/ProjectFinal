
def linkToText(link):
    
    if link.find("title=") !=- 1:
        startIndex = link.find("title=")+6
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
    
    if link.find("svr") !=- 1:
        startIndex = link.find("svr")+4
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
    if link.find("syse")!= -1:
        startIndex = link.find("syse")+5
        link = link[startIndex:]
        
    
        link = link.replace("+", ' ')
        link = link.replace("-", ' ')
        link = link.replace("=", ' ')
        link = ' '.join(link.split())
        return link
        
        
def convertLinks(list):
    links = dict()
    
    for link in list:
        links[link]=linkToText(link)
    return links
 
 
 
list = ['http://spaces.telenav.com:8080/display/svr/Toyota+-+Factual+Search', 'http://spaces.telenav.com:8080/display/svr/Nightly+Builds+Weekly+Summary', 'http://spaces.telenav.com:8080/display/svr/Search+Categories', 'http://spaces.telenav.com:8080/display/svr/Product+and+Search+Data+matrix', 'http://spaces.telenav.com:8080/display/svr/Product+and+Search+Data+matrix']   
    
#print(convertLinks(list))
    
        