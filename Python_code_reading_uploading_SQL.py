# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql

def file_update():
    data = pd.read_table("D:\\masters\\Emden\\project\\professor_agnes\\Nachiket_SQVI\\bom_1.txt",skiprows=3)
#data.head()
#data = data[["WERKS","LGORT","LGOBE"]]
    #print(data.head())

    len_data = len(data)
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="cde345CDE#$%")
    cursor=db.cursor()
    cursor.execute("use sap_data")

    SQL_code = []
    for i in range(len_data):
        row_list = data.iloc[i][:].values.flatten().tolist()
        line = "Insert into bom_table (Col_1,Col_2,Col_3,Col_4,Col_5,Col_6,Col_7,Col_8) values ('{}','{}','{}','{}','{}','{}','{}','{}')".format(row_list[0],row_list[1],row_list[2],row_list[3],row_list[4],row_list[5],row_list[6],row_list[7])
    #print(line)
        cursor.execute(line)

    cursor.close()
    db.commit()
    print("data has been uploaded to SQL")



class OnMyWatch:
	# Set the directory on watch
	watchDirectory = "D:/masters/Emden/project/professor_agnes/Nachiket_SQVI"

	def __init__(self):
		self.observer = Observer()

	def run(self):
		event_handler = Handler()
		self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
		self.observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			self.observer.stop()
			print("Observer Stopped")

		self.observer.join()


class Handler(FileSystemEventHandler):

	@staticmethod
	def on_any_event(event):
		if event.is_directory:
			return None

		elif event.event_type == 'created':
			# Event is created, you can process it now
			print("Watchdog received created event - % s." % event.src_path)
		elif event.event_type == 'modified':
			# Event is modified, you can process it now
			file_update()
            #print("file has been uploaded")
            #print("Watchdog received modified event - % s." % event.src_path)
			

if __name__ == '__main__':
	watch = OnMyWatch()
	watch.run()
