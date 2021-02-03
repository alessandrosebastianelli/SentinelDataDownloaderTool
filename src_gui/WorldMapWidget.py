import tkinter as tk
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from shapely.geometry import Point,Polygon
import pandas as pd
import geopandas as gpd
import descartes
import numpy as np
from matplotlib.figure import Figure
import os

class WorldMapWidget(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root
        self.show_map()

    def get_data(self):
        df_path = os.path.join('src_gui','points.csv')
        map_path = os.path.join('src_gui',os.path.join('map', 'ne_110m_land.shp'))
        #----Load the dataframe
        df = pd.read_csv(df_path).drop(columns=['Unnamed: 0'])
        #----Load the world map
        w_map = gpd.read_file(map_path)

        #----Create a geopandas dataframe
        crs = {'init': 'epsg:4326'}
        geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
        geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

        return w_map, geo_df

    def create_plot(self, w_map, geo_df):
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111)
        ax = fig.axes[0]

        w_map.plot(ax=ax, alpha=0.4, color='gray')
        geo_df[geo_df['State']==0].plot(ax=ax, markersize=8, color='red', marker="o", label='Generated points')
        geo_df[geo_df['State']==1].plot(ax=ax, markersize=8, color='blue', marker="o", label='Downloaded points')
        geo_df[geo_df['State']==2].plot(ax=ax, markersize=8, color='green', marker="o", label='Missing data')
        geo_df[geo_df['State']==3].plot(ax=ax, markersize=8, color='yellow', marker="o", label='To check')

        ax.set_title('Generated points map', fontsize=24)
        ax.set_xlabel('Longitude', fontsize=16)
        ax.set_ylabel('Latitude', fontsize=16)
        ax.legend(prop={'size':15})
        ax.set_xticks(np.arange(-180, 190, 10.0))
        ax.set_yticks(np.arange(-90, 100, 10.0))
        ax.grid()

        return fig

    def show_map(self):
        #----Create a new indipendent window from the root
        self.map_window = tk.Toplevel(self.root)
        #----Set the "attention" on it
        self.map_window .grab_set()
        #self.map_window.geometry('1300x600')
        self.map_window.title("Generated Points World Map")
        m = self.root.maxsize()
        self.map_window.geometry('{}x{}+0+0'.format(*m))

        w_map, geo_df = self.get_data()
        fig = self.create_plot(w_map, geo_df)

        world_map = FigureCanvasTkAgg(fig, master=self.map_window)
        world_map.draw()
        world_map.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(world_map, self.map_window)
        toolbar.update()
        world_map.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #----When press the x button then destroy the child window
        self.map_window.protocol("WM_DELETE_WINDOW", self.quit)
        

    def quit(self):
        self.map_window.destroy()
