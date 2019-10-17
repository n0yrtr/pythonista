import ui
import time
import datetime
import threading

taskList = []
nowWorkTh = ""

def addTask(sender):
	taskName = addTaskNameEdit.text
	global taskList

	taskList.append({"title":taskName, "spendTime": datetime.timedelta()})
	tableReload(sender)
	
def startTimer(sender):
	print("start")
	
	global nowWorkTh
	
	taskTable :ui.TableView = sender.superview['taskTable']
	selected_row = taskTable.selected_row
	delta = taskList[selected_row[1]]["spendTime"]
	title = taskList[selected_row[1]]["title"]
	th = myThread()
	th.beforeSpendTime = delta
	nowWorkTh = th
	th.start()
	print(str(delta))
	print(title)
	tableReload(sender)
	
def stopTimer(sender):
	global nowWorkTh
	global taskList
	taskTable = sender.superview['taskTable']
	selected_row = taskTable.selected_row
	delta = taskList[selected_row[1]]["spendTime"]
	title = taskList[selected_row[1]]["title"]

	nowWorkTh.nowWroking = False
	taskList[selected_row[1]] = {"title":title, "spendTime": nowWorkTh.caluculateSpendTime()}
	nowWorkTh = ""
	print("stop")
	tableReload(sender)
	
def tableReload(sender):
	taskData = ui.ListDataSource("")
	taskData.items = taskList

	taskTable = sender.superview['taskTable']
	selected_row = taskTable.selected_row
	taskTable.data_source = taskData
	taskTable.reload_data()
	
	spendTimeList = []
	for task in taskList :
		spendTimeList.append({"title": str(task["spendTime"])})
		
	spendTimeData = ui.ListDataSource("")
	spendTimeData.items = spendTimeList
	spendTimeTable = sender.superview['spendTimeTable']
	spendTimeTable.data_source = spendTimeData
	spendTimeTable.reload_data()
	taskTable.selected_row = selected_row

class myThread(threading.Thread):
	def __init__(self):
		self.nowWroking = True
		self.beforeSpendTime = datetime.timedelta()
		self.startTime = datetime.datetime.now()
		self.interval = 000.1
		print("init:" + str(self.startTime))
		print("init:" + str(self.beforeSpendTime))
		super(myThread, self).__init__()

	def run(self):
		while self.nowWroking:
			self.caluculateSpendTime()
			time.sleep(self.interval)
			
	def caluculateSpendTime(self):
		nowTime = datetime.datetime.now()
		spendTime = nowTime - self.startTime + self.beforeSpendTime
		timerLabel.text = str(spendTime)
		return spendTime
		
	def setBeforeSpendTime(self, value):
		self.beforeSpendTime = value
	
v = ui.load_view()
v.present('sheet')

timerLabel = v['label1']
timerLabel.text = 'timer'

taskTable = v['taskTable']


addTaskButton = v['addTaskButton']

addTaskNameEdit = v['addTaskNameEdit']





