from collections import defaultdict
import csv
import tkinter.filedialog
import traceback
import tkinter
import tkinter.messagebox
from datetime import datetime
import os

# class DataCheck:

# 	def __init__(self):
# 		print("This is data check for report.")


def hello():
	print("hello function")

def writeLog(errors):
	data = errors
	fieldnames =["Row Number or Column Name","Error Message"]
	currentTime = str(datetime.now())
	filename ='log_'+currentTime[0:10]+"_"+currentTime[11:13]+"."+currentTime[14:16]+"."+currentTime[17:19] 
	filename = 'GoDaddy Data Omissions'
	with open(filename+'.csv','w', newline='') as file:
	# with open('log_20_80_90.csv','w', newline='') as file:
		writer =  csv.writer(file, lineterminator='\r')
		writer.writerow(fieldnames)
		for line in data:
			try:
				writer.writerow(line)
			except:
				pass
	 
	dir_path = os.path.dirname(os.path.realpath(__file__))
	showMsg("Report Central has found: "+str(len(errors))+" errors in your data. To correct the data we have provided a log. all error's are being written into file named: "+filename)
	# showMsg("all error's are being written into file named: "+filename)
		

def readCSVFile():
	filepath = tkinter.filedialog.askopenfilename()
	# filepath = 'D:/Freelance_Business/fiverr_stuff/Mapping_Problem/data_and_report/data_test_file.csv'
	columns =  defaultdict(list)

	with open(filepath, encoding="utf-8-sig") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for row in csv_reader:
			for (k,v) in row.items():
				columns[k].append(v)
	return columns


def perform_data_check():
	columns =  defaultdict(list)
	columns = readCSVFile()

	# print("keys are")
	# print(columns.keys())
	

	''' Column Names '''
	sku_column = ''
	names_column = ''
	qty_column   = ''  
	price_column = ''  
	order_date_column = ''
	Errors = []
	
	order_column =  columns['Order #']
	if len(order_column) == 0:
		message = "Order # column is missing or has a problem it should be written as \"Order #\" and should have some data in that column, and please fix it!"
		single_error = ['Order #', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()


	sku_column = columns['LineItem SKU']
	if len(sku_column) == 0:
		message = "Line Item SKU column is missing or has a problem it should be written as \"LineItem SKU\" and should have some data in that column, and please fix it!"
		single_error = ['LineItem SKU', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()
	
	email_column = columns['Email Address']
	if len(email_column) == 0:
		message = "Email Address column is missing or has a problem it should be written as \"Email Address\" and should have some data in that column, and please fix it!"
		single_error = ['Email Address', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()
	
	c_name_column = columns['Shipping Name']
	if len(c_name_column) == 0:
		message = "Shipping Name column is missing or has a problem it should be written as \"Shipping Name\" and should have some data in that column, and please fix it!"
		single_error = ['Shipping Name', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()
		


	names_column = columns['LineItem Name']
	if len(names_column)==0:
		message = "Line Item NAME is missing or has a problem it should be written as \"LineItem Name\" and should have some data in that column, and please fix it!"
		single_error = ['LineItem Name', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()

	
	qty_column = columns['LineItem Qty']
	if len(qty_column) == 0:
		message = "Line Item QUANTITY is missing or has a problem it should be written as \"LineItem Qty\" and should have some data in that column, and please fix it!"
		single_error = ['LineItem Qty', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()	


	price_column = columns['LineItem Sale Price']
	if len(price_column) == 0:
		message = "Line Item sale price is missing or has a problem it should be written as \"LineItem Sale Price\" and should have some data in that column, and please fix it!" 
		single_error = ['LineItem Sale Price', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()	

	order_date_column = columns['Order Date and Time Stamp']
	if len(order_date_column) == 0:
		message = " Order Date and Time Stamp is missing or has a problem it should be written as \"Order Date and Time Stamp\" and should have some data in that column, and please fix it!"
		single_error = ['Order Date and Time Stamp', message]
		Errors.append(single_error)
		if showMsg(message):
			quit()	
	

	# ,columns['LineItem Name'],columns['LineItem Qty'],columns['LineItem Sale Price'],columns['Order Date and Time Stamp']

	for i in range(len(sku_column)):

		if len(sku_column[i]) == 0:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem SKU, SKU can not be null, please put a sku or delete specific row" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
		
			# print("Please fix it by making same data type as others look like, row above and below or delete specific row")
		if len(names_column[i]) == 0:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem Name, LineItem Name can not be null, please put a LineItem Name or delete specific row" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
		

		if len(qty_column[i]) == 0:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem Qty, LineItem Qty can not be null, please put a LineItem Qty or delete specific row" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
		
		try:
			int(qty_column[i])
		except:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem Qty, Please make sure that there is a digit at given location" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
	
		
		if len(price_column[i]) == 0:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem Sale Price, LineItem Sale Price can not be null, please put a LineItem Sale Price or delete specific row" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
	

		try:
			newprice = float(price_column[i][1:])
		except:
			message  ="problem at row No.: ", str(i+2)," and column: LineItem Sale Price, Please make sure its a price at given location like $8.22 something like that" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()


		if len(order_date_column[i]) == 0:
			message  ="problem at row No.: ", str(i+2)," and column: Order Date and Time Stamp, Order Date and Time Stamp can not be null, please put a Order Date and Time Stamp or delete specific row" 
			# if alertMessage(message):
			single_error = [str(i+2), message]
			Errors.append(single_error)
			# 	pass
			# else:
			# 	quit()
	
	writeLog(Errors)
	return columns


def alertMessage(stringMessage):
	msgBox = tkinter.messagebox.askquestion('Errors',str(stringMessage)+"do you want to skip it?",icon='warning')
	if msgBox == 'yes':
		return True
	else:
		return False


def showMsg(theMessage):
	tkinter.messagebox.showinfo("Info!",theMessage)
	return True





