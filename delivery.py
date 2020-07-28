import sqlite3
import csv
from operator import itemgetter

conn = sqlite3.connect('delivery.db')

c = conn.cursor()

eleven_am = 0
twelve_pm = 0
one_pm = 0
two_pm = 0
three_pm = 0
four_pm = 0
five_pm = 0
six_pm = 0
invalid_time = 0
date_field = 1
day_field = 2
time_field = 3
meds_field = 4
location_field = 5
total_deliveries = 0 
total_medications = 0
total_days = 0
average_deliveries = 0
average_medications = 0

# create a table
c.execute('DROP TABLE IF EXISTS deliveries')
c.execute("""CREATE TABLE "deliveries" (
		"delivery_date" text,
		"delivery_day" text,
		"delivery_time" integer,
		"delivery_meds" integer,
		"delivery_floor" text
	)""")

# default name of csv file to be read
fname = "deliveries.csv"
 
# open and read the cvs file inserted into tuple 
with open(fname) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter = ',')
	for item in csv_reader:
		delivery_date = item[0]
		delivery_day = item[1]
		delivery_time = int(item[2])
		delivery_meds = int(item[3])
		delivery_floor = item[4]
		c.executemany("INSERT INTO deliveries VALUES (?,?,?,?,?)", [(delivery_date, delivery_day, delivery_time, delivery_meds, delivery_floor,)])	

conn.commit()

# query the database and return all records showing totals with average
def show_all():

	#variables to calculate totals and averages
	global total_deliveries
	global total_medications
	global total_days
	global average_deliveries
	global average_medications

	# selecting all items from deliveries including the rowid
	c.execute("SELECT rowid, * FROM deliveries")

	items = c.fetchall()
	
	header()

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[meds_field]

	# grouping by date because of multiple deliveries on same day
	c.execute("SELECT rowid, * FROM deliveries GROUP BY delivery_date")

	items = c.fetchall()

	for item in items:
		total_days += 1

	average_deliveries = total_deliveries / total_days
	average_medications = total_medications / total_days

	line()
	print('The total amount of deliveries is : ' + str(total_deliveries))
	print('The total amount of medications is : ' + str(total_medications))
	print('The average amount of daily deliveries is : ' + str(average_deliveries))
	print('The average amount of daily medications is : ' + str(average_medications))
	line()

# show the deliveries made on weekdays Mon - Fri
def show_weekdays():

	#variables to calculate totals and averages
	global total_deliveries
	global total_medications
	global total_days
	global average_deliveries
	global average_medications

	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = 'Monday' 
				OR delivery_day = 'Tuesday' 
				OR delivery_day = 'Wednesday' 
				OR delivery_day = 'Thursday' 
				OR delivery_day = 'Friday'
	""")

	items = c.fetchall()

	header()

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[4]

	# grouping by date because of multiple deliveries on same day
	c.execute("""SELECT rowid, * FROM deliveries
				WHERE delivery_day = 'Monday' 
				OR delivery_day = 'Tuesday' 
				OR delivery_day = 'Wednesday' 
				OR delivery_day = 'Thursday' 
				OR delivery_day = 'Friday'
				GROUP BY delivery_date
	""")

	items = c.fetchall()

	for item in items:
		total_days += 1

	average_deliveries = total_deliveries / total_days
	average_medications = total_medications / total_days

	line()
	print('The total amount of weekday deliveries is : ' + str(total_deliveries))
	print('The total amount of weekday medications is : ' + str(total_medications))
	print('The average amount of weekday deliveries is : ' + str(average_deliveries))
	print('The average amount of weekday medications is : ' + str(average_medications))
	line()

# show the deliveries on weekends Sat - Sun
def show_weekends():

	#variables to calculate totals and averages
	global total_deliveries
	global total_medications
	global total_days
	global average_deliveries
	global average_medications

	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = 'Sunday' 
				OR delivery_day = 'Saturday'
	""")

	items = c.fetchall()

	header()

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[4]

	# grouping by date because of multiple deliveries on same day
	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = 'Sunday' 
				OR delivery_day = 'Saturday'
				GROUP BY delivery_date
	""")

	items = c.fetchall()

	for item in items:
		total_days += 1

	average_deliveries = total_deliveries / total_days
	average_medications = total_medications / total_days

	line()
	print('The total amount of weekend deliveries is : ' + str(total_deliveries))
	print('The total amount of weekend medications is : ' + str(total_medications))
	print('The average amount of weekend deliveries is : ' + str(average_deliveries))
	print('The average amount of weekend medications is : ' + str(average_medications))
	line()

# shows the # of meds and # of deliveries made on each date
def show_dates():

	c.execute("""SELECT delivery_date, delivery_day, sum(delivery_meds), COUNT(delivery_date) FROM deliveries 
				GROUP BY delivery_date
	""")

	items = c.fetchall()

	line()
	print('{:<12s}{:<12s}{:<12s}{:>12s}'.format("DATE ","DAY ","# OF MEDS", "# OF DELIVERIES"))
	line()

	for item in items:
		print('{:<12s}{:<12s}{:^8s}{:>12s}'.format(item[0], item[1], str(item[2]), str(item[3])))

	line()

# show the deliveries made on a specified day of week with delivery times, medication totals, and averages
def day_lookup(day):

	global eleven_am 
	global twelve_pm 
	global one_pm
	global two_pm
	global three_pm
	global four_pm
	global five_pm
	global six_pm
	global invalid_time

	total_deliveries = 0 
	total_medications = 0
	total_days = 0
	average_deliveries = 0
	average_medications = 0

	c.execute("SELECT rowid, * FROM deliveries WHERE delivery_day = (?)", (day,))

	items = c.fetchall()

	header()

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[time_field], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[meds_field]

		find_times(item)
	
	# grouping by date because of multiple deliveries on same day
	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = (?)
				GROUP BY delivery_date 
		""", (day,)) 

	items = c.fetchall()

	for item in items:
		total_days += 1

	average_deliveries = total_deliveries / total_days
	average_medications = total_medications / total_days

	line()
	print('The amount of ' + day + ' deliveries at 11am is : ' + str(eleven_am))
	print('The amount of ' + day + ' deliveries at 12pm is : ' + str(twelve_pm))
	print('The amount of ' + day + ' deliveries at 1pm is : ' + str(one_pm))
	print('The amount of ' + day + ' deliveries at 2pm is : ' + str(two_pm))
	print('The amount of ' + day + ' deliveries at 3pm is : ' + str(three_pm))
	print('The amount of ' + day + ' deliveries at 4pm is : ' + str(four_pm))
	print('The amount of ' + day + ' deliveries at 5pm is : ' + str(five_pm))
	print('The amount of ' + day + ' deliveries at 6pm is : ' + str(six_pm))
	print('You have ' + str(invalid_time) + ' invalid time(s) in your list.')
	line()
	print('The total amount of deliveries on ' + day + ' is : ' + str(total_deliveries))
	print('The total amount of medications on ' + day + ' is : ' + str(total_medications))
	print('The average amount of deliveries on ' + day + ' is : ' + str(average_deliveries))
	print('The average amount of medications on ' + day + ' is : ' + str(average_medications))
	line()

# show the deliveries made on a specified date with delivery times and totals in 'DD-MON-YY' format
def date_lookup(date):

	global eleven_am 
	global twelve_pm 
	global one_pm
	global two_pm
	global three_pm
	global four_pm
	global five_pm
	global six_pm
	global invalid_time

	total_deliveries = 0 
	total_medications = 0

	c.execute("SELECT rowid, * FROM deliveries WHERE delivery_date = (?)", (date,))

	items = c.fetchall()

	header()

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[meds_field]

		find_times(item)

	print('----------------------------------------------------------------')
	print('The amount of ' + date + ' deliveries at 11am is : ' + str(eleven_am))
	print('The amount of ' + date + ' deliveries at 12pm is : ' + str(twelve_pm))
	print('The amount of ' + date + ' deliveries at 1pm is : ' + str(one_pm))
	print('The amount of ' + date + ' deliveries at 2pm is : ' + str(two_pm))
	print('The amount of ' + date + ' deliveries at 3pm is : ' + str(three_pm))
	print('The amount of ' + date + ' deliveries at 4pm is : ' + str(four_pm))
	print('The amount of ' + date + ' deliveries at 5pm is : ' + str(five_pm))
	print('The amount of ' + date + ' deliveries at 6pm is : ' + str(six_pm))
	print('You have ' + str(invalid_time) + ' invalid time(s) in your list.')
	print('----------------------------------------------------------------')
	print('The total amount of deliveries on ' + date + ' is : ' + str(total_deliveries))
	print('The total amount of medications on ' + date + ' is : ' + str(total_medications))
	print('----------------------------------------------------------------')

# shows the times deliveries were made for all days
def daily_times():

	c.execute("""SELECT rowid, * FROM deliveries
	""")

	items = c.fetchall()

	for item in items:
		find_times(item)
	
	line()
	print('The daily amount of deliveries at 11am is : ' + str(eleven_am))
	print('The daily amount of deliveries at 12pm is : ' + str(twelve_pm))
	print('The daily amount of deliveries at 1pm is : ' + str(one_pm))
	print('The daily amount of deliveries at 2pm is : ' + str(two_pm))
	print('The daily amount of deliveries at 3pm is : ' + str(three_pm))
	print('The daily amount of deliveries at 4pm is : ' + str(four_pm))
	print('The daily amount of deliveries at 5pm is : ' + str(five_pm))
	print('The daily amount of deliveries at 6pm is : ' + str(six_pm))
	print('You have ' + str(invalid_time) + ' invalid time(s) in your list.')
	line()

def find_times(item):

	global eleven_am 
	global twelve_pm 
	global one_pm
	global two_pm
	global three_pm
	global four_pm
	global five_pm
	global six_pm
	global invalid_time

	if item[time_field] / 100 == 11:
		eleven_am += 1
	elif item[time_field] / 100 == 12:
		twelve_pm += 1
	elif item[time_field] / 100 == 13:
		one_pm += 1
	elif item[time_field] / 100 == 14:
		two_pm += 1
	elif item[time_field] / 100 == 15:
		three_pm += 1
	elif item[time_field] / 100 == 16:
		four_pm += 1
	elif item[time_field] / 100 == 17:
		five_pm += 1
	elif item[time_field] / 100 >= 18:
		six_pm += 1
	else:
		invalid_time += 1

def create_time_map():

	global time_field

	c.execute("""SELECT rowid, * FROM deliveries
	""")

	items = c.fetchall()

	di = dict()

	for item in items:

		time = item[time_field]

		military_time = time / 100

		# add am or am to key
		if military_time < 12:
			clock_time = (str(military_time) + 'am')
		elif military_time == 12:
			clock_time = (str(military_time) + 'pm')
		else:
			clock_time = (str(military_time - 12) + 'pm')

		if clock_time in di:
			di[clock_time] += 1
		else:
			di[clock_time] = 1

	# creating a new list to sort by number of deliveries made at a certain time
	tmp = list()
	for k, v in di.items():
		newt = (v, k)
		tmp.append(newt)

	tmp = sorted(tmp, reverse = True)

	line()
	for k, v in tmp:
		print('There were ' + str(k) + ' deliveries made at ' + str(v))
	line()

# counts and shows which floor the drugs were delivered to
def create_location_map():

	global location_field

	c.execute("""SELECT rowid, * FROM deliveries
	""")

	items = c.fetchall()

	di = dict()

	for item in items:

		location = item[location_field]
		
		if location in di :
			di[location] = di[location] + 1
		else:
			di[location] = 1

	# creating a new list to sort by number of deliveries made to a certain floor
	tmp = list()
	for k, v in di.items():
		newt = (v, k)
		tmp.append(newt)
		
	tmp = sorted(tmp, reverse = True)

	line()
	for v, k in tmp:
		print('There were ' + str(v) + ' deliveries made to ' + str(k))
	line()

def sort_meds():

	# selecting all items from deliveries including the rowid
	c.execute("SELECT rowid, * FROM deliveries")

	items = c.fetchall()
	
	header()

	tmp = sorted(items, key = itemgetter(meds_field))

	for item in tmp:

		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))

	line()

	#export function
	command = raw_input('Would you like to export this data (Y)? Hit enter to cancel.')
	if command == 'Y':
		with open('deliveries_medication_sorted.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(tmp)
			print('Data has been exported.')
	else:
		print('Data was not exported.')

def sort_times():

	# selecting all items from deliveries including the rowid
	c.execute("SELECT rowid, * FROM deliveries")

	items = c.fetchall()
	
	header()

	tmp = sorted(items, key = itemgetter(date_field,time_field))

	for item in tmp:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))

	line()

	create_time_map()

	command = raw_input('Would you like to export this data (Y)? Hit enter to cancel.')
	if command == 'Y':
		with open('deliveries_time_sorted.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(tmp)
			print('Data has been exported.')
	else:
		print('Data was not exported.')

def sort_locations():

	# selecting all items from deliveries including the rowid
	c.execute("SELECT rowid, * FROM deliveries")

	items = c.fetchall()
	
	# formatting
	header()

	tmp = sorted(items, key = itemgetter(location_field,date_field))

	for item in tmp:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))

 	line()

 	create_location_map()

 	command = raw_input('Would you like to export this data (Y)? Hit enter to cancel.')
	if command == 'Y':
		with open('deliveries_location_sorted.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(tmp)
			print('Data has been exported.')
	else:
		print('Data was not exported.')

# add a new record to the table
def add_one(date, day, time, meds, floor):
	with conn:
		c.execute("INSERT INTO deliveries VALUES (?,?,?,?,?)", (date, day, time, meds, floor))

# delete record from table
def delete_one(id):
	with conn:
		c.execute("DELETE from deliveries WHERE rowid = (?)", id)

# add many records to table
def add_many(list):
	with conn:
		c.executemany("INSERT INTO deliveries VALUES (?,?,?,?,?)", (list))

def header():
	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

def line():
	print('----------------------------------------------------------------')
