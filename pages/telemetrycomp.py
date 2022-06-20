
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from fastf1.core import Laps
import fastf1 as ff1
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
from fastf1 import utils

def app():
    
    st.header('Telemetry Comparision and Fastest Sectors')

    #Get the input data from the user for Year, Grand Prix Location and Session Respectively
    
    year = st.number_input('Enter Year',min_value=2000, max_value=3000,step=1)
    gp = st.text_input('Enter Grand Prix Location')
    sessiontypechoice=st.number_input('Enter 1 for qualifying or 2 for race',min_value=1, max_value=2,step=1)
    st.write('The current selectd GP is ' + str(year) + ' '+gp+' Grand Prix ')

    ff1.plotting.setup_mpl()
    
    if sessiontypechoice == 1:
        sessiontype='Q'
    elif sessiontypechoice == 2:
        sessiontype='R'
    else:
        print("Unknown choice")

    session = ff1.get_session(year, gp,sessiontype)
    session.load()

    # Get the type of comparision top 2 drivers comparision / custom selection of drivers
    choicedrivers=st.number_input("Enter 1 for the comparision between top 2 drivers \n Enter 2 for the comparision between 2 specified drivers",min_value=1, max_value=2,step=1)

    if choicedrivers==1: 
        quali_results=session.results
        quali_results=quali_results[['DriverNumber','BroadcastName','Abbreviation','TeamName','Position','Q1','Q2','Q3']]
        quali_results[['Abbreviation']]
        x=quali_results['Abbreviation'].iloc[0]
        y=quali_results['Abbreviation'].iloc[1]
        driver1=x
        driver2=y

    elif choicedrivers==2:
        # custom selection of drivers for option 2
        driver1=st.text_input("Enter the first driver initials")
        driver2=st.text_input("Enter the second driver initials")
    
    else :
        print("Invalid Choice !!!")

    # Case Sensitivity handling 
    driver1=driver1.upper()
    driver2=driver2.upper()

    laps=session.load_laps(with_telemetry=True)




    laps_1=laps.pick_driver(driver1)
    laps_2=laps.pick_driver(driver2)



    fastest_1=laps_1.pick_fastest()
    fastest_2=laps_2.pick_fastest()

    

    # total_race1=laps_1.get_car_data().add_distance()
    # total_race2=laps_2.get_car_data().add_distance()


    driver1_telemetry=fastest_1.get_car_data().add_distance()
    driver2_telemetry=fastest_2.get_car_data().add_distance()

    # assignment of driver colors w.r.t to their team colors 

    driver1_color=plotting.team_color(fastest_1['Team'])
    driver2_color=plotting.team_color(fastest_2['Team'])

    # handling case if both the drievrs are from the same team
    if(driver1_color==driver2_color):
        driver2_color='#FFFFFF'
        

   

    #delta_ms=round(delta.total_seconds()*1000)
    nameevent=session.event['OfficialEventName']

    nameevent

    driver1_telemetry
    utils.delta_time(fastest_1, fastest_2)
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_1, fastest_2)
    fig, ax = plt.subplots(4)
    ax[0].plot(ref_tel['Distance'], delta_time)
    ax[0].axhline(0)
    ax[0].set(ylabel=f"Gap to {fastest_2.Driver} (s)")

    ax[1].plot(driver1_telemetry['Distance'], driver1_telemetry['Speed'], color=driver1_color, label=driver1)
    ax[1].plot(driver2_telemetry['Distance'], driver2_telemetry['Speed'], color=driver2_color, label=driver2)

    ax[1].set_xlabel('Distance in m')
    ax[1].set_ylabel('Speed in km/h')

    ax[1].legend()

    ax[2].plot(driver1_telemetry['Distance'], driver1_telemetry['Brake'], color=driver1_color, label=driver1)
    ax[2].plot(driver2_telemetry['Distance'], driver2_telemetry['Brake'], color=driver2_color, label=driver2)

    ax[2].set_xlabel('Distance in m')
    ax[2].set_ylabel('Brake ')

    ax[2].legend()

    ax[3].plot(driver1_telemetry['Distance'], driver1_telemetry['Throttle'], color=driver1_color, label=driver1)
    ax[3].plot(driver2_telemetry['Distance'], driver2_telemetry['Throttle'], color=driver2_color, label=driver2)

    ax[3].set_xlabel('Distance in m')
    ax[3].set_ylabel('Throttle ')

    ax[3].legend()

    plt.suptitle(f"Fastest Lap Comparison  \n"
                f"{nameevent} {session.name}  ")
    fig.set_size_inches(25, 8)
    plt.savefig(nameevent +' '+session.name+'telecomparision.jpg')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)

    x=fastest_1.telemetry['X']
    y=fastest_1.telemetry['Y']
    
    color = fastest_1.telemetry['Speed'] 
    
    
    one=fastest_1.LapTime
    two=fastest_2.LapTime
    if one<two:
        min=one
        max=two
    else:
        min=two
        max=one
    delta=max-min

    deltams=round(delta.total_seconds()*1000)

    telemetrydf=pd.DataFrame(fastest_1.telemetry)
    
    # Rough division of a lap into 3 equal sectors 
    chunksize =  int(telemetrydf.shape[0] / 3)

    chunks = [telemetrydf[i:i+chunksize] for i in range(0,telemetrydf.shape[0],chunksize)]


    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    ms=int(delta.microseconds)
    gap=ms/1000000
    print(gap)
    # changing timedelta to seconds and micro seconds format
    # the above format should be enough for the qualifying session 
    # and one lap pace

    seconds=delta.seconds
    seconds + gap

    gap = seconds + gap


    fig1, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig1.suptitle(f'{session.name} {year} - {fastest_1.Driver} vs {fastest_2.Driver} \n Gap: {gap} ms', size=18, y=0.97)

    # Adjust margins and turn of axis
    #fastest1 alo fastest2 sai
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')
    if fastest_1.Sector1Time<fastest_2.Sector1Time:
        ax.plot(chunks[0]['X'], chunks[0]['Y'], color=driver1_color, linestyle='-', label=driver1+"  Sector 1", linewidth=8, zorder=0)
    else:
        ax.plot(chunks[0]['X'], chunks[0]['Y'], color=driver2_color, linestyle='-',label=driver2+"  Sector 1", linewidth=8, zorder=0)
    if fastest_1.Sector2Time<fastest_2.Sector2Time:
        ax.plot(chunks[1]['X'], chunks[1]['Y'], color=driver1_color, linestyle='-', label=driver1+"  Sector 2",linewidth=8, zorder=0)
    else:
        ax.plot(chunks[1]['X'], chunks[1]['Y'], color=driver2_color, linestyle='-', label=driver2+"  Sector 2",linewidth=8, zorder=0)
    if fastest_1.Sector3Time<fastest_2.Sector3Time:
        ax.plot(chunks[2]['X'], chunks[2]['Y'], color=driver1_color, linestyle='-',label=driver1+"  Sector 3", linewidth=8, zorder=0)
    else:
        ax.plot(chunks[2]['X'], chunks[2]['Y'], color=driver2_color, linestyle='-',label=driver2+"  Sector 3    ", linewidth=8, zorder=0)

    ax.legend()

    #cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    #normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    #legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

    plt.show()
    st.pyplot(fig1)




