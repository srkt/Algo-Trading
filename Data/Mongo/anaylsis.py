from Data.Mongo.server_info import server
import util.utility as util
import pandas as pd

sector_xlsx = "C:\\Users\\suman\\Desktop\\SectorAnalysis.xlsx"


def get_marketcap_def(market_cap):
    if not market_cap:
        return 'Unknown'

    if market_cap < 0.3:
        return 'Penny'

    if market_cap < 2:
        return 'Small'

    if market_cap < 10:
        return 'Mid'

    return 'Large'


def SectorAnalysis():
    fundamentals = server \
        .get_dataframe_from_collection('fundamentalInfo',
                                       query={"stock": {"$regex": "^[a-zA-Z]+$"}})

    sector_info = server \
        .get_dataframe_from_collection('sectorInfo', projection={
        '_id': 0,
        'Sector Code': 1,
        'Sector Name': 1,
        'Industry Name': 1,
        'Industry Code': 1
    })

    # [['Sector Code', 'Sector Name', 'Industry Name', 'Industry Code']]

    sector_groups = fundamentals.groupby('sec_code')

    excel = util.Excel(sector_xlsx)

    for sector_id, sector in sector_groups:
        print(sector_id)
        capsize = sector.groupby(sector['market_cap'].apply(lambda s: get_marketcap_def(s)))

        for name, stocks in capsize:
            print(name)
            print(stocks)

            result = pd.merge(sector_info.drop_duplicates(),
                              stocks,
                              right_on=['sec_code', 'ind_code'],
                              left_on=['Sector Code', 'Industry Code'],
                              how='inner')

            cols = ['Sector Name', 'Industry Name', 'divi_ps', 'market_cap', 'pb_ratio', 'pe_ratio', 'roe', 'stock',
                    'value_score']
            excel.generate(result[cols], str(sector_id) + ' ' + name)
            # util.to_excel(stocks, sector_xlsx, str(sector_id) + ' ' + name)

    excel.save()


SectorAnalysis()
