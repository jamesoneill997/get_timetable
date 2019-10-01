from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import sys

chrome_options = Options()  
chrome_options.add_argument("--headless")  
browser = webdriver.Chrome("/home/james/Desktop/chromedriver", chrome_options = chrome_options)

class Timetable(object):
	def get_index(self,day):
		days = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
		try:
			if days.index(day) < 2:
				day = "None"
				return day

			return days.index(day)

		except:
			return 'Invalid day of week'	

	def get_table(self, day):
		schedule = []
		mod_loc = []
		day = self.get_index(day)
		
		if day == "None":
			print("No college today")
			sys.exit()

		browser.get("https://opentimetable.dcu.ie")
		time.sleep(2)
		browser.find_element_by_xpath("/html/body/app-root/app-layout/app-desktop/div[2]/div/div[1]/app-publish/div/div[1]/div[1]/div[2]/app-entities-search-and-select/div/div[1]/div/app-entity-selector/select/option[4]").click()
		time.sleep(1)
		browser.find_element_by_id("textSearch").send_keys("CASE3")
		time.sleep(2)
		browser.find_element_by_xpath("/html/body/app-root/app-layout/app-desktop/div[2]/div/div[1]/app-publish/div/div[1]/div[1]/div[2]/app-entities-search-and-select/div/div[3]/app-selectable-list/div/div[1]/div/input").click()
		table_text = browser.find_element_by_xpath("/html/body/app-root/app-layout/app-desktop/div[2]/div/div[1]/app-publish/div/div[2]/div/div/div/div").text
		time.sleep(2)

		for i in range(27):
			times = ''
			try:
				times = browser.find_element_by_xpath('//*[@id="week-pdf-content"]/tbody/tr[{}]/td[1]'.format(i)).text
				
			except:
				pass

			try:
				mon_text = browser.find_element_by_xpath('//*[@id="week-pdf-content"]/tbody/tr[{}]/td[{}]'.format(i+1,day)).text
				
			except:
				pass

			time_place = mon_text + ' ' + times
			schedule.append(time_place)

		for lecture in schedule:
			splitter = lecture.split('\n')
			mod_loc.append(splitter)

		for elem in mod_loc:
			if len(elem) > 1:
				if ':00' in elem[1]:
					print('Module: ' + elem[0][:5] + '\n' + 'Time & Place: ' + elem[1][4:] + '\n')
			else:
				pass

def main():
	timetable = Timetable()
	try:
		timetable.get_table(sys.argv[1])
	except IndexError:
		print('Please enter a weekday')
		timetable.get_table(input())

if __name__ == '__main__':
	main()