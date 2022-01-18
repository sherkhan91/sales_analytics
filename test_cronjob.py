# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:51:51 2020

@author: Sher Khan
"""
import sys
arg=sys.argv[1]
import mysql.connector
import config
import warnings
warnings.filterwarnings("ignore")
mysql1 = mysql.connector.connect(
  host=config.HOST,
  user=config.USER,
  passwd=config.PSWD,
  database = config.FRENNS_NAME
  )

mycursor1=mysql1.cursor()
script='arima_commandline_new.py'
mycursor1.execute('select cust_no from sync_queue where script_name="'+str(script)+'" and cust_no="'+str(arg)+'"')
duplicate=mycursor1.fetchall()
print("this is duplicate")

# print(duplicate)
#duplicate=pd.read_sql('select cust_no from sync_queue where script_name="'+str(script)+'" and cust_no="'+str(arg)+'"',con=mysql1)

""" commented by sher 
if duplicate:
	print("yes its duplicate closing all")
	mycursor1.close()
	mysql1.close()
	sys.exit()
"""


#    import csv, sys, os, pytz, datetime, json, re

import warnings,os
from pandas import read_csv
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA 
from numpy import array

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense


def evaluate_arima_model(X, arima_order):
	print("evaluate_arima_model.........")
	from statsmodels.tsa.arima_model import ARIMA
	from sklearn.metrics import mean_squared_error
	# prepare training dataset
	train_size = int(len(X) * 0.66)
	train, test = X[0:train_size], X[train_size:]
	history = [x for x in train]
	# make predictions
	predictions = list()
	
	for t in range(len(test)):
		model = ARIMA(history, order=arima_order)
		model_fit = model.fit(disp=0)
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# calculate out of sample error
	error = mean_squared_error(test, predictions)
	print(error)
	return error

## evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
	print("evaluate_models.........")
	dataset = dataset.astype('float32')
	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)    
				try:
					mse = evaluate_arima_model(dataset, order)
					if mse < best_score:
						best_score, best_cfg = mse, order
					print('ARIMA%s MSE=%.3f' % (order,mse))
				except:
					continue
	print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
	return best_cfg
# split a univariate sequence into samples
def split_sequence(sequence, n_steps_in, n_steps_out):
	print("split_sequence.........")
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

def ysf(cust_no):
	print("ysf.........")

	import mysql.connector
	from pandas import to_datetime
	import warnings
	import numpy as np
	import pandas as pd
	mysql = mysql.connector.connect(
	  host=config.HOST,
	  user=config.USER,
	  passwd=config.PSWD,
	  database =config.FRENNS_NAME#'vkingsol_frennsdevelopment_aug'
	  )
	mycursor=mysql.cursor()
	script='arima_commandline_new.py'
	status=0
	st=[str(arg),str(script),str(status)]
	upd_status=read_sql('select cust_no from sync_queue where script_name="'+str(script)+'" and cust_no="'+str(arg)+'"',con=mysql1)
	if len(upd_status['cust_no'])==0:
		stat="INSERT INTO sync_queue(cust_no,script_name,\
			   status\
			   ) VALUES(%s,%s,%s)"
		mycursor.execute(stat,st)
		mysql.commit()

	df=read_sql("select DISTINCT name from syncinvoice where cust_no = '{0}'".format(cust_no), con=mysql)

	name=df['name'].values.astype(str)
	
	
	#name='qbCompnay'
	p_values = [0, 1, 2, 6]
	d_values = range(0, 2)
	q_values = range(0, 2)
	out=[]
	average=[]
	rec=[]
	
	for i in name:
		qr=read_sql("""SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(collection_date) as pay_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where cust_no = '{0}' and name = "{1}" order by issue_date desc """.format(cust_no,i),con=mysql)
		ser=qr[['issue_date','after_issue_days']]
		ser['issue_date']=to_datetime(ser['issue_date'])
		ser=ser.set_index('issue_date').resample('D').mean().interpolate('linear')
		
		if len(ser)>6:
	
			warnings.filterwarnings("ignore")
			avg=int(qr['after_issue_days'].mean())
			average.append(avg)
			series=ser.astype('float32')
			days=series['after_issue_days']
			days=np.array(days)
			if len(ser)>500:
				import itertools
				import warnings
				import itertools
				import numpy as np
				import matplotlib.pyplot as plt
				warnings.filterwarnings("ignore")
				plt.style.use('fivethirtyeight')
				import pandas as pd
				import statsmodels.api as sm
				import matplotlib
				p = d = q = range(0, 2)
				pdq = list(itertools.product(p, d, q))
				seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
				final_param=[]
				final_param_seasonal=[]
				final_aic=[]
				print("leeeeeength of outer loop: ",len(pdq))
				print("leeeeeength of inner loop: ",len(seasonal_pdq))
				count = 0
				for param in pdq:
					for param_seasonal in seasonal_pdq:
						try:
							#print("=============================coming til here===============================================")
							mod = sm.tsa.statespace.SARIMAX(days,
															order=param,
															seasonal_order=param_seasonal,
															enforce_stationarity=False,
															enforce_invertibility=False)
							results = mod.fit()
							final_param.append(param)
							final_param_seasonal.append(param_seasonal)
							final_aic.append(results.aic)
						except:
							continue
					print("=======this is count===================",count)
					count = count+1
				index=int(final_aic.index(max(final_aic)))
				orderr=final_param_seasonal[index][:3]
				
			else:
				orderr=(0,0,0)

			try:
				index=int(final_aic.index(max(final_aic)))
				model=sm.tsa.statespace.SARIMAX(days,
											order=final_param[index],
											seasonal_order=final_param_seasonal[index],
											enforce_stationarity=False,
											enforce_invertibility=False)
				#train = series.loc[st,p,d,qr(init_dt):str(last_dt)]
				model_fit=model.fit()#disp=0
				output=model_fit.forecast(steps=1)
				out1=int(max(output))#[0]
			except:
				stepwise_model = ARIMA(series, order=orderr)
				model_fit=stepwise_model.fit(disp=0)#disp=0
				output=model_fit.forecast()
				out1=int(max(output[0]))
			# out3=(out1+out2+0.0001)/2
			# out.append(out3)
		##############################################################################################
		####### Mysql queries to Update or insert into syncfinancialanalysis table  ##################
		##############################################################################################
			
		 
			records=[str(cust_no),str(i),str(out1),str(avg),str(avg),str(avg)]
			record=[str(out1),str(avg),str(avg),str(avg)]
			rec.append(records)
			i=str(i)
			cust_no=str(cust_no)
			print(records)
			
			upd=pd.read_sql("""SELECT company_name from syncfinancialanalysis where cust_no = "{0}" and company_name = "{1}" """.format(str(cust_no),str(i)), con=mysql)
			# upd=pd.read_sql("select company_name from syncfinancialanalysis where company_name = '"+str(i)+"' and cust_no='"+str(cust_no)+"'", con=mysql)
			update=upd['company_name']
			update1=update.to_numpy()
			if len(update1)==0:
				sql="""INSERT INTO syncfinancialanalysis(cust_no,company_name,expected_days,average_payment_days,\
				company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
				mycursor.execute(sql,records)
			else:
				sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and cust_no="{1}" """.format(i,cust_no)
				mycursor.execute(sql,record) 
			mysql.commit()
			
			
		else:
			avg=int(qr['after_issue_days'].mean())
			average.append(avg)
			out1=int(qr['after_issue_days'].mean())
			out.append(out1)
			records=[str(cust_no),str(i),str(out1),str(avg),str(avg),str(avg)]
			record=[str(out1),str(avg),str(avg),str(avg)]
			rec.append(records)
			upd=pd.read_sql("""SELECT company_name from syncfinancialanalysis where cust_no = "{0}" and company_name = "{1}" """.format(str(cust_no),str(i)), con=mysql)
			update=upd['company_name']
			#update1=update.as_matrix()
			#update1 = update.values()
			update1 = update['company_name'].tolist()
			if len(update1)==0:
				sql="""INSERT INTO syncfinancialanalysis(cust_no,company_name,expected_days,average_payment_days,\
				company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
				mycursor.execute(sql,records)
			else:
				sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and cust_no="{1}" """.format(i,cust_no)
				mycursor.execute(sql,record) 
			mysql.commit()
	



	status=1
	st=[str(status),str(0)]
	stat="""UPDATE sync_queue SET status=%s,error=%s\
		 WHERE cust_no="{0}" and  script_name='arima_commandline_new.py'""".format(str(arg))  #,acc_type=%s,company_type=%s,cust_no=%s,year_number=%s,                                      

	mycursor.execute(stat,st)        
	mysql.commit()
	mycursor.close()
	mysql.close()



#import mysql.connector
import numpy as np

def name(arg,arg2):
	print("name arg and agr2.........",arg,arg2)
	import mysql.connector
	import config
	mysql = mysql.connector.connect(
	  host=config.HOST,
	  user=config.USER,
	  passwd=config.PSWD,
	  database = config.FRENNS_NAME
		  )
	df=pd.read_sql("select DISTINCT name from syncinvoice where cust_no = '{0}' and company_number='{1}'".format(arg,arg2), con=mysql)
	name=df['name'].values.astype(str)
	return name


def call(arg,arg3):
	print("call arg, arg3.........", arg3)
	print("here is -------------------------arg---------------------------",arg)
	import pandas as pd
	try:
				#nm=name(arg,arg2)
		clr_rec=[]
		clr_rec.extend(ysf(arg))
		clr_rec.extend(yousuf(arg))

		import config
	
		mysql2 = mysql.connector.connect(
					  host=config.HOST,
					  user=config.USER,
					  passwd=config.PSWD,
					  database = config.CLEARSIGHT_NAME
					  )
		cnb=pd.read_sql("""select CompanyName from company_data where CompanyNumber="{0}" """.format(arg3),con=mysql2)
		cnb=cnb['CompanyName']
		try:
			cnb=max(cnb)
		except:
			cnb=arg
		mysql2.close()
		for j in range(0,len(clr_rec)):
			mysql1 = mysql.connector.connect(
				  host=config.HOST,
				  user=config.USER,
				  passwd=config.PSWD,
				  database = config.FRENNS_NAME
				  )
			mycursor=mysql1.cursor()
			records=clr_rec[j]
			record=[records[0],records[1],records[2],records[3],records[3],records[3]]
			recd=[records[2],records[3],records[3],records[3]]
			nm=str(records[1])
			update1=[]
			if nm=='frenns id':
				record1=[records[0],cnb,records[2],records[3],records[3],records[3]]
				recd1=[records[2],records[3],records[3],records[3]]
				upd=pd.read_sql("""select company_name from syncfinancialanalysis where company_name = "{0}"  and cust_no="{1}" """.format(cnb,arg), con=mysql1)
				update=upd['company_name']
				update1=update['company_name'].tolist()
				if len(update1)==0:
					sql="""INSERT INTO syncfinancialanalysis(cust_no,company_name,expected_days,average_payment_days,company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
					mycursor.execute(sql,record1)
				else:
					sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and cust_no="{1}" """.format(cnb,arg)
					mycursor.execute(sql,recd1) 
			else:       
				upd=pd.read_sql("""select company_name from syncfinancialanalysis where company_name = "{0}"  and cust_no="{1}" """.format(nm,arg), con=mysql1)
				update=upd['company_name']
				#update=update.as_matrix()
				update=update['company_name'].tolist()
	
				if len(update)==0:
					sql="""INSERT INTO syncfinancialanalysis(cust_no,company_name,expected_days,average_payment_days,company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
					mycursor.execute(sql,record)
				else:
					sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and cust_no="{1}" """.format(nm,arg)
					mycursor.execute(sql,recd) 
			mysql1.commit()
			mycursor.close()
			mysql1.close()
	
			print(record)
	except Exception as e:
		print(e)
		res="Executed with some errors"
		return res

from pandas import read_sql
from tqdm import tqdm
import time
count = 0
while count<=5:
	print("this is counttttttt: ",count)
	print("this is script name", str(script))
	stats=read_sql('select distinct cust_no from sync_queue where script_name="'+str(script)+'" and status="0"',con=mysql1)
	print('this is stats',stats['cust_no'])
	print("length of status is:",len(stats['cust_no']))
	a=1
	#if len(stats['cust_no'])==0:
	if a==1:
		print("printing inside if")
		# print(idz[0])
		# try:
		ysf(str(arg))
		error=0
	

		mysql1.commit()        
		# ae(10)
		status=1
		st=[str(status),str(error)]
		stat="""UPDATE sync_queue SET status=%s,error=%s\
			 WHERE cust_no="{0}" and  script_name='arima_commandline_new.py'""".format(str(arg))  #,acc_type=%s,company_type=%s,cust_no=%s,year_number=%s,                                      

		mycursor1.execute(stat,st)
		mysql1.commit()
		#break
	else:
		print("else part")
		time.sleep(3)
		print("hello3")
mysql1.commit()
mycursor1.close()
mysql1.close()




# arg='CNO100000570'
# print (arg)
# arg2=sys.argv[2]
# print (arg2)
# arg2='00542515'
# call('CNO100000631','07442456')
# ysf(str(arg))
# print(ysf('CNO100000635'))
# call(arg,arg2)    
