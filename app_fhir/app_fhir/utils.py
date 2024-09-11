import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
from xml.dom.minidom import Element
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from scipy.__config__ import show

def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_graph_data(bmi_data):
    plt.clf()
    bmi_data.sort(key=lambda x: x[0])

        # Separate the data into dates and values for plotting
    dates = [data[0] for data in bmi_data]
    values = [data[1] for data in bmi_data]

    # Plot the data using matplotlib
   
    # plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o', linestyle='-', color='b', label='BMI')

    # Format the plot
    # plt.title(f"BMI Over Time for Patient")
    # plt.xlabel("Date")
    # plt.ylabel("BMI Value")
    # plt.xticks(rotation=45)
    # plt.grid(True)
    # plt.tight_layout()
    # plt.legend()

    
    graph = getGraph()
    return graph