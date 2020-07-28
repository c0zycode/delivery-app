import delivery

command = raw_input('Would you like to sort data (Y)?. Enter "Y" otherwise hit enter for more options. : ')

if command == 'Y':
	command = raw_input('Would you like to sort by date & time (Y)?. Enter "Y" otherwise hit enter for more options. : ')
	if command == 'Y':
		delivery.sort_times()
	else:
		command = raw_input('Would you like to sort by "location" or "medication"? : ')
		if command == 'location':
			delivery.sort_locations()
		else:
			delivery.sort_meds()
else:
	command = raw_input('Would you like to see by "grouped", "specific", "time", or "total" data? : ')
	if command == 'grouped':
		delivery.show_dates()
	elif command == 'specific':
		command = raw_input('Would you like to see by "day", "weekdays", "weekends", or "date"? : ')
		if command == 'day':
			try:
				command = raw_input('Which day would you like? (Ex. Monday) : ')
				delivery.day_lookup(command)
			except: 
				print("Invalid day. Please try again.")
		elif command == 'weekdays':
				delivery.show_weekdays()
		elif command == 'weekends':
				delivery.show_weekends()
		elif command == 'date':
			try:			
				command = raw_input('Enter the date using the following format "DD-MM-YY" : ')
				delivery.date_lookup(command)
			except:
				print("Invalid date. Please try again.")
		else:
			print("Invalid entry. Please try again.")
	elif command == 'time':
			delivery.daily_times()
	else:
		delivery.show_all()

