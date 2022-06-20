import streamlit as st
from multiapp import MultiApp
from pages import f1,telemetrycomp

app = MultiApp()


# Add all your application here
app.add_app("Pace Difference vs Leader", f1.app)
app.add_app("Telemetry Comparision", telemetrycomp.app)


# The main app
app.run()
