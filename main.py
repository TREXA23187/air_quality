import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# 将csv文件通过pandas读进来 此时读入的csv以DataFrame的形式来提供很多帮助
india = pd.read_csv('output/station_day_impute.csv')
geometry = pd.read_csv('resource/stations_with_geo.csv')

# 分别查看india和geometry的列有哪些
# print(india.columns)
# print(geometry.columns)

# 可以发现india的第一列 'Unnamed: 0' 为无用列，使用drop()将其删去
# 其中axis=1是按列删除 axis=0是按行删除。
india = india.drop(india.columns[0], axis=1)

# 合并india和geometry
# 其中geometry部分只需要['StationId', 'latitude', 'longitude']这三列 因此单独取出
# how='inner' 表示inner joint
# on='StationId' 表示两个数据通过StationId来标识连接 此处与数据库sql的表达相近
india_with_geo = pd.merge(india, geometry[['StationId', 'latitude', 'longitude']], how='inner', on='StationId')

# 合并完成 查看合并后带有经纬度信息的india数据
# print(india_with_geo.head())

# 对于每年每个月的平均值计算，首先先把Date这一列的数据从 str 转成 pandas中用于日期操作的类型 Timestamp
# <class 'pandas._libs.tslibs.timestamps.Timestamp'>
# 此时可以通过 time.year time.month time.day 分别得到年月日的信息
india_with_geo['Date'] = pd.to_datetime(india_with_geo['Date'])
india_with_geo = india_with_geo.set_index('Date')


def if_contains_year(df, year):
    for i in df.reset_index()['Date']:
        if i.year == year:
            return True

    return False


def get_geometry_by_station(station_id):
    res = india_with_geo_station[india_with_geo_station['StationId'] == station_id]
    print(res)


# 整理出每个站点每年每个月的平均值
# 按地点分类，得到每个地点在19年有数据的月份的平均值
india_with_geo_month_mean_total = None
# india_with_geo['StationId'].unique将得到StationId出现的所有唯一值 即所有的站点
for station in india_with_geo['StationId'].unique():
    # 对每一个站点进行一次计算
    india_with_geo_station = india_with_geo[india_with_geo['StationId'] == station]
    # 15-20年的数据
    for year in ['2015', '2016', '2017', '2018', '2019', '2020']:
        if if_contains_year(india_with_geo_station, int(year)):
            # 选取属于2019年的数据
            india_with_geo_year = india_with_geo_station.loc[year]
            # 按照月份进行groupby 计算AQI的平均值
            india_with_geo_month_mean = \
                india_with_geo_year.reset_index().groupby(pd.Grouper(key='Date', axis=0, freq='M'))[
                    'AQI'].mean()
            # 将计算得到的平均值 和 StationId整合作为一个 DataFrame
            india_with_geo_month_mean_df = pd.DataFrame({'StationId': [station for i in india_with_geo_month_mean],
                                                         'AQI_Monthly_Mean': india_with_geo_month_mean})
            # 合并到存放之前其他站点月均值的india_with_geo_month_mean_total中
            india_with_geo_month_mean_total = pd.concat([india_with_geo_month_mean_total, india_with_geo_month_mean_df])

# 最终把每个station的月平均整合，得到所有的2019年station每个月的平均值

import geopandas as gpd
from pyproj import CRS

CRS_4326 = CRS('epsg:4326')

india_with_geo_month_mean_2019 = india_with_geo_month_mean_total.loc['2019']
# india_with_geo_month_mean_2019['latitude'] = india_with_geo_month_mean_2019.apply


station_geo_map = {}
for i in range(len(geometry['StationId'])):
    station_geo_map[geometry['StationId'][i]] = (geometry['latitude'][i], geometry['longitude'][i])
