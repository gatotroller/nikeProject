import pandas as pd
from collections import Counter
import string
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, ForeignKey, Text, inspect, text as sa_text


pd.set_option("display.max_columns", None)

nikeData = pd.read_excel("nikeData.xlsx")
nikeData = nikeData[nikeData['shoeMadeIn'] != "Not released"]
nikeData['id'] = [_ for _ in range(1, nikeData.shape[0] + 1)]

# Mover a otra tabla shoeURL, textDescription, shoeStyle
moveColums = ['shoeURL', 'textDescription', 'shoeStyle']
nikeDataAuxiliar = nikeData[moveColums].copy()
nikeDataAuxiliar['shoeId'] = [_ for _ in range(1, nikeDataAuxiliar.shape[0] + 1)]
nikeData.drop(moveColums, axis=1, inplace=True)

# Normalizar shoeCategory
categoryUnique = nikeData['shoeCategory'].unique()
categoryId = [_ for _ in range(1, len(categoryUnique) + 1)]
categoryDict = {
    "categoryId": categoryId,
    "category": categoryUnique
}
categoryDf = pd.DataFrame(categoryDict)

mappingCategory = dict(zip(categoryDf['category'], categoryDf['categoryId']))
nikeData['shoeCategory'] = nikeData['shoeCategory'].map(mappingCategory)
nikeData.rename(columns={'shoeCategory': 'categoryId'}, inplace=True)


# Normalizar shoeMadeIn
MadeInUnique = nikeData['shoeMadeIn'].unique()
madeInId = [_ for _ in range(1, len(MadeInUnique) + 1)]
madeInDict = {
    "madeInId": madeInId,
    "shoeMadeIn": MadeInUnique
}
MadeInDf = pd.DataFrame(madeInDict)

mappingMadeIn = dict(zip(MadeInDf['shoeMadeIn'], MadeInDf['madeInId']))
nikeData['shoeMadeIn'] = nikeData['shoeMadeIn'].map(mappingMadeIn)
nikeData.rename(columns={'shoeMadeIn': 'madeInId'}, inplace=True)


# Contador de palabras
def cleanText(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

excludeWords = {'y', 'de', 'la', 'que', 'los', 'el', 'para', 'con', 'en', 'a', 'un', 'una', 'tu', 'más', 'te', 'del', 'las', 'se', 'al', 
                'estos', 'por', 'lo', 'son', 'parte', 'es', 'su', 'tus', 'hasta', 'como', 'además', 'o', 'no', 'están'}

wordCounter = Counter()

for text in nikeDataAuxiliar['textDescription']:
    words = cleanText(text).split()
    cleanWords = [word for word in words if word not in excludeWords]
    wordCounter.update(cleanWords)

# Convertir el Counter a DataFrame
wordsDf = pd.DataFrame(list(wordCounter.items()), columns=['word', 'count'])
wordsDf.sort_values(by='count', ascending=False, inplace=True)
wordsDf.reset_index(drop=True, inplace=True)
wordsDf['wordId'] = range(1, wordsDf.shape[0] + 1)

# Dropear columnas de ID
categoryDf.drop('categoryId', axis=1, inplace=True)
MadeInDf.drop('madeInId', axis=1, inplace=True)
wordsDf.drop('wordId', axis=1, inplace=True)
nikeDataAuxiliar.drop('shoeId', axis=1, inplace=True)
nikeData.drop('id', axis=1, inplace=True)

# Exportar a SQL: nikeData, nikeDataAuxiliar, categoryDf, madeInDf, wordsDf

server = 'gatotroller\SQLEXPRESS'
database = 'nikeDatabase'
driver = 'ODBC Driver 17 for SQL Server'
connection_string = (
    f"mssql+pyodbc://{server}/{database}"
    f"?driver={driver.replace(' ', '+')}&trusted_connection=yes"
)
engine = create_engine(connection_string)

metadata = MetaData()

MadeInSql = Table (
    'madeInTable', metadata,
    Column('madeInId', Integer, primary_key=True, autoincrement=True),
    Column('shoeMadeIn', Text)
)

categorySql = Table (
    'categoryTable', metadata,
    Column('categoryId', Integer, primary_key=True, autoincrement=True),
    Column('category', Text)
)

wordsSql = Table (
    'wordsTable', metadata,
    Column('word', Text),
    Column('count', Integer),
    Column('wordId', Integer, primary_key=True, autoincrement=True)
)

nikeDataAuxiliarSql = Table(
    'nikeDataAuxiliar', metadata,
    Column('shoeURL', Text),
    Column('textDescription', Text),
    Column('shoeStyle', Text),
    Column('shoeId', Integer, primary_key=True, autoincrement=True)
)

nikeDataSql = Table(
    'nikeData', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('shoeName', Text),
    Column('categoryId', Integer, ForeignKey('categoryTable.categoryId')),
    Column('shoeSubCategory', Text),
    Column('shoePrice', Float),
    Column('shoeImageURL', Text),
    Column('shoeColor', Text),
    Column('madeInId', Integer, ForeignKey('madeInTable.madeInId')),
    Column('shoeNumReviews', Float),
    Column('shoeCalification', Float)
)

inspector = inspect(engine)
for table_name in ['madeInTable', 'categoryTable', 'wordsTable', 'nikeDataAuxiliar', 'nikeData']:
    if inspector.has_table(table_name):
        with engine.begin() as conn:
            count = conn.execute(sa_text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            if count and count > 0:
                conn.execute(sa_text(f"DROP TABLE {table_name}"))

metadata.create_all(engine)

categoryDf.to_sql('categoryTable', engine, if_exists='append', index=False)
MadeInDf.to_sql('madeInTable', engine, if_exists='append', index=False)
wordsDf.to_sql('wordsTable', engine, if_exists='append', index=False)
nikeDataAuxiliar.to_sql('nikeDataAuxiliar', engine, if_exists='append', index=False)
nikeData.to_sql('nikeData', engine, if_exists='append', index=False)

