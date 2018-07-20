import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys


def addNode(conn,nodeName, description,links):
    cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('INSERT INTO nodes (Name, Description, wikilinks) VALUES(nodeName, description,links')
    
    
    

    
