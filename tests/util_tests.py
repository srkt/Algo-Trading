import pandas as pd
import util.utility as ut
import json

path = "C:\\Users\\suman\\Desktop\\\pe-lt-30-pb-lt-15\\"
file_names = ['Small Cap', 'Mid Cap', 'Large Cap']
ext = '.txt'

sector_path = "C:\\Users\\suman\\Desktop\\Sector Information.csv"
fundamentals_path = "C:\\Users\\suman\\Desktop\\FundamentalInfo.txt"


def StockImport():
    for fn in file_names:
        stock_frame = pd.read_csv(path + fn + ext, delimiter="\s+", encoding='utf-8')

        stock_frame = stock_frame[
            (stock_frame['divi_ps'] > 0) &
            (stock_frame['roe'] > 0) &
            (stock_frame['value_score'] > 80)
            ]
        print(stock_frame)

    # stock_frame = pd.read_csv(path, delimiter="\s+")


def SectorImport(cap_size):
    sector_info = pd.read_csv(sector_path, delimiter=",", encoding='utf-8')
    stock_frame = pd.read_csv(path + cap_size + ext, delimiter="\s+", encoding='utf-8')

    result = pd.merge(sector_info[['Sector Code', 'Sector Name', 'Industry Name', 'Industry Code']].drop_duplicates(),
                      stock_frame,
                      right_on=['sec_code', 'ind_code'],
                      left_on=['Sector Code', 'Industry Code'],
                      how='inner')

    ut.to_excel(result[['ticker', 'Sector Name', 'Industry Name', 'close', 'roe', 'value_score', 'divi_ps']],
                'C:\\Users\\suman\\Desktop\\' + cap_size + '.xlsx')


def ImportFromJson():
    # res = pd.read_json(fundamentals_path, orient='records')
    # print(res.head())
    text = open(fundamentals_path, 'r')
    x = text.read()
    r = json.loads(x)
    print(pd.DataFrame(r))


ImportFromJson()
