import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")

def create_mounthly_bike_df(bike_df):
    mounthly_bike_df = bike_df.resample(rule='M', on='dteday').agg({
        'casual':'sum',
        'registered':'sum',
        "cnt": "sum"
    })
    mounthly_bike_df.index = mounthly_bike_df.index.strftime('%y-%b')
    mounthly_bike_df = mounthly_bike_df.reset_index()
    mounthly_bike_df.rename(columns={
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    return mounthly_bike_df

def craete_bike_sesional_df(bike_df):
    bike_sesional_df = bike_df.groupby(by='season').agg({
        'registered':'sum',
        'casual':'sum',
        'cnt':'sum'
    }).sort_values(by="cnt", ascending=False)
    bike_sesional_df = bike_sesional_df.reset_index()

    bike_sesional_df.rename(columns={
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    return bike_sesional_df

def create_bike_time_df(bike_df):
    bike_time_df = bike_df.groupby(by='time').agg({
        'registered':'sum',
        'casual':'sum',
        'cnt':'sum'
    })
    bike_time_df = bike_time_df.reset_index()
    bike_time_df.rename(columns={
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    return bike_time_df

def create_bike_weeked_df(bike_df):
    bike_holiday_df = bike_df.groupby(by='holiday').agg({
        'registered':'sum',
        'casual':'sum',
        'cnt':'sum'
    }).sort_values(by="cnt", ascending=False)

    bike_holiday_df = bike_holiday_df.reset_index()
    bike_holiday_df.rename(columns={
        'holiday':'workingday',
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    bike_holiday_df = bike_holiday_df.drop(0)
    bike_weeked_df = bike_df.groupby(by='workingday').agg({
        'registered':'sum',
        'casual':'sum',
        'cnt':'sum'
    })
    bike_weeked_df = bike_weeked_df.reset_index()
    bike_weeked_df.rename(columns={
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    new_row = {'workingday':bike_holiday_df.values[0][0], 'total_casual_rent':bike_holiday_df.values[0][1], 'total_registered_rent':bike_holiday_df.values[0][2], 'total_all_rent':bike_holiday_df.values[0][3]}
    bike_weeked_df.loc[2] = new_row
    return bike_weeked_df

def create_bike_weather_df(bike_df):
    bike_weather_df = bike_df.groupby(by='weathersit').agg({
        'registered':'sum',
        'casual':'sum',
        'cnt':'sum'
    })
    bike_weather_df = bike_weather_df.reset_index()
    bike_weather_df.rename(columns={
        'weathersit':'weather',
        'casual':"total_casual_rent",
        'registered':'total_registered_rent',
        "cnt": "total_all_rent"
    }, inplace=True)
    return bike_weather_df


bike_df = pd.read_csv("bike.csv")
bike_df["dteday"] = pd.to_datetime(bike_df["dteday"])
mounthly_bike_df = create_mounthly_bike_df(bike_df)
bike_sesional_df = craete_bike_sesional_df(bike_df)
bike_time_df = create_bike_time_df(bike_df)
bike_weeked_df = create_bike_weeked_df(bike_df)
bike_weather_df = create_bike_weather_df(bike_df)


st.header('Bicycle Rent Dashboard :sparkles:')
st.subheader('Daily Rents')

col1, col2 = st.columns(2)
 
with col1:
    total_orders = mounthly_bike_df.total_all_rent.sum()
    st.metric("Total all rent", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    mounthly_bike_df["dteday"],
    mounthly_bike_df["total_all_rent"],
    marker='o', 
    linewidth=2,
    color="#0057e7"
)
 
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    total_orders = mounthly_bike_df.total_casual_rent.sum()
    st.metric("Total casual renter", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    mounthly_bike_df["dteday"],
    mounthly_bike_df["total_casual_rent"],
    marker='o', 
    linewidth=2,
    color="#0057e7"
)
 
st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    total_orders = mounthly_bike_df.total_registered_rent.sum()
    st.metric("Total registered enter", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    mounthly_bike_df["dteday"],
    mounthly_bike_df["total_casual_rent"],
    marker='o', 
    linewidth=2,
    color="#0057e7"
)
 
st.pyplot(fig)


st.subheader("The Season When Most People Rent Bike")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(60, 16))
 
colors = ["#72BCD4", "#8c8d8f", "#8c8d8f", "#8c8d8f"]
 
sns.barplot(y="total_registered_rent", x="season", data=bike_sesional_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Total Registered Renter ", loc="center", fontsize=50)
ax[0].tick_params(axis ='x', labelsize=50)
 
sns.barplot(y="total_casual_rent", x="season", data=bike_sesional_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Total Casual Renter", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=50)
 
sns.barplot(y="total_all_rent", x="season", data=bike_sesional_df, palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Total All Renter", loc="center", fontsize=50)
ax[2].tick_params(axis='x', labelsize=50)
 
st.pyplot(fig)



st.subheader("The Time When Most People Rent Bike")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(60, 16))
 
colors = ["#72BCD4", "#8c8d8f", "#8c8d8f", "#8c8d8f"]
 
sns.barplot(y="total_registered_rent", x="time", data=bike_time_df.sort_values(by="total_registered_rent", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Total Registered Rent", loc="center", fontsize=50)
ax[0].tick_params(axis ='x', labelsize=50)
 
sns.barplot(y="total_casual_rent", x="time", data=bike_time_df.sort_values(by="total_casual_rent", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Total Casual Rent", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=50)
 
sns.barplot(y="total_all_rent", x="time", data=bike_time_df.sort_values(by="total_all_rent", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Total All Renter", loc="center", fontsize=50)
ax[2].tick_params(axis='x', labelsize=50)
 
st.pyplot(fig)


st.subheader("The Day When Most People Rent Bike")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
 
colors = ["#72BCD4", "#8c8d8f", "#8c8d8f"]
 
sns.barplot(y="total_all_rent", x="workingday", data=bike_weeked_df.sort_values(by="total_all_rent", ascending=False), palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader("The Weather When Most People Rent Bike")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
 
colors = ["#72BCD4", "#8c8d8f", "#8c8d8f", "#8c8d8f"]
 
sns.barplot(y="total_all_rent", x="weather", data=bike_weather_df.sort_values(by="total_all_rent", ascending=False), palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
