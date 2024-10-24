import streamlit as st
import numpy as np
import mysql.connector
from streamlit_option_menu import option_menu
st.set_page_config(
    layout="wide",
    page_title=" Home | AI Fraud",
    page_icon=" "
)
with st.sidebar:
    selected = option_menu(
        menu_title= "AI Fraud",
        options=["Home","Contact","Signup","Login"],
        icons=["house","envelope","door-open","key"],
        default_index=0,
        orientation= "vertical",
        menu_icon="cast",
        styles={
        "icon": {"font-size": "17px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"3px", "--hover-color": "#262730"}
    }
    )
    if selected =="Contact":
        st.write("\n\n")
        st.write("""
            # Contact Us   
                """)
        with st.form("Contact"):
            CName = st.text_input('Name',placeholder='Enter Name')
            CPhone = st.text_input('Mobile',placeholder='Enter Mobile')
            CEmail = st.text_input('Email',placeholder='Enter Email')
            CMessage = st.text_area('Message',placeholder='Enter Your Message Here...')
            st.write("\n\n")
            Contact_submit = st.form_submit_button('Submit')
            if Contact_submit:
                st.success("We will contact soon...", icon = "✅")
        st.write("\n\n")   

    if selected =="Signup":
        st.write("\n\n")
        st.write("""
        # Hello 👋, Sign Up Here    """)
        with st.form("Registeration"):
            def init_connection():
                return mysql.connector.connect(**st.secrets["mysql"])
            conn = init_connection()
            RName = st.text_input('Name',placeholder='Enter Name')
            RPhone = st.text_input('Mobile',placeholder='Enter Mobile')
            REmail = st.text_input('Email',placeholder='Enter Email')
            RPassword = st.text_input('Password',placeholder='Enter Password',type="password")
            st.write("\n\n")
            Signup = st.form_submit_button('Register Me')
            if Signup:
                cursor = conn.cursor()
                sql = f"""INSERT INTO register(
                Fname,Phone,Email,Pass)
                VALUES ('{RName}', '{RPhone}','{REmail}','{RPassword}')"""
                cursor.execute(sql)
                conn.commit()
                st.success("Congratulations! You are part of SENSI", icon = "✅")
    if selected =="Login":
        st.write("\n\n")
        st.write("""
        # Hello 👋, Login Here    """)
        with st.form("Registeration"):
            def init_connection():
                return mysql.connector.connect(**st.secrets["mysql"])
            conn = init_connection()
            REmail = st.text_input('Email',placeholder='Enter Email')
            RPassword = st.text_input('Password',placeholder='Enter Password',type="password")
            st.write("\n\n")
            Login = st.form_submit_button('Login')
            
            if Login:
                cursor = conn.cursor()
                sql = f"""SELECT * from register
                where Email = '{REmail}' and Pass = '{RPassword}';"""
                cursor.execute(sql)
                cursor.fetchall()
                result = cursor.rowcount
                if result == 1:
                    st.success("Welcome! Loggined Successfully", icon = "✅")
                else:
                    st.error("OOPS!!! Invalid ID or Password", icon = "🚨")
        st.write("\n\n")

st.title("AI-Powered : Fraud Detection & Prevention")
st.image("images/main.jpg",caption='AI Powered - Fraud Detection & Prevention')
st.write(
    """
    The **AI-Powered Fraud Detection and Prevention** Platform helps users identify and 
    prevent various types of fraud, such as financial fraud, identity theft, and transaction fraud. 
    It works by analyzing user behavior, patterns, and metadata to detect suspicious activities. 
    The platform includes features like real-time fraud detection, which catches fraudulent activities 
    as they happen, and anomaly detection, which identifies unusual behavior or transactions that may indicate fraud. Additionally, the platform offers prevention strategies to stop fraud before it occurs. By leveraging AI technologies, this platform helps businesses and individuals protect themselves from different types of fraud and maintain a secure environment.
    """
)        
st.write("\n")
