from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import random

data = pd.read_excel('shoesDataCleaned.xlsx')
urls = [url for url in data['shoeURL']]
shoeNUmber = 1

textDescriptionList = []
colorList = []
estiloList = []
paisOrigenList = []
reviewList = []
calificationList = []

driver = webdriver.Chrome()

for url in data['shoeURL']:
    waitTime = random.randint(0, 2)
    time.sleep(waitTime)
    print(shoeNUmber)

    try:
        driver.get(url)
    except:
        continue

    toggle_xpath = "//div[contains(@class, 'product-info-accordions')]/div/div/details[@id='pdp-info-accordions__reviews-accordion']/summary"

    toggle_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, toggle_xpath))
    )
    toggle_element.click()

    textDescriptionXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@id='product-description-container' or @data-testid='product-description-container']/p"
    colorXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@id='product-description-container' or @data-testid='product-description-container']/ul/li[1]"
    estiloXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@id='product-description-container' or @data-testid='product-description-container']/ul/li[2]"
    paisOrigenXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@id='product-description-container' or @data-testid='product-description-container']/ul/li[3]"

    reviewsXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@class='product-info-accordions mb8-sm']/div/div/details[@id='pdp-info-accordions__reviews-accordion']/summary/span/div/h4"
    calificationXpath = "/html/body/div[5]/div/main/div[2]/div[3]/div[@class='product-info-accordions mb8-sm']/div/div/details[@id='pdp-info-accordions__reviews-accordion']/div/div/div/div[1]/p"

    textDescriptionRaw = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, textDescriptionXpath))
    )
    colorRaw = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, colorXpath))
    )
    estiloRaw = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, estiloXpath))
    )
    paisOrigenRaw = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, paisOrigenXpath))
    )
    reviewsRaw = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, reviewsXpath))
    )
    if calificationXpath:
        calificationRaw = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, calificationXpath))
        )


    textDescriptionInfo = [element.text for element in textDescriptionRaw]
    colorInfo = [element.text for element in colorRaw]
    estiloInfo = [element.text for element in estiloRaw]
    paisOrigenInfo = [element.text for element in paisOrigenRaw]
    reviewInfo = [element.text for element in reviewsRaw]
    calificationInfo = [element.text for element in calificationRaw]

    textDescription = textDescriptionInfo[0]
    color = colorInfo[0]
    estilo = estiloInfo[0]
    paisOrigen = paisOrigenInfo[0]
    review = reviewInfo[0]
    if calificationXpath:
        calification = calificationInfo[0]
    else:
        calification = "0"

    textDescriptionList.append(textDescription)
    colorList.append(color)
    estiloList.append(estilo)
    paisOrigenList.append(paisOrigen)
    reviewList.append(review)
    calificationList.append(calification)

    shoeNUmber += 1

driver.quit()

shoesDescriptionData = {
    "textDescription":textDescriptionList,
    "shoeColor":colorList,
    "shoeStyle":estiloList,
    "shoeMadeIn":paisOrigenList,
    "shoeNumReviews":reviewList,
    "shoeCalification":calificationList
}

shoesDescdf = pd.DataFrame(shoesDescriptionData)
shoesDescdf.index = range(1, len(textDescriptionList) + 1)

excelName = "shoesDescriptionRawDataExcel.xlsx"
shoesDescdf.to_excel(excelName, index=True, sheet_name="RawData")