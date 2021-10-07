# from ttkwidgets.autocomplete import AutocompleteCombobox
from datetime import datetime
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

class discount_detail:

	def __init__(self):
		print("hello, I'm the discount report")
		# print(root_reference)
		# utils.init()
		
		self.previous_app = utils.root_reference

		# print(previous_app)
		self.entry_frame = tk.Frame()
		self.processed_SKU_NAME  = []
		self.hold_details = []
		

	
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
		detail_dict  = defaultdict(list)
		name_detail_dict =  defaultdict(list)
		all_detail_dict = defaultdict(list)
		check_temp_list = []
		item_sku =  utils.raw_column_list['LineItem SKU']
		item_name = utils.raw_column_list['LineItem Name']
		purchase_qty = utils.raw_column_list['LineItem Qty']
		purchase_dollar =utils.raw_column_list['Subtotal']
		order_number =  utils.raw_column_list['Order #']
		customer_name =  utils.raw_column_list['Shipping Name']
		purchase_date = self.toDateObj(utils.raw_column_list['Order Date and Time Stamp'])
		coupon_code = utils.raw_column_list['Coupon Code']
		coupon_code_name =  utils.raw_column_list['Coupon Code Name']
		discount_dollar = utils.raw_column_list['Discount']
	
		
		for i in range(len(customer_name)):		
			if coupon_code_name[i] in all_detail_dict.keys():
				if len(coupon_code[i]) > 2:
					temp_list = all_detail_dict[coupon_code_name[i]]
					customer_name_list = temp_list[0]
					customer_name_list.append(customer_name[i])
					purchase_date_list = temp_list[1]
					purchase_date_list.append(purchase_date[i])
					discount_list = temp_list[2]

					discount_total = 0
					try:
						discount_total = discount_dollar[i]
						discount_total = float(discount_total)
					except:
						discount_total = discount_dollar[i][1:]
					finally:
						discount_total =  discount_dollar[i][2:(len(purchase_dollar[i])-2)]

					discount_total = float(discount_total)
					
					discount_list.append(discount_total)

					all_detail_dict[coupon_code_name[i]] = ([customer_name_list, purchase_date_list, discount_list])

			else:
				if len(coupon_code[i]) > 2: # Checking if there is string 
					discount_total = 0
					try:
						discount_total = discount_dollar[i]
						discount_total = float(discount_total)
					except:
						discount_total = discount_dollar[i][1:]
					finally:
						discount_total =  discount_dollar[i][2:(len(purchase_dollar[i])-2)]

					discount_total = float(discount_total)

					customer_name_list = []
					customer_name_list.append(customer_name[i])
					purchase_date_list = []
					purchase_date_list.append(purchase_date[i])
					discount_list = []
					discount_list.append(discount_total)

					all_detail_dict[coupon_code_name[i]] = ([customer_name_list, purchase_date_list, discount_list])
		

		self.processed_DISCOUNT_DETAIL = all_detail_dict
		
		# for key, value  in all_detail_dict.items():
		# 	if key == 'MDL-195-FAT-BOY':
		# 		print("key: "+str(key))
		# 		print(str(key)+" : "+str(value))
		# 		print(' ')
		# 		print(' ')
		
	def main_display(self):
		
		mHeight = 190
		mWidth = 900
		self.root = tk.Tk()
		self.root.resizable(width=False, height=False)
		self.root.title("Discount details of individual discount events")
		
		self.mainCanvas = tk.Canvas(self.root, width=mWidth, height=mHeight)
		self.mainCanvas.config(bg='#5DADE2')
		self.mainCanvas.pack()
		self.mainCanvas.create_text(400,20,fill='darkblue', font='Times 20 italic bold', text="Discount details of individual discount events")
		

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
		rows = len(self.processed_DISCOUNT_DETAIL)
		columns = 2
		
		final_items = []
		for key, value in self.processed_DISCOUNT_DETAIL.items():
			print(f"{key}")
			final_items.append(key)

			
		self.name_list = ['first name','name two','name customer']
		self.date_list = ['a@admin.com','c@cc.com','this@anemail.com']
		self.discount_list = [1,2,1,5]
	
		combo_frame = tk.Frame(self.root, width=600, height=100, bg="#5DADE2", highlightbackground="darkblue", highlightcolor="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((170,50), window=combo_frame, anchor='nw')
		
		select_label  = tk.Label(combo_frame, text="Select Discount: ")
		select_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		select_label.grid(row=1, column=0, padx=2, pady=0)

		self.combo_entry =  ttk.Combobox(combo_frame,width=25, values=final_items)
		self.combo_entry.grid(row=1, column=1, padx=32,pady=0)

		# dummy_label  = tk.Label(combo_frame, text="")
		# dummy_label.config(font=("Times 13  italic"), fg=("darkblue"), bg=("#5DADE2"))
		# dummy_label.grid(row=1, column=2, padx=45, pady=0)

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

		
		# self.search_frame_display()

		# The height and width of label frame does not get applied	
		label_frame = tk.Frame(self.root, width=0, height=0, bg="#5DADE2", highlightbackground="darkblue", highlightthickness=1)
		self.mainCanvas.create_window((140,160), window=label_frame, anchor='nw') #nw

		name_label = tk.Label(label_frame, text="Name")
		name_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		name_label.grid(row=1, column=1, padx=50,pady=0)

		date_label = tk.Label(label_frame, text="Date Used")
		date_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		date_label.grid(row=1, column=2, padx=50,pady=0)
		
		discount_label = tk.Label(label_frame, text="Discount")
		discount_label.config(font=("Times 13 bold italic"), fg=("darkblue"), bg=("#5DADE2"))
		discount_label.grid(row=1, column=3, padx=50,pady=0)
		


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

		selected_combo_entry = str(self.combo_entry.get())

		self.name_list.clear()
		self.date_list.clear()
		self.discount_list.clear()
		print(f"yes selected: {selected_combo_entry}")
		
		
		self.hold_details = self.processed_DISCOUNT_DETAIL[selected_combo_entry]
		my_tempList = self.processed_DISCOUNT_DETAIL[selected_combo_entry]
		# for i in range(3):
		for j in range(len(my_tempList[0])):
			self.name_list.append(my_tempList[0][j])
			self.date_list.append(my_tempList[1][j])
			self.discount_list.append(my_tempList[2][j])
			

		self.displayEntries(self.name_list,self.date_list,self.discount_list)
	

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


	def displayEntries(self,name_list,date_list,discount_list):
		for widget in self.entry_frame.winfo_children():
			widget.destroy()

		for i in range(len(name_list)):
			name_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=15)
			name_variable = name_list[i]
			name_entry.insert(1,'%s'%name_variable)
			name_entry.grid(row=i+2, column=1, padx=0,pady=0)
			name_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			date_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=30)
			date_variable = date_list[i]
			date_entry.insert(1,'%s'%date_variable)
			date_entry.grid(row=i+2, column=2, padx=0,pady=0)
			date_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')

			discount_entry = tk.Entry(self.entry_frame,font="Halvetica 10 bold", bd=2, width=5)
			discount_variable = discount_list[i]
			discount_entry.insert(1,'%s'%discount_variable)
			discount_entry.grid(row=i+2, column=3, padx=0,pady=0)
			discount_entry.configure(state='readonly', disabledbackground='white', disabledforeground='black')


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
		file_name = 'discount_report'+file_ending+'.csv'
		with open(file_name, mode='w') as file:
		# data = self.all_in_one
			fieldnames =["Customer_Name","Date","Discount"]
		# with open('report.csv','w', newline='') as file:

			writer =  csv.writer(file, lineterminator='\r')
			writer.writerow(fieldnames)
			combined_str = ''

			my_tempList = self.hold_details
			# for i in range(3):
			# for j in range(len(my_tempList[0])):
			# 	self.name_list.append(my_tempList[0][j])
			# 	self.date_list.append(my_tempList[1][j])
			# 	self.discount_list.append(my_tempList[2][j])
			for i in range(len(self.hold_details[0])):
				combine_list = []
				combine_list.append(self.hold_details[0][i])
				combine_list.append(self.hold_details[1][i])
				combine_list.append(self.hold_details[2][i])
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
