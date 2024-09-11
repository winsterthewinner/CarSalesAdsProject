import streamlit as st
import pandas as pd

df=pd.read_csv('vehicles_us.csv')

st.header('Market of Used Cars.Original data')
st.write("""
##### Filter the data below to see the ads by manufacturer
""")
show_new_cars =  st.checkbox('Include new cars from dealers')
if not show_new_cars:
    df = df[df.condition!='new']

#--------------------------------------------------------------------------------------------------------------------------------------

#creating filtered data by manufacturer and year
model_choice = df['model'].unique()
make_choice_man = st.selectbox('Select Model:', model_choice)


#creating min and max years as limits for slider
min_year, max_year=int(df['model_year'].min()), int(df['model_year'].max())

#creating slider
year_range = st.slider(
    "Choose year",
    value=(min_year,max_year),min_value=min_year,max_value=max_year)

actual_range=list(range(year_range[0],year_range[1]+1))

filtered_type=df[(df.model==make_choice_man)&(df.model_year.isin(list(actual_range)))]

st.table(filtered_type)

#----------------------------------------------------------------------------------------------------------------------------------------

st.header('Price Analysis')
st.write("""###### 
Let's analyze what influences price most. We'll check how distro of price varies depending on transmission, fuel or type and condition
""")

#histogram with the split by parameter of choice: paint_color, transmission, fuel, type, condition
import plotly.express as px

#creating list of options to choose from
list_for_hist=['transmission', 'fuel', 'type', 'condition']

#creating selectbox
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

#plotly histogram, where price_usd is split by the choice made in selectbox
fig1 = px.histogram(df, x="price", color=choice_for_hist)

#adding title
fig1.update_layout(title="<b> Split of price by {}</b>".format(choice_for_hist))
st.plotly_chart(fig1)

#------------------------------------------------------------------------------------------------------------------------------------------

#defining age category of car
df['age']=2022-df['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['age_category']= df['age'].apply(age_category)

#------------------------------------------------------------------------------------------------------------------------------------------

st.write("""
###### Now let's check how price is affected by odometer, fuel or cylinders in the ad
""")

#Distribution of price depending on odometer_value, engine_capacity, number_of_photos with the split by age category

list_for_scatter=['odometer', 'fuel', 'cylinders',  'age_category']
choice_for_scatter =  st.selectbox('Price dependency on: ', list_for_scatter)
fig2 = px.scatter(df, x="price", y=choice_for_scatter,hover_data=['model_year'])

fig2.update_layout(title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)