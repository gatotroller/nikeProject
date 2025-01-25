import pandas as pd

dfShoes = pd.read_excel("shoesDataExcel.xlsx")
dfShoes.fillna('', inplace=True)


dfShoes.drop(['Unnamed: 0'], axis=1, inplace=True)

dfShoes['temporaryColumn'] = (
    dfShoes['shoeName'].str.strip().str.lower() +
    dfShoes['shoeCategory'].str.strip().str.lower() +
    dfShoes['shoeSubCategory'].str.strip().str.lower() +
    dfShoes['shoePrice'].astype(str)
)

dfShoes.drop_duplicates(subset=['temporaryColumn'], inplace=True)
dfShoes.drop(['temporaryColumn'], axis=1, inplace=True)
dfShoes.reset_index(drop=True, inplace=True)
dfShoes['id'] = range(1, len(dfShoes) + 1)
dfShoes = dfShoes[['id'] + [col for col in dfShoes.columns if col != 'id']]

dfShoes.to_excel("shoesDataCleaned.xlsx", index=False)

print(dfShoes)