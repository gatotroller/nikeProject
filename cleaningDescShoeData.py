import pandas as pd
import numpy as np

def cleanCountries(country):
    if country == "Not released":
        return country
    return ", ".join(sorted(country.split(", ")))

def cleanColors(color):
    if color == "Not released":
        return color
    else:
        colors = color.split("/")
        colors = set(colors)
        colors = list(colors)
        return "/".join(sorted(colors))

nikeShoesDf = pd.read_excel('shoesDataCleaned.xlsx')
shoesDf = pd.read_excel('shoesDescriptionRawDataExcel.xlsx')

shoesDf.drop(['Unnamed: 0'], axis=1, inplace=True)

shoesDf['shoeColor'] = shoesDf['shoeColor'].apply(lambda x: x.split(": ", 1)[-1] if ": " in x else x)
shoesDf['shoeStyle'] = shoesDf['shoeStyle'].apply(lambda x: x.split(": ", 1)[-1] if ": " in x else x)
shoesDf['shoeMadeIn'] = shoesDf['shoeMadeIn'].apply(lambda x: x.split(": ", 1)[-1] if ": " in x else x)

shoesDf['shoeNumReviews'] = shoesDf['shoeNumReviews'].str.split("(").str[-1].str.rstrip(")")
shoesDf['shoeNumReviews'] = pd.to_numeric(shoesDf['shoeNumReviews'], errors='coerce')

shoesDf['shoeCalification'] = shoesDf['shoeCalification'].str.split(' ').str[0]
shoesDf['shoeCalification'] = pd.to_numeric(shoesDf['shoeCalification'], errors='coerce')

nikeDataDf = pd.concat([nikeShoesDf, shoesDf], axis=1)
nikeDataDf['shoeMadeIn'] = nikeDataDf['shoeMadeIn'].apply(cleanCountries)
nikeDataDf['shoeColor'] = nikeDataDf['shoeColor'].apply(cleanColors)

excelName = "nikeData.xlsx"
nikeDataDf.to_excel(excelName, index=False, sheet_name="Data")