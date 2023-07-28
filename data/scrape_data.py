import os
from selenium import webdriver
import time
import requests


browser=webdriver.Chrome('C:\\Users\\Sweta\\chromedriver.exe')
query_dict = {y_class:[extracted_keywords]}


def extract_image_links(query,browser=browser, max_image_count = 400):
  img_links = []
	link =f'https://www.google.com/search?q={query}&rlz=1C1CHBF_enIN889IN889&sxsrf=APwXEdeNc8uOF9C9Q3qaMu36chvL6YY76g:1686217760705&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiy34_VsrP_AhUqd2wGHcHqB7AQ_AUoAXoECAEQAw&biw=1024&bih=497&dpr=1.88'
	browser.get(link)
	time.sleep(5)
	img_count = 0
	while img_count<max_image_count:
		els = browser.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy"]')
		img_count=len(els)
		print(img_count)
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
	for n,i in enumerate(els[:10]):
		print(n)
		i.click()
		time.sleep(2)
		try:
			img_links.append(browser.find_element_by_xpath('//img[@class="r48jcc pT0Scc iPVvYb"]').get_attribute('src'))
		except:
			try:
				time.sleep(5)
				img_links.append(browser.find_element_by_xpath('//img[@class="r48jcc pT0Scc iPVvYb"]').get_attribute('src'))
			except: 
				pass
	return img_links



def download_image_links(cl,image_list=img_links,location='C:\\Users\\Sweta\\Desktop\\Wedding_Search\\dataset\\train\\'):
	location = location+cl+'\\'
	os.mkdir(location)
	n=0
	for n,img in enumerate(image_list):
		path = location+cl+'_'+str(n)+'.jpg'
		try:
			response = requests.get(img)
			if response.status_code == 200:
				with open(path, 'wb') as file:
					file.write(response.content)
		except requests.exceptions.RequestException as e:
			print(f"Error downloading image {img}: {e}")


for classes in query_dict.keys():
  links = [extract_image_links(key) for key in query_dict[classes]]
for l in [link for sublist in links for link in sublist]:
    download_image_links(l)
