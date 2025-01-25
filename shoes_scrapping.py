from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

url = "https://www.nike.com/mx/w/calzado-y7ok"
driver = webdriver.Chrome()
driver.get(url)

categories_container_xpath = "/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div/div/div[1]/div[2]/div/div/div/div"
categories_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, categories_container_xpath))
    )

category_links = categories_container.find_elements(By.TAG_NAME, "a")

category_names = []
category_hrefs = []

for link in category_links:
    category_names.append(link.text)
    category_hrefs.append(link.get_attribute("href"))

driver.quit()

images_url_list = []
shoe_names_list = []
shoe_type = []
shoe_category_list = []
shoe_prices_list = []
shoe_link_list = []
url_index = 0

for url in category_hrefs:

    driver = webdriver.Chrome()
    driver.get(url)
    cuenta = 1

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    while True:
        print(cuenta)
        try:
            shoe_image_xpath = f"/html/body/div[4]/div/div/div[2]/div[4]/div/div[7]/div[2]/main/section/div/div[{cuenta}]/div/figure/a[2]/div/img"
            shoe_name_xpath = f"/html/body/div[4]/div/div/div[2]/div[4]/div/div[7]/div[2]/main/section/div/div[{cuenta}]/div/figure/div/div[1]/div/div[1]"
            shoe_category_xpath = f"/html/body/div[4]/div/div/div[2]/div[4]/div/div[7]/div[2]/main/section/div/div[{cuenta}]/div/figure/div/div[1]/div/div[2]"
            shoe_price_xpath = f"/html/body/div[4]/div/div/div[2]/div[4]/div/div[7]/div[2]/main/section/div/div[{cuenta}]/div/figure/div/div[3]/div/div/div/div"
            shoe_link_xpath = f"/html/body/div[4]/div/div/div[2]/div[4]/div/div[7]/div[2]/main/section/div/div[{cuenta}]/div/figure/a[2]"

            shoe_image_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, shoe_image_xpath))
            )
            shoe_name_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, shoe_name_xpath))
            )
            shoe_category_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, shoe_category_xpath))
            )
            shoe_price_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, shoe_price_xpath))
            )
            shoe_link_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, shoe_link_xpath))
            )

            shoe_image = shoe_image_raw.get_attribute("src")
            shoe_name = shoe_name_raw.text
            shoe_category = shoe_category_raw.text
            shoe_price = shoe_price_raw.text
            shoe_link = shoe_link_raw.get_attribute("href")

            images_url_list.append(shoe_image)
            shoe_names_list.append(shoe_name)
            shoe_type.append(category_names[url_index])
            shoe_category_list.append(shoe_category)
            shoe_prices_list.append(shoe_price)
            shoe_link_list.append(shoe_link)
            cuenta += 1

        except Exception as e:
            print(f"Elemento no encontrado para el zapato {cuenta}: {e}")
            url_index += 1
            break

    driver.quit()

shoePriceList = [shoe.replace('$', '').replace(',', '') for shoe in shoe_prices_list]
shoePriceList = [int(shoe) for shoe in shoePriceList]

shoesData = {
    "shoeName":shoe_names_list,
    "shoeCategory":shoe_type,
    "shoeSubCategory":shoe_category_list,
    "shoePrice":shoePriceList,
    "shoeURL":shoe_link_list,
    "shoeImageURL":images_url_list
}

shoesdf = pd.DataFrame(shoesData)
shoesdf.index = range(1, len(shoe_names_list) + 1)

excelName = "shoesDataExcel.xlsx"
shoesdf.to_excel(excelName, index=True, sheet_name="Data")