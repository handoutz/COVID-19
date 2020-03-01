import numpy as np
import pandas as pd
import geopandas as gpd
import descartes
import matplotlib.pyplot as plt
from typing import List
from app import Recovered, ConfirmedCase, Death
import shapely
from pprint import pprint

confirmed = []
ezdata = []
geo = []
crs = {'init': 'epsg:4326'}
for c in ConfirmedCase.objects:
    dd = {
        'Longitude': c.Location["coordinates"][0],
        'Latitude': c.Location["coordinates"][1],
        'Amount': sum([d.Value for d in c.Data])
    }
    geo.append(shapely.geometry.Point((dd['Latitude'], dd['Longitude'])))
    ezdata.append(dd)
