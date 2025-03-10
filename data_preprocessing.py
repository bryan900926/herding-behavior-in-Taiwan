import duckdb
import pandas as pd 
import os 

conn = duckdb.connect('mydb.db')
def catogorize(start_year,end_year):  
  for year in range(start_year,end_year+1):
    conn.execute(f"ALTER TABLE tw_table_{year} ADD COLUMN classification VARCHAR;")
    query = f"""
    UPDATE tw_table_{year}
    SET classification = CASE
            WHEN TSE舊產業名 IN ('M1500 電機機械', 'M2200 汽車工業', 'M2300 電子工業', 'M1600 電器電纜', 'M3600 數位雲端') THEN 'Technology and Electronics'
            WHEN TSE舊產業名 IN ('M2000 鋼鐵工業', 'M1700 化學生技醫', 'M1400 紡織纖維', 'M1800 玻璃陶瓷', 
                                 'M1100 水泥工業', 'M1300 塑膠工業', 'M2500 建材營造', 'M2100 橡膠工業', 'M2900 貿易百貨') THEN 'Manufacturing and Materials'
            WHEN TSE舊產業名 IN ('M3500 綠能環保', 'M9700 油電燃') THEN 'Energy and Environment'
            WHEN TSE舊產業名 IN ('M2800 金融業') THEN 'Finance and Insurance'
            WHEN TSE舊產業名 IN ('M3800 居家生活', 'M1200 食品工業', 'M3700 運動休閒', 'M2900 貿易百貨') THEN 'Consumer Goods and Services'
            WHEN TSE舊產業名 IN ('M2700 觀光餐旅') THEN 'Tourism and Leisure'
            WHEN TSE舊產業名 IN ('M3300 農業科技') THEN 'Agriculture and Biotechnology'
            WHEN TSE舊產業名 IN ('M3200 文化創意業') THEN 'Cultural and Creative Industries'
            WHEN TSE舊產業名 IN ('M1900 造紙工業') THEN 'Paper and Packaging'
            WHEN TSE舊產業名 IN ('M9900 其他') THEN 'Miscellaneous'
            WHEN TSE舊產業名 IN ('whole_market') THEN 'Whole Market'
            ELSE 'Uncategorized'
            END;
    """
    conn.execute(query)
# catogorize(2021,2023)
def retrieve_data(date,year):
    query = f""" 
    
    SELECT 年月日 as date, 報酬率％ as return  FROM tw_table_{year} 
    WHERE 證券代碼 = 'Y9999 加權指數' and 年月日 = '{date}' 
    
    """
    
    market_info = conn.execute(query).fetchdf()
    if market_info.empty:
        return 'empty'
    date = market_info['date'][0]
    market_return = market_info['return'][0]
    
    query1 = f"""
    SELECT AVG(ABS(報酬率％ - {market_return})) AS CSAD, classification,  
    FROM tw_table_{year} 
    WHERE 年月日 = '{date}'
    GROUP BY classification
    """
    query2 = f"""
    SELECT AVG(ABS(報酬率％ - {market_return})) AS CSAD,  
    FROM tw_table_{year} 
    WHERE 年月日 = '{date}'
    """    
    csad_df = conn.execute(query1).fetch_df().dropna()
    csad_whole_marekt = conn.execute(query2).fetch_df()['CSAD'][0]
    row = pd.DataFrame({'industrial':['whole_market'],'CSAD':[csad_whole_marekt]})
    csad_df = pd.concat([csad_df,row],ignore_index=True)
    csad_df['date'] = date 
    csad_df['market_return'] = market_return
    filename = r"C:\Users\bryan\OneDrive\桌面\python\計量分析\tw_csad.csv"
    if os.path.isfile(filename):
        csad_df.to_csv(filename, mode='a', header=False, index=False)
    else:
        csad_df.to_csv(filename, mode='w', header=True, index=False)

# for year in range(2021,2023+1):
#     for date in list(pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D')):
#         time = str(date.strftime("%Y-%m-%d"))
#         retrieve_data(time,year)

def import_data(year):
   folder_path = f"C:\\TejPro\\TejPro\\Transfer\\{year}"
   files = os.listdir(folder_path)
   if files:
        first_file = os.path.join(folder_path, files[0])
        print(f"Using file: {first_file}")
   else:
        print(f"No files {year} found in the folder.")
   df = pd.read_csv(first_file,encoding='utf-16',delimiter='\t')
   df['年月日'] = pd.to_datetime(df['年月日'], format='%Y%m%d')
   conn.register("temp_df", df)
   conn.execute(f"""
    CREATE TABLE tw_table_{year} AS SELECT * FROM temp_df
""")  

for i in range(2000,2023+1):
   import_data(i)

conn.close()
