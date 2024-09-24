import pandas as pd
from sklearn.model_selection import train_test_split

from src.exceptions import DocumentNotFoundError
from src.database.repositories.hospital_settings_repository import SettingsDAO

def convert_docs_to_df(docs):
    # Get list of macs that is going to be used
    settingsDAO = SettingsDAO()
    macs_docs = settingsDAO.get_mac_list()

    macs = list(macs_docs.keys())

    if macs == None:
        raise DocumentNotFoundError("There isn`t a mac list.")
    
    macs.append("room")
    print(macs)

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
    # print(df)

    # Merge mac list with dataframe
    new_df = pd.DataFrame(columns=macs)
    new_df = new_df.combine_first(df)
    new_df = new_df.fillna(0)
    print(new_df[macs])

    return new_df[macs] # returns a dataframe with only the listed macs and the room

def split_data(df):

    #  Divides data into training and testing dat
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    return [train_df, test_df]

def convert_last_data_to_df(doc):
    settingsDAO = SettingsDAO()
    macs_docs = settingsDAO.get_mac_list()

    macs = list(macs_docs.keys())
    
    if macs == None:
        raise DocumentNotFoundError("There isn`t a mac list.")

    df = pd.DataFrame(0, index=[0], columns=macs)

    for item in doc[0]['routers']:
        if item['mac'] in macs:
            df[item['mac']] = item['rssi']

    return df