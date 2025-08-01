#導入套件
import math
import pandas as pd
import re
import os

def run(total_budget, p_attraction, p_restaurant, p_hotel, input_day, input_preference, total_day):

    def data_verification(total_budget, p_attraction, p_restaurant, p_hotel):
        data_verification = True
        if not str(total_budget).isdigit() or not str(p_attraction).isdigit() or not str(p_restaurant).isdigit() or not str(p_hotel).isdigit():
            return False
        if int(p_attraction) + int(p_restaurant) + int(p_hotel) != 100:
            return False
        if total_day == 0:
            return False
        return data_verification

    #分配預算給景點、餐廳、住宿、車資
    def calculate_budget_distribution(total_budget, p_attraction, p_restaurant, p_hotel, input_day, total_day):

        total_budget = int(total_budget)
        p_attraction = int(p_attraction)
        p_restaurant = int(p_restaurant)
        p_hotel = int(p_hotel)

        #計算車資
        fare = 0
        if total_day <= 7:
            fare += 1000
            total_budget -= 1000
        else:
            fare += 2000
            total_budget -= 2000

        budget_attraction = round(total_budget * p_attraction / 100)
        budget_restaurant = round(total_budget * p_restaurant / 100)
        budget_hotel = round(total_budget * p_hotel / 100)

        days = {'Queens': input_day[0], 'Bronx': input_day[1], 'Manhattan': input_day[2], 'Brooklyn': input_day[3],
                'StatenIsland': input_day[4], 'totalday': total_day}
        location = ['Queens', 'Bronx', 'Manhattan', 'Brooklyn', 'StatenIsland']

        #計算每區的景點和餐廳預算，以及每日的住宿預算
        district_attraction_budget = []
        district_restaurant_budget = []
        daily_hotel_budget = []
        for i in range(len(location)):
            district_attraction_budget.append(round(budget_attraction * (days.get(location[i]) / days.get('totalday'))))
            district_restaurant_budget.append(round(budget_restaurant * (days.get(location[i]) / days.get('totalday'))))
        daily_hotel_budget.append(round(budget_hotel / (days.get('totalday')-1) * 1.1))
        daily_hotel_budget.append(round(budget_hotel / (days.get('totalday')-1) * 0.9))
        return days, district_attraction_budget, district_restaurant_budget, daily_hotel_budget, fare
#輸入資料
    # total_budget = i
    # p_attraction = input()
    # p_restaurant = input()
    # p_hotel = input()
    # input_day = input().split(',')
    # input_preference = input()

    #計算總天數
    total_day = 0
    for i in range(5):
        input_day[i] = int(input_day[i])
        total_day += input_day[i]

    #帶入資料驗證、預算分配函數
    data_verification = data_verification(total_budget, p_attraction, p_restaurant, p_hotel)
    if data_verification == True:
        days, district_attraction_budget, district_restaurant_budget, daily_hotel_budget, fare = calculate_budget_distribution(total_budget, p_attraction, p_restaurant, p_hotel, input_day,total_day)
    elif data_verification == False:
        # print('請重新輸入!')
        error_message = '請重新輸入!'
        return error_message

    #偏好中文轉英文
    preference = 'NA'
    if input_preference == '分數':
        preference = 'Score'
    elif input_preference == '評論數':
        preference = 'Comment'
    elif input_preference == '人氣指數':
        preference = 'Popularity'
    ##########################################################################

    #整理住宿資料
    #五大區依序跑入迴圈
    hotellocation = ['Queens','Bronx','Manhattan','Brooklyn','StatenIsland']
    for i in range(5):
        # 讀取 csv 檔案，假設該檔案名稱為 data.csv，且數據位於第一個工作表
        df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/' + hotellocation[i]+'hotel.csv')
        pd.set_option('display.max_colwidth', 200)

        #抓取店名的字串並輸出
        def extract_availability(row):
            if "Breakfast included" in row[0]:
                return row[1]
            match = re.search(r"See availability\s*(.*)", str(row), re.IGNORECASE)
            if match:
                return match.group(1)
            else:
                return None
        df["Name"] = df.apply(extract_availability, axis=1)
        column = 'Name'
        df = df.dropna(subset = [column])

        #抓取價錢並輸出
        def extract_price(row):
            for column in df.columns:
                text = str(row[column]).replace(',' , '')
                match = re.search(r"TWD\s*(\d+)", text, re.IGNORECASE)
                if match:
                    TWD = match.group(1)
                    TWD = int(TWD.replace(",", ""))
                    return round(TWD * 1.07)
            return None
        df["Price"] = df.apply(extract_price, axis=1)

        #抓取評論數並輸出
        def extract_reviews(row):
            for column in df.columns:
                text = str(row[column]).replace(',' , '')
                match = re.search(r"(\d+)\s*reviews", text, re.IGNORECASE)
                if match:
                    reviews = match.group(1)
                    reviews = int(reviews.replace(",", ""))
                    return reviews
            return None
        df["Comment"] = df.apply(extract_reviews, axis=1)

        #抓取分數並輸出
        def check_format(value):
            if pd.isna(value):
                return False
            match = re.search(r"^\d\.\d$", str(value))
            if match:
                return True
            else:
                return False
        for column in df.columns:
            new_column_name = column + "_filtered"
            df[new_column_name] = df[column].apply(lambda x: x if check_format(x) else None)
        def extract_values(row):
            values = []
            for column in df.columns:
                value = row[column]
                if check_format(value):
                    values.append(value)
            return values[0] if values else None
        df["Score"] = df.apply(extract_values, axis=1)

        #計算人氣指數，將分數和評論數相乘
        df['Score'] = df['Score'].astype(float)
        df['Comment'] = df['Comment'].astype(float)
        df['Popularity'] = df['Score'] * df['Comment']

        #依照偏好輸出不同的資料
        #分數
        def hotel_prefer_score(df):
            column = 'Score'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df
        #評論數
        def hotel_prefer_comments(df):
            column = 'Comment'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df
        #人氣指數
        def hotel_prefer_popularity(df):
            column = 'Popularity'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df

        if preference == 'Score':
            df = hotel_prefer_score(df)
        elif preference == 'Comment':
            df = hotel_prefer_comments(df)
        elif preference == 'Popularity':
            df = hotel_prefer_popularity(df)

    #輸出只包含店名、價錢、分數、評論數、人氣指數新資料檔，分區儲存
    #hotellocation = ['Queens','Bronx','Manhattan','Brooklyn','StatenIsland']
        if i == 0:
            Queens_hotel = df[['Name', 'Price', 'Score', 'Comment', 'Popularity']]
        elif i == 1:
            Bronx_hotel = df[['Name', 'Price', 'Score', 'Comment', 'Popularity']]
        elif i == 2:
            Manhattan_hotel = df[['Name', 'Price', 'Score', 'Comment', 'Popularity']]
        elif i == 3:
            Brooklyn_hotel = df[['Name', 'Price', 'Score', 'Comment', 'Popularity']]
        elif i == 4:
            StatenIsland_hotel = df[['Name', 'Price', 'Score', 'Comment', 'Popularity']]
    ######################################################################################

    #住宿演算法，分區輸出結果
    def filter_hotel(daily_hotel_budget, days, Queens_hotel, Bronx_hotel, Manhattan_hotel, Brooklyn_hotel, StatenIsland_hotel):

        Queenshoteloutput = []
        Bronxhoteloutput = []
        Manhattanhoteloutput = []
        Brooklynhoteloutput = []
        StatenIslandhoteloutput = []

        if days.get('Queens') > 0:
            for i in range(len(Queens_hotel['Price'])):
                if daily_hotel_budget[0] > Queens_hotel.loc[i,'Price'] > daily_hotel_budget[1] and len(Queenshoteloutput) < 6:
                    data = Queens_hotel.loc[i, 'Name']
                    Queenshoteloutput.append(data)
                    data = Queens_hotel.loc[i, 'Price']
                    Queenshoteloutput.append(data)
                elif len(Queenshoteloutput) == 6:
                    break
            if len(Queenshoteloutput) != 6:
                for i in range(6 - len(Queenshoteloutput)):
                    Queenshoteloutput.append(None)

        if days.get('Bronx') > 0:
            for j in range(len(Bronx_hotel['Price'])):
                if daily_hotel_budget[0] > Bronx_hotel.loc[j,'Price'] > daily_hotel_budget[1] and len(Bronxhoteloutput) < 6:
                    data = Bronx_hotel.loc[j, 'Name']
                    Bronxhoteloutput.append(data)
                    data = Bronx_hotel.loc[j, 'Price']
                    Bronxhoteloutput.append(data)
                elif len(Bronxhoteloutput) == 6:
                    break
            if len(Bronxhoteloutput) != 6:
                for i in range(6 - len(Bronxhoteloutput)):
                    Bronxhoteloutput.append(None)

        if days.get('Manhattan') > 0:
            for j in range(1,len(Manhattan_hotel['Price'])):
                if daily_hotel_budget[0] > Manhattan_hotel.loc[j,'Price'] > daily_hotel_budget[1] and len(Manhattanhoteloutput) < 6:
                    data = Manhattan_hotel.loc[j, 'Name']
                    Manhattanhoteloutput.append(data)
                    data = Manhattan_hotel.loc[j, 'Price']
                    Manhattanhoteloutput.append(data)
                elif len(Manhattanhoteloutput) == 6:
                    break
            if len(Manhattanhoteloutput) != 6:
                for i in range(6 - len(Manhattanhoteloutput)):
                    Manhattanhoteloutput.append(None)

        if days.get('Brooklyn') > 0:
            for j in range(len(Brooklyn_hotel['Price'])):
                if daily_hotel_budget[0] > Brooklyn_hotel.loc[j,'Price'] > daily_hotel_budget[1] and len(Brooklynhoteloutput) < 6:
                    data = Brooklyn_hotel.loc[j, 'Name']
                    Brooklynhoteloutput.append(data)
                    data = Brooklyn_hotel.loc[j, 'Price']
                    Brooklynhoteloutput.append(data)
                elif len(Brooklynhoteloutput) == 6:
                    break
            if len(Brooklynhoteloutput) != 6:
                for i in range(6 - len(Brooklynhoteloutput)):
                    Brooklynhoteloutput.append(None)

        if days.get('StatenIsland') > 0:
            for j in range(len(StatenIsland_hotel['Price'])):
                if daily_hotel_budget[0] > StatenIsland_hotel.loc[j,'Price'] > daily_hotel_budget[1] and len(StatenIslandhoteloutput) < 6:
                    data = StatenIsland_hotel.loc[j, 'Name']
                    StatenIslandhoteloutput.append(data)
                    data = StatenIsland_hotel.loc[j, 'Price']
                    StatenIslandhoteloutput.append(data)
                elif len(StatenIslandhoteloutput) == 6:
                    break
            if len(StatenIslandhoteloutput) != 6:
                for i in range(6 - len(StatenIslandhoteloutput)):
                    StatenIslandhoteloutput.append(None)

        return Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput

    if data_verification == True:
        Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput= filter_hotel(daily_hotel_budget, days, Queens_hotel, Bronx_hotel, Manhattan_hotel, Brooklyn_hotel, StatenIsland_hotel)
    ###################################################################################

    #整理餐廳資料
    #五大區依序跑入迴圈
    restaurantlocation = ['Queens', 'Bronx', 'Manhattan', 'Brooklyn', 'StatenIsland']
    for j in range(5):
        df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/' + restaurantlocation[j] + 'Restaurant.csv')
        pd.set_option('display.max_colwidth', 200)

        # 將價格轉為數字並輸出
        price_mapping = {'·$': 300, '·$$': 750, '·$$$': 1350, '·$$$$': 1500}
        df['Price'] = df['Price'].map(price_mapping).fillna(700)

        # 整理營業時間並輸出
        df['Operating Time'] = df['Opening time'].str.extract(r'(\d{2}:\d{2} 到 \d{2}:\d{2})')
        df['Operating Time'] = df['Operating Time'].fillna('NA')
        for i in range(len(df['Operating Time'])):
            df.loc[i, 'Operating at noon'] = 'True'
            df.loc[i, 'Operating Time'] = str(df.loc[i, 'Operating Time'])
            if df.loc[i, 'Operating Time'] != 'NA':
                character = df.loc[i, 'Operating Time']
                if int(character[0:2]) > 13:
                    df.loc[i, 'Operating at noon'] = 'False'

        # 進行分區並出出
        df['Post code'] = df['Address'].str.extract(r'(\d{5})美國')
        A = [
            [11105, 11102, 11106, 11101, 11103, 11104, 11371, 11369, 11370, 11377, 11378, 11372, 11373, 11368, 11374, 11379,
            11375, 11385, 11424, 11415, 11418, 11421, 11419, 11416, 11417, 11420, 11414],
            [10471, 10470, 10466, 10475, 10464, 10463, 10467, 10469, 10468, 10458, 10462, 10461, 10453, 10457, 10460],
            [10034, 10040, 10033, 10032, 10031, 10039, 10030, 10037, 10027, 10026, 10035, 10025, 10029, 10000, 10024, 10128,
            10028, 10075, 10021, 10023, 10065],
            [11222, 11237, 11211, 11206, 11221, 11233, 11208, 11207, 11239, 11212, 11236, 11205, 11216, 11213, 11203, 11249],
            [10301, 10302, 10303, 10304, 10305, 10310]]
        B = [
            [11356, 11351, 11357, 11360, 11359, 11354, 11358, 11361, 11355, 11363, 11367, 11365, 11364, 11362, 11432, 11423,
            11366, 11428, 11427, 11426, 11004, 11005, 11435, 11451, 11433, 11412, 11411, 11429, 11436, 11434, 11422],
            [10452, 10456, 10459, 10472, 10473, 10465, 10451, 10455, 10474, 10454],
            [10019, 10022, 10020, 10036, 10017, 10018, 10016, 10001, 10010, 10011, 10003, 10025, 10009, 10012, 10013, 10002,
            10007, 10038, 10005, 10282, 10280, 10006, 10004],
            [11201, 11217, 11238, 11225, 11234, 11231, 11215, 11226, 11210, 11232, 11218, 11230, 11229, 11235, 11220, 11219,
            11204, 11223, 11209, 11228, 11214, 11224, 11425], [10306, 10307, 10308, 10309, 10312, 10311, 10314]]
        A[j] = [str(x) for x in A[j]]
        B[j] = [str(x) for x in B[j]]

        for i in range(len(df['Post code'])):
            df.loc[i, 'District'] = 'C'
            if df.loc[i, 'Post code'] in A[j]:
                df.loc[i, 'District'] = 'A'
            elif df.loc[i, 'Post code'] in B[j]:
                df.loc[i, 'District'] = 'B'

        # 整理分數和評論數資料，並計算人氣指數，將分數和評論數相乘
        df[['Score', 'Comment']] = df['Rating'].str.split('\n', expand=True)
        df['Comment'] = df['Comment'].str.strip('()').str.replace(',', '')
        df['Score'] = df['Score'].astype(float)
        df['Comment'] = df['Comment'].astype(float)
        df['Popularity'] = df['Score'] * df['Comment']

        # 依照偏好輸出不同的資料
        # 分數
        def restaurant_prefer_score(df):
            column = 'Score'
            df = df.dropna(subset=[column])
            df = df.sort_values(by=column, ascending=False).round(1)
            df = df.reset_index(drop=True)
            return df
        # 評論數
        def restaurant_prefer_comments(df):
            column = 'Comment'
            df = df.dropna(subset=[column])
            df = df.sort_values(by=column, ascending=False).round(1)
            df = df.reset_index(drop=True)
            return df
        # 人氣指數
        def restaurant_prefer_popularity(df):
            column = 'Popularity'
            df = df.dropna(subset=[column])
            df = df.sort_values(by=column, ascending=False).round(1)
            df = df.reset_index(drop=True)
            return df

        if preference == 'Score':
            df = restaurant_prefer_score(df)
        elif preference == 'Comment':
            df = restaurant_prefer_comments(df)
        elif preference == 'Popularity':
            df = restaurant_prefer_popularity(df)

        # 輸出只包含店名、價錢、分數、評論數、人氣指數、郵遞區號、營業時間、區域新資料檔，分區儲存
        # restaurantlocation = ['Queens','Bronx','Manhattan','Brooklyn','StatenIsland']
        if j == 0:
            Queens_restaurant = df[['Restaurant', 'Price', 'Score', 'Comment', 'Popularity', 'Post code', 'Operating at noon', 'District']]
        elif j == 1:
            Bronx_restaurant = df[['Restaurant', 'Price', 'Score', 'Comment', 'Popularity', 'Post code', 'Operating at noon', 'District']]
        elif j == 2:
            Manhattan_restaurant = df[['Restaurant', 'Price', 'Score', 'Comment', 'Popularity', 'Post code', 'Operating at noon', 'District']]
        elif j == 3:
            Brooklyn_restaurant = df[['Restaurant', 'Price', 'Score', 'Comment', 'Popularity', 'Post code', 'Operating at noon', 'District']]
        elif j == 4:
            StatenIsland_restaurant = df[['Restaurant', 'Price', 'Score', 'Comment', 'Popularity', 'Post code', 'Operating at noon', 'District']]
    ###############################################################################################

    #整理景點資料
    #五大區依序跑入迴圈
    attractionlocation = ['Queens', 'Bronx', 'Manhattan', 'Brooklyn', 'StatenIsland']
    for j in range(5):
        df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/' + attractionlocation[j] + 'Attraction.csv')
        pd.set_option('display.max_colwidth', 200)

        #分區並輸出
        df['Post code'] = df['Address'].str.extract(r'(\d{5})美國')
        A[j] = [str(x) for x in A[j]]
        B[j] = [str(x) for x in B[j]]
        for i in range(len(df['Post code'])):
            df.loc[i, 'District'] = 'C'
            if df.loc[i,'Post code'] in A[j]:
                df.loc[i,'District'] = 'A'
            elif df.loc[i,'Post code'] in B[j]:
                df.loc[i,'District'] = 'B'

        #整理價錢資料並輸出
        def extract_price(value):
            if value == '免費' or pd.isna(value):
                return 0
            else:
                text = str(value).replace(',' , '') 
                match = re.search(r'\$\s*(\d+)', text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
                else:
                    return 0
        df['Price'] = df['Price'].apply(extract_price)
        print(df['Price'])

        #整理分數和評論數資料，並計算人氣指數，將分數和評論數相乘
        df[['Score', 'Comment']] = df['Rating'].str.split('\n', expand=True)
        df['Comment'] = df['Comment'].str.strip('()').str.replace(',', '')
        df['Score'] = df['Score'].astype(float)
        df['Comment'] = df['Comment'].astype(float)
        df['Popularity'] = df['Score'] * df['Comment']

        # 依照偏好輸出不同的資料
        # 分數
        def tourism_prefer_score(df):
            column = 'Score'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df
        #評論數
        def tourism_prefer_comments(df):
            column = 'Comment'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df
        #人氣指數
        def tourism_prefer_popularity(df):
            column = 'Popularity'
            df = df.dropna(subset = [column])
            df = df.sort_values(by = column, ascending = False).round(1)
            df = df.reset_index(drop=True)
            return df

        if preference == 'Score':
            df = tourism_prefer_score(df)
        elif preference == 'Comment':
            df = tourism_prefer_comments(df)
        elif preference == 'Popularity':
            df = tourism_prefer_popularity(df)

        # 輸出只包含店名、分數、評論數、人氣指數、郵遞區號、區域、價錢新資料檔，分區儲存
        # attractionlocation = ['Queens','Bronx','Manhattan','Brooklyn','StatenIsland']
        if j == 0:
            Queens_attraction = df[['tourist attraction', 'Score', 'Comment', 'Popularity', 'Post code', 'District', 'Price']]
        elif j == 1:
            Bronx_attraction = df[['tourist attraction', 'Score', 'Comment', 'Popularity', 'Post code', 'District', 'Price']]
        elif j == 2:
            Manhattan_attraction = df[['tourist attraction', 'Score', 'Comment', 'Popularity', 'Post code', 'District', 'Price']]
        elif j == 3:
            Brooklyn_attraction = df[['tourist attraction', 'Score', 'Comment', 'Popularity', 'Post code', 'District', 'Price']]
        elif j == 4:
            StatenIsland_attraction = df[['tourist attraction', 'Score', 'Comment', 'Popularity', 'Post code', 'District', 'Price']]
    #################################################################################################################################

    #每日景點、行程演算法
    schedule = []
    #分區進入函數
    def filter_Queens_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Queens_restaurant, Queens_attraction):

        #檢視是否前往該地區，並新增schedule的list
        district = []
        if days.get('Queens') > 0:
            a = days.get('Queens')
            for i in range(a):
                inner_list = [None] * 8
                schedule.append(inner_list)
                district.append('NA')
        else:
            return schedule

        #景點演算法
        number_list = []
        for i in range(a):
            for j in range(len(Queens_attraction['Price'])):
                if j not in number_list and district_attraction_budget[0] >= Queens_attraction.loc[j,'Price']:
                    schedule[i][0] = Queens_attraction.loc[j,'tourist attraction']
                    schedule[i][1] = int(Queens_attraction.loc[j, 'Price'])
                    district_attraction_budget[0] -= Queens_attraction.loc[j,'Price']
                    number_list.append(j)
                    district.append(Queens_attraction.loc[j,'District'])
                    break
            if district[i] != 'A' or district[i] != 'B':
                district[i] = 'A'
            for j in range(len(Queens_attraction['Price'])):
                if j not in number_list and district_attraction_budget[0] >= Queens_attraction.loc[j, 'Price'] and district[i] == Queens_attraction.loc[j, 'District']:
                    schedule[i][4] = Queens_attraction.loc[j, 'tourist attraction']
                    schedule[i][5] = int(Queens_attraction.loc[j, 'Price'])
                    district_attraction_budget[0] -= Queens_attraction.loc[j, 'Price']
                    number_list.append(j)
                    break

        #餐廳演算法
        district_restaurant_budget[0] = district_restaurant_budget[0] // (2 * a)
        number_list_2 = []
        for i in range(a):
            for j in range(len(Queens_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[0] >= Queens_restaurant.loc[j,'Price'] and district[i] == Queens_restaurant.loc[j, 'District'] and Queens_restaurant.loc[j, 'Operating at noon'] == 'True':
                    schedule[i][2] = Queens_restaurant.loc[j,'Restaurant']
                    schedule[i][3] = int(Queens_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
            for j in range(len(Queens_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[0] >= Queens_restaurant.loc[j, 'Price'] and district[i] == Queens_restaurant.loc[j, 'District']:
                    schedule[i][6] = Queens_restaurant.loc[j, 'Restaurant']
                    schedule[i][7] = int(Queens_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
        return schedule

    def filter_Bronx_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Bronx_restaurant, Bronx_attraction):

        #檢視是否前往該地區，並新增schedule的list
        district = []
        if days.get('Bronx') > 0:
            a = days.get('Bronx')
            for i in range(a):
                inner_list = [None] * 8
                schedule.append(inner_list)
                district.append('NA')
        else:
            return schedule

        # 景點演算法
        number_list = []
        b = days.get('Queens')
        for i in range(a):
            for j in range(len(Bronx_attraction['Price'])):
                if j not in number_list and district_attraction_budget[1] >= Bronx_attraction.loc[j,'Price']:
                    schedule[b+i][0] = Bronx_attraction.loc[j,'tourist attraction']
                    schedule[b+i][1] = int(Bronx_attraction.loc[j, 'Price'])
                    district_attraction_budget[1] -= Bronx_attraction.loc[j,'Price']
                    number_list.append(j)
                    district.append(Bronx_attraction.loc[j,'District'])
                    break
            if district[i] != 'A' or district[i] != 'B':
                district[i] = 'A'
            for j in range(len(Bronx_attraction['Price'])):
                if j not in number_list and district_attraction_budget[1] >= Bronx_attraction.loc[j, 'Price'] and district[i] == Bronx_attraction.loc[j, 'District']:
                    schedule[b+i][4] = Bronx_attraction.loc[j, 'tourist attraction']
                    schedule[b+i][5] = int(Bronx_attraction.loc[j, 'Price'])
                    district_attraction_budget[1] -= Bronx_attraction.loc[j, 'Price']
                    number_list.append(j)
                    break

        # 餐廳演算法
        district_restaurant_budget[1] = district_restaurant_budget[1] // (2 * a)
        number_list_2 = []
        for i in range(a):
            for j in range(len(Bronx_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[1] >= Bronx_restaurant.loc[j,'Price'] and district[i] == Bronx_restaurant.loc[j, 'District'] and Bronx_restaurant.loc[j, 'Operating at noon'] == 'True':
                    schedule[b+i][2] = Bronx_restaurant.loc[j,'Restaurant']
                    schedule[b+i][3] = int(Bronx_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
            for j in range(len(Bronx_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[1] >= Bronx_restaurant.loc[j, 'Price'] and district[i] == Bronx_restaurant.loc[j, 'District']:
                    schedule[b+i][6] = Bronx_restaurant.loc[j, 'Restaurant']
                    schedule[b+i][7] = int(Bronx_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
        return schedule

    def filter_Manhattan_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Manhattan_restaurant, Manhattan_attraction):

        #檢視是否前往該地區，並新增schedule的list
        district = []
        if days.get('Manhattan') > 0:
            a = days.get('Manhattan')
            for i in range(a):
                inner_list = [None] * 8
                schedule.append(inner_list)
                district.append('NA')
        else:
            return schedule

        # 景點演算法
        number_list = []
        b = days.get('Queens') + days.get('Bronx')
        for i in range(a):
            for j in range(len(Manhattan_attraction['Price'])):
                if j not in number_list and district_attraction_budget[2] >= Manhattan_attraction.loc[j,'Price']:
                    schedule[b+i][0] = Manhattan_attraction.loc[j,'tourist attraction']
                    schedule[b+i][1] = int(Manhattan_attraction.loc[j, 'Price'])
                    district_attraction_budget[2] -= Manhattan_attraction.loc[j,'Price']
                    number_list.append(j)
                    district.append(Manhattan_attraction.loc[j,'District'])
                    break
            if district[i] != 'A' or district[i] != 'B':
                district[i] = 'A'
            for j in range(len(Manhattan_attraction['Price'])):
                if j not in number_list and district_attraction_budget[2] >= Manhattan_attraction.loc[j, 'Price'] and district[i] == Manhattan_attraction.loc[j, 'District']:
                    schedule[b+i][4] = Manhattan_attraction.loc[j, 'tourist attraction']
                    schedule[b+i][5] = int(Manhattan_attraction.loc[j, 'Price'])
                    district_attraction_budget[2] -= Manhattan_attraction.loc[j, 'Price']
                    number_list.append(j)
                    break

        # 餐廳演算法
        district_restaurant_budget[2] = district_restaurant_budget[2] // (2 * a)
        number_list_2 = []
        for i in range(a):
            for j in range(len(Manhattan_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[2] >= Manhattan_restaurant.loc[j,'Price'] and district[i] == Manhattan_restaurant.loc[j, 'District'] and Manhattan_restaurant.loc[j, 'Operating at noon'] == 'True':
                    schedule[b+i][2] = Manhattan_restaurant.loc[j,'Restaurant']
                    schedule[b+i][3] = int(Manhattan_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
            for j in range(len(Manhattan_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[2] >= Manhattan_restaurant.loc[j, 'Price'] and district[i] == Manhattan_restaurant.loc[j, 'District']:
                    schedule[b+i][6] = Manhattan_restaurant.loc[j, 'Restaurant']
                    schedule[b+i][7] = int(Manhattan_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
        return schedule

    def filter_Brooklyn_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Brooklyn_restaurant, Brooklyn_attraction):

        #檢視是否前往該地區，並新增schedule的list
        district = []
        if days.get('Brooklyn') > 0:
            a = days.get('Brooklyn')
            for i in range(a):
                inner_list = [None] * 8
                schedule.append(inner_list)
                district.append('NA')
        else:
            return schedule

        # 景點演算法
        number_list = []
        b = days.get('Queens') + days.get('Bronx') + days.get('Manhattan')
        for i in range(a):
            for j in range(len(Brooklyn_attraction['Price'])):
                if j not in number_list and district_attraction_budget[3] >= Brooklyn_attraction.loc[j,'Price']:
                    schedule[b+i][0] = Brooklyn_attraction.loc[j,'tourist attraction']
                    schedule[b+i][1] = int(Brooklyn_attraction.loc[j, 'Price'])
                    district_attraction_budget[3] -= Brooklyn_attraction.loc[j,'Price']
                    number_list.append(j)
                    district.append(Brooklyn_attraction.loc[j,'District'])
                    break
            if district[i] != 'A' or district[i] != 'B':
                district[i] = 'A'
            for j in range(len(Brooklyn_attraction['Price'])):
                if j not in number_list and district_attraction_budget[3] >= Brooklyn_attraction.loc[j, 'Price'] and district[i] == Brooklyn_attraction.loc[j, 'District']:
                    schedule[b+i][4] = Brooklyn_attraction.loc[j, 'tourist attraction']
                    schedule[b+i][5] = int(Brooklyn_attraction.loc[j, 'Price'])
                    district_attraction_budget[3] -= Brooklyn_attraction.loc[j, 'Price']
                    number_list.append(j)
                    break

        # 餐廳演算法
        district_restaurant_budget[3] = district_restaurant_budget[3] // (2 * a)
        number_list_2 = []
        for i in range(a):
            for j in range(len(Brooklyn_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[3] >= Brooklyn_restaurant.loc[j,'Price'] and district[i] == Brooklyn_restaurant.loc[j, 'District'] and Brooklyn_restaurant.loc[j, 'Operating at noon'] == 'True':
                    schedule[b+i][2] = Brooklyn_restaurant.loc[j,'Restaurant']
                    schedule[b+i][3] = int(Brooklyn_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
            for j in range(len(Brooklyn_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[3] >= Brooklyn_restaurant.loc[j, 'Price'] and district[i] == Brooklyn_restaurant.loc[j, 'District']:
                    schedule[b+i][6] = Brooklyn_restaurant.loc[j, 'Restaurant']
                    schedule[b+i][7] = int(Brooklyn_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
        return schedule

    def filter_StatenIsland_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, StatenIsland_restaurant, StatenIsland_attraction):

        #檢視是否前往該地區，並新增schedule的list
        district = []
        if days.get('StatenIsland') > 0:
            a = days.get('StatenIsland')
            for i in range(a):
                inner_list = [None] * 8
                schedule.append(inner_list)
                district.append('NA')
        else:
            return schedule

        # 景點演算法
        number_list = []
        b = days.get('Queens') + days.get('Bronx') + days.get('Manhattan') + days.get('Brooklyn')
        for i in range(a):
            for j in range(len(StatenIsland_attraction['Price'])):
                if j not in number_list and district_attraction_budget[4] >= StatenIsland_attraction.loc[j,'Price']:
                    schedule[b+i][0] = StatenIsland_attraction.loc[j,'tourist attraction']
                    schedule[b+i][1] = int(StatenIsland_attraction.loc[j, 'Price'])
                    district_attraction_budget[4] -= StatenIsland_attraction.loc[j,'Price']
                    number_list.append(j)
                    district.append(StatenIsland_attraction.loc[j,'District'])
                    break
            if district[i] != 'A' or district[i] != 'B':
                district[i] = 'A'
            for j in range(len(StatenIsland_attraction['Price'])):
                if j not in number_list and district_attraction_budget[4] >= StatenIsland_attraction.loc[j, 'Price'] and district[i] == StatenIsland_attraction.loc[j, 'District']:
                    schedule[b+i][4] = StatenIsland_attraction.loc[j, 'tourist attraction']
                    schedule[b+i][5] = int(StatenIsland_attraction.loc[j, 'Price'])
                    district_attraction_budget[4] -= StatenIsland_attraction.loc[j, 'Price']
                    number_list.append(j)
                    break

        # 餐廳演算法
        district_restaurant_budget[4] = district_restaurant_budget[4] // (2 * a)
        number_list_2 = []
        for i in range(a):
            for j in range(len(StatenIsland_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[4] >= StatenIsland_restaurant.loc[j,'Price'] and district[i] == StatenIsland_restaurant.loc[j, 'District'] and StatenIsland_restaurant.loc[j, 'Operating at noon'] == 'True':
                    schedule[b+i][2] = StatenIsland_restaurant.loc[j,'Restaurant']
                    schedule[b+i][3] = int(StatenIsland_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
            for j in range(len(StatenIsland_restaurant['Price'])):
                if j not in number_list_2 and district_restaurant_budget[4] >= StatenIsland_restaurant.loc[j, 'Price'] and district[i] == StatenIsland_restaurant.loc[j, 'District']:
                    schedule[b+i][6] = StatenIsland_restaurant.loc[j, 'Restaurant']
                    schedule[b+i][7] = int(StatenIsland_restaurant.loc[j, 'Price'])
                    number_list_2.append(j)
                    break
        return schedule

    if data_verification == True:
        schedule = filter_Queens_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Queens_restaurant, Queens_attraction)
        schedule = filter_Bronx_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Bronx_restaurant, Bronx_attraction)
        schedule = filter_Manhattan_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Manhattan_restaurant, Manhattan_attraction)
        schedule = filter_Brooklyn_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, Brooklyn_restaurant, Brooklyn_attraction)
        schedule = filter_StatenIsland_schedule(schedule,district_attraction_budget, district_restaurant_budget, days, StatenIsland_restaurant, StatenIsland_attraction)

    #輸出結果
    if data_verification == True:
        # print(fare)
        # print(Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput)
        # print(schedule)
        return fare, Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput, schedule

# if __name__ == '__main__':
#     fare_return, Queenshoteloutput_return, Bronxhoteloutput_return, Manhattanhoteloutput_return, Brooklynhoteloutput_return, StatenIslandhoteloutput_return, schedule_return = run(100000, 20, 30, 50, [3, 2, 1, 2, 2], '人氣指數', 10)
# print(schedule_return)