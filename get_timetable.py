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
				day == "Weekend"
			elif days.index(day) >= 2:
				day = days.index(day)
		except ValueError:
			day = 'Invalid'
		return day

	def get_module_name(self, module_code):
		code_dictionary = {
			'CA304': 'Computer Networks 2',
			'CA314': 'OO Analysis and Design',
			'CA318': 'Advanced Algorithms and A.I. Search',
			'CA320': 'Computability and Complexibility',
			'CA341': 'Comparative Programming Languages',
			'CA357': 'User Interface and Completion'
			}
		
		return code_dictionary.get(module_code)

		


	def get_table(self, day):
		schedule = []
		mod_loc = []
		day = self.get_index(day)
		
		if day == "Weekend":
			print("No college today")
			sys.exit()

		elif day == "Invalid":
			print("Invalid Day of week. Please try again")
			timetable.get_table(input())


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
				mod_code = elem[0][:5]
				if ':00' in elem[1]:
					print('Module: ' + self.get_module_name(mod_code) + '\n' + 'Time & Place: ' + elem[1][4:] + '\n')



def main():
	timetable = Timetable()
	timetable.get_table(sys.argv[1])


if __name__ == '__main__':
	main()