import streamlit as st
import helper  # Ensure this module contains the generate_restaurant_name_and_items function

# Title of the Streamlit app
st.title("Restaurant Name & Items Generator")

# Sidebar for selecting cuisine
cuisine = st.sidebar.selectbox("Pick a Cuisine", ('Indian', 'Italian', 'Mexican'))

# Check if a cuisine is selected
if cuisine:
    # Call the helper function to get the response
    response = helper.generate_restaurant_name_and_items(cuisine)

    # Display the generated restaurant name
    restaurant_name = response['restaurant_name'].strip()
    st.header(restaurant_name)

    # Display the menu items
    st.write('Menu Items:')
    menu_items = response['menu_items'].strip().split('\n')  # Split by new lines

    # Loop through the menu items and display each
    for item in menu_items:
        st.write("-", item.strip())

