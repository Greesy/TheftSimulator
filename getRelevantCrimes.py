import csv

relevantData = []
with open('Crimes_-_2001_to_present.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    data = list(reader)

    #Locations we care about
    locations = ["RESIDENCE", "APARTMENT", "RESIDENCE-GARAGE", "RESIDENCE PORCH/HALLWAY"]

    print("Total rows:", len(data))
    for idx in range(len(data)):
        # Delete entries that should never be needed
        del data[idx][12:17]     # Deletes: Ward, Community Area, FBI Code, X coord, and Y coord
        del data[idx][9]         # Deletes: Domestic
        del data[idx][4:6]       # Deletes: IUCR and Primary type (will always be "THEFT")
        del data[idx][-4:]       # Deletes last 4 entries: Location, Longitude, latitude, and Updated On

        # Each entry should now look like this:
        # [ 0   1            2     3      4            5                     6       7     8         9    ]
        # [ ID, Case number, Date, Block, Description, Location Description, Arrest, Beat, District, Year ]

        if idx == 0:
            relevantData.append(data[idx])
            continue

        # Skip entries involving locations we aren't interested in
        if data[idx][5] not in locations:
            continue

        # If iteration reaches this point the current row is one we want to analyze, so store it in relevantData
        relevantData.append(data[idx])
    
    print("Relevant rows:", len(relevantData))

with open('Relevant_Crimes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    print("Writing csv file with relevant rows...")
    for idx in range(len(relevantData)):
        writer.writerow(relevantData[idx])

print("Done.")
