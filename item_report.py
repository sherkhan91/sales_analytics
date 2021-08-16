from operator import le
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

class item_detail:

	def __init__(self):
		print("I'm the purchase report!")
			# print(root_reference)
		# utils.init()
		self.previous_app = utils.root_reference

		# print(previous_app)
		self.entry_frame = tk.Frame()
		self.processed_SKU_NAME  = []
		self.hold_details = []
		# print("hello, I'm the item report")
		
	
		
	def process_data(self):
		detail_dict  = defaultdict(list)
		name_detail_dict =  defaultdict(list)
		sku_detail_dict = defaultdict(list)
		check_temp_list = []
		item_sku =  utils.raw_column_list['LineItem SKU']
		item_name = utils.raw_column_list['LineItem Name']
		purchase_qty = utils.raw_column_list['LineItem Qty']
		customer_email = utils.raw_column_list['Email Address']
		customer_name =  utils.raw_column_list['Shipping Name']
		customer_country =  utils.raw_column_list['Shipping Country']
		customer_city = utils.raw_column_list['Shipping City']
		customer_address = utils.raw_column_list['Shipping Street Address']
		customer_phone = utils.raw_column_list['Shipping Phone']
		
		for i in range(len(item_sku)):
			if item_sku[i] in sku_detail_dict:
				
				sku_temp_list = sku_detail_dict[item_sku[i]]
				current_list = [customer_name[i],customer_email[i],purchase_qty[i],customer_country[i],customer_city[i],customer_address[i],customer_phone[i]]
				# print("process temp list is:")
				# print(sku_temp_list)
				# print("--------------------")
				found = False
				for temp_item_list in sku_temp_list:
					# print("temp list: "+str(temp_item_list))
					# print(str(customer_email[i]+"  :  "+str(temp_item_list[1])))
					compare_email = 0
					try:
						compare_email = temp_item_list[1]
					except:
						compare_email  = 'compare'

					if customer_email[i] == compare_email:
						qty = int(temp_item_list[2])+int(purchase_qty[i])
						sku_detail_dict[item_sku[i]] = [customer_name[i], customer_email[i], qty,customer_country[i],customer_city[i],customer_address[i],customer_phone[i]]
						name_detail_dict[item_name[i]] = [customer_name[i], customer_email[i], qty, customer_country[i],customer_city[i],customer_address[i],customer_phone[i]]
						found = True
				
				if found == False:
					sku_detail_dict[item_sku[i]].append(current_list)
					name_detail_dict[item_name[i]].append(current_list)
			
			else:
				sku_detail_dict[item_sku[i]] = []
				# current_list = 
				sku_detail_dict[item_sku[i]].append([customer_name[i], customer_email[i],purchase_qty[i],customer_country[i],customer_city[i],customer_address[i],customer_phone[i]])
				name_detail_dict[item_name[i]] = []
				name_detail_dict[item_name[i]].append([customer_name[i], customer_email[i], purchase_qty[i], customer_country[i],customer_city[i],customer_address[i],customer_phone[i]])
	
		self.processed_SKU_NAME = [sku_detail_dict, name_detail_dict]
		
		# for key, value  in sku_detail_dict.items():
		# 	if key == 'MDL-195-FAT-BOY':
		# 		print(str(key)+" : "+str(value))
		# for key, value  in name_detail_dict.items():
			# print(str(key)+" : "+str(value))


	def showMsg(self,theMessage):
		tkinter.messagebox.showinfo("Info!",theMessage)
		return True

	
	def main_display(self):
		
		mHeight = 190
		mWidth=   900
		self.root = tk.Tk()
		self.root.resizable(width=False, height=False)
		self.root.title("Purchase details of individual product")
		
		self.mainCanvas = tk.Canvas(self.root, width=mWidth, height=mHeight)
		self.mainCanvas.config(bg='#5DADE2')
		self.mainCanvas.pack()
		self.mainCanvas.create_text(400,20,fill='darkblue', font='Times 20 italic bold', text="Purchase detail of individual product")
		



	
	def search_frame_display(self):
			
		""" SEARCH frame starts from here """
		search_frame = tk.Frame(self.root, width=535, height=40, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,95), window=search_frame, anchor='nw')

		""" Radio buttons start here """
		# self.var = tk.IntVar()
		# self.var.set(1)
		# R1 =  tk.Radiobutton(search_frame,text="SKU  ",  variable=self.var, value=1, command=self.selSKU)
		# R1.configure(background='#5DADE2')
		# R1.configure(foreground='darkblue')
		# R1.grid(row=1, column=0, padx=0,pady=0)
		
		# R2 =  tk.Radiobutton(search_frame,text="NAME ",  variable=self.var, value=2, command=self.selNAME)
		# R2.configure(background='#5DADE2')
		# R2.configure(foreground='darkblue')
		# R2.grid(row=2, column=0, padx=0,pady=0)

		""" Radio buttons end here """

		search_guide_label = tk.Label(search_frame, text="Please write product SKU or product name")
		search_guide_label.config(font=("Times 13 italic"), fg=("darkblue"), bg=("#5DADE2"))
		search_guide_label.grid(row=1, column=1, padx=5,pady=0)

		self.search_entry =tk.Entry(search_frame, font="Halvetica 10 bold", bd=2, width=25)
		self.search_entry.grid(row=2, column=1, padx=5, pady=0)

	
		searchBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Search & Populate", command=lambda: self.showdetailsSearch(str(self.search_entry.get())))
		searchBtn.configure(background='#5DADE2')
		searchBtn.configure(foreground='darkblue')
		searchBtn.grid(row=2, column=2, padx=3,pady=0)

		""" SEARCH frame ends here """
	
	def main_displaygrid(self):
		#scrolling shit -------start----------
		frame_main = tk.Frame(self.root, bg="gray")
		frame_main.pack()
		# frame_main.grid(sticky='news')
		
		self.frame_for_scroll = tk.Frame(frame_main, bg="#5DADE2", height=300, width=900)
		self.frame_for_scroll.grid(row=0, column=1, sticky='we')
		self.frame_for_scroll.grid_rowconfigure(1,weight=1)
		self.frame_for_scroll.grid_columnconfigure(1, weight=1)
		self.frame_for_scroll.grid_propagate(False)

		
		self.canvas_for_scroll = tk.Canvas(self.frame_for_scroll, bg="lightgrey")
		self.canvas_for_scroll.grid(row=1, column=1, sticky="news", padx=15) #ew

		vertical_scrollbar =  tk.Scrollbar(self.frame_for_scroll, orient="vertical", command=self.canvas_for_scroll.yview)
		vertical_scrollbar.grid(row=1, column=2, sticky='ns')

		self.canvas_for_scroll.configure(yscrollcommand=vertical_scrollbar.set)
		#scrolling shit -------ENND----------
		rows = len(self.processed_SKU_NAME[0])
		columns = 2
		
		final_items = []
		for key, value in self.processed_SKU_NAME[0].items():
			final_items.append(key)
			
		self.name_list = ['first name','name two','name customer']
		self.email_list = ['a@admin.com','c@cc.com','this@anemail.com']
		self.qty_list = [7,3,5]
		self.country_list = ['Itlay','France','Germany']
		self.city_list = ['Amsterdam','Den Haag','Rotterdam']
		self.address_list = ['One Address','Two Address','Three Address']
		self.phone_list = [123,456,789]


		search_frame = tk.Frame(self.root, width=600, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,60), window=search_frame, anchor='nw')
		
		select_label  = tk.Label(search_frame, text="Enter SKU: ")
		select_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		select_label.grid(row=1, column=0, padx=0, pady=0)

		self.sku_entry =  tk.Entry(search_frame,width=22)
		self.sku_entry.grid(row=1, column=1, padx=0,pady=0)

		product_label  = tk.Label(search_frame, text="Enter Product Name: ")
		product_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		product_label.grid(row=1, column=2, padx=5, pady=0)

		self.name_entry =  tk.Entry(search_frame,width=22)
		self.name_entry.grid(row=1, column=3, padx=5,pady=0)

		resultBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Show Details", command=self.showdetails)
		resultBtn.configure(background='#5DADE2')
		resultBtn.configure(foreground='darkblue')
		resultBtn.grid(row=2, column=3, padx=0,pady=5)

		clearBtn = tk.Button(search_frame, font="Times 12 bold italic", text="Clear Search", command=self.clearEntries)
		clearBtn.configure(background='#5DADE2')
		clearBtn.configure(foreground='darkblue')
		clearBtn.grid(row=2, column=2, padx=10,pady=5)


		back_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((20,90), window=back_frame, anchor='nw')
		backBtn = tk.Button(back_frame, font="Times 12 bold italic", text="Previous Module", command= self.gotoPreviousModule)
		backBtn.configure(background='#5DADE2')
		backBtn.configure(foreground='darkblue')
		backBtn.grid(row=1, column=0, padx=0,pady=0)



		export_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((770,90), window=export_frame, anchor='nw')
		exportBtn = tk.Button(export_frame, font="Times 12 bold italic", text="Export Data", command= self.exportDataToFile2)
		exportBtn.configure(background='#5DADE2')
		exportBtn.configure(foreground='darkblue')
		exportBtn.grid(row=1, column=1, padx=0,pady=0)

		
		# self.search_frame_display()



	
		label_frame = tk.Frame(self.root, width=900, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((20,160), window=label_frame, anchor='nw') #nw

		name_label = tk.Label(label_frame, text="Name")
		name_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		name_label.grid(row=1, column=1, padx=20,pady=0)

		email_label = tk.Label(label_frame, text="Email")
		email_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		email_label.grid(row=1, column=2, padx=115,pady=0)

		units_label = tk.Label(label_frame, text="Qty")
		units_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		units_label.grid(row=1, column=3, padx=28,pady=0)

		address_label = tk.Label(label_frame, text="Address")
		address_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		address_label.grid(row=1, column=4, padx=50,pady=0)

		phone_label = tk.Label(label_frame, text="Phone")
		phone_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		phone_label.grid(row=1, column=5, padx=100,pady=0)
		
		
		# self.showall()	


		label_frame.update_idletasks()

		self.entry_frame = tk.Frame(self.canvas_for_scroll, width=800, height=20, bg="#5DADE2")
		self.canvas_for_scroll.create_window((10,0), window=self.entry_frame, anchor='nw')


		self.mainCanvas.pack()
		# self.root.mainloop()

	def clearEntries(self):
		self.sku_entry.delete(0,'end')
		self.name_entry.delete(0,'end')
	
	def showall(self):
		self.name_list.clear()
		self.email_list.clear()
		self.qty_list.clear()
		self.country_list.clear()
		self.city_list.clear()
		self.address_list.clear()
		self.phone_list.clear()
		my_tempList = []
		self.hold_details.clear()
		self.process_data()

		# self.hold_details = self.processed_SKU_NAME[0]
		# my_tempList = self.processed_SKU_NAME[0]
		for key,value in self.processed_SKU_NAME[0].items():
			my_tempList.append(value)
			self.hold_details.append(value)



		if type(my_tempList[0])==list:
			for i in range(len(my_tempList)):
				self.name_list.append(my_tempList[i][0])
				self.email_list.append(my_tempList[i][1])
				self.qty_list.append(my_tempList[i][2])
				self.country_list.append(my_tempList[i][3])
				self.city_list.append(my_tempList[i][4])
				self.address_list.append(my_tempList[i][5])
				self.phone_list.append(my_tempList[i][6])
		else:
			# for i in range(len(my_tempList)):
			self.name_list.append(my_tempList[0])
			self.email_list.append(my_tempList[1])
			self.qty_list.append(my_tempList[2])
			self.country_list.append(my_tempList[3])
			self.city_list.append(my_tempList[4])
			self.address_list.append(my_tempList[5])
			self.phone_list.append(my_tempList[6])
	

		self.displayEntries(self.name_list,self.email_list, self.qty_list, self.country_list,self.city_list,self.address_list,self.phone_list)
		

	def showdetails(self):
		
		self.name_list.clear()
		self.email_list.clear()
		self.qty_list.clear()
		self.country_list.clear()
		self.city_list.clear()
		self.address_list.clear()
		self.phone_list.clear()
		my_tempList = []
		self.hold_details.clear()
		self.process_data()
		
		search_SKU = str(self.sku_entry.get())
		search_NAME = str(self.name_entry.get())

		product_SKU = 0
		product_NAME = 0
		
		if len(search_SKU)==0 and len(search_NAME)==0:
			self.showMsg("Please write SKU or item name to search.")

		if len(search_SKU)>0:
			match = False
			for key,value in self.processed_SKU_NAME[0].items():
				if search_SKU.lower() in key.lower():
					product_SKU = key
					match = True
					break
			if match:
				var = product_SKU
				self.sku_entry.delete(0,'end')
				self.sku_entry.insert(1,'%s'%var)
				self.hold_details = self.processed_SKU_NAME[0][product_SKU]
				my_tempList = self.processed_SKU_NAME[0][product_SKU]
				# print("current temp list:")
				# print(my_tempList)
				# print("=================")
			else:
				self.showMsg("Sorry, provided SKU does not match with available SKU's.")
		else:	
			match = False
			for key,value in self.processed_SKU_NAME[1].items():
				if search_NAME.lower() in key.lower():
					product_NAME = key
					match = True
					break
			if match:
				var = product_NAME
				self.name_entry.delete(0,'end')
				self.name_entry.insert(1,'%s'%var)
				self.hold_details = self.processed_SKU_NAME[1][product_NAME]
				my_tempList = self.processed_SKU_NAME[1][product_NAME]
				# print("current temp list:")
				# print(my_tempList)
				# print("=================")
			else:
				self.showMsg("Sorry, provided NAME does not match with available product Names.")
			self.hold_details = self.processed_SKU_NAME[1][product_NAME]
			my_tempList = self.processed_SKU_NAME[1][product_NAME]

		
		
		if type(my_tempList[0])==list:
			for i in range(len(my_tempList)):
				self.name_list.append(my_tempList[i][0])
				self.email_list.append(my_tempList[i][1])
				self.qty_list.append(my_tempList[i][2])
				self.country_list.append(my_tempList[i][3])
				self.city_list.append(my_tempList[i][4])
				self.address_list.append(my_tempList[i][5])
				self.phone_list.append(my_tempList[i][6])
		else:
			# for i in range(len(my_tempList)):
			self.name_list.append(my_tempList[0])
			self.email_list.append(my_tempList[1])
			self.qty_list.append(my_tempList[2])
			self.country_list.append(my_tempList[3])
			self.city_list.append(my_tempList[4])
			self.address_list.append(my_tempList[5])
			self.phone_list.append(my_tempList[6])
	
		sort_list = []
		for i in range(len(self.name_list)):
			temp_list = [self.name_list[i], self.email_list[i], self.qty_list[i],self.country_list[i],self.city_list[i],self.address_list[i],self.phone_list[i]]
			sort_list.append(temp_list)
			# sort_list.append(self.email_list[i])
			# sort_list.append(self.qty_list[i])
		sort_list.sort(key=lambda x:x[2], reverse=True)
		self.name_list.clear()
		self.email_list.clear()
		self.qty_list.clear()
		self.country_list.clear()
		self.city_list.clear()
		self.address_list.clear()
		self.phone_list.clear()

		for i in range(len(sort_list)):
			self.name_list.append(sort_list[i][0])
			self.email_list.append(sort_list[i][1])
			self.qty_list.append(sort_list[i][2])
			self.country_list.append(my_tempList[i][3])
			self.city_list.append(my_tempList[i][4])
			self.address_list.append(my_tempList[i][5])
			self.phone_list.append(my_tempList[i][6])

		self.hold_details.clear()
		self.hold_details = sort_list
		self.displayEntries(self.name_list,self.email_list, self.qty_list,self.country_list,self.city_list,self.address_list,self.phone_list)


	def displayEntries(self,name_list,email_list, qty_list,country_list,city_list,address_list,phone_list):
		for widget in self.entry_frame.winfo_children():
			widget.destroy()

		for i in range(len(email_list)):
			name_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=18)
			name_variable = name_list[i]
			name_entry.insert(1,'%s'%name_variable)
			name_entry.grid(row=i+2, column=1, padx=0,pady=0)
			name_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			email_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=35)
			email_variable = email_list[i]
			email_entry.insert(1,'%s'%email_variable)
			email_entry.grid(row=i+2, column=2, padx=0,pady=0)
			email_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			qty_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=5)
			qty_variable = qty_list[i]
			qty_entry.insert(1,'%s'%qty_variable)
			qty_entry.grid(row=i+2, column=3, padx=0,pady=0)
			qty_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			country_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=10)
			country_variable = str(country_list[i])
			country_entry.insert(1,'%s'%country_variable)
			country_entry.grid(row=i+2, column=4, padx=0,pady=0)
			country_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			city_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=10)
			city_variable = str(city_list[i])
			city_entry.insert(1,'%s'%city_variable)
			city_entry.grid(row=i+2, column=5, padx=0,pady=0)
			city_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			address_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=20)
			address_variable = str(address_list[i])
			address_entry.insert(1,'%s'%address_variable)
			address_entry.grid(row=i+2, column=6, padx=0,pady=0)
			address_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			phone_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=17)
			phone_variable = str(phone_list[i])
			phone_entry.insert(1,'%s'%phone_variable)
			phone_entry.grid(row=i+2, column=7, padx=0,pady=0)
			phone_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

		self.entry_frame.update_idletasks()
		self.frame_for_scroll.update_idletasks()	
		self.canvas_for_scroll.config(scrollregion=self.canvas_for_scroll.bbox("all"))






	
	def exportDataToFile2(self):
		filename = 'Item Purchase Report'
		fieldnames =["Customer Name","Email","Num of units","Country","State","Address","Phone"]
	
		with open(filename+'.csv','w', newline='') as file:
			writer =  csv.writer(file, lineterminator='\r')
			writer.writerow(fieldnames)
			if type(self.hold_details[0])==list:
				for i in range(len(self.hold_details)):
					string_row = [str(self.hold_details[i][0]),str(self.hold_details[i][1]),str(self.hold_details[i][2]),str(self.hold_details[i][3]),str(self.hold_details[i][4]),str(self.hold_details[i][5]),str(self.hold_details[i][6])]
					writer.writerow(string_row)
			else:
				for i in range(1):
					string_row = [str(self.hold_details[0]),str(self.hold_details[1]),str(self.hold_details[2]),str(self.hold_details[3]),str(self.hold_details[4]),str(self.hold_details[5]),str(self.hold_details[6])]
					writer.writerow(string_row)

		
		# except:
		# 	self.showMsg("Please close already opened csv file or choose a different name for this file. Please try again!")

		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.showMsg("Item Purchase Report has been saved at location: "+str(dir_path)+" in file: "+filename)


	def gotoPreviousModule(self):
		self.previous_app.deiconify()
		self.root.destroy()

	def on_closing(self):
		if messagebox.askokcancel('Quit','Warning: By closing this screen, Program will exit completely!'):
			self.previous_app.destroy()
			self.root.destroy()

	def main(self):
		self.process_data()
		self.main_display()
		self.main_displaygrid()
		self.root.wm_protocol("WM_DELETE_WINDOW", lambda:self.on_closing())