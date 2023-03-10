import pandas as pd
from sklearn.impute import KNNImputer

station_day_path = "resource/station_day.csv"
station_day = pd.read_csv(station_day_path)


def bucket_group(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Satisfactory"
    elif x <= 200:
        return "Moderate"
    elif x <= 300:
        return "Poor"
    elif x <= 400:
        return "Very Poor"
    else:
        return "Severe"


# station_day = station_day[:5000]

missing_col = [col for col in station_day.columns if sum(pd.isna(station_day[col]) > 0) and col != "AQI_Bucket"]
imputer = KNNImputer()
imputer.fit(station_day[missing_col])
station_day[missing_col] = imputer.transform(station_day[missing_col])
station_day.head()
levels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
bucket_dict = dict()
for level in levels:
    max_AQI = max(station_day[station_day["AQI_Bucket"] == level]["AQI"])
    min_AQI = min(station_day[station_day["AQI_Bucket"] == level]["AQI"])

    bucket_dict[level] = [min_AQI, max_AQI]

for level in levels:
    print("For level '{}': AQI index range is {}".format(level, bucket_dict[level]))

station_day.loc[pd.isna(station_day["AQI_Bucket"]), "AQI_Bucket"] = station_day.loc[
    pd.isna(station_day["AQI_Bucket"]), "AQI_Bucket"].apply(lambda x: bucket_group(x))

print('Imputation is done!')
station_day.to_csv('output/station_day_impute.csv')
