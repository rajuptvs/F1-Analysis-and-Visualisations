import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from fastf1.core import Laps
from timple.timedelta import strftimedelta
import streamlit as st

def app():
    st.header('F1 Qualifying Dashboard')

    #ff1.Cache.enable_cache(cache_dir='c:\\Users\\Rajup\\AppData\\Local\\Programs\\Python\\Python310\\lib\\cache') 
    year = st.number_input('Enter Year',min_value=1, max_value=3000,step=1)
    gp = st.text_input('Enter Grand Prix Location')
    sessiontypechoice=st.number_input('Enter 1 for qualifying or 2 for race',min_value=1, max_value=2,step=1)
    st.write('The current selectd GP is ' + str(year) + ' '+gp+' Grand Prix ')

    # year=int(input('Enter Year'))
    # gp=input('Enter the Grand Prix Location')
    # sessiontypechoice=int(input('Enter 1 for qualifying or 2 for race'))

    if sessiontypechoice == 1:
        sessiontype='Q'
    elif sessiontypechoice == 2:
        sessiontype='R'
    else:
        print("Unknown choice")

    quali = ff1.get_session(year, gp,sessiontype )
    quali.load()
    quali_data=quali.laps
    quali_data=pd.DataFrame(quali_data)
    quali_results=quali.results
    quali_results=quali_results[['DriverNumber','BroadcastName','Abbreviation','TeamName','Position','Q1','Q2','Q3']]
    driver=pd.unique(quali_data['Driver'])
    fastest_laps_driver=list()
    for drivers in driver:
        fastest_lap=quali.laps.pick_driver(drivers).pick_fastest()
        fastest_laps_driver.append(fastest_lap)
    fastest_laps = Laps(fastest_laps_driver).sort_values(by='LapTime')
    fastest_laps=fastest_laps.reset_index()
    fastest_laps.drop('index', inplace=True, axis=1)
    def  getdelta(index):      
        times=fastest_lapdf['LapTime'].iloc[index]
        times=times.total_seconds()
        delta_cars=times-fastest_time_temp
        return delta_cars
    fastest_lapdf=pd.DataFrame(fastest_laps)
    fastest_time=fastest_lapdf['LapTime'].iloc[0]
    fastest_time
    fastest_time_temp=fastest_time.total_seconds()
    fastest_time_temp
    secondfastest_time=fastest_lapdf['LapTime'].iloc[2]
    secondfastest_time
    secondfastest_time_temp=secondfastest_time.total_seconds()
    secondfastest_time_temp
    delta=secondfastest_time_temp-fastest_time_temp
    delta
    ranges=len(fastest_lapdf)
    ranges
    deltas=[]
    for i in range(1,ranges):
        time_diff=getdelta(i)
        deltas.append(time_diff)

    pole=fastest_time
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = ff1.plotting.team_color(lap['Team'])
        team_colors.append(color)
    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    lap_time_string = strftimedelta(pole, '%m:%s.%ms')

    # st.suptitle(f"{quali.event['EventName']} {quali.event.year} Qualifying\n"
    #              f"Fastest Lap: {lap_time_string} ({pole})")
    st.write(f"{quali.event['EventName']} {quali.event.year} Qualifying\n"
            f"Fastest Lap: {lap_time_string} ({pole})")
    fig.savefig("quali.jpg")
    st.pyplot(fig)