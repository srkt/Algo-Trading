from Data.Mongo.database import MongoServer
import pandas as pd
import json
import util.utility as ut
from trading.pandas_data_reader_api import StockExchange
import datetime as dt
from Data.Mongo.server_info import server

fundamentals_path = "C:\\Users\\suman\\Desktop\\FundamentalInfo.txt"
sector_path = "C:\\Users\\suman\\Desktop\\Sector Information.csv"


# database_name = 'equitydb'
# server.
# # Mongo database info
# server = MongoServer()
# server.set_database_name(database_name)


def ImportSectorInfo():
    sector_csv = pd.read_csv(sector_path, delimiter=",", encoding='utf-8')
    sectorInfo = server.get_collection('sectorInfo')
    sectorInfo.drop()
    sectorInfo.insert_many(sector_csv.to_dict(orient='records'))


def ImportFundamentalsFromMorningStar():
    text = open(fundamentals_path, 'r')
    x = text.read()
    r = json.loads(x)

    fundamentals = server.get_collection('fundamentalInfo')
    fundamentals.drop()
    fundamentals.insert_many(pd.DataFrame(r).to_dict(orient='records'))


def FundamentalAnalysis():
    fundamental_df = server.get_dataframe_from_collection('fundamentalInfo',
                                                          query={"stock": {"$regex": "^[a-zA-Z]+$"}})

    selection = {"_id": 0, "Sector Name": 1, "Sector Code": 1, "Industry Name": 1, "Industry Code": 1}
    sector_info = server.get_dataframe_from_collection('sectorInfo',
                                                       projection=selection).drop_duplicates()

    result = pd.merge(sector_info,
                      fundamental_df,
                      right_on=['sec_code', 'ind_code'],
                      left_on=['Sector Code', 'Industry Code'],
                      how='inner')

    ut.to_excel(result[['stock', 'Sector Name', 'Industry Name',
                        'market_cap', 'roe', 'value_score', 'divi_ps',
                        'pe_ratio', 'pb_ratio']],
                'C:\\Users\\suman\\Desktop\\Fundamentals.xlsx')

    print(fundamental_df.head())


def getStockInfo():
    stock = server.get_dataframe_from_collection('stockInfo',
                                                 projection={"_id": 0})
    print(stock.head())


def get_stockdata(tickers):
    start = dt.datetime(2018, 9, 1)
    end = dt.datetime.now()
    se = StockExchange(source='stooq')
    data = se.get_data(tickers, start, end)
    return data


def ImportStockData():
    fundamental_df = server.get_dataframe_from_collection('fundamentalInfo',
                                                          projection={"_id": 0, "stock": 1},
                                                          query={"stock": {"$regex": "^[a-zA-Z]+$"}})
    tickers = fundamental_df['stock'].tolist()
    tickers_list = [tickers[x:x + 25] for x in range(0, len(tickers), 25)]

    stock_collection = server.get_collection('stockInfo')
    deleted = stock_collection.delete_many({})
    print(deleted.deleted_count, " documents deleted.")

    for tl in tickers_list:
        results = get_stockdata(tl)

        for result in results:
            if not result[1].empty:
                result[1]['Stock'] = result[0].replace('.US', '')
                stock_collection.insert_many(result[1].reset_index().to_dict(orient='records'))
                print(result[0])

    # aapl = server.get_dataframe_from_collection('stockInfo', query={"Stock": {"$eq": "AAPL"}})

# db = db.getDatabase()
# print(db.command("collstats", "stockInfo"))

# FundamentalAnalysis()
# ImportStockData()
# getStockInfo()
