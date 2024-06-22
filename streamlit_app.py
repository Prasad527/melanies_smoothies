# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize Your Smoothies :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be",name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df=my_dataframe.to_pandas()


ingredients_list = st.multiselect('Choose uptop 5 ingredeints:',my_dataframe,max_selections=5)


if ingredients_list:
    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        st.subheader(fruit_choosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


