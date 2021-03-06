import tkinter as tk
import utils
import tkinter.messagebox
from tkinter import ttk
from collections import defaultdict
from tkinter import filedialog
import csv
from tkinter import messagebox
from collections import OrderedDict
import os
from datetime import datetime
# from fpdf import FPDF

class customer_detail:

	def __init__(self):
		
		self.entry_frame = tk.Frame()
		self.processed_CUSTOMER_DETAIL  = 0
		self.previous_app = utils.root_reference
		self.hold_details = []

		self.previous_app = utils.root_reference
		self.previous_orders_row_length = 0
	


	def showMsg(self,theMessage):
		tkinter.messagebox.showinfo("Info!",theMessage)
		return True

	def toDateObj(self,dates):
		date_objects = []
		date_obj = 0
		for date in dates:
			try:
				date_obj = 	datetime.strptime(date, '%d/%m/%Y %H:%M')
			except:
				date_obj = datetime.strptime(date, '%d-%m-%Y %H:%M:%S -%f')

			# print(date_obj.date())
			
			date_objects.append(date_obj.date())
		return date_objects
		
	def process_data(self):
		all_detail_dict = defaultdict(list)

		customer_name =  utils.raw_column_list['Shipping Name']
		purchase_dollar =utils.raw_column_list['LineItem Sale Price']
		order_qty = utils.raw_column_list['LineItem Qty']
		order_number =  utils.raw_column_list['Order #']
		customer_email = utils.raw_column_list['Email Address']
		purchase_date = self.toDateObj(utils.raw_column_list['Order Date and Time Stamp'])
		customer_country =  utils.raw_column_list['Shipping Country']
		customer_city = utils.raw_column_list['Shipping City']
		customer_address = utils.raw_column_list['Shipping Street Address']
		customer_phone = utils.raw_column_list['Shipping Phone']
		
		# print("customer name length: "+str(len(customer_name)))
		# print("customer order length: "+str(len(order_number)))
		# print("Length of date time:  "+str(len(date_time)))
		# print("example date time instance: "+str(date_time[0]))
				
		for i in range(len(customer_name)):		
			if customer_name[i] in all_detail_dict.keys():

				temp_list = all_detail_dict[customer_name[i]]
				m_orders = []
				m_orders = temp_list[4]	# pull out orders
				price = 0
				try:
					price = purchase_dollar[i]
					price = float(price)
				except:
					price = purchase_dollar[i][1:]

				order_total =  float(order_qty[i])*float(price)
				m_orders.append((order_number[i],order_total))  # append new order to orders
				
				total = temp_list[2]     # add money to total
				total = float(total) + float(order_total)
				all_detail_dict[customer_name[i]] = (customer_name[i], customer_email[i], total, purchase_date[i], m_orders, customer_country[i],customer_city[i],customer_address[i],customer_phone[i])

			else:
				order_total_f = 0
				try:
					order_total_f = purchase_dollar[i]
					order_total_f = float(order_total_f)
				except:
					order_total_f = purchase_dollar[i][1:]

				order_total_f = float(order_qty[i])*float(order_total_f)
				order = (order_number[i],order_total_f)
				orders = []
				orders.append(order)
				all_detail_dict[customer_name[i]] = ([customer_name[i], customer_email[i],order_total_f,purchase_date[i], orders,customer_country[i],customer_city[i],customer_address[i],customer_phone[i]])
	

		self.processed_CUSTOMER_DETAIL = all_detail_dict
		# print("--------------------------------")
		# print(self.processed_CUSTOMER_DETAIL['Jeff Starr'])
		# print("--------------------------------")

		# print("itself type: ")
		# print(type(self.processed_CUSTOMER_DETAIL))
		print("length is: ")
		print(str(len(self.processed_CUSTOMER_DETAIL)))
		# print("type at [0] type")
		# print(type(self.processed_CUSTOMER_DETAIL[0]))

		# for key, value  in all_detail_dict.items():
			# print(str(key)+" : "+str(value))


	def main_display(self):
		mHeight = 240
		mWidth=   900
		self.root = tk.Tk()
		self.root.resizable(width=False, height=False)
		self.root.title("Customer Lifetime Value Report")
		
		self.mainCanvas = tk.Canvas(self.root, width=mWidth, height=mHeight)
		self.mainCanvas.config(bg='#5DADE2')
		self.mainCanvas.pack()
		self.mainCanvas.create_text(400,20,fill='darkblue', font='Times 20 italic bold', text="Customer Lifetime Value Report")
		

	def selEMAIL(self):
		self.var.set(1)
		# print("you have selected "+str(self.var.get()))
		return str(self.var.get())
	
	def selNAME(self):
		self.var.set(2)
		# print("you have selected "+str(self.var.get()))
		return str(self.var.get())

	def handle_placeholder(self, event):
		print("im handling an even")


	def main_displaygrid(self):
		#scrolling shit -------start----------
		frame_main = tk.Frame(self.root, bg="gray")
		frame_main.pack()
		# frame_main.grid(sticky='news')
		
		self.frame_for_scroll = tk.Frame(frame_main, bg="#5DADE2", height=300, width=900)
		self.frame_for_scroll.grid(row=0, column=1, sticky='nw')
		self.frame_for_scroll.grid_rowconfigure(1,weight=1)
		self.frame_for_scroll.grid_columnconfigure(1, weight=1)
		self.frame_for_scroll.grid_propagate(False)

		
		self.canvas_for_scroll = tk.Canvas(self.frame_for_scroll, bg="lightgrey")
		# self.canvas_for_scroll.grid(row=1, column=1, sticky="news", padx=165) #ew
		self.canvas_for_scroll.grid(row=1, column=1, sticky="news", padx=5) #ew

		vertical_scrollbar =  tk.Scrollbar(self.frame_for_scroll, orient="vertical", command=self.canvas_for_scroll.yview)
		vertical_scrollbar.grid(row=1, column=2, sticky='ns')

		self.canvas_for_scroll.configure(yscrollcommand=vertical_scrollbar.set)
		#scrolling shit -------ENND----------

		rows = len(self.processed_CUSTOMER_DETAIL)
		columns = 2
		
		final_names = []
		name_price_list = []
		for key, value in self.processed_CUSTOMER_DETAIL.items():
			temp_list = []

			name_price_tuple = (key, int(value[2]))
			name_price_list.append(name_price_tuple)

			# final_names.append(str(key))
			# print(value[2])
		name_price_list.sort(key=lambda x:x[1], reverse=True)
		self.name_list = ['first name','name two','name customer']
		self.email_list = ['a@admin.com','c@cc.com','this@anemail.com']
		self.totals_list = [99, 100, 200]
		self.orders_list = [(10,123),(20, 789),(30, 456)]
		self.country_list = ['Itlay','France','Germany']
		self.city_list = ['Amsterdam','Den Haag','Rotterdam']
		self.address_list = ['One Address','Two Address','Three Address']
		self.phone_list = [123,456,789]


		combo_frame = tk.Frame(self.root, width=600, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,50), window=combo_frame, anchor='nw')

		select_label = tk.Label(combo_frame, text="Select One: ")
		select_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		select_label.grid(row=1, column=1, padx=(0,0), pady=0)

		self.combo_entry =  ttk.Combobox(combo_frame,width=20, values=name_price_list)
		self.combo_entry.grid(row=1, column=2, padx=(5,0),pady=0)

		resultBtn = tk.Button(combo_frame, font="Times 12 bold italic", text="Show Details", command=self.showdetailsCombo)
		# resultBtn = tk.Button(combo_frame, font="Times 12 bold italic", text="Show Details")
		resultBtn.configure(background='#5DADE2')
		resultBtn.configure(foreground='darkblue')
		resultBtn.grid(row=1, column=3, padx=(185,2),pady=0)


		export_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((770,90), window=export_frame, anchor='nw')
		exportBtn = tk.Button(export_frame, font="Times 12 bold italic", text="Export Data", command= self.exportDataToFile2)
		# exportBtn = tk.Button(export_frame, font="Times 12 bold italic", text="Export Data")
		exportBtn.configure(background='#5DADE2')
		exportBtn.configure(foreground='darkblue')
		exportBtn.grid(row=1, column=1, padx=0,pady=0)

		
		search_frame = tk.Frame(self.root, width=535, height=40, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)

		self.mainCanvas.create_window((170,95), window=search_frame, anchor='nw')

		""" Radio buttons start here """
		self.var = tk.IntVar()
		self.var.set(1)
		R1 =  tk.Radiobutton(search_frame,text="Email  ",  variable=self.var, value=1, command=self.selEMAIL)
		# R1 =  tk.Radiobutton(search_frame,text="Email",  variable=self.var, value=1)
		R1.configure(background='#5DADE2')
		R1.configure(foreground='darkblue')
		R1.grid(row=1, column=0, padx=0,pady=0)
		

		R2 =  tk.Radiobutton(search_frame,text="NAME ",  variable=self.var, value=2, command=self.selNAME)
		# R2 =  tk.Radiobutton(search_frame,text="Name ",  variable=self.var, value=2)
		R2.configure(background='#5DADE2')
		R2.configure(foreground='darkblue')
		R2.grid(row=2, column=0, padx=0,pady=0)

		""" Radio buttons end here """

		self.search_entry =tk.Entry(search_frame, font="Halvetica 10 bold", bd=2, width=25)
		self.search_entry.grid(row=1, column=1, padx=(30,0), pady=0)

	
		searchBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Search Term", command=lambda: self.showdetailsSearch(str(self.search_entry.get())))
		# searchBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Search & Populate")
		searchBtn.configure(background='#5DADE2')
		searchBtn.configure(foreground='darkblue')
		searchBtn.grid(row=1, column=2, padx=(153,2),pady=0)

		date_frame = tk.Frame(self.root, width=535, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,165), window=date_frame, anchor='nw')

		start_label = tk.Label(date_frame, text="Start date: ")
		start_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		start_label.grid(row=1, column=1, padx=5, pady=0)

		self.start_entry =tk.Entry(date_frame, font="Halvetica 10 bold", bd=2, width=15)
		self.start_entry.insert(0,'dd-mm-yyyy')
		self.start_entry.grid(row=1, column=2, padx=0, pady=0)
		self.start_entry.bind('<Button-1>',self.handle_placeholder)

		end_label = tk.Label(date_frame, text="End date: ")
		end_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		end_label.grid(row=1, column=3, padx=5, pady=0)

		self.end_entry =tk.Entry(date_frame, font="Halvetica 10 bold", bd=2, width=15)
		self.end_entry.insert(0,'dd-mm-yyyy')
		self.end_entry.grid(row=1, column=4, padx=0, pady=0)

		filterBtn = tk.Button(date_frame, font="Times 12 bold italic", text="Apply Filter", command=lambda: self.datefilter(str(self.start_entry.get()),str(self.end_entry.get())))
		# searchBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Search & Populate")
		filterBtn.configure(background='#5DADE2')
		filterBtn.configure(foreground='darkblue')
		filterBtn.grid(row=1, column=5, padx=(20,2),pady=0)



		label_frame = tk.Frame(self.root, width=900, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((10,210), window=label_frame, anchor='nw') #nw

		name_label = tk.Label(label_frame, text="Name")
		name_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		name_label.grid(row=1, column=1, padx=10,pady=0)

		email_label = tk.Label(label_frame, text="Email")
		email_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		email_label.grid(row=1, column=2, padx=(80,0),pady=0)

		total_label = tk.Label(label_frame, text="Total")
		total_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		total_label.grid(row=1, column=3, padx=(140,30),pady=0)

		orders_label = tk.Label(label_frame, text="Orders")
		orders_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		orders_label.grid(row=1, column=4, padx=(50,18),pady=0)

		address_label = tk.Label(label_frame, text="Phone")
		address_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		address_label.grid(row=1, column=5, padx=(40,18),pady=0)

		phone_label = tk.Label(label_frame, text="Address")
		phone_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		phone_label.grid(row=1, column=6, padx=(40,60),pady=0)
		
		


		back_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((20,90), window=back_frame, anchor='nw')
		backBtn = tk.Button(back_frame, font="Times 12 bold italic", text="Previous Module", command= self.gotoPreviousModule)
		# backBtn = tk.Button(back_frame, font="Times 12 bold italic", text="Previous Module")
		backBtn.configure(background='#5DADE2')
		backBtn.configure(foreground='darkblue')
		backBtn.grid(row=1, column=0, padx=0,pady=0)


		label_frame.update_idletasks()

		self.entry_frame = tk.Frame(self.canvas_for_scroll, width=900, height=20, bg="#5DADE2")
		self.canvas_for_scroll.create_window((0,0), window=self.entry_frame, anchor='nw')

		self.showComplete()

		self.mainCanvas.pack()
		# self.root.mainloop()

	# def labels_display(self):


	def datefilter(self, start, end):
		start_date  =  datetime.strptime(start,'%d-%m-%Y').date()
		end_date = datetime.strptime(end,'%d-%m-%Y').date()

		complete_list = []
		# for i in range(len(self.processed_CUSTOMER_DETAIL)):
		names_list = []
		emails_list = []
		totals_list = [] 
		orders_list = []
	
		complete_list = []

		for key, value in self.processed_CUSTOMER_DETAIL.items():
			temp_list = [value[0],value[1],value[2],value[4]]
			# print("date from dict: "+str(value[3])+" end date compare: "+str(value[3]))
			# print(value[3])
			if value[3] > start_date:
				if  value[3] < end_date:
					print("following match the condition")
					print(temp_list)
					complete_list.append(temp_list)

		if len(complete_list) < 1:
			self.showMsg("Sorry, no data found for given range.")

		temp_complete_list= sorted(complete_list, reverse=True, key=lambda x:x[2])	
		
		
		for i in range(len(temp_complete_list)):
			names_list.append(temp_complete_list[i][0])
			emails_list.append(temp_complete_list[i][1])
			totals_list.append(temp_complete_list[i][2])
			orders_list.append(temp_complete_list[i][3])

		print("total records found")
		print(str(len(names_list)))
	
		# self.display_complete(names_list,emails_list,totalss_list,orderss_list)
		self.hold_details.clear()
		new_list = []
		new_list.append(names_list)
		new_list.append(emails_list)
		new_list.append(totals_list)
		new_list.append(orders_list)
		self.hold_details = new_list
		self.displayEntries_modified(names_list,emails_list,totals_list,orders_list)

	



	def showComplete(self):
		complete_list = []
		# for i in range(len(self.processed_CUSTOMER_DETAIL)):
		names_list = []
		emails_list = []
		totalss_list = [] 
		orderss_list = []
		country_list = []
		city_list = []
		address_list = []
		phone_list = []
	
		complete_list = []

		for key, value in self.processed_CUSTOMER_DETAIL.items():
			temp_list = [value[0],value[1],value[2],value[4],value[5],value[6],value[7],value[8]]
			complete_list.append(temp_list)

		temp_complete_list= sorted(complete_list, reverse=True, key=lambda x:x[2])	
		
		for i in range(len(temp_complete_list)):
			names_list.append(temp_complete_list[i][0])
			emails_list.append(temp_complete_list[i][1])
			totalss_list.append(temp_complete_list[i][2])
			orderss_list.append(temp_complete_list[i][3])
			country_list.append(temp_complete_list[i][4])
			city_list.append(temp_complete_list[i][5])
			address_list.append(temp_complete_list[i][6])
			phone_list.append(temp_complete_list[i][7])


	
		# self.display_complete(names_list,emails_list,totalss_list,orderss_list)
		self.hold_details.clear()
		new_list = []
		new_list.append(names_list)
		new_list.append(emails_list)
		new_list.append(totalss_list)
		new_list.append(orderss_list)
		new_list.append(country_list)
		new_list.append(city_list)
		new_list.append(address_list)
		new_list.append(phone_list)
		self.hold_details = new_list
		self.displayEntries_modified(names_list,emails_list,totalss_list,orderss_list,country_list,city_list,address_list,phone_list)

	

	def showdetailsCombo(self):
		
		self.name_list.clear()
		self.email_list.clear()
		self.totals_list.clear()
		self.orders_list.clear()
		self.country_list.clear()
		self.city_list.clear()
		self.address_list.clear()
		self.phone_list.clear()

		my_tempList = []
		# self.hold_details.clear()
		
		# selected_name = str(self.combo_entry.get())
		selected_name = self.combo_entry.get()
		selected_name = selected_name.split('}')
		# selected_name = eval(selected_name)
		selected_name = selected_name[0][1:]
		print("selected name is: ")
		print(selected_name)
		# self.hold_details = self.processed_CUSTOMER_DETAIL[selected_name]
		my_tempList = self.processed_CUSTOMER_DETAIL[selected_name]
		self.name_list.append(my_tempList[0])
		self.email_list.append(my_tempList[1])
		self.totals_list.append(my_tempList[2])
		self.orders_list.append(my_tempList[4])	
		self.country_list.append(my_tempList[5])
		self.city_list.append(my_tempList[6])
		self.address_list.append(my_tempList[7])
		self.phone_list.append(my_tempList[8])
		
		self.displayEntries(self.name_list, self.email_list, self.totals_list, self.orders_list,self.country_list, self.city_list,self.address_list,self.phone_list)
	

	
	def showdetailsSearch(self,search_string):
		
		name = []
		email = []
		total = []
		orders = []
		country = []
		city = []
		address = []
		phone = []
		# self.hold_details = []
		found=False
		if int(self.var.get()) == 1:
			for key, value in self.processed_CUSTOMER_DETAIL.items():
				if search_string.lower() in value[1].lower():
					name.append(key)
					email.append(self.processed_CUSTOMER_DETAIL[key][1])
					total.append(self.processed_CUSTOMER_DETAIL[key][2])
					orders.append(self.processed_CUSTOMER_DETAIL[key][4])
					country.append(self.processed_CUSTOMER_DETAIL[key][5])
					city.append(self.processed_CUSTOMER_DETAIL[key][6])
					address.append(self.processed_CUSTOMER_DETAIL[key][7])
					phone.append(self.processed_CUSTOMER_DETAIL[key][8])
					self.displayEntries(name, email, total, orders, country,city,address,phone)
					found = True
					break
			
			if not found:
				self.showMsg("Sorry no matching record found for given query!")

		elif int(self.var.get()) ==2:
			for key, value in self.processed_CUSTOMER_DETAIL.items():
				if search_string.lower() in value[0].lower():
					name.append(key)
					email.append(self.processed_CUSTOMER_DETAIL[key][1])
					total.append(self.processed_CUSTOMER_DETAIL[key][2])
					orders.append(self.processed_CUSTOMER_DETAIL[key][4])
					country.append(self.processed_CUSTOMER_DETAIL[key][5])
					city.append(self.processed_CUSTOMER_DETAIL[key][6])
					address.append(self.processed_CUSTOMER_DETAIL[key][7])
					phone.append(self.processed_CUSTOMER_DETAIL[key][8])
					self.displayEntries(name, email, total, orders, country,city,address,phone)
					found = True
					break
			
			if not found:
				self.showMsg("Sorry no matching record found for given query!")

	
	
	def displayEntries_modified(self,name,email, total, orders_list, country_list,city_list,address_list,phone_list):
		for widget in self.entry_frame.winfo_children():
			widget.destroy()
		previous_length = 0
		innerFinished = True
		for i in range(len(name)):
			
			curr_row = i+2+previous_length # is constant for row, it will be there always

			name_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=20)
			name_variable = name[i]
			name_entry.insert(1,'%s'%name_variable)
			name_entry.grid(row=curr_row, column=1, padx=0,pady=0)
			name_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			email_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=27)
			email_variable = email[i]
			email_entry.insert(1,'%s'%email_variable)
			email_entry.grid(row=curr_row, column=2, padx=0,pady=0)
			email_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			total_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=7)
			total_variable = total[i]
			total_entry.insert(1,'%0.2f'%total_variable)
			total_entry.grid(row=curr_row, column=3, padx=0,pady=0)
			total_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			phone_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=10)
			phone_variable = phone_list[i]
			phone_entry.insert(1,'%s'%phone_variable)
			phone_entry.grid(row=curr_row, column=5, padx=0,pady=0)
			phone_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			address_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=100)
			# address_variable = country_list[i]+","+city_list[i]+","+address_list[i]
			address_variable = address_list[i]+","+city_list[i]+","+country_list[i]
			address_entry.insert(1,'%s'%address_variable)
			address_entry.grid(row=curr_row, column=6, padx=0,pady=0)
			address_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')


			for j in range(len(orders_list[i])):
				inner_row = curr_row+j
				# print("inner row: "+str(inner_row))
				orders_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=23)
				order_variable = orders_list[i][j]
				orders_entry.insert(1,'%s'%str(order_variable))
				orders_entry.grid(row=inner_row, column=4, padx=0,pady=0)
				orders_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			previous_length += len(orders_list[i])
		


		self.entry_frame.update_idletasks()
		self.frame_for_scroll.update_idletasks()	
		self.canvas_for_scroll.config(scrollregion=self.canvas_for_scroll.bbox("all"))





	
	def displayEntries(self,name_list,email_list, totals_list, orders_list,country_list,city_list,address_list,phone_list):
		for widget in self.entry_frame.winfo_children():
			widget.destroy()
		
		self.hold_details.clear()
		self.hold_details =[name_list[0], email_list[0], totals_list[0], orders_list[0], country_list[0],city_list[0],address_list[0],phone_list[0]]
		

		if 1==1:
			i = 0
			name_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=20)
			name_variable = name_list[i]
			name_entry.insert(1,'%s'%name_variable)
			name_entry.grid(row=i+2, column=1, padx=0,pady=0)
			name_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			email_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=27)
			email_variable = email_list[i]
			email_entry.insert(1,'%s'%email_variable)
			email_entry.grid(row=i+2, column=2, padx=0,pady=0)
			email_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')


			total_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=7)
			total_variable = totals_list[i]
			total_entry.insert(1,'%0.2f'%total_variable)
			total_entry.grid(row=i+2, column=3, padx=0,pady=0)
			total_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')


			phone_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=10)
			phone_variable = phone_list[i]
			phone_entry.insert(1,'%s'%phone_variable)
			phone_entry.grid(row=i+2, column=5, padx=0,pady=0)
			phone_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			address_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=100)
			# address_variable = country_list[i]+","+city_list[i]+","+address_list[i]
			address_variable = +address_list[i]+","+city_list[i]+","+country_list[i]
			address_entry.insert(1,'%s'%address_variable)
			address_entry.grid(row=i+2, column=6, padx=0,pady=0)
			address_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')



		for j in range(len(orders_list[0])):
			orders_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=23)
			order_variable = orders_list[0][j]
			orders_entry.insert(1,'%s'%str(order_variable))
			orders_entry.grid(row=j+2, column=4, padx=0,pady=0)
			orders_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

		self.entry_frame.update_idletasks()
		self.frame_for_scroll.update_idletasks()	
		self.canvas_for_scroll.config(scrollregion=self.canvas_for_scroll.bbox("all"))



	def showMsg(self,theMessage):
		tkinter.messagebox.showinfo("Info!",theMessage)


	def exportDataToFile(self):

		file = ''
		# try:
			# file = filedialog.asksaveasfile(mode='w', defaultextension=".pdf")
		file = filedialog.asksaveasfile(mode='w')
		filePath = file.name
		# except:
			# self.showMsg("Please close already opened  file or choose a different name for this file. Please try again!")
		if file is None:
			return
		

		# Create instance of FPDF class
		# Letter size paper, use inches as unit of measure
		pdf=FPDF(format='letter', unit='in')
		
		# Add new page. Without this you cannot create the document.
		pdf.add_page()
		
		# Remember to always put one of these at least once.
		pdf.set_font('Times','',10.0) 
		
		# Effective page width, or just epw
		epw = pdf.w - 2*pdf.l_margin
		
		# Set column width to 1/4 of effective page width to distribute content 
		# evenly across table and page
		col_width = epw/4
		
		# Since we do not need to draw lines anymore, there is no need to separate
		# headers from data matrix.

		data = [['customer name','customer email','total','orders']]
		for i in range(len(self.hold_details[3])):
			if i == 0:
				data.append([str(self.hold_details[0]),str(self.hold_details[1]),str(float("{:.2f}".format(self.hold_details[2]))),str(self.hold_details[3][i])])
			else:
				data.append([' ',' ',' ',str(self.hold_details[3][i])])

		
		# Document title centered, 'B'old, 14 pt
		pdf.set_font('Times','B',18.0) 
		pdf.cell(epw, 0.0, 'Customer Life Time Value Report', align='C')
		pdf.set_font('Times','',13.0) 
		pdf.ln(0.5)
		
		# Text height is the same as current font size
		th = pdf.font_size
		
		for row in data:
			for datum in row:
				# Enter data in colums
				# Notice the use of the function str to coerce any input to the 
				# string type. This is needed
				# since pyFPDF expects a string, not a number.
				pdf.cell(col_width, 3*th, str(datum), border=1)
		
			pdf.ln(3*th)
		
		# Line break equivalent to 4 lines
		pdf.ln(3*th)

		# save the pdf with name.pdf
		
		# pdf.output("C:\\Users\\sher\\Desktop\\fiverr_stuff\\Mapping_Problem\\\data_and_report\\module_output4\\samplepdf.pdf")
		pdf.output(str(filePath)+".pdf")


	def gotoPreviousModule(self):
		self.previous_app.deiconify()
		self.root.destroy()


	def exportDataToFile2(self):
		filename = 'Customer Value Report'
		fieldnames =["Customer Name","Email","Total", "Orders","Phone","Address"]
		try:
			with open(filename+'.csv','w', newline='') as file:
				writer =  csv.writer(file, lineterminator='\r')
				writer.writerow(fieldnames)
				for i in range(len(self.hold_details[0])):
					combine_list = []
					combine_list.append(self.hold_details[0][i])
					combine_list.append(self.hold_details[1][i])
					combine_list.append(self.hold_details[2][i])
					combine_list.append(self.hold_details[3][i])
					combine_list.append(self.hold_details[7][i])
					combine_list.append(self.hold_details[4][i]+","+self.hold_details[5][i]+","+self.hold_details[6][i])

					# string_row = "[\""+str(self.hold_details[0][i])+"\",\""+str(self.hold_details[1][i])+"\",\""+str(self.hold_details[2][i])+"\",\""+str(self.hold_details[3][i])+"\"]"
					string_row = [str(self.hold_details[0][i]),str(self.hold_details[1][i]),str(self.hold_details[2][i]),str(self.hold_details[3][i]),str(self.hold_details[7][i]),str(self.hold_details[4][i]+","+self.hold_details[5][i]+","+self.hold_details[6][i])]
					# try:
					writer.writerow(string_row)
					# except:
						# pass
		
			dir_path = os.path.dirname(os.path.realpath(__file__))
			self.showMsg("Customer Value Report has been saved at location: "+str(dir_path)+" in file: "+filename)
		except:
			self.showMsg("Please close already opened csv file or choose a different name for this file. Please try again!")

		
		# showMsg("a
		
		# with open('report.csv','w', newline='') as file:
	
	
	


	def printsimple(self):
		print("function is working..")


	def on_closing(self):
		if messagebox.askokcancel('Quit','Warning: By closing this screen, Program will exit completely!'):
			self.previous_app.destroy()
			self.root.destroy()



	def main(self):
		self.main_display()
		self.process_data()
		self.main_displaygrid()
		self.root.wm_protocol("WM_DELETE_WINDOW", lambda:self.on_closing())
		# report.main_display()
		# report.printsimple() 