import pandas as pd
import sklearn
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from models.schemas import Base, CurrentWeather, StaticBike
from config.config import MySQL
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle


def build_availability_model(app):
    try:
        db = create_engine(MySQL.URI)
        conn = db.connect()
    except Exception as e:
        # Close connections
        conn.close()
        db.dispose()
        return
    # retrieve data
    df_all_data = pd.read_sql_query("SELECT * FROM dublin_bike.bike_history AS b INNER JOIN "
                                    "dublin_bike.weather_history AS w ON b.scraping_time = w.datetime and b.number = "
                                    "w.stationNum", conn)
    # convert data
    df_all_data['scraping_time'] = pd.to_datetime(df_all_data['scraping_time'])
    df_all_data['hour'] = df_all_data['scraping_time'].dt.hour
    df_all_data['minutes'] = df_all_data['scraping_time'].dt.minute
    df_all_data['weekday'] = df_all_data['weekday'].replace(1, 'Monday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(2, 'Tuesday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(3, 'Wednesday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(4, 'Thursday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(5, 'Friday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(6, 'Saturday')
    df_all_data['weekday'] = df_all_data['weekday'].replace(7, 'Sunday')
    data_input = pd.DataFrame(df_all_data['weekday'])
    dummy = pd.get_dummies(data_input)
    df_all_data = pd.concat([df_all_data, dummy], axis=1)

    # select input features
    input_model = pd.DataFrame(
        df_all_data[['latitude', 'longitude', 'temperature', 'wind_spd', 'pressure', 'humidity', 'hour']])
    input_model = pd.concat([input_model, dummy], axis=1)
    output = df_all_data['available_bike']

    # split dataset to train and test
    x_train, x_test, y_train, y_test = train_test_split(input_model, output, test_size=0.2, random_state=40)

    # train model
    model = RandomForestRegressor(n_estimators=10)
    model.fit(x_train, y_train)

    # test model
    prediction = model.predict(x_test)
    df_predicated = pd.DataFrame(prediction, columns=['Predicted'])
    df_test_y = df_all_data.iloc[y_test]
    df_bikes = pd.DataFrame(df_test_y['available_bike']).reset_index(drop=True)
    actual_vs_predicted = pd.concat([df_bikes, df_predicated], axis=1)

    # evaluate
    def print_metrics(actual_val, predictions):
        # print evaluation measures
        print("MAE (Mean Absolute Error): ", metrics.mean_absolute_error(actual_val, predictions))
        print("MSE (Mean Squared Error): ", metrics.mean_squared_error(actual_val, predictions))
        print("RMSE (Root Mean Squared Error): ", metrics.mean_squared_error(actual_val, predictions)**0.5)
        print("R2: ", metrics.r2_score(actual_val, predictions))
    print_metrics(y_test, prediction)
    pickle.dump(model, open(app.root_path + '\\bike_prediction_model.pickle', 'wb'))
