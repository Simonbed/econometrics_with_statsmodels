
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import sqlite
import pandas.io.sql as pdsql

from dash.dependencies import Input, Output


conn = sqlite.connect("exemple.db")
sql = """ 
SELECT top 5 *
FROM Table
"""

df = pdsql.read_sql(sql, conn)

print(df.head())

app = dash.Dash()











if __name__ == '__main__':
    app.run_server(debug=True)
