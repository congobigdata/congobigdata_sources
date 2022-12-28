import pandas as pd
import mysql.connector as connection
import streamlit as st
import streamlit_authenticator as stauth
import toml
from streamlit_option_menu import option_menu
from PIL import Image

from copy import deepcopy
from datetime import date
from textwrap import fill
from turtle import color
from unicodedata import name
import plotly.express as px
import folium
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
import matplotlib.pyplot as plt
from pandas.plotting import table
from fpdf import FPDF
import base64
import datetime
from io import StringIO
import streamlit.components.v1 as components


# IMPORT FUNCTIONS

from functions import view_unique_desable_partner, view_unique_active_partner, view_all_partners, view_unique_partner, get_partner, update_partner, delete_partner, active_partner, disable_partner, view_all_sectors, view_unique_sector, get_sector, update_sector, delete_sector, delete_user, update_user, view_unique_user, get_user, page_about, add_subscription, add_sector, add_user, view_all_users, add_partner

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

# Variable to diplay title of page and favicon
st.set_page_config(page_title="Congo Big Data", page_icon=":earth_africa:", layout="wide")

# -- USER AUTHENTICATION

c.execute("""SELECT * FROM user""")
users = c.fetchall()
usernames1=[]
ids1 = []
names1 = []
passwords1 = []
types1 = []
for row in users:
    id2 = row[0]
    name2 = row[1]
    username2 = row[2]
    password2 = row[3]
    type2 = row[4]
    ids1.append(id2)
    names1.append(name2)
    usernames1.append(username2)
    passwords1.append(password2)
    types1.append(type2)
credentials = {"usernames":{}}
for name, uname, pwd, typ, id in zip(names1, usernames1, passwords1, types1, ids1):
    user_dict = {"name":name, "password":pwd, "type":typ}
    credentials["usernames"].update({uname:user_dict})
authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

# tes = st.write('LOGIN IN THE SYSTEM')
# col_01, col_02 = st.columns([0.5, 0.5])
# with col_01:
#     st.text('PRINCE')

# with col_02:
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    page_about()

elif authentication_status == None:
    st.warning("Please enter your username and password")
    page_about()

elif authentication_status:
    query = """SELECT id, type FROM user WHERE username = %s"""
    c.execute(query,(name,))
    connected = c.fetchall()
    for row in connected:
        user_type = row[1]
        user_id = row[0]
    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.markdown(f"You are connected as {name}")

    logo = Image.open(r"images/IES-CONGO1.png")
    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    with c1:
        st.markdown("""<style>background-color: aqua;} 
            </style> """, unsafe_allow_html=True)
        st.image(logo, width=150)
        # st.markdown("""
        #         <div id="avatar"> </div>
        #         <style>
        #             #avatar {
        #             background-image: url(images/IES-CONGO1.png);
        #             background-repeat: no-repeat;
        #             width: 80px;
        #             height: 20px;
        #             padding: 0;
        #             }
        #         </style>
                
        # """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="container">
                <span class="txt t1">
                    CONGO BIG DATA &nbsp;
                </span>
                </div>
                <div class="real">
                <span class="txt1 t2">
                    Your Real Time Data for Relevant Decisions! &nbsp;
                </span>
            </div>
            <style>
                html{
                    --res: calc(0.01 * 10vmin)
                }
                .real{
                    position: asbolute;
                    text-align: center;
                    font-style: italic;
                }
                .txt1{
                    font-size: 1vw;
                    font-familly: 'roboto'
                }
                .t2{
                    color: #457e57;
                }
                .container {
                overflow: hidden;
                display: flex;
                width: 100%;
                position: absolute;
                top: 40%;
                transform: translateY(-80%);
                }
                .txt {
                white-space: nowrap;
                font-size: calc(64 * var(--res));
                animation: scrollTxt 5s linear infinite;
                font-familly:work;
                }
                @keyframes scrollTxt {
                0%{
                    transform: translate(100%, 0);
                }
                100% {
                    transform: translate(-100%, 0);
                }
                }
                .t1 {
                color: #21662f;
                }
            </style>
        """, unsafe_allow_html=True)
    with c3:
        # st.markdown("""<div id="float"><img src="images/IES-CONGO1.png" alt="IES-DML"></div>""", unsafe_allow_html=True)
        st.image(logo, width=150)

    st.markdown("""---""")

    # Test if is the Admin logged in

    if user_type == "Admin":
        with st.sidebar:
            choose = option_menu("MENU", ["About", "Our Partners", "Our Sector", "Subscription", "Settings"],
                                icons=['house', 'camera fill', 'book', 'kanban', 'person lines fill'],
                                menu_icon="app-indicator", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa", "color":"black"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#02ab21", "color": "white"},
            }
            )
     
        if choose == "About":
            page_about()
        elif choose == "Our Partners":
            menu = ["Add partners", "Update partners", "Delete partners", "Active partner", "Disabled partner"]
            choice = st.sidebar.selectbox("Manage Partners", menu)
            if choice =="Add partners":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Add Partner</h1>", unsafe_allow_html=True)
                name = st.text_input("Name of Partner", max_chars=20)
                website=st.text_input("Web Site of Partner")
                active = 0
                c.execute("""SELECT id, username FROM user WHERE type = 'Partner'""")
                pairs_1 = c.fetchall()
                users_1 = st.selectbox('User / Partner', options=[row_1[1] for row_1 in pairs_1])
                for row_1 in pairs_1:
                    if users_1 == row_1[1]:
                        user_1 = row_1[0]
                submit=st.button("Add")
                if submit:
                    add_partner(name, website, active, user_1)
                    st.success('Partner {} saved'.format(name))

            elif choice == "Update partners":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Update partner</h1>", unsafe_allow_html=True)
                result = view_all_partners()
                # st.write(result)
                with st.expander('Current partners'):
                    df = pd.DataFrame(result, columns=['ID', 'Name', 'Web site', 'Active'])
                    st.dataframe(df)
                
                list_of_partner = [i[0] for i in view_unique_partner()]
                selected_partner = st.selectbox('Partner to Edit', list_of_partner)
                selected_partner_result = get_partner(selected_partner)

                if selected_partner_result:
                    id_partner = selected_partner_result[0][0]
                    name_partner = selected_partner_result[0][1]
                    website_partner = selected_partner_result[0][2]
                    state_active_partner = selected_partner_result[0][3]
                    with st.form(key='update_partner'):
                        new_name = st.text_input("Name of Partner", name_partner, max_chars=20, )
                        new_website=st.text_input("Web Site of Partner", website_partner)
                        new_active = st.text_input("Active", state_active_partner)
                        if st.form_submit_button('Update'):
                            update_partner(new_name, new_website, new_active, id_partner)
                            st.success("Partner {} updated".format(new_name))
            
            elif choice == "Delete partners":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Delete partner</h1>", unsafe_allow_html=True)
                result = view_all_partners()
                # st.write(result)
                with st.expander('Current partners'):
                    df = pd.DataFrame(result, columns=['ID', 'Name', 'Web site', 'Active'])
                    st.dataframe(df)
                
                list_of_partner = [i[0] for i in view_unique_partner()]
                selected_partner = st.selectbox('Partner to Edit', list_of_partner)
                selected_partner_result = get_partner(selected_partner)
                id_partner = selected_partner_result[0][0]
                if st.button('Delete'):
                    delete_partner(id_partner)
                    st.success('Partner {} deleted'.format(selected_partner))
                
            elif choice == "Active partner":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Active partner</h1>", unsafe_allow_html=True)
                result = view_all_partners()
                # st.write(result)
                with st.expander('Current partners'):
                    df = pd.DataFrame(result, columns=['ID', 'Name', 'Web site', 'Active'])
                    st.dataframe(df)
                
                list_of_partner = [i[0] for i in view_unique_active_partner()]
                selected_partner = st.selectbox('Partner to Edit', list_of_partner)
                selected_partner_result = get_partner(selected_partner)
                id_partner = selected_partner_result[0][0]
                if st.button('Active'):
                    active_partner(id_partner)
                    st.success('Partner {} activeted'.format(selected_partner))
            
            elif choice == "Disabled partner":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Desible partner</h1>", unsafe_allow_html=True)
                result = view_all_partners()
                # st.write(result)
                with st.expander('Current partners'):
                    df = pd.DataFrame(result, columns=['ID', 'Name', 'Web site', 'Active'])
                    st.dataframe(df)
                
                list_of_partner = [i[0] for i in view_unique_desable_partner()]
                selected_partner = st.selectbox('Partner to Edit', list_of_partner)
                selected_partner_result = get_partner(selected_partner)
                id_partner = selected_partner_result[0][0]
                if st.button('Disable'):
                    disable_partner(id_partner)
                    st.success('Partner {} disabled'.format(selected_partner))

        elif choose == "Subscription":
            menu = ["Add subscription", "Update subscription", "Delete subscription"]
            choice = st.sidebar.selectbox("Manage Subscription", menu)
            if choice == "Add subscription":
                c.execute("""SELECT id, name FROM sector""")
                pairs = c.fetchall()
                sectors = st.selectbox("Sectors", options=[row[1] for row in pairs])
                for row in pairs:
                    if sectors == row[1]:
                        sector = row[0]
                
                c.execute("""SELECT id, name FROM partner""")
                pairs = c.fetchall()
                partners = st.selectbox("Partners", options=[row[1] for row in pairs])
                for row in pairs:
                    if partners == row[1]:
                        partner = row[0]
                start_date = st.date_input("Start date")
                end_date = st.date_input("End date")
                if st.button('Add'):
                    add_subscription(sector, partner, start_date, end_date)
                    st.success('Subscription added successify')
        
        
        elif choose == "Our Sector":
            menu = ["Add sector", "Update sector", "Delete sector"]
            choice = st.sidebar.selectbox("Manage sectors", menu)
            if(choice == "Add sector"):
                    with st.form(key='add_sector'):
                        title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Add Sector</h1>", unsafe_allow_html=True)
                        # id = st.number_input("ID", disabled=True)
                        name = st.text_input("Name of sectors")
                        if st.form_submit_button("Add"):
                            add_sector(name)
                            st.success("Sector {} saved".format(name))
            elif choice == "Update sector":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Update Sector</h1>", unsafe_allow_html=True)
                result = view_all_sectors()
                with st.expander('Current sectors'):
                    df = pd.DataFrame(result, columns=['ID', 'Name'])
                    st.dataframe(df)

                list_of_sector = [i[0] for i in view_unique_sector()]
                selected_sector = st.selectbox('Sector to Edit', list_of_sector)
                selected_sector_result = get_sector(selected_sector)
                # st.write(selected_sector_result)

                if selected_sector_result:
                    id_sector = selected_sector_result[0][0]
                    name_sector = selected_sector_result[0][1]
                    with st.form(key='add_sector'):
                        new_name = st.text_input("Name of sectors", name_sector)
                        if st.form_submit_button("Update"):
                            update_sector(new_name, id_sector)
                            st.success("Sector {} Updated".format(new_name))

            elif choice == "Delete sector":
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Delete Sector</h1>", unsafe_allow_html=True)
                result = view_all_sectors()
                with st.expander('Current sectors'):
                    df = pd.DataFrame(result, columns=['ID', 'Name'])
                    st.dataframe(df)

                list_of_sector = [i[0] for i in view_unique_sector()]
                selected_sector = st.selectbox('Sector to Edit', list_of_sector)
                selected_sector_result = get_sector(selected_sector)
                id_sector = selected_sector_result[0][0]
                if st.button('Delete'):
                    delete_sector(id_sector)
                    st.success('Sector {} deleted'.format(selected_sector))
        
        elif choose == "Settings" : 
            menu = ["Add user", "Update user", "Delete user"]
            choice = st.sidebar.selectbox("Manage sittings", menu)
            if choice == "Add user":
                with st.form(key='form1'):
                    title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Register new user</h1>", unsafe_allow_html=True)
                    username = st.text_input("Name", placeholder="Enter name of user or partner")
                    email = st.text_input("Email", placeholder="Enter a new email")
                    password = st.text_input("Password", placeholder="Enter your password", type="password")
                    repeat_password = st.text_input("Repeat Password", placeholder="Repeat your password", type="password")
                    user_type = st.selectbox("Type of user", ('Admin', 'Partner'))
                    phone = st.text_input("Phone number")

                    hashed_passwords = stauth.Hasher([password]).generate()
                    hashed_password = hashed_passwords[0]

                    c.execute("""SELECT username, email FROM user""")
                    users = c.fetchall()
                    for row in users:
                        user = row[0]
                        mail = row[1]

                    if st.form_submit_button("Register"):
                        if password != repeat_password:
                            st.error("Incorrect password")
                        elif email == mail:
                            st.error('Email {} is already used'.format(email))
                        else:
                            add_user(username, email, hashed_password, user_type, phone)
                            st.success("User {} saved".format(username))

            elif choice == "Update user":
                st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Update user</h1>", unsafe_allow_html=True)
                result = view_all_users()
                with st.expander("Current Users"):
                    df = pd.DataFrame(result, columns=['ID', 'Username', 'Email', 'Password', 'Type of user', 'Phone number'], index=None)
                    st.dataframe(df)
                
                list_of_user = [i[0] for i in view_unique_user()]
                selected_username = st.selectbox('User to Edit', list_of_user)

                selected_user_result = get_user(selected_username)
                # st.write(selected_user_result)
                
                if selected_user_result:
                    id_user = selected_user_result[0][0]
                    username_user = selected_user_result[0][1]
                    email_user = selected_user_result[0][2]
                    password_user = selected_user_result[0][3]
                    type_user = selected_user_result[0][4]
                    phone_user = selected_user_result[0][5]
                    with st.form(key='form1'):
                        new_title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Update user</h1>", unsafe_allow_html=True)
                        new_username = st.text_input("Name", username_user)
                        new_email = st.text_input("Email", email_user)
                        new_password = st.text_input("Password", password_user, type='password')
                        new_repeat_password = st.text_input("Repeat Password", password_user, type="password")
                        new_user_type = st.selectbox(type_user, ('Admin', 'Partner'))
                        new_phone = st.text_input("Phone number", phone_user)
                        
                        new_hashed_passwords = stauth.Hasher([new_password]).generate()
                        new_hashed_password = new_hashed_passwords[0]

                        if st.form_submit_button("Register"):
                            if new_password != new_repeat_password:
                                st.error("Incorrect password")
                            else:
                                update_user(new_username, new_email, new_hashed_password, new_user_type, new_phone, id_user)
                                st.success("User {} updated".format(new_username))
                
            elif choice == "Delete user":
                st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Delete user</h1>", unsafe_allow_html=True)
                result = view_all_users()
                with st.expander("Current Users"):
                    df = pd.DataFrame(result, columns=['ID', 'Username', 'Email', 'Password', 'Type of user', 'Phone number'], index=None)
                    st.dataframe(df)
                
                list_of_user = [i[0] for i in view_unique_user()]
                selected_username = st.selectbox('User to Edit', list_of_user)

                selected_user_result = get_user(selected_username)
                id_user = selected_user_result[0][0]
                if st.button("Delete"):
                    delete_user(id_user)
                    st.success("User {} deleted".format(selected_username))

# PARTNER

    elif typ =="Partner":
        
        # VERIFICATION OF EXPRIRED TIME 

        query_date = """SELECT u.username, p.name, s.startDate, s.endDate , se.name
                            FROM user u, partner p, subscription s, sector se
                            WHERE p.id = s.partnerId AND s.sectorId = se.id AND u.username = %s"""
        c.execute(query_date,(name,))
        pairs = c.fetchall()
        sector_name = []
        for row in pairs:
            user = row[0]
            partner = row[1]
            date_start = row[2]
            date_end = row[3]
            sector_name.append(row[4])
        current_date = datetime.datetime.today()
        fixed_date = date_end - current_date

        # VERIFICATION IF THE PARTNER IS ACTIVE
        query_verificate = """SELECT p.active FROM partner p, user u WHERE p.userId = u.id AND u.username =%s """
        c.execute(query_verificate, (name,))
        actives = c.fetchall()
        for row in actives:
            partner_active = row[0]
        
        if partner_active==0:
            st.markdown("<h1 style='text-align: center; font-familly:work; color: red;'>Welcome! You are not currently activated in our system. Please contact the management for administrative reasons. Cordially. Contact: info@iescongo.com</h1>", unsafe_allow_html=True)
        else:
            # IMPORT KOBO COLLECT DATA
            u="iesmeal"
            pw="IESict4dKobo"
            pd.set_option('display.max_columns',None)
            df3=requests.get(r"https://kc.kobotoolbox.org/api/v1/data/1208139.csv", auth=(u,pw))

            s=str(df3.content,'utf-8')
            data = StringIO(s)
            df3=pd.read_csv(data)

            with st.sidebar:
                choose = option_menu("MENU", ["About Congo big data", "My Sectors", "My Indicators", "Settings"],
                                    icons=['house', 'book', 'kanban', 'gear'],
                                    menu_icon="app-indicator", default_index=0,
                                    styles={
                    "container": {"padding": "5!important", "background-color": "#fafafa", "color":"black"},
                    "icon": {"color": "#234228", "font-size": "25px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                    "nav-link-selected": {"background-color": "#21662f", "color": "white"},
                }
                )
            if choose == "About Congo big data":
                st.markdown(""" <style> .font {
                            font-size:35px ; font-family: 'work'; color: #21662f;} 
                            </style> """, unsafe_allow_html=True)
                page_about()
                
            elif choose == 'My Sectors':
                title = st.markdown("<h1 style='text-align: center; font-familly:work; color: #21662f;'>Sectors which I am subscribed</h1>", unsafe_allow_html=True)
                st.write("Dear {}, IES and DML firms thank you for subscribing to the {} sectors for a period ranging from {} to {}. As a reminder, you have {} left and if you do not renew your subscription, you will be automatically logged out of our system.".format(user, sector_name, date_start, date_end, fixed_date))
                st.write("In addition, we still have a few sectors you can join.")
                st.write('In case of technical problem, please write to webmaster@dmlcongo.com while copying webmaster@iescongo.com and info@iescongo.com')
                st.write('Cordially')
                st.write('Technical team')
            elif choose == 'My Indicators':
                if fixed_date==0:
                    st.markdown("<h1 style='text-align: center; font-familly:work; color: red;'>Please, your subscription is over! Please make sure to resubscribe your formula. Contact: info@iescongo.com</h1>", unsafe_allow_html=True)
                else:
                    # df=pd.read_csv('C:/Users/jkitu/Downloads/iesprincetest/indicesemessai.csv',sep=";",decimal=',')
                    liste_code_province=[52,41,	71,	73,	53,	54,	92,	91,	82,	10,	20,	31,	32,	81,	72,	33,	63,	44,	61,	43,	83,	62,	42,	74,	51,	45]
                    liste_noms_provinces=['Bas-Uele',	'Equateur',	'Haut-Katanga',	'Haut-Lomami',	'Haut-Uele',	'Ituri',	'Kasaï',	'Kasaï-Central',	'Kasaï-Oriental',	'Kinshasa',	'Kongo-Central',	'Kwango',	'Kwilu',	'Lomami',	'Lualaba',	'Maï-Ndombe',	'Maniema',	'Mongala',	'Nord-Kivu',	'Nord-Ubangi',	'Sankuru',	'Sud-Kivu',	'Sud-Ubangi',	'Tanganyika',	'Tshopo',	'Tshuapa']

                    liste_code_territoire=[1000,	2001,	2002,	2003,	2005,	2007,	2009,	2010,	2011,	2013,	2015,	2017,	2019,	3102,	3103,	3105,	3106,	3108,	3201,	3202,	3203,	3204,	3206,	3210,	3212,	3302,	3303,	3304,	3306,	3307,	3308,	3310,	3311,	4101,	4102,	4103,	4104,	4105,	4107,	4108,	4109,	4202,	4203,	4204,	4205,	4206,	4301,	4302,	4304,	4305,	4306,	4402,	4404,	4405,	4502,	4503,	4504,	4505,	4506,	4507,	5101,	5102,	5103,	5105,	5107,	5109,	5110,	5111,	5202,	5204,	5206,	5207,	5208,	5302,	5303,	5305,	5307,	5309,	5311,	5402,	5403,	5405,	5407,	5409,	6101,	6102,	6103,	6104,	6105,	6107,	6109,	6110,	6111,	6201,	6202,	6203,	6205,	6206,	6207,	6208,	6210,	6212,	6301,	6302,	6303,	6305,	6307,	6309,	6311,	6313,	7101,	7102,	7104,	7105,	7106,	7107,	7108,	7109,	7202,	7203,	7205,	7206,	7207,	7302,	7303,	7304,	7305,	7306,	7402,	7404,	7406,	7407,	7409,	7410,	8102,	8103,	8104,	8105,	8106,	8108,	8201,	8202,	8205,	8207,	8208,	8209,	8302,	8303,	8306,	8307,	8308,	8309,	9101,	9102,	9104,	9105,	9106,	9107,	9202,	9204,	9205,	9207,	9208]
                    liste_noms_territoire=['Kinshasa',	'Matadi',	'Boma',	'Moanda',	'Lukula',	'Tshela',	'Seke-Banza',	'Luozi',	'Songololo',	'Mbanza-Ngungu',	'Kasangulu',	'Madimba',	'Kimvula',	'Kenge',	'Feshi',	'Kahemba',	'Kasongo-Lunda',	'Popokabaka',	'Bandundu',	'Bagata',	'Kikwit',	'Bulungu',	'Idiofa',	'Gungu',	'Masi-Manimba',	'Inongo',	'Kiri',	'Oshwe',	'Kutu',	'Kwamouth',	'Bolobo',	'Yumbi',	'Mushie',	'Mbandaka',	'Bikoro',	'Lukolela',	'Bomongo',	'Makanza',	'Basankusu',	'Bolomba',	'Ingende',	'Gemena',	'Budjala',	'Kungu',	'Libenge',	'Zongo',	'Gbadolite',	'Mobayi-Mbongo',	'Yakoma',	'Businga',	'Bosobolo',	'Lisala',	'Bumba',	'Bongandanga',	'Boende',	'Befale',	'Djolu',	'Ikela',	'Bokungu',	'Monkoto',	'Kisangani',	'Ubundu',	'Opala',	'Isangi',	'Yahuma',	'Basoko',	'Banalia',	'Bafwasende',	'Buta',	'Aketi',	'Bondo',	'Ango',	'Poko',	'Rungu',	'Niangara',	'Dungu',	'Faradje',	'Watsa',	'Wamba',	'Irumu',	'Mambasa',	'Djugu',	'Mahagi',	'Aru',	'Goma',	'Nyiragongo',	'Masisi',	'Walikale',	'Lubero',	'Oïcha',	'Beni',	'Butembo',	'Rutshuru',	'Bukavu',	'Kabare',	'Shabunda',	'Kalehe',	'Idjwi',	'Walungu',	'Uvira',	'Fizi',	'Mwenga',	'Kindu',	'Kailo',	'Punia',	'Lubutu',	'Pangi',	'Kabambare',	'Kasongo',	'Kibombo',	'Lubumbashi',	'Kipushi',	'Sakania',	'Kambove',	'Likasi',	'Kasenga',	'Mitwaba',	'Pweto',	'Mutshatsha',	'Lubudi',	'Dilolo',	'Sandoa',	'Kapanga',	'Kamina',	'Kaniama',	'Kabongo',	'Malemba-Nkulu',	'Bukama',	'Kalemie',	'Moba',	'Manono',	'Kabalo',	'Kongolo',	'Nyunzu',	'Kabinda',	'Mwene-Ditu',	'Luilu',	'Kamiji',	'Ngandajika',	'Lubao',	'Mbuji-Mayi',	'Tshilenge',	'Miabi',	'Kabeya-Kamwanga',	'Lupatapata',	'Katanda',	'Lusambo',	'Lodja',	'Kole',	'Lomela',	'Katako Kombe',	'Lubefu',	'Kananga',	'Dibaya',	'Luiza',	'Kazumba',	'Demba',	'Dimbelenge',	'Kamonia',	'Luebo',	'Ilebo',	'Mweka',	'Dekese']

                    df3['Localisation/Territoire'].replace(liste_code_territoire,liste_noms_territoire,inplace=True)
                    # df3['Localisation/Province'].replace([61,62,53,63,10,52,41,71,31,44],['Nord-Kivu','Sud-Kivu','Haut-Uélé','Maniema','Kinshasa','Bas-Uélé','Equateur','Haut-Katanga','Kwango','Mongala'],inplace=True)
                    df3['Localisation/Province'].replace(liste_code_province,liste_noms_provinces,inplace=True)

                    df3.rename(columns={'Localisation/Province':'state_name'}, inplace=True)
                    ## CHOIX DU TYPE D'Enquete et Consentement: Oui enquete Menage ou Cooperative.
                    ## 1. MENAGES
                    # ###################### Base de donnes enquete menage
                    df1=df3[df3['consentement']==1]
                    df1=df1[df3['Type_Enquete']=='menage']
                    df1=df1[df1.columns[2:]]

                    ## 2. COOPERATIVE
                    # # BASE DE DONNEES ENQUETES COOPERATIVES : ELEMENTS RELATIFS AU CHAINE DE VALEUR
                    df2=df3[df3['Type_Enquete']=='cooperative']
                    df2=df2.loc[:,df2.columns.str.startswith('state_name')|df2.columns.str.startswith('Localisation') | df2.columns.str.startswith('gCV') | df2.columns.str.startswith('periode') | df2.columns.str.startswith('semestre')]


                    df2['Nbre Membres']=df2['gCV/nbredehomme']+ df2['gCV/nbredefemme']
                    df2['Nbre Salaries']=df2['gCV/nbres_salaries_hommes']+ df2['gCV/nbres_salaries_femmes']
                    df2['Nbre Commite de gestion']=df2['gCV/nbredehommegest']+ df2['gCV/nbredefemmegest']


                    df2['Pourcentage de femmes membres de cooperatives']= df2['gCV/nbredefemme']/df2['Nbre Membres']*100
                    df2['Pourcentage de femmes salariées  de cooperatives']= df2['gCV/nbres_salaries_femmes']/df2['Nbre Salaries']*100
                    df2['Pourcentage de femmes dans les organes de decision']= df2['gCV/nbredefemmegest']/df2['Nbre Commite de gestion']*100

                    df2.rename(columns={'periode':'year',"Localisation/Territoire": "Territoire"}, inplace=True)
                    year1=[]
                    for row in df2['year']:
                        date = row
                        datem = datetime. datetime. strptime(date, "%Y-%m-%d")
                        year1.append(datem.year)
                    df2['year']=year1


                    # Calcul du chiffre d'affaire moyen de différentes coopératives
                    ## cretation de centres de classes pour les différents intervalles de chiffre d'affaire
                    chiffre_affaire=df2.loc[:,df2.columns.str.startswith('gCV/rCV/chiffre_affaire_')]

                    chiffre_affaire.rename(columns={'gCV/rCV/chiffre_affaire_manioc':' manioc', 'gCV/rCV/chiffre_affaire_mais':'mais', 
                                                    'gCV/rCV/chiffre_affaire_cafe' : 'cafe', 'gCV/rCV/chiffre_affaire_cacao': 'cacao',
                                                    'gCV/rCV/chiffre_affaire_palmier':'palmier', 'gCV/rCV/chiffre_affaire_riz':'riz'},
                                        inplace=True)



                    for variable in chiffre_affaire:
                        df2["Chiffre d\'affaire moyen : {}".format(variable)]= chiffre_affaire[variable].replace([1,2,3,4,5,6],[5000,20000,45000,90000,160000,300000])


                    # attente de la complétude de données pour calculer le chirre d'affaire moyen par filière agricole de chaine des valeurs
                    df2['Chiffre d\'affaire global']=df2.loc[:,df2.columns.str.startswith('Chiffre d\'affaire moyen')].sum(axis=1)
                    df2.rename(columns={'periode':'year','Localisation/Territoire':'Territoire'},inplace=True)
                    #####################################################CONSENTEMENT DONE############################

                    ####################################ENQUETE RELATIVE AU MENAGE###############################################
                    # Indice de score de consommation
                    # df1.loc[:, df1.columns.str.startswith('gCA/gSCA')].columns
                    df1['Score de Consommation Alimentaire']=3*df1['gCA/gSCA/cerealtubercul']+2*df1['gCA/gSCA/oleagineuxetleg']+2*df1['gCA/gSCA/legume']+df1['gCA/gSCA/fruits']+4*df1['gCA/gSCA/proteinesanimal']+0.5*df1['gCA/gSCA/sucreprodsucr']+df1['gCA/gSCA/produitslaitiers']+0.5*df1['gCA/gSCA/huilegraisse']

                    # Indice de Strategie de Survie
                    df1.rename(columns={'gCA/Indice_Strategie_Survie': 'Indice de Strategie de Survie'}, inplace=True)

                    # # Score de faim dans le ménage
                    df1['Indice de Faim dans de menage']=df1[['gCA/gIDF/NombreAAlim','gCA/gIDF/nbrefdormaff','gCA/gIDF/nbrejnsansmang']].sum(axis=1)

                    # Indice de participation de la femme dans le ménage
                    df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')]=df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')].replace([1.0,2.0,3.0,4.0],[1,0,0.5,0])
                    df1['Indice_Participation_femme']=df1.loc[:, df1.columns.str.startswith('Genre/gIPF/')].sum(axis=1)/7

                    ##GENRE 
                    ## INDICE D"AUTONOMISATION DE LA FEMME
                    Auto=df1.loc[:,df1.columns.str.startswith('Genre/gASE/')]
                    # #Auto

                    for column in Auto.columns:
                        Auto.loc[Auto[column]=='oui', column]=1
                        Auto.loc[Auto[column]=='non', column]=0
                        Auto.loc[Auto[column]=='daccc_asser_1', column]=1
                        Auto.loc[Auto[column]=='daccc_asser_2', column]=0
                        Auto.loc[Auto[column]=='beaucoup_de_temps', column]=3
                        Auto.loc[Auto[column]=='dutemps', column]=2
                        Auto.loc[Auto[column]=='trespeudetemps', column]=1
                        Auto.loc[Auto[column]=='pasdetemps', column]=0
                    
                    # #Auto['Genre/gASE/quidecidesirevfem']=Auto['Genre/gASE/quidecidesirevfem'].fillna(0)
                    Auto['Genre/gASE/quidecidesirevfem']=np.where(Auto['Genre/gASE/gain6lastmont']==0,0,Auto['Genre/gASE/quidecidesirevfem'])
                    Auto=Auto.dropna(axis=0)

                    ## LA FONCTION CI-DESSOUS GERE LES ELEMENTS DE LA DATA FRAME NUMERIC MAIS PAS PRISE COMME TEL
                    def Converter_to_numeric(dataframe):
                        for column in dataframe.columns:
                            dataframe[column]=pd.to_numeric(dataframe[column])
                        return dataframe

                    Auto=Converter_to_numeric(Auto)
                    #Auto['Genre/gASE/quidecidesirevfem']=pd.to_numeric(Auto['Genre/gASE/quidecidesirevfem'])
                    Auto[['Genre/gASE/quidecidesirevfem','Genre/gASE/decisiontypetrav','Genre/gASE/qudeciderevhom']]=Auto[['Genre/gASE/quidecidesirevfem','Genre/gASE/decisiontypetrav','Genre/gASE/qudeciderevhom']].replace({1:1,2:0,3:0.5,4:0})
                    Auto['Indice de participation Socioéconomique']=Auto.sum(axis=1)/9


                    df1['Genre/gASE/gain6lastmont'].replace({'oui':1,'non':0}, inplace=True)
                    df1['Genre/gASE/utilisationdesourcefemme'].replace({'oui':1,'non':0}, inplace=True)
                    df1['Genre/gASE/competencedefemme'].replace({'daccc_asser_1':1,'daccc_asser_2':0}, inplace=True)
                    df1['Genre/gASE/disponibinitefemme'].replace(['beaucoup_de_temps','dutemps','trespeudetemps','pasdetemps'],[3,2,1,0], inplace=True)
                    df1['Indice d\'autonominsationn de la femme']=df1.loc[:,df1.columns.str.startswith('Genre/gASE/')].sum(axis=1)/9 


                    ### ENVIRONNEMENT ET WASH
                    ####CHARBON & BRAISE
                    # df1.loc[:, df1.columns.str.startswith('gEEHA/quantitecharbon/gQcharbon/')]
                    df1['unite_charbon']=df1['gEEHA/quantitecharbon/gQcharbon/unite_braise'].replace(['sac','sachet','bassin','seau'],[1,1/50,1/15,1/18])

                    df1['unite_biochar']=df1['gEEHA/quantitecharbon/gQcharbon/unite_biochar'].replace(['sac','sachet','bassin','seau'],[1,1/50,1/15,1/18])
                    # df1.loc[:, df1.columns.str.startswith('gEEHA/quantitecharbon/gQcharbon/')]
                    df1['Quantite de Charbon']=df1['unite_charbon']*df1['gEEHA/quantitecharbon/gQcharbon/Quantite_braise_consommee']*60
                    df1['Quantite de Charbon'].fillna(0,inplace=True)
                    df1['Quantite de Biochar']=df1['unite_biochar']*df1['gEEHA/quantitecharbon/gQcharbon/Quantite_biochar']*40
                    df1['Quantite de Biochar'].fillna(0,inplace=True)


                    ## LAVAGE DE MAIN 
                    df1.loc[:, df1.columns.str.startswith('gEEHA/lavagedemains')]=df1.loc[:, df1.columns.str.startswith('gEEHA/lavagedemains')].replace([True,False],[1,0])
                    df1['Lavage de mains au moins à trois moments'] = df1.loc[:, df1.columns.str.startswith('gEEHA/lavagedemains')].sum(axis=1)
                    df1['Indice de Lavage de mains au moins à trois moments'] =np.where(df1['Lavage de mains au moins à trois moments'] >=3,'Oui','Non')
                    df1['Exposition_Choc/Recuperartion']=df1['Exposition_Choc/Recuperartion'].replace(['a','b','c','d'],[1,2,3,4])
                    df1['Exposition_Choc/urgence']=df1['Exposition_Choc/urgence'].replace(['a','b','c','d','e','f'],[3,2,1,0,0,0])
                    # df1.loc[:, df1.columns.str.startswith(('Exposition_Choc/Recuperartion','Exposition_Choc/urgence'))].fillna(0)
                    df1['Indice de résilience']=df1.loc[:, df1.columns.str.startswith(('Exposition_Choc/Recuperartion','Exposition_Choc/urgence'))].sum(axis=1)
                    df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')]=df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')].fillna(0)
                    df1["Indice d'exposition aux chocs"]=df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')].sum(axis=1)/32
                    GroupeIPM=df1.loc[:,df1.columns.str.startswith('IPM')]

                    ## INDICE DE PAUVRETE MULTIDIMENSIONNELLE(IPM)
                    df1['IPM/IPM_1']=pd.to_numeric(df1['IPM/IPM_1'])/12
                    df1['IPM/IPM_2']=pd.to_numeric(df1['IPM/IPM_2'])/12
                    df1['IPM/IPM_3']=pd.to_numeric(df1['IPM/IPM_3'])/12
                    df1['IPM/IPM_31']=pd.to_numeric(df1['IPM/IPM_31'])
                    df1['IPM/IPM_31']=df1['IPM/IPM_31']/pd.to_numeric(df1['renseignement_generaux/Taille_menage'])*100
                    df1['IPM/IPM_31']=np.where(df1['IPM/IPM_31']>=50,1/12,0)
                    IPM32=[]
                    IPM41=[]
                    for row in df1['IPM/IPM_32']:
                        if row in ['b','c','d']:
                            IPM32.append(1/12)
                        else:
                            IPM32.append(0)
                    df1['IPM/IPM_32']=IPM32
                    # print(GroupeIPM['IPM32'])
                    df1['IPM/IPM_4']=pd.to_numeric(df1['IPM/IPM_4'])/9
                    for row in df1['IPM/IPM_41']:
                        if row in ['a','b','d']:
                            IPM41.append(1/9)
                        else:
                            IPM41.append(0)
                    # GroupeIPM['IPM41']=IPM41
                    df1['IPM/IPM_41']=IPM41
                    df1['IPM/Nature_energie_eclairage']=np.where(df1['IPM/Nature_energie_eclairage']=='a', 1/24,0)
                    df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_base')]=df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_base')].replace([True,False],[1,0])
                    df1["Assets_base"]=df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_base')].sum(axis=1)
                    df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_distinction')]=df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_distinction')].replace([True,False],[1,0])
                    df1["Assets_distinction"]=df1.loc[:,df1.columns.str.startswith('IPM/Actifs_Bien_de_distinction')].sum(axis=1)
                    #GroupeIPM[(GroupeIPM['Assets_base']>=2) & (GroupeIPM['Assets_distinction']>=1),'Assets' ]=0#
                    df1['Assets']=np.where((df1['Assets_base']>=2) & (df1['Assets_distinction']>=1),1/24,0)

                    df1['IPM/Nature_energie_eclairage']=np.where(df1['IPM/Nature_energie_eclairage']=='a',1/24,0)
                    df1['IPM/IPM_6']=np.where(df1['IPM/IPM_6']=='1',1/24,0)
                    df1['IPM/Plancher']=np.where(df1['IPM/Plancher']=='a',1/24,0)

                    df1['IPM/mur']=np.where(df1['IPM/mur']=='a',1/24,0)
                    df1['IPM/mur']=np.where(df1['IPM/mur']=='a',1/24,0)
                    df1['Energie_cuisson']=df1['gEEHA/sourcedenergie']
                    df1['Energie_cuisson']=df1['Energie_cuisson'].replace({'braise':1/24,'bois':1/24,'biochar':0,'electricite':0})

                    df1.loc[:,df1.columns.str.endswith('_litres_utilises')]=Converter_to_numeric(df1.loc[:,df1.columns.str.endswith('_litres_utilises')])
                    df1['Quantite_eau_par_personne']=df1.loc[:,df1.columns.str.endswith('_litres_utilises')].sum(axis=1)
                    df1['Taille_menage']=df1['renseignement_generaux/Taille_menage']
                    df1['Quantite_eau_par_personne']=df1['Quantite_eau_par_personne']/df1['Taille_menage']
                    df1['Acces_eau_qte_suffisante']=np.where(df1['Quantite_eau_par_personne']<20,1/24,0)
                    df1['Indice de Pauvrete Multidimentionnelle']=df1.loc[:,df1.columns.str.contains('IPM_')].sum(axis=1) +df1[['Acces_eau_qte_suffisante','IPM/Plancher','IPM/mur','Energie_cuisson','Assets']].sum(axis=1)



                    ##################################COHESION SOCIAL SOCIALE

                    df1['CS/Securite_humaine/Niveau_accord_que_Excombatants_insecurise'].replace(['a','b','c','d','e'],[5,4,3,2,1], inplace=True)
                    df1['CS/Satisfaction_Vie_Civique/Accees_systeme_judiciaire'].replace([99],[np.NaN], inplace=True)
                    df1['CS/Satisfaction_Vie_Civique/Accees_systeme_judiciaire'].replace([99],[np.NaN], inplace=True)

                    df1['CS/Satisfaction_Vie_Civique/Niveau_Accord_Equite_Justice'].replace(['a','b','c','d','e',],[5,4,3,2,1], inplace=True) 
                    df1['CS/Satisfaction_Vie_Civique/Niveau_de_confiance_dans_la_justice'].replace(['a','b','c','d','e','f','g'],[6,5,4,3,2,1,np.NaN], inplace=True) # revision de la codification

                    ####SCORE D'IDENTiFiCATION
                    df1['CS/Dim1/Relation_interpersonnelles/membre_de_votre_groupe_ethniuqe'].replace(99,np.NaN, inplace=True)
                    df1['CS/Dim1/Relation_interpersonnelles/membre_des_autres_groupes_ethniques'].replace(99,np.NaN, inplace=True)
                    df1['CS/Dim1/Perception_interperonnelles/niveau_violence'].replace([4,3,2,1],[1,2,3,4], inplace=True)
                    # df1['CS/Dim1/Perception_interperonnelles/niveau_violence'].replace(99,np.NaN, inplace=True)
                    df1['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se'].replace(99,np.NaN, inplace=True)
                    df1['CS/Dim1/frequentation_interpersonnelle/Se_rendre_a_la_meme_eglise_ou_autre_lieu_de_culte'].replace(99,np.NaN, inplace=True)
                    df1['Score Identification']=df1.loc[:,df1.columns.str.contains('Dim1')].select_dtypes('float64').sum(axis=1)
                    # name of the rescaled value = "real value + space ""
                    df1['Score Identification ']=df1['Score Identification']/32

                    df1['Score Confiance Mutuelle']=df1.loc[:,df1.columns.str.contains('CS/Confiance_mutuelle/')].sum(axis=1)
                    # rescaled value
                    df1['Score Confiance Mutuelle ']=df1['Score Confiance Mutuelle']/11


                    df1['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se'].replace([99],[np.NaN], inplace=True)
                    df1['CS/Dim1/frequentation_interpersonnelle/Se_rendre_a_la_meme_eglise_ou_autre_lieu_de_culte'].replace([99.0],[0], inplace=True)
                    df1['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se']=pd.to_numeric(df1['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se'])

                    df1['Score Correcte Representation']=df1.loc[:,df1.columns.str.startswith('CS/Sentiment_Correcte_Representation/')].sum(axis=1)
                    # rescaled value
                    df1['Score Correcte Representation ']=df1['Score Correcte Representation']/12
                    df1['Score Correcte Representation']=df1.loc[:,df1.columns.str.startswith('CS/Sentiment_Correcte_Representation/')].sum(axis=1)
                    # rescaled value
                    df1['Score Correcte Representation ']=df1['Score Correcte Representation']/12

                    df1['Score Absence Corruption']=df1.loc[:,df1.columns.str.startswith('CS/Absence_de_corruption')].sum(axis=1)
                    # rescaled value
                    df1['Score Absence Corruption ']=df1['Score Absence Corruption']/12

                    df1['Score Confiance Institution']=df1.loc[:,df1.columns.str.startswith('CS/Confiance_institutions')].select_dtypes('float64').sum(axis=1)
                    # rescaled value
                    df1['Score Confiance Institution ']=df1['Score Confiance Institution']/12

                    df1['Score Participation_Citoyenne']=df1.loc[:,df1.columns.str.startswith('CS/Participation_Citoyenne')].select_dtypes('float64').sum(axis=1)
                    # rescaled value
                    df1['Score Participation_Citoyenne ']=df1['Score Participation_Citoyenne']/6

                    df1['CS/Securite_humaine/Perspective_securite_future'].replace([1,2,3,99],[3,1,2,np.NaN], inplace=True)
                    df1['CS/Securite_humaine/crainte_attaque'].replace([1,2,3,4,99],[4,3,2,1,np.NaN])
                    df1['Score Securite humaine']=df1[['CS/Securite_humaine/Jour','CS/Securite_humaine/Aller_Quartier_a_un_autre',
                        'CS/Securite_humaine/crainte_attaque','CS/Securite_humaine/Niveau_secu_rencontre_autre_groupe_ethnique',
                        'CS/Securite_humaine/Perspective_securite_future'
                        ]].sum(axis=1)
                    # rescaled value
                    df1['Score Securite humaine ']=df1['Score Securite humaine']/21
                    df1['CS/Satisfaction_Vie_Civique/Acces_physique_tribunaux'].replace(99,np.NaN, inplace=True)


                    df1['Score satisfaction vie civique']=df1.loc[:,df1.columns.str.startswith('CS/Satisfaction_Vie_Civique/')].select_dtypes(['float64','int64']).sum(axis=1)
                    # rescaled value
                    df1['Score satisfaction vie civique ']=df1['Score satisfaction vie civique']/29


                    df1['Score satisfaction vie personnelle']=df1.loc[:,df1.columns.str.startswith('CS/satisfaction_vie_personnelle')].select_dtypes('float').sum(axis=1)
                    # rescaled value
                    df1['Score satisfaction vie personnelle ']=df1['Score satisfaction vie personnelle']/21

                    df1['Index de Cohesion Sociale']=df1[['Score satisfaction vie personnelle','Score satisfaction vie civique','Score Securite humaine',
                                                        'Score Participation_Citoyenne','Score Confiance Institution','Score Absence Corruption',
                                                        'Score Correcte Representation','Score Identification','Score Confiance Mutuelle'
                                                        ]].sum(axis=1)
                    # rescaled value
                    df1['Index de Cohesion Sociale ']=df1['Index de Cohesion Sociale']/156




                    # ASSEMBLAGE DES INDICATEUR  base de données UNIQUES POUR LES MENAGES
                    Indicateurs_Data=df1.loc[:,  df1.columns.str.startswith('periode')|df1.columns.str.startswith('semestre')|df1.columns.str.startswith('renseignement_generaux/') | df1.columns.str.startswith('Score') | df1.columns.str.startswith('Score') | df1.columns.str.startswith('Indice') | df1.columns.str.startswith('Index') | df1.columns.str.startswith('Quantit') | df1.columns.str.startswith('Localisation') | df1.columns.str.startswith('state')]
                    # Indicateurs_Data
                    Newnames= {'periode':'year','Localisation/Territoire':'Territoire',
                    'Localisation/ZS':'Zone de Santé', 'Localisation/AS':'Aire de Santé','Quantite_eau_par_personne':"Quantité d'eau par personne",'renseignement_generaux/Duree_residence': 'Residence',"Indice_Participation_femme":"Indice de Participation de la femme",
                    'renseignement_generaux/Qualite_repondant':'Qualite du repondant','Index_CS':'Index CS',
                    'renseignement_generaux/Sexe':'Sexe', 'renseignement_generaux/Tranche_age': "Tranche d\' age",
                    'renseignement_generaux/Etat_Civil':'Etat Civil', 'renseignement_generaux/Niveau_etude':'Niveau Etude',
                    'renseignement_generaux/Activite_Principale':'Profession',
                    'renseignement_generaux/Filiere_Chaine_de_valeur':'Chaine de Valeur Principale',
                    'renseignement_generaux/Filiere_Chaine_de_valeur_autre':'Chaine de valeur autre',
                    'renseignement_generaux/Taille_menage': 'Taille du menage'
                            }

                    Indicateurs_Data.rename(columns=Newnames, inplace=True)
                    year=[]
                    for row in Indicateurs_Data['year']:
                        date = row
                        datem = datetime. datetime. strptime(date, "%Y-%m-%d")
                        year.append(datem.year)
                    Indicateurs_Data['year']=year
                    Indicateurs_Data["Territoire"]=Indicateurs_Data["Territoire"].values.astype(str)
                    # Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=np.where(Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=='non',0,1)
                    Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"].replace(['Oui','Non'],[1,0])
                    Indicateurs_Data["Sexe"]=Indicateurs_Data["Sexe"].replace(['F','M'],['Femme','Homme'])
                    df20=Indicateurs_Data

                    def Compute_mean(df_col):
                        return df_col.mean()
                    #############################
                    ###################Creating the dataset for Household study
                    # ############################################??????????????????<>
                    df08=df20.drop(['Zone de Santé', 'Aire de Santé', 'Residence', 'Qualite du repondant','Chaine de Valeur Principale','Chaine de valeur autre'],axis=1)
                    df_transf=df08


                    df_transf[['year', 'state_name', 'Etat Civil','Tranche d\' age']] = df_transf[['year', 'state_name', 'Etat Civil','Tranche d\' age']]. astype(str)


                    menage=df_transf.groupby(['semestre','Territoire','year','state_name'])['Taille du menage'].sum()
                    # menage.values

                    # Get FInal data to Be used
                    df_transf1=df_transf.groupby(['semestre','Territoire','year','state_name']).mean(1)
                    df_transf1.reset_index(inplace=True)
                    new_order=[2,0,3,1]
                    new_order.extend(range(4,len(df_transf1.columns.tolist())))
                    df_transf1=df_transf1[df_transf1.columns[new_order]]
                    df_transf1['Taille du menage']=menage.values

                    df=df_transf1.round(decimals = 2)
                    df['year']=df['year'].astype(int)
                    df.head()
                    dfg=deepcopy(df)
                    # convert the data frame to csv
                    @st.experimental_memo
                    def convert_df(df):
                        return df.to_csv(index=False).encode('utf-8')

                    ##### ELEMENT DE REGRESSION POUR TOUT 
                    ##########################
                    def estimate_coef(x, y):
                            # number of observations/points
                            #     x=x.to_numpy()
                            #     y=y.to_numpy()
                            n = np.size(x)
                            
                            # mean of x and y vector
                            m_x = np.mean(x)
                            m_y = np.mean(y)
                        
                            # calculating cross-deviation and deviation about x
                            SS_xy = np.sum(y*x) - n*m_y*m_x
                            SS_xx = np.sum(x*x) - n*m_x*m_x
                        
                            # calculating regression coefficients
                            b_1 = SS_xy / SS_xx
                            b_0 = m_y - b_1*m_x
                        
                            return (b_0, b_1)

                    #########################################################
                    ################Organisateurs############################
                    #####Utiliser les éléments de login #####################
                    #########################################################
                    # Organisateur=['IES-CONGO', 'IES-PARTENER STAB']
                    # org=st.sidebar.radio("Selectionne l'organisateur",Organisateur)
                    #Manual USER
                    # org=st.text_input('User: ')
                    # password=st.text_input('password: ')
                    ##################################################################
                    ########## DANS LE CAS OU L'Organisation est IES-CONGO############
                    ##################################################################

                    # if org=='IES-CONGO':
                    new_title = '<p style="font-family:sans-serif; color:#21662f; font-size: 42px;">IES Indicators 2022</p>'
                    st.markdown(new_title, unsafe_allow_html=True)

                    ## SELECTION OF DOMAIN
                    # Domain_option =['cohesion social', 'WASH', 'ECONOMIE', "SECAL"]

                    #### SELECT PATNERS
                    
                    query_1 = """SELECT u.id, p.name
                                FROM user u, partner p
                                WHERE u.id = p.userId AND u.username = %s"""
                    c.execute(query_1, (name,))
                    partners_1 = c.fetchall()
                    for row in partners_1:
                        partner_name_1 = row[1]

                    # Partner_Option = ['USAID','PNUD','MISERERE']
                    # partner_name =st.sidebar.radio("Selectionne l'organisation",Partner_Option)
                    partner_name = partner_name_1
                    ### PARTNER RESTRICTIONS
                    ## To modify the restriction one should change the options which is in  the list of options
                    
                    query_2 = """SELECT se.name
                                    FROM user u, partner p, subscription s, sector se
                                    WHERE u.id = p.userId AND p.id = s.partnerId AND s.sectorId = se.id AND u.username = %s"""
                    c.execute(query_2, (name,))
                    partner_2 = c.fetchall()
                    for row in partner_2:
                        domain_name_1 = row[0]

                        # row[0] for row in partner_2

                    col_1, col_2, col_3, col_4 = st.columns([0.4, 0.2, 0.2, 0.2])
                    with col_1:
                        if partner_name:
                            domain_name=st.selectbox('Select domain',options=[row[0] for row in partner_2])
                            if domain_name =="STABILISATION ET COHÉSION SOCIALE":
                                y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[[38]])
                            elif domain_name =='RÉSILIENCE ET ECONOMIE':
                                y_val1=st.selectbox("Selectionne l'indicateur",options=[df.columns[15],df.columns[16],df.columns[18]])
                            
                            elif domain_name =='SÉCURITÉ ALIMENTAIRE ET NUTRITION':
                                y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[7:10])

                            elif domain_name =='ENVIRONNEMENT ET WASH':
                                y_val1=st.selectbox("Selectionne l'indicateur",options=[df.columns[12],df.columns[13],df.columns[14],df.columns[17]])
                                
                            elif domain_name =="GENRE":
                                y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[10:12])

                            elif domain_name =="CHAINE DE VALEUR":
                                y_val1=st.selectbox("Selectionne l'indicateur",options=df2.columns[29:])
                    # ## Select State: One should set the obtion and the the selection type, like (radio,checkbox,selectbox,...)
                    state_option = df['state_name'].unique().tolist()
                    # state_name = st.selectbox("Choisir la province", state_option)
                    with col_2:
                        state_name=st.selectbox('Select the province:', state_option)

                    with col_3:
                        ####  This alows the selection of years 
                        year_option = df['year'].unique().tolist()
                        year = st.selectbox("Année", year_option)
                        df = df[df['year']==year]
                    with col_4:
                        sem_option = df['semestre'].unique().tolist()
                        semester = st.selectbox("Semestre", sem_option)
                        df = df[df['semestre']==semester]
                

                #############################################################
                ##*********************MAP DISPLAYER************************
                ##############################################################
                    def display_map(df, year,semester, province):
                        if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] :
                            df = df[(df['year'] == year)&(df['semestre'] == semester) & (df['state_name'] == province)]
                        

                            map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                            
                            choropleth = folium.Choropleth(
                                    geo_data='./geojson/rdcongo.geojson',
                                    data=df,
                                    columns=['state_name', y_val1],
                                    key_on='feature.properties.name',
                                    line_opacity=0.8,
                                    fill_color='YlOrRd',
                                    highlight=True,
                                    legend_name=y_val1,
                                    # color=y_val1
                                )
                            choropleth.geojson.add_to(map)
                            df_indexed = df.set_index('state_name')
                            
                            for feature in choropleth.geojson.data['features']:
                                    state_name = feature['properties']['name']
                                    feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),1)) if state_name in list(df_indexed.index)else ''
                            
                            
                            choropleth.geojson.add_child(
                                    folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                                )
                        
                        
                            st_map = st_folium(map, width=700, height=450)

                            
                            state_name = ''
                            if st_map['last_active_drawing']:
                                state_name = st_map['last_active_drawing']['properties']['name']
                            return state_name
                        elif domain_name=="CHAINE DE VALEUR": 
                            df = df[(df['year'] == year) & (df['state_name'] == province)]
                            map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                            
                            choropleth = folium.Choropleth(
                                    geo_data='./geojson/rdcongo.geojson',
                                    data=df,
                                    columns=['state_name', y_val1],
                                    key_on='feature.properties.name',
                                    fill_color='YlOrRd',
                                    line_opacity=0.8,
                                    highlight=True,
                                    legend_name=y_val1
                                )
                            choropleth.geojson.add_to(map)
                            df_indexed = df.set_index('state_name')
                            
                            for feature in choropleth.geojson.data['features']:
                                    state_name = feature['properties']['name']
                                    feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),1)) if state_name in list(df_indexed.index)else ''
                                    
                            choropleth.geojson.add_child(
                                    folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                                )
                        
                        
                            st_map = st_folium(map, width=700, height=450)

                            
                            state_name = ''
                            if st_map['last_active_drawing']:
                                state_name = st_map['last_active_drawing']['properties']['name']
                            return state_name     

                    ### PLOTING FUNCTIONS 
                    def interactiveplot(dataframe):
                        x_val=st.selectbox("Selectionne l'indicateur X",options=df.columns[4:])
                        y_val=st.selectbox("Selectionne l'indicateur Y",options=df.columns[4:])
                        plot=px.scatter(dataframe, x=x_val, y=y_val,size='Population', color="Territoire",hover_name="Territoire",log_x=True)
                        st.plotly_chart(plot)

                    # USED FUCTION FOR THE PLOT ON IES STREAMLIT
                    def interactivehist(dataframe):
                        x_val1=dataframe.columns[3]
                        
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du {} indicateur {} ".format(state_name, df[y_val1].name))
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)


                    def interactivepie(dataframe):
                        # colors = ['gold', 'mediumturquoise']
                        # colors=['blue','darkblue']
                        # colors=['lightcyan','cyan']
                        colors=["red", "blue"]
                        fig2 = px.pie(dataframe, values=dataframe['Sexe'].value_counts(), names=dataframe['Sexe'].unique(),color_discrete_map={'F':'darkblue','M':'cyan'},hole=.3,title=("Participants"))
                        fig2.update_traces(hoverinfo='label+percent',  textfont_size=20,
                                marker=dict(colors=dataframe['Sexe'].value_counts(), line=dict(color='#000000', width=2)))
                        st.plotly_chart(fig2)

                    def interactiveprovinceval(dataframe):
                        d1=dataframe.loc[state_name][y_val1]
                        fig1= px.scatter(d1)

                        st.plotly_chart(fig1)


                    def main(df):    
                        return interactivehist(df)
                    
                    def Evolutionplot(dataframe):
                        if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] :
                            a2=dataframe.loc[dataframe['state_name']==state_name]
                            a1=a2.groupby(['year','semestre'])[y_val1].mean()
                            prov1=pd.DataFrame(a1)
                            prov1.reset_index(inplace=True)
                            
                            Repub=dataframe.groupby(['year','semestre'])[y_val1].mean()
                            Repub=pd.DataFrame(Repub)
                            Repub.reset_index(inplace=True)


                            ###################
                            X=pd.Series(list(Repub.index))
                            Y=Repub[y_val1]
                            B11=estimate_coef(X,Y)
                            X1=pd.Series(range(len(Repub.index),len(Repub.index)+6))
                            Y1=B11[0]+B11[1]*X1
                            
                            
                            Xp=pd.Series(list(prov1.index))
                            Yp=prov1[y_val1]
                            B21=estimate_coef(Xp,Yp)
                            Xp1=pd.Series(range(len(prov1.index),len(prov1.index)+6))
                            Yp1=B21[0]+B21[1]*Xp1
                        
                            fig1=go.Figure()
                            fig1.add_trace(go.Scatter(
                                x=[Repub['year'].append(pd.Series(np.repeat([max(Repub['year'])+1,max(Repub['year'])+2],[2,2]))), 
                                Repub['semestre'].append(pd.Series(['S1p','S2p','S1p','S2p']))], 
                                y=Repub[y_val1].append(Y1),
                                name='DRC',
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15},
                                text=Repub['semestre']
                                ))
                            fig1.add_trace(go.Scatter(
                            x=[pd.Series(np.repeat([max(Repub['year'])+1,max(Repub['year'])+2],[2,2])), pd.Series(['S1p','S2p','S1p','S2p'])], 
                            y=Y1,
                            name='DRC',
                            fill='tozeroy',
                            mode='lines+markers',
                            marker={'size':15,'color':'darkcyan'},
                            showlegend=False
                            ))
                            
                            fig1.add_trace(go.Scatter(
                                x=[prov1['year'].append(pd.Series(np.repeat([max(prov1['year'])+1,max(prov1['year'])+2],[2,2]))),
                                prov1['semestre'].append(pd.Series(['S1p','S2p','S1p','S2p']))],
                                y=prov1[y_val1].append(Yp1),
                                name=state_name,
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15,'color':'fuchsia'}
                                ))

                            fig1.add_trace(go.Scatter(
                                x=[pd.Series(np.repeat([max(prov1['year'])+1,max(prov1['year'])+2],[2,2])),pd.Series(['S1p','S2p','S1p','S2p'])],
                                y=Yp1,
                                name=state_name,
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15,'color':'darkcyan'},
                                text=prov1['semestre'],
                                showlegend=False
                                ))

                            fig1.update_layout(legend_title_text='Region', title_text="Tendance de {} au {} et en RDC".format(Repub[y_val1].name,state_name),xaxis_title="Années", yaxis_title="{}".format(Repub[y_val1].name))
                                
                            st.plotly_chart(fig1)


                        if domain_name == 'CHAINE DE VALEUR':
                            # dataframe.set_index("state_name", inplace=True)
                            # state_list=list(dataframe.index)
                            dataframe.replace(['Semestre1','Semestre2'],['S1','S2'],inplace=True)
                            a2=dataframe.loc[dataframe['state_name']==state_name]
                            a1=a2.groupby(['year'])[y_val1].mean()
                            prov1=pd.DataFrame(a1)
                            prov1.reset_index(inplace=True)
                            
                            Repub=pd.DataFrame(dataframe.groupby(['year'])[y_val1].mean())
                            Repub.reset_index(inplace=True)

                            B1=estimate_coef(prov1['year'], prov1[y_val1])
                            B2=estimate_coef(Repub['year'], Repub[y_val1])
                            fig = go.Figure()
                            fig.add_trace(go.Scatter( 
                                x=Repub['year'],
                                y=Repub[y_val1],
                                fill='tozeroy',
                                name="RDC",
                                mode='lines+markers',
                                marker={'size':10}
                            ))
                        

                            fig.add_trace(go.Scatter( 
                                x=Repub['year'].append(pd.Series([max(Repub['year'])+1,max(Repub['year'])+2,max(Repub['year'])+3])), 
                                y=Repub[y_val1].append(pd.Series([B2[0] + B2[1]*(max(Repub['year'])+1),B2[0] + B2[1]*(max(Repub['year'])+2),B2[0] + B2[1]*(max(Repub['year'])+3)])),
                                fill='tozeroy',
                                name="RDC",
                                mode='lines+markers',
                                marker={'size':10},
                                showlegend=False
                            ))
                            
                            fig.add_trace(go.Scatter(
                                
                                x=prov1['year'].append(pd.Series([max(prov1['year'])+1,max(prov1['year'])+2,max(prov1['year'])+3])), 
                                y=prov1[y_val1].append(pd.Series([B1[0] + B1[1]*(max(prov1['year'])+1),B1[0] + B1[1]*(max(prov1['year'])+2),B1[0] + B1[1]*(max(prov1['year'])+3)])),
                                name=state_name,
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15}
                            ))
                            
                            fig.add_trace(go.Scatter(
                                
                                x=[max(Repub['year'])+1,max(Repub['year'])+2,max(Repub['year'])+3], 
                                y=[B2[0] + B2[1]*(max(Repub['year'])+1),B2[0] + B2[1]*(max(Repub['year'])+2),B2[0] + B2[1]*(max(Repub['year'])+3)],
                                name='RDC Prediction',
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15},
                                showlegend=False
                            ))

                            fig.add_trace(go.Scatter(
                                
                                x=[max(prov1['year'])+1,max(prov1['year'])+2,max(prov1['year'])+3], 
                                y=[B1[0] + B1[1]*(max(prov1['year'])+1),B1[0] + B1[1]*(max(prov1['year'])+2),B1[0] + B1[1]*(max(prov1['year'])+3)],
                                name=state_name+' Prediction',
                                fill='tozeroy',
                                mode='lines+markers',
                                marker={'size':15},
                                showlegend=False
                            ))
                            fig.update_layout(legend_title_text="Tendance {}".format(Repub[y_val1].name), title_text="Tendance de {} au {} et en RDC".format(Repub[y_val1].name,state_name),xaxis_title="Années", yaxis_title="{}".format(Repub[y_val1].name))
                            
                            st.plotly_chart(fig)
                    col1, col2 = st.columns([0.5, 0.5])
                    with col1:
                        if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]:
                            df_indexed = df.set_index('state_name')
                            MapDRC = display_map(df, year,semester, list(df_indexed.index))
                        if domain_name=="CHAINE DE VALEUR":
                            df_indexed1 = df2.set_index('state_name')
                            MapDRC = display_map(df2, year,semester, list(df_indexed1.index))

                        # ## Select State: One should set the obtion and the the selection type, like (radio,checkbox,selectbox,...)
                        if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]:
                            state_option = df['state_name'].unique().tolist()
                            # state_name=st.sidebar.selectbox('Select the province:', state_option)
                            df = df[df['state_name']==state_name]
                        
                        elif domain_name=="CHAINE DE VALEUR":
                            state_option = df2['state_name'].unique().tolist()
                            # state_name=st.sidebar.selectbox('Select the province:', state_option)
                            df2 = df2[df2['state_name']==state_name]
                
                    with col2:
                        if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] :
                            main(df)
                        
                        else:
                            df2 = df2[df2['state_name']==state_name]
                            fig=px.bar(df2,df2.columns[3],y_val1,color=y_val1,hover_name="semestre")
                            fig.data[-1].text = round(df2[y_val1],2)
                            fig.update_traces(textposition='inside')
                            st.plotly_chart(fig)
                        
                        # #### This part allows the  visualisation of the indicators evolution in the State and the Whole country
                        ### In fact The trend of means of indicators is the one plotted.
                    
                    if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] :
                        col11, col22 = st.columns([0.5, 0.5])
                        with col11:
                            Evolutionplot(dfg)
                        with col22:
                            df20 = df20[df20['state_name']==state_name]
                            interactivepie(df20)
                    
                    
                    elif domain_name=="CHAINE DE VALEUR":
                        col111, col222 = st.columns([0.5, 0.5])
                        with col111:
                            Evolutionplot(df2)
                        with col222:
                            df2 = df2[df2['state_name']==state_name]
                            colors=["red", "blue"]
                            fig2 = px.pie(df2, values=df2['Nbre Membres'].value_counts(), names=df2['Nbre Membres'].unique(),color_discrete_map={'F':'darkblue','M':'cyan'},hole=.3, title="Participant")
                            fig2.update_traces(hoverinfo='label+percent',  textfont_size=20,
                                    marker=dict(colors=df2['Nbre Membres'].value_counts(), line=dict(color='#000000', width=2)))
                        
                            st.plotly_chart(fig2)
                        
                # with st.form(key='forgot'):
                #     current_password = st.text_input("Current password", type='password')
                #     new_password = st.text_input("New password", type='password')
                #     repeat_password = st.text_input("Repeat password", type='password')
                #     hashed_1 = stauth.Hasher([current_password]).generate()
                #     hashed_password_1 = hashed_1[0]
                #     if st.form_submit_button('Reset'):
                #         if hashed_password_1 != pwd:
                #             st.error('The current password is incorrect')
                #         else:
                #             st.success('Password modified successfully')


    # ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#                 <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;}
#                 header {visibility: hidden;}
#                 </style>
#                 """
# st.markdown(hide_st_style, unsafe_allow_html=True)
