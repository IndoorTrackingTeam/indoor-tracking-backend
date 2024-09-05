import pandas as pd
from sklearn.model_selection import train_test_split

from src.database.repositories.hospital_settings_repository import SettingsDAO

def convert_docs_to_df(docs):
    # Set dataframe with all the docs from the database
    data = []
    for doc in docs:
        room_ = doc['room']
        date_ = doc['date']

        for date, routers in date_.items():
            temp_row = {'room': room_}

            for router in routers:
                temp_row[router['mac']] = router['rssi']
            
            data.append(temp_row)
        
    df = pd.DataFrame(data)

    df = df.fillna(0)

    # Get list of macs that is going to be used
    settingsDAO = SettingsDAO()
    macs = settingsDAO.get_mac_list()
    macs.append("room")
    print(macs)

    return df[macs] # returns a dataframe with only the listed macs and the room

def split_data(df):

    #  Divides data into training and testing dat
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    print(test_df)
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    print(test_df)

    return [train_df, test_df]