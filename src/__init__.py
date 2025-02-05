import logging
from datetime import date
from src.data_provider import DataProvider
from src.power_station import PowerStationDataProvider

if __name__ == "__main__":
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level = logging.DEBUG)
    data_provider = DataProvider("username", "pasword")
    data_provider.login()

    power_station_data_provider = PowerStationDataProvider(data_provider)
    power_station_data_provider.fetch_data()
    start = date(2024, 6, 1)
    end = date(2024, 12, 21)
    power_station_data_provider.fetch_chart_data(start, end)