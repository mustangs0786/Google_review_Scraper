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

missed_url = []
verizon_store_url = pd.read_csv('verizon_store_url.csv')
for id_no,url in enumerate(verizon_store_url['url'].unique()):
    time.sleep(2)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    #driver.get('https://www.google.com/maps/place/Verizon/@40.779407,-73.9569109,17z/data=!3m1!5s0x89c258982c3a3473:0x9af2ffc0e0039886!4m5!3m4!1s0x89c258bc94782bc3:0x57c8ff86c0e0982e!8m2!3d40.779407!4d-73.9547222?authuser=0&hl=en')
    driver.get(url)
    time.sleep(3)
    try:
        source_code=driver.page_source
        time.sleep(1)
        soup = BeautifulSoup(source_code,'lxml')


        address =soup.find('div',class_='Io6YTe fontBodyMedium').text
        print(address)
        driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]/button').click()

        time.sleep(3)
        driver.find_element(By.XPATH, "//button[@data-value='Sort']").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@role='menuitemradio']")))
        driver.find_element(By.XPATH, "(//li[@role='menuitemradio'])[2]").click()
        time.sleep(3)
        count = 30
        while count > 1:
            try:
                scrollable_div = driver.find_element_by_css_selector('div.siAUzd-neVct.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc')
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                count = count -1
                time.sleep(1)
            except Exception:
                count = 0


        time.sleep(3)
        source_code=driver.page_source
        time.sleep(1)
        soup = BeautifulSoup(source_code,'lxml')

        result =soup.find_all('div',class_='ODSEW-ShBeI-ShBeI-content')
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
        print(len(final_date))
        print(len(final_text))
        review = pd.DataFrame()
        review['review'] = final_text
        review['Date'] = final_date
        review['address'] = address
        review.to_csv(f'review_{id_no}.csv')
        time.sleep(2)
        driver.quit()
    except Exception:
        missed_url.append(url)
        print(missed_url)


pd.DataFrame(missed_url).to_csv('missed_url.csv')