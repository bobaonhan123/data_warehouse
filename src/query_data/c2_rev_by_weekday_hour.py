import json
import pandas as pd

from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]
WEEKDAY_MAP = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}
def c2_rev_by_weekday_hour():
    weekdays = {i: {j: 0 for j in range(24)} for i in range(7)}
    sales_by_time = list(sales_by_time_db.find())
    for sale in sales_by_time:
        time_dimension = time_db.find_one({'time_id': sale['time_dim_id']})
        sale['time'] = time_dimension
    for sale in sales_by_time:
        weekday = sale['time']['weekday']
        hour = sale['time']['hour']
        weekdays[weekday][hour] += sale['quantity'] * sale['unit_price']
    
    rows = []
    for weekday, hours in weekdays.items():
        for hour, revenue in hours.items():
            rows.append({
                "Weekday": WEEKDAY_MAP[weekday],
                "Hour": int(hour),
                "Revenue": revenue
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path+'c2_rev_by_weekday_hour.csv', index=False)