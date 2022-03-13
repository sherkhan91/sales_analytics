import csv
import tkinter.filedialog
import  tkinter as tk
from collections import defaultdict
from operator import itemgetter
from datetime import datetime, timedelta
import datetime
from tkinter import DISABLED, filedialog
import tkinter.messagebox
import validate_data
import utils
import purchase_report
import customer_report
import item_report
import discount_report
from tkinter import messagebox
from tkinter import ttk




#screen_width=root.winfo_screenwidth()-100
#screen_height=root.winfo_screenheight()-100
# screen_height=200
# screen_width=900

class Report:


	def __init__(self,_root,_width,_height):
		# self.root = tk.Tk()
		reference_data = 0
		
		self.screen_width = _width
		self.screen_height = _height
		self.root = _root
		self.root.resizable(width=False, height=False)
		self.root.title("Report Central(TM)")


		# self.root.title("Dummy Analytics Report Work")
		self.myCanvas = tk.Canvas(root, width=_width, height=_height)
		self.myCanvas.config(bg='#5DADE2')
		self.myCanvas.pack()
		self.myCanvas.create_text(400,20, fill="darkblue", font="Times 20 italic bold", text="Report Central(TM)")
		self.all_in_one = []
		
		# utils.init()
		utils.root_reference = self.root
		
		#print("initialized")
	def extra_git_function(self):
		mylist = [0, 1, 1]
		x = all(mylist)
		for i in mylist:
			b= i*1

	def on_closing(self):
		if messagebox.askokcancel('Quit','Warning: By closing this screen, you can not do further processing.!'):
			self.root.destroy()

	def guessDate(self,date_string):
		date_obj = 0
		try:
			date_obj = datetime.datetime.strptime(date_string, '%d-%m-%Y %H:%M:%S -%f').date()
		except:
			date_obj =  datetime.datetime.strptime(date_string, '%d/%m/%Y %H:%M').date()
		return date_obj

	def format_dates(self,item_dict):
		item_dates = []
		splited_dates =[]
		for key in item_dict:
			item_dates.append(item_dict[key])
			splited_dates = []
		for i in range(len(item_dates)):
			date_string = item_dates[i][3]
			temp = date_string.split('*')
			splited_dates.append(temp)

		finilized_dates = []
		for i in range(len(splited_dates)):
			blist = []
			for j in range(len(splited_dates[i])):
				dates_only = self.guessDate(splited_dates[i][j])
				blist.append(dates_only)
			finilized_dates.append(blist)
		
		return finilized_dates

	def countdays(self,dates_from_data, last_date):
		# Qty_list, dates purchased, day count from last
		# nowdate = datetime.date.today()
		last_nowdate = last_date
		#month_old = nowdate - datetime.timedelta(days =30)
		sale_Qty = 0
		month_list = [last_nowdate - datetime.timedelta(days=x) for x in range(30)]
		# print("last day:",last_nowdate)
		for i in month_list:
			if i in dates_from_data:
				sale_Qty =  sale_Qty +1
			
		# print(sale_Qty)
		return sale_Qty

	def readCSVFile(self):
		filepath = tkinter.filedialog.askopenfilename()
		# filepath = 'D:/Freelance_Business/fiverr_stuff/Mapping_Problem/data_and_report/data_test_file.csv'
		#root.update()
		columns =  defaultdict(list)

		with open(filepath, encoding="utf8") as csv_file:
			csv_reader = csv.DictReader(csv_file, delimiter=',')
			for row in csv_reader:
				for (k,v) in row.items():
					columns[k].append(v)
		return columns

	def dateFilterUI(self):
		"""date filter 30, 90, 365 days or no filter"""
		filter_values = ['30', '90', '365', 'alltime']
		self.myCanvas.create_text(280,100, fill="darkblue", font="Times 13 bold italic", text="date range")
	
		self.filter_entry =  ttk.Combobox(width=15, values=filter_values, state="readonly")
		self.myCanvas.create_window(330,110, window=self.filter_entry, height=20, width=150, anchor=tk.SW)

		filterBtn = tk.Button(font="Times 12 bold italic", text="Filter", command=self.filterResults)
		filterBtn.configure(background='#5DADE2')
		filterBtn.configure(foreground='darkblue')
		self.myCanvas.create_window(490,110, window=filterBtn, height=20, width=100, anchor=tk.SW)
		

	def columnHeadings(self):
		# columns labels
		self.myCanvas.create_text(70,120,fill="darkblue",font="Times 13 bold italic", text="Item Name")
		self.myCanvas.create_text(280,120, fill="darkblue", font="Times 13 bold italic",text="Item SKU")
		self.myCanvas.create_text(400,120, fill="darkblue",font="Times 13 bold italic", text="Quantity")
		self.myCanvas.create_text(500,120, fill="darkblue",font="Times 13 bold italic", text="Avg Unit Price")
		self.myCanvas.create_text(580,120, fill="darkblue",font="Times 13 bold italic", text="Total")
		self.myCanvas.create_text(690,120, fill="darkblue", font="Times 13 bold italic", text="last month Qty")
		self.myCanvas.create_text(840,120, fill="darkblue", font="Times 13 bold italic", text="last month Dollar")

		self.dateFilterUI()
		

	def filterResults(self):
		selected_filter = self.filter_entry.get()
		if selected_filter == '30':
			self.filter30Days()
		elif selected_filter == '90':
			self.filter90Days()
		elif selected_filter == '365':
			self.filter365Days()
		else:
			print('reset to default all time')
		


	def sortQty(self):
		# all_in_one = self.getall()
		temp_all_in_one = self.all_in_one
		self.all_in_one= sorted(temp_all_in_one, reverse=True, key=lambda x:x[2])	
		self.displayGrid(self.all_in_one)
	
	def createEntryUI(self):
		#================= grid frame starts here================
		self.rootFrame  =  tk.Frame(self.root, width=900, height=200, bg="gray")
		self.rootFrame.pack()
		self.frame_main = tk.Frame(self.rootFrame, bg="gray")
		self.frame_main.grid(sticky='news')
		# Create a frame for the canvas with non-zero row&column weights
		self.frame_canvas = tk.Frame(self.frame_main)
		self.frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
		self.frame_canvas.grid_rowconfigure(0, weight=1)
		self.frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		self.frame_canvas.grid_propagate(False)
		# Add a canvas in that frame
		self.canvas = tk.Canvas(self.frame_canvas, bg="lightgrey")
		self.canvas.grid(row=0, column=0, sticky="news")
		# Link a scrollbar to the canvas
		self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
		self.vsb.grid(row=0, column=1, sticky='ns')
		self.canvas.configure(yscrollcommand=self.vsb.set)

		# Create a frame to contain the entries
		self.grid_frame = tk.Frame(self.canvas, bg="blue")
		self.canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')

		# # Create a frame to contain the entries
		# self.grid_frame = tk.Frame(self.canvas, bg="blue")
		# self.canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')
	
	def sel(self):
		print("you have selected "+str(self.var.get()))
		return str(self.var.get())

	def search(self):
		self.bottomCanvas.create_line(0,130,900,130)

		self.var = tk.IntVar()
		self.var.set(1)
		R1 =  tk.Radiobutton(text="SKU  ", variable=self.var, value=1, command=self.sel)
		R1.configure(background='#5DADE2')
		R1.configure(foreground='darkblue')
		R1.pack()
		self.bottomCanvas.create_window(180,155, window=R1, height=20, width=50, anchor=tk.SW)

		R2 =  tk.Radiobutton(text="Name", variable=self.var, value=2, command=self.sel)
		R2.configure(background='#5DADE2')
		R2.configure(foreground='darkblue')
		R2.pack()
		self.bottomCanvas.create_window(180,175, window=R2, height=20, width=50, anchor=tk.SW)

		self.SearchEntry=  tk.Entry()
		self.SearchEntry.insert(1,'search here')
		self.bottomCanvas.create_window(250,170, window=self.SearchEntry, height=30, width=180, anchor=tk.SW)

		searchButton = tk.Button(font="Times 12 bold italic", text="Search", command=self.searchQuery)
		searchButton.configure(background='#5DADE2')
		searchButton.configure(foreground='darkblue')
		self.bottomCanvas.create_window(450,170, window=searchButton, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)
		
		
		#================= bottom scroll and canvas plus frame starts here================
		# rootFrame1  =  tk.Frame(width=800, height=20, bg="blue")
		rootFrame1  =  tk.Frame( bg="blue")
		rootFrame1.pack(expand=True,fill=tk.BOTH) # grid(row=0, column=0)
		self.searchCanvas = tk.Canvas(rootFrame1,width=800,height=50, bg='lightgrey') 

		vbar = tk.Scrollbar(rootFrame1, orient=tk.VERTICAL)
		vbar.pack(side=tk.RIGHT, fill=tk.Y)
		vbar.config(command=self.searchCanvas.yview)
		self.searchCanvas.config(width=900,height=50)
		self.searchCanvas.config(yscrollcommand=vbar.set)
		# self.searchCanvas.pack(side=tk.RIGHT, expand=True,fill=tk.BOTH)
		self.searchCanvas.pack(side=tk.RIGHT, expand=True)
		self.searchCanvas.config(scrollregion=self.canvas.bbox("all"))

		self.bottomCanvas.create_window(452,220, window=rootFrame1, height=60, width=900)
		
	def searchQuery(self):
		all_lists = self.all_in_one
		# resultset  = [0,0,0,0,0,0,0]
		resultset  = []
		print("length of all", len(all_lists))
		searchvalue = self.SearchEntry.get()
		if len(searchvalue)==0:
			# print("its a blank space")
			resultset  = [0,0,0,0,0,0,0]
		self.SearchEntry.delete(0,'end')
		radioValue = self.sel()
		if radioValue == '1':
			print("im in here")
			for i in range(len(all_lists)):	
				if searchvalue.lower() in all_lists[i][0].lower():
					resultset.append(all_lists[i])
		elif radioValue == '2':
			for i in range(len(all_lists)):	
				if searchvalue.lower() in all_lists[i][1].lower():
					resultset.append(all_lists[i])
		
		
		resultEntryList = []
		entryFont = "Halvetica 10 bold"
	
		entryheight = 30
			
		for i in range(len(resultset)):
			print("tis come after")
			ResultEntry1 =  tk.Entry(font="Halvetica 10 bold")
			ResultEntry1.insert(1,'%s'%(str(resultset[i][1])))
			# ResultEntry1.insert(1,"One ")
			ResultEntry1.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(0,entryheight, window=ResultEntry1, height=30, width=220, anchor=tk.SW)
			resultEntryList.append(ResultEntry1)

			ResultEntry2=  tk.Entry(font=entryFont)
			ResultEntry2.insert(1,'%s'%(str(resultset[i][0])))
			# ResultEntry2.insert(1,"Two")
			ResultEntry2.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(221,entryheight, window=ResultEntry2, height=30, width=140, anchor=tk.SW)
			resultEntryList.append(ResultEntry2)

			ResultEntry3=  tk.Entry(font=entryFont)
			ResultEntry3.insert(1,'%s'%(str(resultset[i][2])))
			ResultEntry3.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(362,entryheight, window=ResultEntry3, height=30, width=90, anchor=tk.SW)
			resultEntryList.append(ResultEntry3)
		
			ResultEntry4=  tk.Entry(font=entryFont)
			ResultEntry4.insert(1,'%s'%(str(resultset[i][3])))
			ResultEntry4.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(452,entryheight, window=ResultEntry4, height=30, width=90, anchor=tk.SW)
			resultEntryList.append(ResultEntry4)

			ResultEntry5=  tk.Entry(font=entryFont)
			ResultEntry5.insert(1,'%s'%(str(resultset[i][4])))
			ResultEntry5.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(540,entryheight, window=ResultEntry5, height=30, width=90, anchor=tk.SW)
			resultEntryList.append(ResultEntry5)
		
			ResultEntry6=  tk.Entry(font=entryFont)
			ResultEntry6.insert(1,'%s'%(str(resultset[i][5])))
			ResultEntry6.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(631,entryheight, window=ResultEntry6, height=30, width=130, anchor=tk.SW)
			resultEntryList.append(ResultEntry6)
		
			ResultEntry7=  tk.Entry(font=entryFont)
			ResultEntry7.insert(1,'%s'%(str(resultset[i][6])))
			ResultEntry7.configure(state='disabled', disabledbackground='white', disabledforeground='black')
			self.searchCanvas.create_window(762,entryheight, window=ResultEntry7, height=30, width=120, anchor=tk.SW)
			resultEntryList.append(ResultEntry7)

			entryheight = entryheight+30

	
						
		
	
	


	

		# self.myCanvas.pack()
	
	def modules_menu(self):
		""" Menu to open purchase report """
		def openPurchaseModule():
			mReport  = purchase_report.purchase_detail()
			mReport.main()
			self.root.withdraw()
		
		""" Menu to open customer report """
		def openCustomerModule():
			cReport = customer_report.customer_detail()
			cReport.main()
			self.root.withdraw()

		""" Menu to open item report """

		def openItemModule():
			iReport = item_report.item_detail()
			iReport.main()
			self.root.withdraw()

			
		def openDiscountModule():
			dReport = discount_report.discount_detail()
			dReport.main()
			self.root.withdraw()

		menubar =  tk.Menu(self.root)
		moduleMenu = tk.Menu(menubar, tearoff=0)
		moduleMenu.add_command(label="Open Customer Detail Module", command=openCustomerModule )
		moduleMenu.add_command(label="Open Discount Detail Module", command=openDiscountModule )
		moduleMenu.add_command(label="Open Item Detail Module", command=openItemModule )
		moduleMenu.add_command(label="Open Purchase Detail Module", command=openPurchaseModule)
		menubar.add_cascade(label="Module Menu", menu=moduleMenu)
		self.root.config(menu=menubar)
		""" Menu bar closed here """



	""" Menu function call inside this function. """
	def ProcessInput(self):
		self.createEntryUI()
		columns =  defaultdict(list)
		columns = validate_data.perform_data_check()
		utils.init()
		utils.raw_column_list = columns


		""" Menubar stuff will go here """
		self.modules_menu()

		def get_current_qty(item_qty_array, i):
			currentQty = 0
			try:
				currentQty = int(item_qty_array[i])
			except:
				currentQty = 0
			return currentQty

		def price_to_float(item_price,i):
			floatPrice = 0.0
			try:
				floatPrice = float(item_price[i][1:])
			except:
				floatPrice = 0.0
			return floatPrice

		item_sku =   columns['LineItem SKU']
		item_names =   columns['LineItem Name']
		item_qty   =   columns['LineItem Qty']
		item_price =   columns['LineItem Sale Price']
		item_order_date = columns['Order Date and Time Stamp']

		item_dict = {}
		self.validatedCSV = [item_sku, item_names, item_qty, item_price, item_order_date] 

		for i in range(len(item_sku)):
			if item_sku[i] in item_dict:
				alist = item_dict.get(item_sku[i])
				date_list = []
				currentQty = get_current_qty(item_qty, i)
				savedQty = 0
				try:
					date_list =  item_order_date[i]
				except:
					date_list = list('01-10-0001')
				
				try:
					savedQty = int(alist[1])
				except:
					savedQty = 0
				
				floatPrice = price_to_float(item_price, i)
					# item_price = 
				# print("a list is: ", alist)
				# print("a list specific: ", alist[0],alist[1],item_qty[i],alist[2],alist[3] )
				previous_total = alist[4]
				total = previous_total+(currentQty*floatPrice)
				avg_price = (total/(savedQty+currentQty))
				item_dict[item_sku[i]] = [alist[0],savedQty+currentQty, avg_price ,alist[3]+"*"+date_list, total]
			else:
				floatPrice = 0.0
				try:
					currentQty = get_current_qty(item_qty, i)
					floatPrice = price_to_float(item_price, i)
					order_date = '01-10-0001'

					try:
						order_date = item_order_date[i]
					except:
						order_date = '01-10-0001'

					item_dict[item_sku[i]] = [str(""+item_names[i]),currentQty,float(item_price[i]),order_date, (float(currentQty)*floatPrice)]
				except:
					# print("one cycle:----------------------------------------------")
					# print(int(item_qty[i]))
					# print(float(item_price[i][1:]))
					# print(item_order_date[i])
					currentQty = 0
					floatPrice = price_to_float(item_price, i)
					order_date = '01-10-0001'
					try:
						currentQty = int(item_qty[i])
					except:
						currentQty = 0

					try:
						order_date = item_order_date[i]
					except:
						order_date = '01-10-0001'
					item_dict[item_sku[i]] = [str(""+item_names[i]),currentQty,floatPrice,order_date, (float(currentQty)*floatPrice)]
					# print([str(""+item_names[i]),int(item_qty[i]),float(item_price[i][1:]),item_order_date[i]])

		self.grid_height = len(item_dict)
		self.grid_width = 7

		sku_list = []
		item_list =  []
		qty_list = []
		unit_price_list = []
		sold_lastmonth_list = []
		total_price_list = []

		proper_dates = self.format_dates(item_dict)
		timestamps = self.format_dates(item_dict)
		timestamps.sort()
		
		last_date_from_report =  timestamps[len(timestamps)-1][0]
		print(f'last date from report: {last_date_from_report}')
		for l in range(len(proper_dates)):
			how_many =  self.countdays(proper_dates[l],last_date_from_report)
			sold_lastmonth_list.append(how_many)
		
		total_units_sold = []
		total_sales_dollar = []
		
		print_value = True

		for key in item_dict.keys():
			myList = item_dict[key]
			# if print_value:
			# 	print(key)
			# 	print("-------------------")
			# 	print(myList[4])
			# 	print_value = False
			
			sku_list.append(key)
			item_list.append(myList[0])
			qty_list.append(myList[1])
			unit_price_list.append(myList[2])
			total_price_list.append(myList[4])
			
			
			# print(f'Quantity: {myList[1]}, Unit price: {myList[2]}')
		# print(total_price_list)
		for total in qty_list:
			total_units_sold.append(total)

		entryList = []
		
		temp_list = []
		self.all_in_one =[]
		all_in_one_qty = []
		all_in_one_dollar = []
		all_in_one_lastmonth_qty = []
		all_in_one_lastmonth_dollar = []

		for i in range(self.grid_height):
			#print(item_list[i],qty_list[i],unit_price_list[i],float(qty_list[i])*float(unit_price_list[i]))
			temp_list = [sku_list[i],item_list[i],int(qty_list[i]),float(unit_price_list[i]),total_price_list[i],sold_lastmonth_list[i],(int(sold_lastmonth_list[i])*float(unit_price_list[i]))]
			self.all_in_one.append(temp_list)

		self.columnHeadings()
		initial_all_in_one = self.all_in_one
		self.displayGrid(initial_all_in_one)
		
			# after table to view the end buttons
		self.bottomCanvas = tk.Canvas(root, width=self.screen_width, height=250)
		self.bottomCanvas.config(bg='#5DADE2')
		self.bottomCanvas.pack()

		for i in range(len(self.all_in_one)):
			total_sales_dollar.append(int(self.all_in_one[i][2])*float(self.all_in_one[i][3]))
		self.final_total_units = 0
		self.final_total_dollar = 0
		for i in total_units_sold:
			self.final_total_units =  self.final_total_units+i
		for j in total_sales_dollar:
			self.final_total_dollar = self.final_total_dollar +j

		self.bottomButtons()
		self.displayGrid(initial_all_in_one)
		# 5 and 6, 5 for lastmonth Qty

		# self.search()

	def getall(self):
		return self.all_in_one

	def exportCSV(self):
		file = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
		if file is None:
			return
		data = self.all_in_one
		fieldnames =["Item SKU","Item Name","Quantity","Avg Unit Price","Total","last month Qty","last month Dollar"]
		# with open('report.csv','w', newline='') as file:
		writer =  csv.writer(file, lineterminator='\r')
		writer.writerow(fieldnames)
		for line in data:
			try:
				writer.writerow(line)
			except:
				pass
		

	def displayGrid(self,all_items_list):
		
		total_rows = self.grid_height
		total_columns =self.grid_width
		sku_list = []
		item_list =  []
		qty_list = []
		unit_price_list = []
		sold_lastmonth_qty = []
		total_sales_dollar = []
		totals_list = []

		for i in range(len(all_items_list)):
			sku_list.append(all_items_list[i][0])
			item_list.append(all_items_list[i][1])
			qty_list.append(all_items_list[i][2])
			unit_price_list.append(all_items_list[i][3])
			totals_list.append(all_items_list[i][4])
			sold_lastmonth_qty.append(all_items_list[i][5])
			total_sales_dollar.append(all_items_list[i][6])

		''' Destroying all previous entries from the grid frame so that we don't need to overwrite '''
		for widget in self.grid_frame.winfo_children():
			widget.destroy()
		for i in range(total_rows): # rows
			for j in range(total_columns): # columns
				if j==0:
					b = tk.Entry(self.grid_frame,font="Halvetica 10 bold", bd=2, width=30)
					# print("problematic: ",item_list[i])
					
					itemName =  item_list[i]
					try:
						b.insert(1,'%s'%(itemName))
						b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					except:
						itemName = 'Could not parse item name'
						b.insert(1,'%s'%(itemName))
						b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					
					# b.insert(1,'%s'%(itemName))
					# b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				elif j==1:
					b = tk.Entry(self.grid_frame, font="Halvetica 10 bold", bd=2, width=20)
					b.insert(1,'%s'%(sku_list[i]))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
					#b.configure(disabledbackground='LightGray', disabledforeground='black')
				elif j==2:
					b = tk.Entry(self.grid_frame,font="Halvetica 10 bold", bd=2, width=12)
					b.insert(1,'%s'%(qty_list[i]))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				elif j==3:
					b = tk.Entry(self.grid_frame, font="Halvetica 10 bold",bd=2, width=12)
					b.insert(1, '%0.2f'%(float(unit_price_list[i])))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				elif j==4:
					b = tk.Entry(self.grid_frame, font="Halvetica 10 bold", bd=2, width=12)
					# print()
					# number = 0
					b.insert(1,'%0.2f'%(totals_list[i]))
					# total_sales_dollar.append(int(qty_list[i])*float(unit_price_list[i]))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				elif j==5:
					b = tk.Entry(self.grid_frame, font="Halvetica 10 bold", bd=2, width=17)
					b.insert(1,'%s'%(str(sold_lastmonth_qty[i])))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				else:
					b = tk.Entry(self.grid_frame, font="Halvetica 10 bold", bd=2, width=20)
					b.insert(1,'%0.2f'%(float(total_sales_dollar[i])))
					b.configure(state='disabled', disabledbackground='white', disabledforeground='black')
					# entryList.append(b)
				b.grid(row=i, column=j, sticky='ns')

		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		# self.grid_frame.update_idletasks()
		self.frame_canvas.config(width=900 ,height=200)
		# Set the canvas scrolling region
		self.canvas.config(scrollregion=self.canvas.bbox("all"))
		# Launch the GUI			
		self.grid_frame.update_idletasks()
		
	def bottomButtons(self):

		self.search()

		dollar_sign = "$"
		self.bottomCanvas.create_text(150,30,fill="darkblue",font="Times 17 italic",text="Total units sold: "+str(self.final_total_units)+"   ")
		self.bottomCanvas.create_text(150,50,fill="darkblue",font="Times 17 italic",text="    Total sales dollar: %s %0.2f"%(dollar_sign,float(self.final_total_dollar)))
		
		
		exportBtn = tk.Button(font="Times 12 bold italic", text="Export to csv", command=self.exportCSV)
		exportBtn.configure(background='#5DADE2')
		exportBtn.configure(foreground='darkblue')
		self.bottomCanvas.create_window(500,40, window=exportBtn, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)

		closeButton2 = tk.Button(font= "Times 12 bold italic",text="Close Application", command=self.close_window)
		closeButton2.configure(background='#5DADE2')
		closeButton2.configure(foreground="red")
		self.bottomCanvas.create_window(700,40, window=closeButton2, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)
		

		sortQtyBtn = tk.Button(font="Times 12 bold italic", text="Sort by Quantity", command=self.sortQty)
		sortQtyBtn.configure(background='#5DADE2')
		sortQtyBtn.configure(foreground='darkblue')
		self.bottomCanvas.create_window(500,80, window=sortQtyBtn, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)

		sortQtyBtn = tk.Button(font="Times 12 bold italic", text="Sort by Dollar$", command=self.sortDollar)
		sortQtyBtn.configure(background='#5DADE2')
		sortQtyBtn.configure(foreground='darkblue')
		self.bottomCanvas.create_window(500,120, window=sortQtyBtn, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)

		lastmonthSortQtyBtn =  tk.Button(font="Times 12 bold italic", text="Sort Last Month Qty", command=self.sortLastMonthQty)
		lastmonthSortQtyBtn.configure(background='#5DADE2')
		lastmonthSortQtyBtn.configure(foreground='darkblue')
		self.bottomCanvas.create_window(700,80, window=lastmonthSortQtyBtn, height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)


		lastmonthSortDollarBtn =  tk.Button(font="Times 12 bold italic", text="Sort Last Month Dollar", command=self.sortLastMonthDollar)
		lastmonthSortDollarBtn.configure(background='#5DADE2')
		lastmonthSortDollarBtn.configure(foreground='darkblue')
		self.bottomCanvas.create_window(700,120, window=lastmonthSortDollarBtn , height=30, width=180, anchor=tk.SW)
		self.bottomCanvas.pack(side=tk.RIGHT)
		

	def close_window(self):
		root.destroy()

	def heading_buttons(self):
		# Buttons on top of the canvas
		
		fetchData =  tk.Button(font="Times 12 bold italic", text="Choose file and Process", command=self.ProcessInput)
		fetchData.configure(background='#5DADE2')
		fetchData.configure(foreground='darkblue')
		self.myCanvas.create_window(240,80, window=fetchData, height=30, width=180, anchor=tk.SW)
		self.myCanvas.create_text(445,65,font="Times 12 italic bold", text="OR")

		
		closeButton = tk.Button(font= "Times 12 bold italic",text="Cancel", command=self.close_window)
		closeButton.configure(background='#5DADE2')
		closeButton.configure(foreground='darkblue')
		self.myCanvas.create_window(470,80, window=closeButton, height=30, width=180, anchor=tk.SW)
		self.myCanvas.pack()
		
	def sortLastMonthQty(self):
		temp_all_in_one = self.all_in_one
		self.all_in_one = sorted(temp_all_in_one, reverse=True, key=lambda x:x[5])
		self.displayGrid(self.all_in_one)

	def sortLastMonthDollar(self):
		temp_all_in_one = self.all_in_one
		self.all_in_one= sorted(temp_all_in_one, reverse=True, key=lambda x:x[6])	
		self.displayGrid(self.all_in_one)

	def sortDollar(self):
		temp_all_in_one = self.all_in_one
		self.all_in_one= sorted(temp_all_in_one, reverse=True, key=lambda x:x[4])	
		self.displayGrid(self.all_in_one)

	def return_filtered_column(self, days):
		raw_columns = self.validatedCSV
		item_sku =   raw_columns[0]
		item_names =   raw_columns[1]
		item_qty   =   raw_columns[2]
		item_price =   raw_columns[3]
		item_order_date = raw_columns[4]

		filter_sku =   []
		filter_names =   []
		filter_qty   =   []
		filter_price =   []

		formatted_dates = [] 
		for raw_date in item_order_date:
			formatted_dates.append(self.guessDate(raw_date))
		
		formatted_dates.sort()
		last_sale_date = formatted_dates[len(formatted_dates)-1]
		break_date = last_sale_date+timedelta(days=days)

		for sku,name,qty,price, fdate in zip(item_sku, item_names, item_qty, item_price, formatted_dates):
			if  last_sale_date <= fdate <=break_date:
				filter_sku.append(sku)
				filter_names.append(name)
				filter_qty.append(qty)
				filter_price.append(price)

		return [filter_sku, filter_names, filter_qty, filter_price]

	def filter30Days(self):
		print('only 30 days')
		filtered_list = self.return_filtered_column(30)
		skus = filtered_list[0]
		names = filtered_list[1]
		qtys = filtered_list[2]
		prices = filtered_list[3]

		processed_sku = []
		processed_names = []
		processed_qtys = []
		processed_prices = []
		

	
	def filter90Days(self):
		print('only 90 days')
		

	def filter365Days(self):
		print('only 365 days')
		


if __name__ == "__main__":
	'''Process Input file must be called in starting to settle down everything '''
	root = tk.Tk()
	saleReport = Report(root,900,130)
	saleReport.heading_buttons()
	# saleReport.bottomButtons()
	
	root.wm_protocol("WM_DELETE_WINDOW", lambda: saleReport.on_closing())
	root.mainloop()
	

