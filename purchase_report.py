# from ttkwidgets.autocomplete import AutocompleteCombobox
from operator import mod
from os import environ, path
import tkinter as tk
import utils
import tkinter.messagebox
from tkinter import ttk
from collections import defaultdict
from tkinter import filedialog
import csv
import main_report
from tkinter import messagebox
import random
# from report_main import report_main.root_reference
# utils.raw_column_list.append("hello")

class purchase_detail:

	def __init__(self):
		# utils.init()
		
		self.previous_app = utils.root_reference

		
		self.entry_frame = tk.Frame()
		self.processed_SKU_NAME  = []
		self.hold_details = []
		
	def process_data(self):
		detail_dict  = defaultdict(list)
		name_detail_dict =  defaultdict(list)
		all_detail_dict = defaultdict(list)
		check_temp_list = []
		item_sku =  utils.raw_column_list['LineItem SKU']
		item_name = utils.raw_column_list['LineItem Name']
		purchase_qty = utils.raw_column_list['LineItem Qty']
		purchase_dollar =utils.raw_column_list['Subtotal']
		customer_email = utils.raw_column_list['Email Address']
		customer_name =  utils.raw_column_list['Shipping Name']
		customer_country =  utils.raw_column_list['Shipping Country']
		customer_city = utils.raw_column_list['Shipping City']
		customer_address = utils.raw_column_list['Shipping Street Address']
		customer_phone = utils.raw_column_list['Shipping Phone']
		
		for i in range(len(item_sku)):
			if item_sku[i] in detail_dict:
				check_temp_list = detail_dict[item_sku[i]]
				check_temp_list2 = all_detail_dict[item_sku[i]]

				if [customer_name[i], customer_email[i]] in check_temp_list:
					my_temp = []
					my_temp = all_detail_dict[item_sku[i]]
					c_name = my_temp[0][0]
					c_email = my_temp[0][1]
					c_qty = int(my_temp[0][2])
					c_money = 0
					try:
						c_money = float(my_temp[0][3])
					except:
						c_money = float(my_temp[0][3][1:])
					
					try:
						c_money = c_money+ float(purchase_dollar[i])
					except:
						c_money =  c_money+float(purchase_dollar[i][1:])
					c_qty = c_qty + int(purchase_qty[i])
					c_country = customer_country[i]
					c_city = customer_city[i]
					c_add = customer_address[i]
					c_phone = customer_phone[i]

					all_detail_dict[item_sku[i]] = [c_name,c_email,c_qty, c_money,c_country, c_city, c_add, c_phone]
					#---------------------after modification requested--------------------
					sku_temp_list = detail_dict[item_sku[i]]
					name_temp_list = name_detail_dict[item_name[i]]
					detail_dict[item_sku[i]] = [c_name,c_email,c_qty,c_country, c_city, c_add,c_phone]
					name_detail_dict[item_name[i]] = [c_name,c_email,c_qty,c_country, c_city, c_add, c_phone]


				else:
				
					dollar = 0
					qty = 0
					try:
						dollar = float(purchase_dollar[i])
					except:
						dollar = float(purchase_dollar[i][1:])
					qty = int(purchase_qty[i])

					mList = [customer_name[i],customer_email[i],qty, customer_country[i], customer_city[i], customer_address[i], customer_phone[i]]
					# custom_list.append(mList)
					detail_dict[item_sku[i]].append(mList)
					mList2 = [customer_name[i], customer_email[i],qty, customer_country[i], customer_city[i], customer_address[i], customer_phone[i]]
					name_detail_dict[item_name[i]].append(mList2)

					mList3 = [customer_name[i], customer_email[i],qty,dollar,customer_country[i], customer_city[i], customer_address[i], customer_phone[i]]
					all_detail_dict[item_sku[i]].append(mList3)
			else:
				detail_dict[item_sku[i]] = []
				detail_dict[item_sku[i]].append([customer_name[i], customer_email[i],purchase_qty[i], customer_country[i], customer_city[i],customer_address[i], customer_phone[i]])
				name_detail_dict[item_name[i]] = []
				name_detail_dict[item_name[i]].append([customer_name[i], customer_email[i],purchase_qty[i], customer_country[i], customer_city[i],customer_address[i],customer_phone[i]])
				all_detail_dict[item_sku[i]] = []
				all_detail_dict[item_sku[i]].append([customer_name[i], customer_email[i], purchase_qty[i],purchase_dollar[i],customer_country[i], customer_city[i],customer_address[i], customer_phone[i]])
	
		self.processed_SKU_NAME = [detail_dict, name_detail_dict,all_detail_dict]
		
		# for key, value  in all_detail_dict.items():
		# 	if key == 'MDL-195-FAT-BOY':
		# 		print("key: "+str(key))
		# 		print(str(key)+" : "+str(value))
		# 		print(' ')
		# 		print(' ')
		
	def main_display(self):
		
		mHeight = 190
		mWidth=   900
		self.root = tk.Tk()
		self.root.resizable(width=False, height=False)
		self.root.title("Purchase details of customers of individual product")
		
		self.mainCanvas = tk.Canvas(self.root, width=mWidth, height=mHeight)
		self.mainCanvas.config(bg='#5DADE2')
		self.mainCanvas.pack()
		self.mainCanvas.create_text(400,20,fill='darkblue', font='Times 20 italic bold', text="Purchase detail of customers of individual product")
		
	def selSKU(self):
		self.var.set(1)
		# print("you have selected "+str(self.var.get()))
		return str(self.var.get())
	
	def selNAME(self):
		self.var.set(2)
		# print("you have selected "+str(self.var.get()))
		return str(self.var.get())

	def search_frame_display(self):
			
		""" SEARCH frame starts from here """
		search_frame = tk.Frame(self.root, width=535, height=40, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,95), window=search_frame, anchor='nw')

		""" Radio buttons start here """
		self.var = tk.IntVar()
		self.var.set(1)
		R1 =  tk.Radiobutton(search_frame,text="SKU  ",  variable=self.var, value=1, command=self.selSKU)
		R1.configure(background='#5DADE2')
		R1.configure(foreground='darkblue')
		R1.grid(row=1, column=0, padx=0,pady=0)
		
		R2 =  tk.Radiobutton(search_frame,text="NAME ",  variable=self.var, value=2, command=self.selNAME)
		R2.configure(background='#5DADE2')
		R2.configure(foreground='darkblue')
		R2.grid(row=2, column=0, padx=0,pady=0)

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
		self.canvas_for_scroll.grid(row=1, column=1, sticky="news", padx=100) #ew

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
		self.qty_list = [1,1,1,1]
		self.country_list = ['USA','UK','DE','BE']
		self.city_list = ['Amsterdam','Rotterdam','Utrech','Denhaag']
		self.addr_list = ['Street Add1','Street Add2','City','State']


		combo_frame = tk.Frame(self.root, width=600, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,50), window=combo_frame, anchor='nw')
		
		select_label  = tk.Label(combo_frame, text="Select SKU: ")
		select_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		select_label.grid(row=1, column=0, padx=2, pady=0)

		self.combo_entry =  ttk.Combobox(combo_frame,width=25, values=final_items)
		self.combo_entry.grid(row=1, column=1, padx=32,pady=0)

		dummy_label  = tk.Label(combo_frame, text="")
		dummy_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		dummy_label.grid(row=1, column=2, padx=45, pady=0)

		resultBtn = tk.Button(combo_frame, font="Times 12 bold italic", text="Show Details", command=self.showdetailsCombo)
		resultBtn.configure(background='#5DADE2')
		resultBtn.configure(foreground='darkblue')
		resultBtn.grid(row=1, column=3, padx=0,pady=0)




		export_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((770,90), window=export_frame, anchor='nw')
		exportBtn = tk.Button(export_frame, font="Times 12 bold italic", text="Export Data", command= self.exportDataToFile)
		exportBtn.configure(background='#5DADE2')
		exportBtn.configure(foreground='darkblue')
		exportBtn.grid(row=1, column=1, padx=0,pady=0)

		

	

		self.search_frame_display()



		# The height and width of label frame does not get applied	
		label_frame = tk.Frame(self.root, width=0, height=0, bg="#5DADE2", highlightbackground="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((100,160), window=label_frame, anchor='nw') #nw

		name_label = tk.Label(label_frame, text="Name")
		name_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		name_label.grid(row=1, column=1, padx=50,pady=0)

		email_label = tk.Label(label_frame, text="Email")
		email_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		email_label.grid(row=1, column=2, padx=50,pady=0)
		
		qty_label = tk.Label(label_frame, text="Qty")
		qty_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		qty_label.grid(row=1, column=3, padx=50,pady=0)

		add_label = tk.Label(label_frame, text="Address")
		add_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		add_label.grid(row=1, column=4, padx=100,pady=0)
		
		


		back_frame = tk.Frame(self.root, width=200, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((20,90), window=back_frame, anchor='nw')
		backBtn = tk.Button(back_frame, font="Times 12 bold italic", text="Previous Module", command= self.gotoPreviousModule)
		backBtn.configure(background='#5DADE2')
		backBtn.configure(foreground='darkblue')
		backBtn.grid(row=1, column=0, padx=0,pady=0)


		label_frame.update_idletasks()

		self.entry_frame = tk.Frame(self.canvas_for_scroll, width=650, height=20, bg="#5DADE2")
		self.canvas_for_scroll.create_window((0,0), window=self.entry_frame, anchor='nw')


		self.mainCanvas.pack()
		# self.root.mainloop()


	def showdetailsCombo(self):
		# print("im clicked")
		# print("here is list:")
		# self.hold_details = self.processed_SKU_NAME[0]
		# print(self.processed_SKU_NAME[0])
	
		self.name_list.clear()
		self.email_list.clear()
		self.qty_list.clear()
		self.city_list.clear()
		self.country_list.clear()
		self.addr_list.clear()
		my_tempList = []
		# self.hold_details.clear()
		
		product_SKU = str(self.combo_entry.get())
		self.hold_details = self.processed_SKU_NAME[0][product_SKU]
		my_tempList = self.processed_SKU_NAME[0][product_SKU]
		for i in range(len(my_tempList)):
			self.name_list.append(my_tempList[i][0])
			self.email_list.append(my_tempList[i][1])
			self.qty_list.append(my_tempList[i][2])
			self.country_list.append(my_tempList[i][3])
			self.city_list.append(my_tempList[i][4])
			self.addr_list.append(my_tempList[i][5])

		self.displayEntries(self.name_list,self.email_list,self.qty_list,self.country_list,self.city_list,self.addr_list)
	

	def showdetailsSearch(self,search_string):
		
		self.hold_details = []
		found=False
		if int(self.var.get()) == 1:
			self.hold_details.clear()
			processed_data = self.processed_SKU_NAME[0]
			self.name_list.clear()
			self.email_list.clear()
			self.qty_list.clear()
			self.country_list.clear()
			self.city_list.clear()
			self.addr_list.clear()
			
			for key, value in processed_data.items():
				# print("befo")
				# print("key: ",key, "search: ", search_string)
				original_key =  key
				key = key.lower()
				search_string =  search_string.lower()
				if search_string in key:
					found = True
					self.hold_details = processed_data[original_key]
					self.search_entry.delete(0,tk.END)
					self.search_entry.insert(1,original_key)
					break
			if found:
				for i in range(len(self.hold_details)):
					self.name_list.append(self.hold_details[i][0])
					self.email_list.append(self.hold_details[i][1])
					self.qty_list.append(self.hold_details[i][2])
					self.country_list.append(self.hold_details[i][3])
					self.city_list.append(self.hold_details[i][4])
					self.addr_list.append(self.hold_details[i][5])

				self.displayEntries(self.name_list,self.email_list,self.qty_list,self.country_list,self.city_list,self.addr_list)
			else:
				self.showMsg("Sorry no matching record found for given query!")

		elif int(self.var.get()) ==2:
			self.hold_details.clear()
			processed_data = self.processed_SKU_NAME[1]
			self.name_list.clear()
			self.email_list.clear()
			self.qty_list.clear()
			self.country_list.clear()
			self.city_list.clear()
			self.addr_list.clear()
			
			for key, value in processed_data.items():
				# print("befo")
				# print("key: ",key, "search: ", search_string)
				original_key =  key
				key = key.lower()
				search_string =  search_string.lower()
				if search_string in key:
					found = True
					self.hold_details = processed_data[original_key]
					self.search_entry.delete(0,tk.END)
					self.search_entry.insert(1,original_key)
					break

			if found:
				for i in range(len(self.hold_details)):
					self.name_list.append(self.hold_details[i][0])
					self.email_list.append(self.hold_details[i][1])
					self.qty_list.append(self.hold_details[i][2])
					self.country_list.append(self.hold_details[i][3])
					self.city_list.append(self.hold_details[i][4])
					self.addr_list.append(self.hold_details[i][5])

				self.displayEntries(self.name_list,self.email_list,self.qty_list,self.country_list,self.city_list,self.addr_list)
			else:
				self.showMsg("Sorry no matching record found for given query!")




	def searchItem(self):
			print("yes I'm searching")

	def this_function_for_git(self):
		mylist = [0, 1, 1]
		x = all(mylist)
		for i in mylist:
			b= i*1

		
		# Returns False because 0 is the same as False

	def displayEntries(self,name_list,email_list,qty_list,country_list,city_list,addr_list):
		for widget in self.entry_frame.winfo_children():
			widget.destroy()

		for i in range(len(email_list)):
			name_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=15)
			name_variable = name_list[i]
			name_entry.insert(1,'%s'%name_variable)
			name_entry.grid(row=i+2, column=1, padx=0,pady=0)
			name_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			email_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=30)
			email_variable = email_list[i]
			email_entry.insert(1,'%s'%email_variable)
			email_entry.grid(row=i+2, column=2, padx=0,pady=0)
			email_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			qty_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=5)
			qty_variable = qty_list[i]
			qty_entry.insert(1,'%s'%qty_variable)
			qty_entry.grid(row=i+2, column=3, padx=0,pady=0)
			qty_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			address_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=70)
			address_variable = str(addr_list[i]+","+str(city_list[i])+","+str(country_list[i]))
			address_entry.insert(1,'%s'%address_variable)
			address_entry.grid(row=i+2, column=4, padx=0,pady=0)
			address_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

		self.entry_frame.update_idletasks()
		self.frame_for_scroll.update_idletasks()	
		self.canvas_for_scroll.config(scrollregion=self.canvas_for_scroll.bbox("all"))


	def showMsg(self,theMessage):
		tkinter.messagebox.showinfo("Info!",theMessage)

	def exportDataToFile(self):
		# file = ''
		
		# path_dir = 'C:\\Users\\Public\\Desktop\\Report Central'
		# import pathlib
		# path_dir = pathlib.Path(__file__).parent.resolve()
	
		# try:
			# file = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
		# 	file = str(path_dir)+"\\sales_report.csv" 
		# # except:
		# 	# self.showMsg("Please close already opened csv file or choose a different name for this file. Please try again!")
		# if file is None:
		# 	return
		first_int = random.randint(1,9)
		second_int = random.randint(1,9)
		third_int = random.randint(1,9)
		file_ending = str(first_int)+str(second_int)+str(third_int)
		# file_location_and_name = str(path_dir)+'\\sales_report'+file_ending+'.csv'
		file_name = 'sales_report'+file_ending+'.csv'
		with open(file_name, mode='w') as file:
		# data = self.all_in_one
			fieldnames =["Customer_Name","Email","Qty", "Address"]
		# with open('report.csv','w', newline='') as file:

			writer =  csv.writer(file, lineterminator='\r')
			writer.writerow(fieldnames)
			combined_str = ''
			for i in range(len(self.hold_details)):
				combine_list = []
				combine_list.append(self.hold_details[i][0])
				combine_list.append(self.hold_details[i][1])
				combine_list.append(self.hold_details[i][2])
				# Address_list = []
				combine_list.append(self.hold_details[i][5]+","+self.hold_details[i][4]+","+self.hold_details[i][3])
				# Address_list.extend()
				# Address_list.extend()
				# combine_list.append(Address_list) # City
				try:
					writer.writerow(combine_list)
				except PermissionError:
					self.showMsg("Please close the previous file to save another file.")
			self.showMsg("The file has been saved at location where this program located with file name: "+file_name)	
					
		
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
