
from connection import*

#readValues(conn)

def readValues(connection):
	nodes =[ ]
	#relations = {}

	# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
	# psycopg2 creates a server-side cursor, which prevents all of the
	# records from being downloaded at once from the server.
	cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute('SELECT * FROM nodes LIMIT 1000')

	# Because cursor objects are iterable we can just call 'for - in' on
	# the cursor object and the cursor will automatically advance itself
	# each iteration.
	# This loop should run 1000 times, assuming there are at least 1000
	# records in 'my_table'
	row_count = 0

	for row in cursor:
		row_count += 1
		nodes.extend([row])

		print ("row: %s    %s\n" % (row_count, row))
	print(nodes)
	cursor = conn.cursor('cursor_unique_name1', cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute('SELECT * FROM parent LIMIT 1000')

	# Because cursor objects are iterable we can just call 'for - in' on
	# the cursor object and the cursor will automatically advance itself
	# each iteration.
	# This loop should run 1000 times, assuming there are at least 1000
	# records in 'my_table'
	row_count = 0
	for row in cursor:
		row_count += 1
		print ("row: %s    %s\n" % (row_count, row))

