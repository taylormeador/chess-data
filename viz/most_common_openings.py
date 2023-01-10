import seaborn as sns
import pandas as pd
import sys
from db import DB
import matplotlib.pyplot as plt

# attempt db connection
try:
    print('\nAttempting to connect to database...')
    db = DB()
    print('Success!')
except:
    print('Error connecting to database. Exiting...')
    sys.exit()

# 15 most played openings from db
query = pd.read_sql_query('SELECT opening FROM games WHERE opening IN (SELECT opening FROM games GROUP BY opening ORDER BY COUNT(opening) DESC LIMIT 15)', db.conn)
df = pd.DataFrame(query)

# chart
plt.xticks(rotation=75)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)
sns.histplot(df.opening)
plt.show()