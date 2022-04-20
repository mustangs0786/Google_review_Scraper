from selenium import webdriver    #  //span[@class='ODSEW-ShBeI-text']
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
driver.get("https://www.google.com/maps/place/Burger+King/@32.0011625,75.3330782,10z/data=!4m11!1m2!2m1!1sburger+king!3m7!1s0x391b9b0d711774a3:0x8054ed6e05863858!8m2!3d32.0011625!4d75.6132296!9m1!1b1!15sCgtidXJnZXIga2luZyIDiAEBWg0iC2J1cmdlciBraW5nkgEUZmFzdF9mb29kX3Jlc3RhdXJhbnSaASNDaFpEU1VoTk1HOW5TMFZKUTBGblNVTnRiWEJtUW1aQkVBRQ")
# driver.get('https://www.google.com/maps/place/Verizon/@40.7777231,-74.0414055,12z/data=!4m11!1m2!2m1!1sverizon+store+in+New+York!3m7!1s0x89c259a26ba0fbcf:0x63396e33ee80e2ac!8m2!3d40.7373605!4d-73.9903984!9m1!1b1!15sChl2ZXJpem9uIHN0b3JlIGluIE5ldyBZb3JrIgOIAQFaGyIZdmVyaXpvbiBzdG9yZSBpbiBuZXcgeW9ya5IBEGNlbGxfcGhvbmVfc3RvcmU')
# driver.get('https://www.google.com/maps/place/Verizon/@40.7777231,-74.0414055,12z/data=!3m1!5s0x89c258982c3a3473:0x9af2ffc0e0039886!4m11!1m2!2m1!1sverizon+store+in+New+York!3m7!1s0x89c258bc94782bc3:0x57c8ff86c0e0982e!8m2!3d40.779407!4d-73.9547222!9m1!1b1!15sChl2ZXJpem9uIHN0b3JlIGluIE5ldyBZb3JrIgOIAQFaGyIZdmVyaXpvbiBzdG9yZSBpbiBuZXcgeW9ya5IBEGNlbGxfcGhvbmVfc3RvcmU')
print(driver.title)
time.sleep(5)
driver.find_element(By.XPATH, "//button[@data-value='Sort']").click()
WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@role='menuitemradio']")))
driver.find_element(By.XPATH, "(//li[@role='menuitemradio'])[2]").click()
time.sleep(10)
count = 30
while count > 1:
    try:
        scrollable_div = driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        count = count -1
        time.sleep(1)
    except Exception:
        count = 0


time.sleep(3)
source_code=driver.page_source
time.sleep(2)
soup = BeautifulSoup(source_code,'lxml')

result =soup.find_all('div',class_='MyEned')
# print(result)
print(len(result))
final_text = []
for i in result:
    comment = i.find('span', class_='ODSEW-ShBeI-text').text
    final_text.append(comment)



result =soup.find_all('div',class_='DU9Pgb')
final_date = []
for i in result:
    date = i.find('span', class_='ODSEW-ShBeI-RgZmSc-date').text 
    final_date.append(date)


result =soup.find_all('div',class_='DU9Pgb')
stars = []
for i in result:
    star = i.find('span', class_='ODSEW-ShBeI-H1e3jb').get('aria-label')
    stars.append(star)


print(len(final_date))
print(len(final_text))
print(len(stars))
review = pd.DataFrame()
review['review'] = final_text
review['Date'] = final_date
review['star']  = stars
review.to_csv('review.csv')

time.sleep(2)
driver.quit()
