import streamlit as st
import pytz
from datetime import datetime, timedelta

# Title of the app
st.title('Real-Time Digital Clock and Timer')

# Timezone selection
st.subheader('Select Time Zone')
selected_timezone = st.selectbox('', pytz.all_timezones)

# Function to display current time in the selected timezone
def get_time_in_timezone(tz):
    timezone = pytz.timezone(tz)
    return datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

st.write('Current Time in Selected Time Zone:', get_time_in_timezone(selected_timezone))

# Stopwatch feature
st.subheader('Stopwatch')
if st.button('Start'):
    st.session_state.start_time = datetime.now()
    st.session_state.running = True

if st.button('Stop') and st.session_state.running:
    st.session_state.end_time = datetime.now()
    st.session_state.running = False
    elapsed_time = st.session_state.end_time - st.session_state.start_time
    st.write(f'Elapsed Time: {elapsed_time}')

# Timer feature
st.subheader('Timer')
timer_minutes = st.number_input('Set Timer (minutes)', min_value=1)
if st.button('Start Timer'):
    target_time = datetime.now() + timedelta(minutes=timer_minutes)
    st.session_state.timer_running = True

if st.session_state.get('timer_running'):
    remaining_time = target_time - datetime.now() 
    st.write(f'Time Remaining: {remaining_time}')
    if remaining_time.total_seconds() <= 0:
        st.write('Timer Finished!')
        st.session_state.timer_running = False

timer_minutes = st.number_input('Set Timer (minutes)', min_value=1)
