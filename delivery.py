import sqlite3
import csv

conn = sqlite3.connect('delivery.db')

c = conn.cursor()

# create a table
c.execute('DROP TABLE IF EXISTS deliveries')
c.execute("""CREATE TABLE "deliveries" (
		"delivery_date" text,
		"delivery_day" text,
		"delivery_time" integer,
		"delivery_meds" integer,
		"delivery_floor" text
	)""")

fname = "deliveries.csv"

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

	# variables to calculate totals and averages
	total_deliveries = 0 
	total_medications = 0
	total_days = 0
	average_deliveries = 0
	average_medications = 0

	c.execute("SELECT rowid, * FROM deliveries")

	items = c.fetchall()
	
	# formatting
	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[4]

	# grouping by date because of multiple deliveries on same day
	c.execute("SELECT rowid, * FROM deliveries GROUP BY delivery_date")

	items = c.fetchall()

	for item in items:
		total_days += 1

	average_deliveries = total_deliveries / total_days
	average_medications = total_medications / total_days

	print('----------------------------------------------------------------')
	print('The total amount of deliveries is : ' + str(total_deliveries))
	print('The total amount of medications is : ' + str(total_medications))
	print('The average amount of daily deliveries is : ' + str(average_deliveries))
	print('The average amount of daily medications is : ' + str(average_medications))
	print('----------------------------------------------------------------')

# show the deliveries made on weekdays Mon - Fri
def show_weekdays():

	# variables to calculate totals and averages
	total_deliveries = 0 
	total_medications = 0
	total_days = 0
	average_deliveries = 0
	average_medications = 0

	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = 'Monday' 
				OR delivery_day = 'Tuesday' 
				OR delivery_day = 'Wednesday' 
				OR delivery_day = 'Thursday' 
				OR delivery_day = 'Friday'
	""")

	items = c.fetchall()

	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

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

	print('----------------------------------------------------------------')
	print('The total amount of weekday deliveries is : ' + str(total_deliveries))
	print('The total amount of weekday medications is : ' + str(total_medications))
	print('The average amount of weekday deliveries is : ' + str(average_deliveries))
	print('The average amount of weekday medications is : ' + str(average_medications))
	print('----------------------------------------------------------------')

# show the deliveries on weekends Sat - Sun
def show_weekends():

	# variables to calculate totals and averages
	total_deliveries = 0 
	total_medications = 0
	total_days = 0
	average_deliveries = 0
	average_medications = 0

	c.execute("""SELECT rowid, * FROM deliveries 
				WHERE delivery_day = 'Sunday' 
				OR delivery_day = 'Saturday'
	""")

	items = c.fetchall()

	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

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

	print('----------------------------------------------------------------')
	print('The total amount of weekend deliveries is : ' + str(total_deliveries))
	print('The total amount of weekend medications is : ' + str(total_medications))
	print('The average amount of weekend deliveries is : ' + str(average_deliveries))
	print('The average amount of weekend medications is : ' + str(average_medications))
	print('----------------------------------------------------------------')

def show_dates():

	c.execute("""SELECT delivery_date, delivery_day, sum(delivery_meds), COUNT(delivery_date) FROM deliveries 
				GROUP BY delivery_date
	""")

	items = c.fetchall()

	print('----------------------------------------------------------------')
	print('{:<12s}{:<12s}{:<12s}{:>12s}'.format("DATE ","DAY ","# OF MEDS", "# OF DELIVERIES"))
	print('----------------------------------------------------------------')

	for item in items:
		
		print('{:<12s}{:<12s}{:^8s}{:>12s}'.format(item[0], item[1], str(item[2]), str(item[3])))

	print('----------------------------------------------------------------')

# show the deliveries made on a specified day of week with delivery times, medication totals, and averages
def day_lookup(day):

	# variables to calculate totals and averages
	total_deliveries = 0 
	total_medications = 0
	total_days = 0
	average_deliveries = 0
	average_medications = 0

	# variables to count deliveries made during certain times
	eleven_am = 0
	twelve_pm = 0
	one_pm = 0
	two_pm = 0
	three_pm = 0
	four_pm = 0
	five_pm = 0
	six_pm = 0
	invalid_time = 0

	c.execute("SELECT rowid, * FROM deliveries WHERE delivery_day = (?)", (day,))

	items = c.fetchall()

	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[4]

		if item[3] >= 1100 and item[3] < 1160:
			eleven_am += 1
		elif item[3] >= 1200 and item[3] < 1260:
			twelve_pm += 1
		elif item[3] >= 1300 and item[3] < 1360:
			one_pm += 1
		elif item[3] >= 1400 and item[3] < 1460:
			two_pm += 1
		elif item[3] >= 1500 and item[3] < 1560:
			three_pm += 1
		elif item[3] >= 1600 and item[3] < 1660:
			four_pm += 1
		elif item[3] >= 1700 and item[3] < 1760:
			five_pm += 1
		elif item[3] >= 1800 and item[3] < 1860:
			six_pm += 1
		else:
			invalid_time += 1
	
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

	print('----------------------------------------------------------------')
	print('The amount of ' + day + ' deliveries at 11am is : ' + str(eleven_am))
	print('The amount of ' + day + ' deliveries at 12pm is : ' + str(twelve_pm))
	print('The amount of ' + day + ' deliveries at 1pm is : ' + str(one_pm))
	print('The amount of ' + day + ' deliveries at 2pm is : ' + str(two_pm))
	print('The amount of ' + day + ' deliveries at 3pm is : ' + str(three_pm))
	print('The amount of ' + day + ' deliveries at 4pm is : ' + str(four_pm))
	print('The amount of ' + day + ' deliveries at 5pm is : ' + str(five_pm))
	print('The amount of ' + day + ' deliveries at 6pm is : ' + str(six_pm))
	print('You have ' + str(invalid_time) + ' invalid time(s) in your list.')
	print('----------------------------------------------------------------')
	print('The total amount of deliveries on ' + day + ' is : ' + str(total_deliveries))
	print('The total amount of medications on ' + day + ' is : ' + str(total_medications))
	print('The average amount of deliveries on ' + day + ' is : ' + str(average_deliveries))
	print('The average amount of medications on ' + day + ' is : ' + str(average_medications))
	print('----------------------------------------------------------------')

# show the deliveries made on a specified date with delivery times and totals in 'DD-MON-YY' format
def date_lookup(date):

	# variables to calculate totals and averages
	total_deliveries = 0 
	total_medications = 0

	# variables to count deliveries made during certain times
	eleven_am = 0
	twelve_pm = 0
	one_pm = 0
	two_pm = 0
	three_pm = 0
	four_pm = 0
	five_pm = 0
	six_pm = 0
	invalid_time = 0

	c.execute("SELECT rowid, * FROM deliveries WHERE delivery_date = (?)", (date,))

	items = c.fetchall()

	print('----------------------------------------------------------------')
	print('{:<10s}{:<10s}{:<12s}{:<8s}{:<8s}{:^12s}'.format("ID", "DATE ","DAY ","TIME ","# OF MEDS ","UNIT"))
	print('----------------------------------------------------------------')

	for item in items:
		print('{:<10d}{:<10s}{:<12s}{:<8d}{:^8d}{:>12s}'.format(item[0], item[1], item[2], item[3], item[4], item[5]))
		total_deliveries += 1
		total_medications += item[4]

		if item[3] >= 1100 and item[3] < 1160:
			eleven_am += 1
		elif item[3] >= 1200 and item[3] < 1260:
			twelve_pm += 1
		elif item[3] >= 1300 and item[3] < 1360:
			one_pm += 1
		elif item[3] >= 1400 and item[3] < 1460:
			two_pm += 1
		elif item[3] >= 1500 and item[3] < 1560:
			three_pm += 1
		elif item[3] >= 1600 and item[3] < 1660:
			four_pm += 1
		elif item[3] >= 1700 and item[3] < 1760:
			five_pm += 1
		elif item[3] >= 1800 and item[3] < 1860:
			six_pm += 1
		else:
			invalid_time += 1

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

	# variables to count deliveries made during certain times
	eleven_am = 0
	twelve_pm = 0
	one_pm = 0
	two_pm = 0
	three_pm = 0
	four_pm = 0
	five_pm = 0
	six_pm = 0
	invalid_time = 0

	c.execute("""SELECT rowid, * FROM deliveries
	""")

	items = c.fetchall()

	for item in items:
		if item[3] >= 1100 and item[3] < 1160:
			eleven_am += 1
		elif item[3] >= 1200 and item[3] < 1260:
			twelve_pm += 1
		elif item[3] >= 1300 and item[3] < 1360:
			one_pm += 1
		elif item[3] >= 1400 and item[3] < 1460:
			two_pm += 1
		elif item[3] >= 1500 and item[3] < 1560:
			three_pm += 1
		elif item[3] >= 1600 and item[3] < 1660:
			four_pm += 1
		elif item[3] >= 1700 and item[3] < 1760:
			five_pm += 1
		elif item[3] >= 1800 and item[3] < 1860:
			six_pm += 1
		else:
			invalid_time += 1
	
	print('The daily amount of deliveries at 11am is : ' + str(eleven_am))
	print('The daily amount of deliveries at 12pm is : ' + str(twelve_pm))
	print('The daily amount of deliveries at 1pm is : ' + str(one_pm))
	print('The daily amount of deliveries at 2pm is : ' + str(two_pm))
	print('The daily amount of deliveries at 3pm is : ' + str(three_pm))
	print('The daily amount of deliveries at 4pm is : ' + str(four_pm))
	print('The daily amount of deliveries at 5pm is : ' + str(five_pm))
	print('The daily amount of deliveries at 6pm is : ' + str(six_pm))
	print('You have ' + str(invalid_time) + ' invalid time(s) in your list.')


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
