import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"  # Change to your backend's deployed URL if necessary

def show_authentication_page():
    st.title("Auction Portal Login")
    phone_number = st.text_input("Enter your Indian phone number:")
    if st.button("Send OTP"):
        response = requests.post(f"{BACKEND_URL}/api/send-otp", json={"phone_number": phone_number})
        st.write(response.json()["message"])

def show_auction_room():
    st.title("Auction Room")
    st.write("Welcome to the live auction!")
    stats = requests.get(f"{BACKEND_URL}/api/auction-stats").json()
    st.write(stats)

# Navigation
page = st.sidebar.selectbox("Choose Page", ["Login", "Auction Room"])

if page == "Login":
    show_authentication_page()
elif page == "Auction Room":
    show_auction_room()