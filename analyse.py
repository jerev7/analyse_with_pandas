import pandas as pd
import requests
from config import KEY # importing google API key from config.py

# Reading the file to analyse
activities = pd.read_csv("equipment_activities.csv")
installations = pd.read_csv("equipment_installations.csv")

# Creating a list of all equipments
equip_id_list = []
equipements = installations["EquipementId"]
for equip in equipements:
    equip_id_list.append(equip)

# We delete columns existing in both csv
for column in installations.columns:
    if column in activities.columns and column != "EquipementId":
        activities = activities.drop(columns=column)

# We merge both csv together using common key EquipementId
merged_data = pd.merge(installations, activities, how="left", on="EquipementId")


def address_from_latitude_longitude(latitude, longitude):
    """
    Function using google geocode API to get the real address using latitude longitude.
    """

    try:
        r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={KEY}")
        address = r.json()["results"][0]["formatted_address"]
        print("Google request was successful !")
    except:
        address = "Address not found"
        print("Google request failed")

    return address.replace(",", "")


def add_address_to_equipment(equipment_id):
    """
    Function to add an address to each rows which match the given equipment. 
    """
    latitude = merged_data.loc[merged_data["EquipementId"] == equipment_id, "EquGpsY"]
    longitude = merged_data.loc[merged_data["EquipementId"] == equipment_id, "EquGpsX"]
    list_of_rows_to_modify = merged_data.index[merged_data["EquipementId"] == equipment_id].tolist()

    for row in list_of_rows_to_modify:
        merged_data.loc[row, "Address"] = address_from_latitude_longitude(latitude[row], longitude[row])


    
for equipment in equip_id_list:
    add_address_to_equipment(equipment)

# Saving to a new csv file
merged_data.to_csv("results.csv", index=False)
print("Data saved")

