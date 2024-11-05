import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Function to update the Google Sheet with feedback for the "Home" page
def update_home_feedback():
    # Get the selected rating from session state
    selected_rating = st.session_state.home_feedback
    if selected_rating is not None:
        # Create a new DataFrame with the new data
        df_data = {
            "Page": ["Home"],
            "Count": [sentiment_mapping[selected_rating]]
        }
        new_df = pd.DataFrame(df_data)

        # Concatenate the new DataFrame with the existing data
        updated_df = pd.concat([existing_data, new_df], axis=0, ignore_index=True)

        # Update the Google Sheet
        conn.update(worksheet="Ratings", data=updated_df)
        st.success("Home Feedback updated in Google Sheets.")

# Function to update the Google Sheet with feedback for the "About" page
def update_about_feedback():
    # Get the selected rating from session state
    selected_rating = st.session_state.about_feedback
    if selected_rating is not None:
        # Create a new DataFrame with the new data
        df_data = {
            "Page": ["About"],
            "Count": [sentiment_mapping[selected_rating]]
        }
        new_df = pd.DataFrame(df_data)

        # Concatenate the new DataFrame with the existing data
        updated_df = pd.concat([existing_data, new_df], axis=0, ignore_index=True)

        # Update the Google Sheet
        conn.update(worksheet="Ratings", data=updated_df)
        st.success("About Feedback updated in Google Sheets.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Ratings", usecols=list(range(2)), ttl=5)
existing_data = existing_data.dropna(how="all")
st.sidebar.title("Sidebar")
st.title("Tag Factory")
c1, c2, c3 = st.columns(3)

with c1:
    st.html("<div class='status' style='background-color: #31709e; color: white; padding-top: 2px; padding-bottom: 2px; padding-left: 7px; padding-right: 7px; border-radius: 6px; font-family: Arial, sans-serif; font-size: 12px; display: inline-block; text-align: center; box-shadow: 0px 3px 4px rgba(0, 0, 0, 0.2);'>Vote for Streamlit</div>")
with c2:
    st.html("<div class='status' style='background-color: #aa485b; color: white; padding-top: 2px; padding-bottom: 2px; padding-left: 7px; padding-right: 7px; border-radius: 6px; font-family: Arial, sans-serif; font-size: 12px; display: inline-block; text-align: center; box-shadow: 0px 3px 4px rgba(0, 0, 0, 0.2);'><b>NEW Patero Analysis</b></div>")
with c3:
    st.html("<div class='status' style='background-color: #f2a947; color: white; padding-top: 2px; padding-bottom: 2px; padding-left: 7px; padding-right: 7px; border-radius: 6px; font-family: Arial, sans-serif; font-size: 12px; display: inline-block; text-align: center; box-shadow: 0px 3px 4px rgba(0, 0, 0, 0.2);'>Python</div>")

# Feedback widget for the "Home" page
sentiment_mapping = [1, 2, 3, 4, 5]
st.feedback(
    options="stars",
    key="home_feedback",
    on_change=update_home_feedback  # Provide a callable function here
)

# Feedback widget for the "About" page
st.feedback(
    options="stars",
    key="about_feedback",
    on_change=update_about_feedback  # Provide a callable function here
)

st.title("Google Sheets as a DataBase")

# Function to create a sample Orders dataframe
def create_orders_dataframe():
    return pd.DataFrame({
        'OrderID': [101, 102, 103, 104, 105],
        'CustomerName': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'ProductList': ['ProductA, ProductB', 'ProductC', 'ProductA, ProductC', 'ProductB, ProductD', 'ProductD'],
        'TotalPrice': [200, 150, 250, 300, 100],
        'OrderDate': ['2023-08-18', '2023-08-19', '2023-08-19', '2023-08-20', '2023-08-20']
    })

# Create the Orders dataframe
orders = create_orders_dataframe()

# Update the TotalPrice column in the orders dataframe to create updated_orders
updated_orders = orders.copy()
updated_orders['TotalPrice'] = updated_orders['TotalPrice'] * 100

with st.expander("Data ⤵"):
    st.write("Orders")
    st.dataframe(orders)
    st.write("Updated Orders")
    st.dataframe(updated_orders)

st.divider()
st.write("CRUD Operations:")
# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Taking actions based on user input
if st.button("New Worksheet"):
    conn.create(worksheet="Ratings", data=orders)
    st.success("Worksheet Created 🎉")

if st.button("Calculate Total Orders Sum"):
    sql = 'SELECT SUM("TotalPrice") as "TotalOrdersPrice" FROM Orders;'
    total_orders = conn.query(sql=sql)  # default ttl=3600 seconds / 60 min
    st.dataframe(total_orders)

if st.button("Update Worksheet"):
    conn.update(worksheet="Ratings", data=updated_orders)
    st.success("Worksheet Updated 🤓")

if st.button("Clear Worksheet"):
    conn.clear(worksheet="Ratings")
    st.success("Worksheet Cleared 🧹")

st.dataframe(existing_data)

with st.popover("Popover"):
    st.write("### How are you")
    st.html("<div class='status' style='background-color: #31709e; color: white; padding-top: 2px; padding-bottom: 2px; padding-left: 7px; padding-right: 7px; border-radius: 6px; font-family: Arial, sans-serif; font-size: 12px; display: inline-block; text-align: center; box-shadow: 0px 3px 4px rgba(0, 0, 0, 0.2);'>Vote for Streamlit</div>")
    text = st.text_input("What is your name?")
    job = st.selectbox("Job", ['Plumber', 'Carpenter', 'Builder'], index=0)

st.write(f"You are a {job}, {text}.")
