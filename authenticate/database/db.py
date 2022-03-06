import sqlite3
import pandas as pd






class database:
    def __init__(self):
        self.conn = sqlite3.connect(r'./database.db')

    def readFile(self, path):
        df = pd.read_csv(path, sep=':', engine='python')
        return df
        
    def insert(self, spectrum):
        spectrum.to_sql('trm', self.conn, if_exists='append', index=False)
        return 0
            
    def remove(self):
        return 0

    def deviceList(self):
        return 0

    def keyList(self):
        return 0

    def exitDB(self):
        self.conn.close()


# Load data into Pandas DataFrame
#spectra = pd.read_csv('E190909A 2p0P 0p7W 146 Pol.0.dpt', delimiter=r'\s+', header=None)

# Connect to SQLite database
#conn = sqlite3.connect(r'/home/pi/SeniorDesign/464_FH18/database.db')
#conn = sqlite3.connect(r'./database.db')

# Write the data to a sqlite table
#spectra.to_sql('trm', conn, if_exists='append', index=False)

# Create a cursor object
#cur = conn.cursor()
# Fetch and display result
#for row in cur.execute("SELECT * FROM trm"):
#    print(row)
# Close connection to SQLite database
#conn.close()
