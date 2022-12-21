import pandas as pd
import mysql.connector as connection
import streamlit as st
import streamlit_authenticator as stauth
import toml
from streamlit_option_menu import option_menu
from PIL import Image

# Connection to database
toml_data = toml.load("connector.toml")
HOST_NAME = toml_data['mysql']['host']
DATABASE = toml_data['mysql']['database']
PASSWORD = toml_data['mysql']['password']
USER = toml_data['mysql']['user']
PORT = toml_data['mysql']['port']

# Using the variables we read from secrets.toml
conn = connection.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True)
c = conn.cursor()


# SOME FUNCTIONS

def add_sector(name):
    query = """INSERT INTO sector (name) VALUES (%s)"""
    c.execute(query,(name,))
    conn.commit()

# def add_indicator(name, sector):
#     c.execute("""INSERT INTO indicator (name, sectorId) VALUES(%s, %s)""", (name, sector))
#     conn.commit()

# MANAGE THE USERS
def add_user(username, email, password, type, phone):
    c.execute("""INSERT INTO user (username, email, password, type, phone) VALUES (%s,%s,%s,%s,%s)""", (username, email, password, type, phone))
    conn.commit()

def add_partner(name, website, active, userId):
    c.execute("""INSERT INTO partner (name, website, active, userId) VALUES (%s, %s, %s,%s)""", (name, website, active, userId))
    conn.commit()

def add_subscription(sector, partner, startDate, endDate):
    c.execute("""INSERT INTO subscription (sectorId, partnerId, startDate, endDate) VALUES (%s, %s, %s, %s)""", (sector, partner, startDate, endDate))
    conn.commit()
img1 = Image.open(r"C:\xampp\htdocs\Congo-Big-Data\images\capture 1.JPG")
img2 = Image.open(r"C:\xampp\htdocs\Congo-Big-Data\images\Capture2.JPG")
img3 = Image.open(r"C:\xampp\htdocs\Congo-Big-Data\images\Capture3.JPG")
def page_about():
    title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>About Congo Big Data</h1>", unsafe_allow_html=True) 
    st.write("Congo Big Data is an online platform for viewing statistical data relating to various sectors of the DR Congo. In a rigorous and innovative way, data is collected periodically from participants in different territories and cities of 26 Congolese provinces by two consulting firms, namely Innovations et Entrepreneuriat Social (www.iescongo.com) and Data Mining Lab (www.dmlcongo.com). Other data is collected from accredited secondary sources.")
    st.write("From data collection to analysis, a rigorous, systematic, ethical and deontological methodological protocol is followed for Quality assurance. Any cleaning or modification made to the collected data is documented and provided to users for reliability and accountability.")
    st.write("Congo Big data is an important tool to guide Managers in decision-making. It produces integrated and disaggregated data for the formulation, monitoring/evaluation of development policies and programs. It is set up using raw multi-sector data from half-yearly surveys in order to allow subscriber development actors (Government, Donors, Non-Governmental Organizations, Companies, Universities, etc.) to monitor in real time the level performance of their actions and/or the context by geographical area in the DRC. This allows them to make the necessary adaptations based on evidence (Adaptation Management and results-based).")
    st.write("Apart from the specific themes addressed at the request of partners, data on impact indicators are collected every six months for 6 sectors, namely: (1) Stabilization and Social Cohesion, (2) Resilience and Economy, (3) Food Security and Nutrition , (4) Environment and WASH, (5) Agricultural Value Chains and Market Systems Development and (6) Gender.")
    st.write('Some images from our plateform')
    col1, col2, col3 = st.columns([0.33, 0.33, 0.33])
    with col1:
        st.image(img1)
    with col2:
        st.image(img2)
    with col3:
        st.image(img3)

# MANAGE THE USER

def view_all_users():
    c.execute("""SELECT * FROM user""")
    data = c.fetchall()
    return data

def view_unique_user():
    c.execute("""SELECT DISTINCT username FROM user""")
    data = c.fetchall()
    return data

def get_user(username):
    query = """SELECT * FROM user WHERE username=%s"""
    c.execute(query,(username,))
    data = c.fetchall()
    return data

def update_user(username, email, password, type, phone, id):
    c.execute("""UPDATE user SET username = %s, email = %s, password = %s, type = %s, phone = %s WHERE id = %s""", (username, email, password, type, phone, id))
    conn.commit()

def delete_user(user):
    query = """DELETE FROM user WHERE id = %s"""
    c.execute(query,(user,))
    conn.commit()

# MANAGE THE PARTNER

def view_all_partners():
    c.execute("""SELECT id, name, website, active FROM partner""")
    data = c.fetchall()
    return data

def view_unique_partner():
    c.execute("""SELECT DISTINCT name FROM partner""")
    data = c.fetchall()
    return data

def view_unique_active_partner():
    c.execute("""SELECT DISTINCT name FROM partner WHERE active='0'""")
    data = c.fetchall()
    return data

def view_unique_desable_partner():
    c.execute("""SELECT DISTINCT name FROM partner WHERE active='1'""")
    data = c.fetchall()
    return data

def get_partner(name):
    query = """SELECT * FROM partner WHERE name = %s"""
    c.execute(query, (name,))
    data = c.fetchall()
    return data

def update_partner(name, website, state, id):
    c.execute("""UPDATE partner SET name=%s, website=%s, active=%s WHERE id = %s""", (name, website, state, id))
    conn.commit()

def delete_partner(partner):
    query = """DELETE FROM partner WHERE id = %s"""
    c.execute(query,(partner,))
    conn.commit()

def active_partner(partner):
    c.execute("""UPDATE partner SET active = %s WHERE id = %s""", (1, partner))
    conn.commit()

def disable_partner(partner):
    c.execute("""UPDATE partner SET active = %s WHERE id = %s""", (0, partner))
    conn.commit()

# MANAGE SECTORS

def view_all_sectors():
    c.execute("""SELECT * FROM sector""")
    data = c.fetchall()
    return data

def view_unique_sector():
    c.execute("""SELECT DISTINCT name FROM sector""")
    data = c.fetchall()
    return data

def get_sector(name):
    query = """SELECT * FROM sector WHERE name = %s"""
    c.execute(query,(name,))
    data = c.fetchall()
    return data

def update_sector(name, id):
    c.execute("""UPDATE sector SET name=%s WHERE id=%s""",(name, id))
    conn.commit()

def delete_sector(id):
    query = """DELETE FROM sector WHERE id = %s"""
    c.execute(query,(id,))
    conn.commit()