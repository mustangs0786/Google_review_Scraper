from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

driver.get('https://www.google.com/maps/@41.4974707,-74.0678276,12z')
time.sleep(3)

searchPlace = driver.find_element_by_class_name("tactile-searchbox-input")
searchPlace.send_keys('Verizon Store in New York')
driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button').click()
links = []
for i in range(3):
    # try:
        time.sleep(3)
        count = 22
        while count > 1:
            try:
                scrollable_div = driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]')
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                count = count -1
                time.sleep(1)
            except Exception:
                count = 0
        source_code=driver.page_source
        time.sleep(1)    
        soup = BeautifulSoup(source_code,'lxml')
        result =soup.find_all('div',class_='Nv2PK tH5CWc THOPZb')
        for i in result:
            comment = i.find('a', class_='hfpxzc')
            comment = comment.get('href')
            links.append(comment)
        print(len(links))
        driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/button[2]').click()
    # except Exception:
    #     break

verizon_store_url = pd.DataFrame()
verizon_store_url['url'] = links
verizon_store_url.to_csv('verizon_store_url.csv')

time.sleep(2)
driver.quit()
