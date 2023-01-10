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

# most played time controls from db
query = pd.read_sql_query('SELECT time_control FROM games WHERE time_control IN (SELECT time_control FROM games GROUP BY time_control ORDER BY COUNT(time_control) DESC LIMIT 25) ORDER BY time_control', db.conn)
df = pd.DataFrame(query)
print(df)

# chart
plt.xticks(rotation=75)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)
sns.histplot(df.time_control)
plt.show()