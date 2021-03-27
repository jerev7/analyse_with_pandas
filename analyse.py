import pandas as pd
import requests


activities = pd.read_csv("equipment_activities.csv")
installations = pd.read_csv("equipment_installations.csv")

# print(activities[["ComInsee", "ActLib"]])


# iterate all rows

# for index, row in activities.iterrows():
#     print(index, row['ActLib'])



# Get specific row, column

# print(activities.iloc[1, 2])



# Get all row which match a specific value

# print(activities.loc[activities["EquipementId"] == 73821])



# Sort

# print(activities.sort_values('ActLib', ascending=False))


# Add column

# activities["new column"] = "New"
# print(activities.head(1))



# Drop column

# activities = activities.drop(columns=["new column"])
# print(activities.head(1))

install_equip = installations.iloc[0, 4]
# print(install_equip)

# rowIneed = activities.loc[activities["EquipementId"] == install_equip]
# rowIneed["ActLib"] = installations.iloc[0, 4]
# print(rowIneed)
install_equip_all = installations.loc[4]
# print(install_equip_all)

# print(columns_to_add[0])
# for column in installations.columns:
#     if column not in activities.columns:
#         activities[column] = installations.loc[installations["EquipementId"] == 73821, column]
# else:
#     print("Column already exists")
# print(activities.columns)


# Creating a list of all equipments
equip_id_list = []
equipements = installations["EquipementId"]
for equip in equipements:
    equip_id_list.append(equip)
# print(equip_id_list)

# all_rows_of_one_equip = activities.loc[activities["EquipementId"] == 73821]
# print(all_rows_of_one_equip)

# We delete columns existing in both csv
for column in installations.columns:
    if column in activities.columns and column != "EquipementId":
        activities = activities.drop(columns=column)

# print(equip_id_list)
# activities = activities.drop(columns=["ComInsee", "ComLib", "EquNbEquIdentique"])
# activities = activities.drop(columns=["ComLib"])
# activities = activities.drop(columns=["EquNbEquIdentique"])

# We merge both csv together using common key EquipementId
merged_data = pd.merge(installations, activities, how="left", on="EquipementId")


def address_from_latitude_longitude(latitude, longitude):
    """
    Function to get the real address using latitude longitude.
    """
    

    try:
        r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={key}")
        address = r.json()["results"][0]["formatted_address"]
        print("Google request was successful !")
    except:
        address = "Address not found"

    return address.replace(",", "")
# merged_data["Address"] = ""
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
merged_data.to_csv("testing.csv", index=False)
print("Data saved")


#result_get_adress["formatted_address"]
#r = requests.get("https://maps.google.com/maps/api/geocode/"

# r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=" + key)
# address = r.json()["results"][0]["formatted_address"]
# print(address)


    

# print(address_from_latitude_longitude(40.714224, -73.961452))