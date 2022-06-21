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
from datetime import timedelta
from timple.timedelta import strftimedelta
from fastf1 import utils

def app():
    
    st.header('RacePace comparision among the entire grid')

    #Get the input data from the user for Year, Grand Prix Location and Session Respectively
    
    year = st.number_input('Enter Year',min_value=2000, max_value=3000,step=1)
    gp = st.text_input('Enter Grand Prix Location')
    #sessiontypechoice=st.number_input('Enter 1 for qualifying or 2 for race',min_value=1, max_value=2,step=1)
    if gp != "":
        st.write('The current selectd GP is ' + str(year) + ' '+gp+' Grand Prix ')

        #ff1.plotting.setup_mpl()
        
            # if sessiontypechoice == 1:
            #     sessiontype='Q'
            # elif sessiontypechoice == 2:
            #     sessiontype='R'
            # else:
            #     print("Unknown choice")

        session = ff1.get_session(year, gp,"R")
        session.load()
        laps=session.load_laps(with_telemetry=True)
        sessiondf=pd.DataFrame(session.results)
        #getting the drivernumbers into a list for usage
        drivernumber_list=sessiondf['DriverNumber'].tolist()
        # Creating a new variable for each dataframe 
        index=1
        for i in drivernumber_list:
        
            temp=laps.pick_driver(i)
            temp2=temp.pick_fastest()
            getdrivername=temp2.Driver
            globals()['Driver%s' % index] = laps.pick_driver(getdrivername)
            # assigning only the laps which doesn't involve safety laps and involve 
            #also eliminates the in/out laps
            globals()['Driver%s' % index]=pd.DataFrame(globals()['Driver%s' % index].pick_accurate())
        
            index=index+1
        # Creating a list from 1 to 20 
        # So that this can be used to loop from driver 1
        looper = list(range(1,20+1))
        # creation of empty dataframe for plotting purpose 
        racepace_df=pd.DataFrame({'Driver':[],
                        'DriverNumber':[],
                        'RacePace':[],
                        'Team':[],
                        'TeamColor':[]})
        # Creating a loop to iterate through all the drivers
        #  and get their average race pace

        for i in looper:
            globals()['n%s' % i]=timedelta(seconds=0)
            
            for index, row in globals()['Driver%s' % i].iterrows():
            
                globals()['n%s' % i]+=row["LapTime"]

            # get the driver names 
            driver_name=globals()['Driver%s' % i].Driver.head(1).tolist()
            driver_name=driver_name[0]
            # driver number
            driver_number=globals()['Driver%s' % i].DriverNumber.head(1).tolist()
            driver_number=driver_number[0]
            # driver team
            driver_team=globals()['Driver%s' % i].Team.head(1).tolist()
            driver_team=driver_team[0]
            # team color
            driver_team_color=ff1.plotting.team_color(driver_team)
            

            globals()['average_racepace%s' % driver_name]=(globals()['n%s' % i]/len(globals()['Driver%s' % i]))

            print("Average Race Pace of  "+driver_name+" in "+ session.event['EventName']+" : "+str(globals()['average_racepace%s' % driver_name]))
            #adding a row with the data
            data=[{'Driver': driver_name,'DriverNumber':driver_number,'RacePace':globals()['average_racepace%s' % driver_name],'Team':driver_team,'TeamColor': str(driver_team_color)}]
            # data added to DataFrame 
            racepace_df=racepace_df.append(data,ignore_index=True,sort=False)
    
        # add colors to a list of all the teams
        team_colors = list()
        for index,lap in racepace_df.iterrows():
            colors=lap["TeamColor"]
            team_colors.append(colors)
        fastest_pace=timedelta(seconds=0)
        tempss=timedelta(seconds=0)
        #calculating the fastest race pace
        for index,pace in racepace_df.iterrows():
            nexts=pace['RacePace']
            if (fastest_pace==tempss) or (fastest_pace > nexts):
                fastest_pace = pace['RacePace']
        # Creating a col for delta values w.r.t fastest race pace
        racepace_df['Delta']=racepace_df['RacePace'] - fastest_pace
        #deltalist
        deltalist=list()
        for index, deltas in racepace_df.iterrows():
            delta=deltas['Delta']
            delta=strftimedelta(delta, '%s.%ms')

            deltalist.append(delta)
        racepace_df.index=racepace_df.index+1
        # finally plotting the drivers race pace w.r.t to the leader
        fig, ax = plt.subplots()

        ax.barh(racepace_df.index, racepace_df['Delta'],
                color=team_colors, edgecolor='grey')
        ax.set_yticks(racepace_df.index)
        ax.set_yticklabels(racepace_df['Driver'])

        # show fastest at the top
        ax.invert_yaxis()

        # draw vertical lines behind the bars
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
        lap_time_string = strftimedelta(fastest_pace, '%m:%s.%ms')

        for i, v in enumerate(deltalist):
                ax.text(1, i+1.3, "+" +str(v),color = 'black', fontweight = 'bold')

        plt.suptitle(f"{session.event['EventName']} {session.event.year} {session.name}\n"
                    f"Fastest Lap: {lap_time_string} ")
        fig.set_size_inches(16, 10)
        fig.set_dpi(800)
        st.pyplot(fig)
        fig.savefig(session.event['EventName']+" racepace.jpg",dpi=800)

        plt.show()