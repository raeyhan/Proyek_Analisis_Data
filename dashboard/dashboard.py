import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
dongsiDf = pd.read_csv("PRSA_Data_Dongsi_20130301-20170228.csv")

# Convert date columns
years = dongsiDf['year'].values
months = dongsiDf['month'].values
days = dongsiDf['day'].values
hours = dongsiDf['hour'].values
full_date = []

for i in range(dongsiDf.shape[0]):
    date_time = str(years[i])+'-'+str(months[i])+'-'+str(days[i])+' '+str(hours[i])+':'+str(0)
    full_date.append(date_time)

dates = pd.to_datetime(full_date)
dates = pd.DataFrame(dates, columns=['date'])
dongsiDf = pd.concat([dates, dongsiDf], axis=1)

# Fill missing values for numerical columns
numerical_cols = dongsiDf.select_dtypes(include=['float64', 'int64']).columns
dongsiDf[numerical_cols] = dongsiDf[numerical_cols].fillna(dongsiDf[numerical_cols].mean())

# Fill missing values for categorical columns
categorical_cols = dongsiDf.select_dtypes(include=['object']).columns
for col in categorical_cols:
    mode_val = dongsiDf[col].mode()[0]
    dongsiDf[col].fillna(mode_val, inplace=True)

# Verify no missing values remain
if dongsiDf.isna().sum().sum() == 0:
    st.write("No missing values remain in the dataset.")

# Streamlit app
st.title('Dashboard Analisis Meteorologi Dongsi')

# Display Data
st.subheader('Data Awal')
st.write(dongsiDf.head())

# Temperature over time
st.subheader('Temperature Over Time')
fig_temp = plt.figure(figsize=(15, 6))
plt.plot(dongsiDf['date'], dongsiDf['TEMP'], color='red', label='Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.legend()
st.pyplot(fig_temp)

# Pressure over time
st.subheader('Pressure Over Time')
fig_pres = plt.figure(figsize=(15, 6))
plt.plot(dongsiDf['date'], dongsiDf['PRES'], color='green', label='Pressure')
plt.xlabel('Date')
plt.ylabel('Pressure (hPa)')
plt.title('Pressure Over Time')
plt.legend()
st.pyplot(fig_pres)

# Dew Point over time
st.subheader('Dew Point Over Time')
fig_dewp = plt.figure(figsize=(15, 6))
plt.plot(dongsiDf['date'], dongsiDf['DEWP'], color='purple', label='Dew Point')
plt.xlabel('Date')
plt.ylabel('Dew Point (°C)')
plt.title('Dew Point Over Time')
plt.legend()
st.pyplot(fig_dewp)

# Rain over time
st.subheader('Rain Over Time')
fig_rain = plt.figure(figsize=(15, 6))
plt.plot(dongsiDf['date'], dongsiDf['RAIN'], color='blue', label='Rain')
plt.xlabel('Date')
plt.ylabel('Rain (mm)')
plt.title('Rain Over Time')
plt.legend()
st.pyplot(fig_rain)

# Wind Speed over time
st.subheader('Wind Speed Over Time')
fig_wspm = plt.figure(figsize=(15, 6))
plt.plot(dongsiDf['date'], dongsiDf['WSPM'], color='orange', label='Wind Speed')
plt.xlabel('Date')
plt.ylabel('Wind Speed (m/s)')
plt.title('Wind Speed Over Time')
plt.legend()
st.pyplot(fig_wspm)

# Yearly average PM2.5
dongsiDf['date'] = pd.to_datetime(dongsiDf['date'])
dongsiDf['year'] = dongsiDf['date'].dt.year
yearly_avg_pm25 = dongsiDf.groupby('year')['PM2.5'].mean().reset_index()

st.subheader('Yearly Average PM2.5')
fig_pm25 = plt.figure(figsize=(10, 6))
plt.plot(yearly_avg_pm25['year'], yearly_avg_pm25['PM2.5'], marker='o', linestyle='-', color='b')
plt.xlabel('Year')
plt.ylabel('Average PM2.5')
plt.title('Yearly Average PM2.5 in Dongsi')
plt.grid(True)
st.pyplot(fig_pm25)

# Correlation Matrix
st.subheader('Correlation Matrix')
correlation_matrix = dongsiDf[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig_corr = plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
st.pyplot(fig_corr)
