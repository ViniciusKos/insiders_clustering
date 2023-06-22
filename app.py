import matplotlib.pyplot as plt
import numpy as np
from shiny import App, render, ui


import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('insiders_cluster.db')

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL query
cursor.execute('SELECT * FROM insiders')

# Fetch all the results
results = cursor.fetchall()

# Get the column names from the cursor description
columns = [column[0] for column in cursor.description]

# Create a Pandas DataFrame from the results and column names
df = pd.DataFrame(results, columns=columns)

# Close the cursor and connection
cursor.close()
conn.close()

# Print the DataFrame
print(df.head())



app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("n", "N", 0, 100, 20),
        ),
        ui.panel_main(
            ui.output_plot("histogram"),
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot(alt="A histogram")
    def histogram():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)
        plt.hist(x, input.n(), density=True)


app = App(app_ui, server, debug=True)
