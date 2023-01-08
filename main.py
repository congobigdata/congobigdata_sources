import pandas as pd
import mysql.connector as connection
import streamlit as st
import streamlit_authenticator as stauth
import toml
from streamlit_option_menu import option_menu
from PIL import Image
import json
from pickle import NONE, TRUE
from copy import deepcopy
from datetime import date
from select import select
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
# pip install streamlit-card
from streamlit_card import card
# pip install streamlit-aggrid
from st_aggrid import GridOptionsBuilder, AgGrid
# pip install imgkit
import imgkit
# pip install plot_likert
import plot_likert



# IMPORT FUNCTIONS

from functions import update_status, page_home, view_unique_desable_partner, view_unique_active_partner, view_all_partners, view_unique_partner, get_partner, update_partner, delete_partner, active_partner, disable_partner, view_all_sectors, view_unique_sector, get_sector, update_sector, delete_sector, delete_user, update_user, view_unique_user, get_user, page_about, add_subscription, add_sector, add_user, view_all_users, add_partner

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

logo = Image.open(r"./images/IES-CONGO1.png")
c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c1:
    st.markdown("""<style>background-color: aqua;} 
            </style> """, unsafe_allow_html=True)
    st.image(logo, width=100)
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
                .e1tzin5v0{
                    padding-top: auto;
                    margin-top: -10px;
                }
                .e16nr0p30{
                    padding-top: 20px;
                }
            </style>
        """, unsafe_allow_html=True)
with c3:
        # st.markdown("""<div id="float"><img src="images/IES-CONGO1.png" alt="IES-DML"></div>""", unsafe_allow_html=True)
    st.image(logo, width=100)


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    page_home()

elif authentication_status == None:
    st.warning("Please enter your username and password")
    page_home()

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

    
    st.markdown("""---""")
    # Test if is the Admin logged in

    if user_type == "Admin":
        with st.sidebar:
            choose = option_menu("MENU", ["More Informations", "Partners Management", "Sectors Management", "Subscriptions", "Account Settings"],
                                icons=['info', 'bookmark', 'book', 'kanban', 'person lines fill'],
                                menu_icon="app-indicator", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa", "color":"black"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#02ab21", "color": "white"},
            }
            )
        if choose == "More Informations":
            page_about()
        elif choose == "Partners Management":
            menu = ["Add partners", "Update partners", "Delete partners", "Active partner", "Disabled partner"]
            choice = st.sidebar.selectbox("Manage Partners", menu)
            if choice =="Add partners":
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Add Partner</h2>", unsafe_allow_html=True)
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
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Update partner</h2>", unsafe_allow_html=True)
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
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Delete partner</h2>", unsafe_allow_html=True)
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
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Active partner</h2>", unsafe_allow_html=True)
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
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Desible partner</h2>", unsafe_allow_html=True)
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

        elif choose == "Subscriptions":
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
        
        
        elif choose == "Sectors Management":
            menu = ["Add sector", "Update sector", "Delete sector"]
            choice = st.sidebar.selectbox("Manage sectors", menu)
            if(choice == "Add sector"):
                    with st.form(key='add_sector'):
                        title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Add Sector</h2>", unsafe_allow_html=True)
                        # id = st.number_input("ID", disabled=True)
                        name = st.text_input("Name of sectors")
                        if st.form_submit_button("Add"):
                            add_sector(name)
                            st.success("Sector {} saved".format(name))
            elif choice == "Update sector":
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Update Sector</h2>", unsafe_allow_html=True)
                result = view_all_sectors()
                with st.expander('List of current sectors'):
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
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Delete Sector</h2>", unsafe_allow_html=True)
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
        
        elif choose == "Account Settings" : 
            menu = ["Add user", "Update user", "Delete user"]
            choice = st.sidebar.selectbox("Manage sittings", menu)
            if choice == "Add user":
                with st.form(key='form1'):
                    title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Register new user</h2>", unsafe_allow_html=True)
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
                st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Update user</h2>", unsafe_allow_html=True)
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
                        new_title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Update user</h2>", unsafe_allow_html=True)
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
                st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Delete user</h2>", unsafe_allow_html=True)
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

        query_date = """SELECT  se.name, DATE_FORMAT(s.startDate, "%d / %m / %Y") AS startDate, DATE_FORMAT(s.endDate, "%d / %m / %Y") AS endDate, DATEDIFF(s.endDate, s.startDate) AS duration, DATEDIFF(s.endDate, CURRENT_DATE) AS remaining, s.status
                            FROM user u, partner p, subscription s, sector se
                            WHERE p.id = s.partnerId AND s.sectorId = se.id AND u.username = %s"""
        c.execute(query_date,(name,))
        pairs = c.fetchall()
        data_user = []
        for row in pairs:
            sector = row[0]
            date_start = row[1]
            date_end = row[2]
            duration = row[3]
            remaining= row[4]
            status= row[5]
            data_user.append({
                'Sector': [sector],
                'Start date': [date_start],
                'End date': [date_end],
                'Duration (in days)': [duration],
                'Time remaining (in days)': [remaining],
                'Status': [status]
            })
        
        query_subscription="""SELECT s.id FROM user u, subscription s, partner p WHERE u.id=p.userId AND p.id=s.partnerId AND DATEDIFF(s.endDate, CURRENT_DATE)<0 AND u.username=%s"""
        c.execute(query_subscription,(name,))
        expered_subscriptions = c.fetchall()
        for row in expered_subscriptions:
            id_subscription=row[0]
            update_status("Expired", id_subscription)

        # VERIFICATION IF THE PARTNER IS ACTIVE
        query_verificate = """SELECT p.active FROM partner p, user u WHERE p.userId = u.id AND u.username =%s """
        c.execute(query_verificate, (name,))
        actives = c.fetchall()
        for row in actives:
            partner_active = row[0]
        
        if partner_active==0:
            st.markdown("<h2 style='text-align: center; font-familly:work; color: red;'>Welcome! You are not currently activated in our system. Please contact the management for administrative reasons. Cordially. Contact: info@iescongo.com</h2>", unsafe_allow_html=True)
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
                choose = option_menu("MENU", ["More informations", "My Subscription", "Data visualisation", "Account Settings"],
                                    icons=['info', 'book', 'kanban', 'gear'],
                                    menu_icon="app-indicator", default_index=0,
                                    styles={
                    "container": {"padding": "5!important", "background-color": "#fafafa", "color":"black"},
                    "icon": {"color": "#d3e3d6", "font-size": "25px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                    "nav-link-selected": {"background-color": "#21662f", "color": "white"},
                }
                )
            if choose == "More informations":
                st.markdown(""" <style> .font {
                            font-size:35px ; font-family: 'work'; color: #21662f;} 
                            </style> """, unsafe_allow_html=True)
                page_about()
                
            elif choose == 'My Subscription':
                title = st.markdown("<h2 style='text-align: center; font-familly:work; color: #21662f;'>Sectors to which you have subscribed</h2>", unsafe_allow_html=True)
                # st.write("Dear {}, IES and DML firms thank you for subscribing to the {} sectors for a period ranging from {} to {}. As a reminder, you have {} left and if you do not renew your subscription, you will be automatically logged out of our system.".format(user, sector, date_start, date_end, remaining))
                table = st.dataframe(data_user)
                # st.write("In addition, we still have a few sectors you can join.")
                # st.write('In case of technical problem, please write to webmaster@dmlcongo.com while copying webmaster@iescongo.com and info@iescongo.com')
                # st.write('Cordially')
                # st.write('Technical team')
            elif choose == 'Data visualisation':
                ####### CHARGEMENT DE DONNEES ##############

                ### DONNEES SECONDAIRES ###
                # Parametres du compte d'utilisateur  
                u="iesmeal"
                pw="IESict4dKobo"
                pd.set_option('display.max_columns',None)
                # df3=requests.get(r"https://kc.kobotoolbox.org/api/v1/data/1208139.csv", auth=(u,pw))

                donnsecond= requests.get(r"https://kc.kobotoolbox.org/api/v1/data/1222011.csv", auth=(u,pw))
                s1=str(donnsecond.content,'utf-8')
                data11 = StringIO(s1)
                donnsecond=pd.read_csv(data11,on_bad_lines='skip')
                # st.write(donnsecond.head())
                ListNamesSec={"Annee_Exercice":"Années d'Exercice","Credit_par_secteur/Commerce":"Crédits en Commerce" ,
                "Credit_par_secteur/Industries_mines":"Crédits Industries de Mines",
                "Credit_par_secteur/Production_distribution_de_gaz_electricite":"Crédits Production de Gaz et Electricité",
                "Credit_par_secteur/Agriculture_Elevage_peche_et_sylviculture":"Crédits Agriculture, Elevage, pêche et sylviculture",
                "Credit_par_secteur/Enseignement":"Crédits dans l'Enseignement",
                "Credit_par_secteur/Production_et_distribution_d_eau":"Crédits production de l'eau",
                "Credit_par_secteur/Sante":"Crédits Santé",
                "Credit_par_secteur/Exploitation_forestiere":"Crédits Exploitation Forestière",
                "budjet_national/justice":"Part du Budget: Justice","budjet_national/defense":"Part du Budget: défense",
                "budjet_national/sante":"Part du Budget: Santé","budjet_national/enseignement":"Part du Budget: Enseignement",
                "budjet_national/agriculture":"Part du Budget: Agriculture","budjet_national/commerce":"Part du Budget: Commerce",
                "budjet_national/environnement":"Part du Budget: Environnement",
                "budjet_national/entrepreuneuriat_PME":"Part du Budget: Entrepreneuriat et PME",
                'budjet_national/genre_famille':"Part du Budget: Genre et Famille"
                }
                donnsecond.rename(columns=ListNamesSec, inplace=True)
                # donnsecond.head()
                #### AIDE HUMANITAIRES ### 
                Aid= requests.get(r"https://kc.kobotoolbox.org/api/v1/data/1223119.csv", auth=(u,pw))
                s2=Aid.content
                data12 = StringIO(s2.decode('utf-8'))
                df22=pd.read_csv(data12,on_bad_lines='skip')
                # df22.head()


                ####  INDICATEUR GENERAUX #####
                IndcUrl = requests.get(r"https://kc.kobotoolbox.org/api/v1/data/1208139?format=json",auth=(u,pw))
                # convertir en JSON
                donneeIndic=IndcUrl.json()
                # Converir au format DataFrame de Pandas
                df3 = pd.DataFrame.from_dict(donneeIndic)
                # df3.head()
                # st.write(df3['renseignement_generaux/Filiere_Chaine_de_valeur'])

                #### PROVINCES ET TERRITOIRE, ZONE DE SANTE, AIRE DE SANTE ENCODING
                liste_code_province=[52,41,	71,	73,	53,	54,	92,	91,	82,	10,	20,	31,	32,	81,	72,	33,	63,	44,	61,	43,	83,	62,	42,	74,	51,	45]
                liste_noms_provinces=['Bas-Uele',	'Equateur',	'Haut-Katanga',	'Haut-Lomami',	'Haut-Uele',	'Ituri',	'Kasaï',	'Kasaï-Central',	'Kasaï-Oriental',	'Kinshasa',	'Kongo-Central',	'Kwango',	'Kwilu',	'Lomami',	'Lualaba',	'Maï-Ndombe',	'Maniema',	'Mongala',	'Nord-Kivu',	'Nord-Ubangi',	'Sankuru',	'Sud-Kivu',	'Sud-Ubangi',	'Tanganyika',	'Tshopo',	'Tshuapa']
                liste_code_province=[str(i) for i in liste_code_province]
                Prov= dict(zip(liste_code_province, liste_noms_provinces))
                df3['Localisation/Province'].replace(Prov,inplace=True)
                df3.rename(columns={'Localisation/Province':'state_name'}, inplace=True)

                liste_code_territoire=[1000,	2001,	2002,	2003,	2005,	2007,	2009,	2010,	2011,	2013,	2015,	2017,	2019,	3102,	3103,	3105,	3106,	3108,	3201,	3202,	3203,	3204,	3206,	3210,	3212,	3302,	3303,	3304,	3306,	3307,	3308,	3310,	3311,	4101,	4102,	4103,	4104,	4105,	4107,	4108,	4109,	4202,	4203,	4204,	4205,	4206,	4301,	4302,	4304,	4305,	4306,	4402,	4404,	4405,	4502,	4503,	4504,	4505,	4506,	4507,	5101,	5102,	5103,	5105,	5107,	5109,	5110,	5111,	5202,	5204,	5206,	5207,	5208,	5302,	5303,	5305,	5307,	5309,	5311,	5402,	5403,	5405,	5407,	5409,	6101,	6102,	6103,	6104,	6105,	6107,	6109,	6110,	6111,	6201,	6202,	6203,	6205,	6206,	6207,	6208,	6210,	6212,	6301,	6302,	6303,	6305,	6307,	6309,	6311,	6313,	7101,	7102,	7104,	7105,	7106,	7107,	7108,	7109,	7202,	7203,	7205,	7206,	7207,	7302,	7303,	7304,	7305,	7306,	7402,	7404,	7406,	7407,	7409,	7410,	8102,	8103,	8104,	8105,	8106,	8108,	8201,	8202,	8205,	8207,	8208,	8209,	8302,	8303,	8306,	8307,	8308,	8309,	9101,	9102,	9104,	9105,	9106,	9107,	9202,	9204,	9205,	9207,	9208]
                liste_noms_territoire=['Kinshasa',	'Matadi',	'Boma',	'Moanda',	'Lukula',	'Tshela',	'Seke-Banza',	'Luozi',	'Songololo',	'Mbanza-Ngungu',	'Kasangulu',	'Madimba',	'Kimvula',	'Kenge',	'Feshi',	'Kahemba',	'Kasongo-Lunda',	'Popokabaka',	'Bandundu',	'Bagata',	'Kikwit',	'Bulungu',	'Idiofa',	'Gungu',	'Masi-Manimba',	'Inongo',	'Kiri',	'Oshwe',	'Kutu',	'Kwamouth',	'Bolobo',	'Yumbi',	'Mushie',	'Mbandaka',	'Bikoro',	'Lukolela',	'Bomongo',	'Makanza',	'Basankusu',	'Bolomba',	'Ingende',	'Gemena',	'Budjala',	'Kungu',	'Libenge',	'Zongo',	'Gbadolite',	'Mobayi-Mbongo',	'Yakoma',	'Businga',	'Bosobolo',	'Lisala',	'Bumba',	'Bongandanga',	'Boende',	'Befale',	'Djolu',	'Ikela',	'Bokungu',	'Monkoto',	'Kisangani',	'Ubundu',	'Opala',	'Isangi',	'Yahuma',	'Basoko',	'Banalia',	'Bafwasende',	'Buta',	'Aketi',	'Bondo',	'Ango',	'Poko',	'Rungu',	'Niangara',	'Dungu',	'Faradje',	'Watsa',	'Wamba',	'Irumu',	'Mambasa',	'Djugu',	'Mahagi',	'Aru',	'Goma',	'Nyiragongo',	'Masisi',	'Walikale',	'Lubero',	'Oïcha',	'Beni',	'Butembo',	'Rutshuru',	'Bukavu',	'Kabare',	'Shabunda',	'Kalehe',	'Idjwi',	'Walungu',	'Uvira',	'Fizi',	'Mwenga',	'Kindu',	'Kailo',	'Punia',	'Lubutu',	'Pangi',	'Kabambare',	'Kasongo',	'Kibombo',	'Lubumbashi',	'Kipushi',	'Sakania',	'Kambove',	'Likasi',	'Kasenga',	'Mitwaba',	'Pweto',	'Mutshatsha',	'Lubudi',	'Dilolo',	'Sandoa',	'Kapanga',	'Kamina',	'Kaniama',	'Kabongo',	'Malemba-Nkulu',	'Bukama',	'Kalemie',	'Moba',	'Manono',	'Kabalo',	'Kongolo',	'Nyunzu',	'Kabinda',	'Mwene-Ditu',	'Luilu',	'Kamiji',	'Ngandajika',	'Lubao',	'Mbuji-Mayi',	'Tshilenge',	'Miabi',	'Kabeya-Kamwanga',	'Lupatapata',	'Katanda',	'Lusambo',	'Lodja',	'Kole',	'Lomela',	'Katako Kombe',	'Lubefu',	'Kananga',	'Dibaya',	'Luiza',	'Kazumba',	'Demba',	'Dimbelenge',	'Kamonia',	'Luebo',	'Ilebo',	'Mweka',	'Dekese']
                liste_code_territoire=[str(i) for i in liste_code_territoire]
                Terri=dict(zip(liste_code_territoire,liste_noms_territoire))
                df3['Localisation/Territoire'].replace(Terri,inplace=True)
                    
                liste_code_zs=['1000ZS01',	'1000ZS02',	'1000ZS03',	'1000ZS04',	'1000ZS05',	'1000ZS06',	'1000ZS07',	'1000ZS08',	'1000ZS09',	'1000ZS10',	'1000ZS11',	'1000ZS12',	'1000ZS13',	'1000ZS14',	'1000ZS15',	'1000ZS16',	'1000ZS17',	'1000ZS18',	'1000ZS19',	'1000ZS20',	'1000ZS21',	'1000ZS22',	'1000ZS23',	'1000ZS24',	'1000ZS25',	'1000ZS26',	'1000ZS27',	'1000ZS28',	'1000ZS29',	'1000ZS30',	'1000ZS31',	'1000ZS32',	'1000ZS33',	'1000ZS34',	'1000ZS35',	'2001ZS01',	'2001ZS02',	'2002ZS01',	'2003ZS01',	'2003ZS02',	'2003ZS03',	'2005ZS01',	'2005ZS02',	'2007ZS01',
               '2007ZS02',	'2007ZS03',	'2007ZS04',	'2007ZS05',	'2009ZS01',	'2009ZS02',	'2010ZS01',	'2010ZS02',	'2010ZS03',	'2011ZS01',	'2011ZS02',	'2013ZS01',	'2013ZS02',	'2013ZS03',	'2013ZS04',	'2013ZS05',	'2015ZS01',	'2015ZS02',	'2017ZS01',	'2017ZS02',	'2017ZS03',	'2019ZS01',	'3102ZS01',	'3102ZS02',	'3102ZS03',	'3103ZS01',	'3103ZS02',	'3103ZS03',	'3105ZS01',	'3105ZS02',	'3106ZS01',	'3106ZS02',	'3106ZS03',	'3106ZS04',	'3106ZS05',	'3108ZS01',	'3201ZS01',	'3202ZS01',	'3202ZS02',	'3202ZS03',	'3203ZS01',	'3203ZS02',	'3204ZS01',	'3204ZS02',
               '3204ZS03',	'3204ZS04',	'3204ZS05',	'3204ZS06',	'3206ZS01',	'3206ZS02',	'3206ZS03',	'3206ZS04',	'3206ZS05',	'3206ZS06',	'3210ZS01',	'3210ZS02',	'3210ZS03',	'3212ZS01',	'3212ZS02',	'3212ZS03',	'3212ZS04',	'3302ZS01',	'3302ZS02',	'3302ZS03',	'3303ZS01',	'3303ZS02',	'3304ZS01',	'3304ZS02',	'3304ZS03',	'3306ZS01',	'3306ZS02',	'3307ZS01',	'3308ZS01',	'3310ZS01',	'3311ZS01',	'4101ZS01',	'4101ZS02',	'4101ZS03',	'4102ZS01',	'4102ZS02',	'4102ZS03',	'4103ZS01',	'4103ZS02',	'4104ZS01',	'4104ZS02',	'4105ZS01',	'4107ZS01',	'4107ZS02',
               '4108ZS01',	'4108ZS02',	'4108ZS03',	'4109ZS01',	'4109ZS02',	'4202ZS01',	'4202ZS02',	'4202ZS03',	'4202ZS04',	'4202ZS05',	'4203ZS01',	'4203ZS02',	'4203ZS03',	'4203ZS04',	'4203ZS05',	'4204ZS01',	'4204ZS02',	'4204ZS03',	'4205ZS01',	'4205ZS02',	'4206ZS01',	'4301ZS01',	'4302ZS01',	'4304ZS01',	'4304ZS02',	'4304ZS03',	'4304ZS04',	'4305ZS01',	'4305ZS02',	'4305ZS03',	'4306ZS01',	'4306ZS02',	'4402ZS01',	'4402ZS02',	'4402ZS03',	'4404ZS01',	'4404ZS02',	'4404ZS03',	'4404ZS04',	'4404ZS05',	'4405ZS01',	'4405ZS02',	'4405ZS03',	'4405ZS04',
               '4502ZS01',	'4502ZS02',	'4503ZS01',	'4503ZS02',	'4504ZS01',	'4504ZS02',	'4505ZS01',	'4505ZS02',	'4506ZS01',	'4506ZS02',	'4506ZS03',	'4507ZS01',	'5101ZS01',	'5101ZS02',	'5101ZS03',	'5101ZS04',	'5101ZS05',	'5102ZS01',	'5102ZS02',	'5102ZS03',	'5103ZS01',	'5103ZS02',	'5105ZS01',	'5105ZS02',	'5105ZS03',	'5105ZS04',	'5107ZS01',	'5109ZS01',	'5109ZS02',	'5109ZS03',	'5110ZS01',	'5110ZS02',	'5111ZS01',	'5111ZS02',	'5111ZS03',	'5202ZS01',	'5202ZS02',	'5204ZS01',	'5204ZS02',	'5206ZS01',	'5206ZS02',	'5206ZS03',	'5207ZS01',	'5208ZS01',	
               '5208ZS02',	'5302ZS01',	'5302ZS02',	'5303ZS01',	'5305ZS01',	'5305ZS02',	'5307ZS01',	'5307ZS02',	'5307ZS03',	'5309ZS01',	'5309ZS02',	'5311ZS01',	'5311ZS02',	'5311ZS03',	'5402ZS01',	'5402ZS02',	'5402ZS03',	'5402ZS04',	'5402ZS05',	'5402ZS06',	'5403ZS01',	'5403ZS02',	'5403ZS03',	'5403ZS04',	'5405ZS01',	'5405ZS02',	'5405ZS03',	'5405ZS04',	'5405ZS05',	'5405ZS06',	'5405ZS07',	'5405ZS08',	'5405ZS09',	'5405ZS10',	'5405ZS11',	'5405ZS12',	'5405ZS13',	'5407ZS01',	'5407ZS02',	'5407ZS03',	'5407ZS04',	'5407ZS05',	'5407ZS06',	'5407ZS07',	
               '5409ZS01',	'5409ZS02',	'5409ZS03',	'5409ZS04',	'5409ZS05',	'5409ZS06',	'6101ZS01',	'6101ZS02',	'6102ZS01',	'6103ZS01',	'6103ZS02',	'6103ZS03',	'6103ZS04',	'6104ZS01',	'6104ZS02',	'6104ZS03',	'6104ZS04',	'6105ZS01',	'6105ZS02',	'6105ZS03',	'6105ZS04',	'6105ZS05',	'6105ZS06',	'6105ZS07',	'6107ZS01',	'6107ZS02',	'6107ZS03',	'6107ZS04',	'6107ZS05',	'6107ZS06',	'6107ZS07',	'6109ZS01',	'6110ZS01',	'6110ZS02',	'6111ZS01',	'6111ZS02',	'6111ZS03',	'6111ZS04',	'6111ZS05',	'6111ZS06',	'6201ZS01',	'6201ZS02',	'6201ZS03',	'6202ZS01',
               '6202ZS02',	'6202ZS03',	'6202ZS04',	'6202ZS05',	'6203ZS01',	'6203ZS02',	'6203ZS03',	'6203ZS04',	'6205ZS01',	'6205ZS02',	'6205ZS03',	'6205ZS04',	'6206ZS01',	'6207ZS01',	'6207ZS02',	'6207ZS03',	'6207ZS04',	'6208ZS01',	'6208ZS02',	'6208ZS03',	'6208ZS04',	'6210ZS01',	'6210ZS02',	'6210ZS03',	'6210ZS04',	'6212ZS01',	'6212ZS02',	'6212ZS03',	'6212ZS04',	'6212ZS05',	'6301ZS01',	'6301ZS02',	'6302ZS01',	'6303ZS01',	'6303ZS02',	'6305ZS01',	'6305ZS02',	'6307ZS01',	'6307ZS02',	'6307ZS03',	'6309ZS01',	'6309ZS02',	'6309ZS03',	'6311ZS01',	
               '6311ZS02',	'6311ZS03',	'6313ZS01',	'6313ZS02',	'7101ZS01',	'7101ZS02',	'7101ZS03',	'7101ZS04',	'7101ZS05',	'7101ZS06',	'7101ZS07',	'7101ZS08',	'7101ZS09',	'7101ZS10',	'7101ZS11',	'7102ZS01',	'7102ZS02',	'7104ZS01',	'7105ZS01',	'7105ZS02',	'7105ZS03',	'7105ZS04',	'7105ZS05',	'7106ZS01',	'7107ZS01',	'7107ZS02',	'7107ZS03',	'7107ZS04',	'7108ZS01',	'7108ZS02',	'7109ZS01',	'7109ZS02',	'7202ZS01',	'7202ZS02',	'7202ZS03',	'7203ZS01',	'7203ZS02',	'7203ZS03',	'7203ZS04',	'7205ZS01',	'7205ZS02',	'7206ZS01',	'7206ZS02',	'7207ZS01',
               '7207ZS02',	'7302ZS01',	'7302ZS02',	'7302ZS03',	'7302ZS04',	'7303ZS01',	'7304ZS01',	'7304ZS02',	'7304ZS03',	'7305ZS01',	'7305ZS02',	'7305ZS03',	'7305ZS04',	'7306ZS01',	'7306ZS02',	'7306ZS03',	'7306ZS04',	'7402ZS01',	'7402ZS02',	'7404ZS01',	'7404ZS02',	'7406ZS01',	'7406ZS02',	'7406ZS03',	'7407ZS01',	'7409ZS01',	'7409ZS02',	'7410ZS01',	'8102ZS01',	'8102ZS02',	'8102ZS03',	'8103ZS01',	'8103ZS02',	'8104ZS01',	'8104ZS02',	'8104ZS03',	'8104ZS04',	'8105ZS01',	'8106ZS01',	'8106ZS02',	'8106ZS03',	'8108ZS01',	'8108ZS02',	'8108ZS03',
               '8201ZS01',	'8201ZS02',	'8201ZS03',	'8201ZS04',	'8201ZS05',	'8201ZS06',	'8201ZS07',	'8201ZS08',	'8201ZS09',	'8201ZS10',	'8202ZS01',	'8202ZS02',	'8205ZS01',	'8205ZS02',	'8207ZS01',	'8208ZS01',	'8208ZS02',	'8209ZS01',	'8209ZS02',	'8302ZS01',	'8302ZS02',	'8302ZS03',	'8303ZS01',	'8303ZS02',	'8303ZS03',	'8306ZS01',	'8306ZS02',	'8307ZS01',	'8307ZS02',	'8308ZS01',	'8308ZS02',	'8308ZS03',	'8309ZS01',	'8309ZS02',	'8309ZS03',	
               '9101ZS01',	'9101ZS02',	'9101ZS03',	'9101ZS04',	'9101ZS05',	'9101ZS06',	'9102ZS01',	'9102ZS02',	'9102ZS03',	'9102ZS04',	'9104ZS01',	'9104ZS02',	'9104ZS03',	'9104ZS04',	'9105ZS01',	'9105ZS02',	'9105ZS03',	'9105ZS04',	'9105ZS05',	'9106ZS01',	'9106ZS02',	'9106ZS03',	'9107ZS01',	'9107ZS02',	'9107ZS03',	'9107ZS04',	'9202ZS01',	'9202ZS02',	'9202ZS03',	'9202ZS04',	'9202ZS05',	'9202ZS06',	'9202ZS07',	'9202ZS08',	'9204ZS01',	'9204ZS02',	'9205ZS01',	'9205ZS02',	'9205ZS03',	'9207ZS01',	'9207ZS02',	'9207ZS03',	'9207ZS04',	'9208ZS01']
                liste_code_zs=[str(i) for i in liste_code_zs]
                liste_noms_zs=['Bandalungwa',	'Barumbu',	'Binza Meteo',	'Binza Ozone',	'Biyela',	'Bumbu',	'Gombe',	'Kalamu I',	'Kalamu II',	'Kasa-Vubu',	'Kikimi',	'Kimbanseke',	'Kingabwa',	'Kingasani',	'Kinshasa',	'Kintambo',	'Kisenso',	'Kokolo',	'Lemba',	'Limete',	'Lingwala',	'Makala',	'Maluku I',	'Maluku II',	'Masina I',	'Masina II',	'Matete',	'Mont Ngafula I',	'Mont Ngafula II',	'Ndjili',	'Ngaba',	'Ngiri-Ngiri',	'Nsele',	'Police',	'Selembao',	'Matadi',	'Nzanza',	'Boma',	'Boma Bungu',	'Kitona',	'Moanda',	'Kangu',	'Lukula',	'Kinkonzi',	
                            'Kizu',	'Kuimba',	'Tshela',	'Vaku',	'Inga',	'Seke-Banza',	'Kibunzi',	'Luozi',	'Mangembo',	'Kimpese',	'Nsona-Mpangu',	'Boko-Kivulu',	'Gombe-Matadi',	'Kimpangu',	'Kwilu-Ngongo',	'Mbanza-Ngungu',	'Masa',	'Sona-Bata',	'Kisantu',	'Ngidinga',	'Nselo',	'Kimvula',	'Boko',	'Kenge',	'Kimbau',	'Feshi',	'Kisanji',	'Mwela Lembwa',	'Kahemba',	'Kajiji',	'Kasongo Lunda',	'Kitenda',	'Panzi',	'Tembo',	'Wamba Lwadi',	'Popokabaka',	'Bandundu',	'Bagata',	'Kikongo',	'Sia',	'Kikwit-Nord',	'Kikwit-Sud',	'Bulungu',	'Djuma',
                            'Ganga',	'Lusanga',	'Pay Kongila',	'Vanga',	'Idiofa',	'Ipamu',	'Kimputu',	'Koshibanda',	'Mokala',	'Mungindu',	'Gungu',	'Kingandu',	'Mukedi',	'Masi-Manimba',	'Moanza',	'Mosango',	'Yasa-Bonga',	'Banjow Moke',	'Inongo',	'Ntandembelo',	'Kiri',	'Penjwa',	'Bosobe',	'Mimia',	'Oshwe',	'Bokoro',	'Nioki',	'Kwamouth',	'Bolobo',	'Yumbi',	'Mushie',	'Bolenge',	'Mbandaka',	'Wangata',	'Bikoro',	'Iboko',	'Ntondo',	'Irebu',	'Lukolela',	'Bomongo',	'Lilanga Bobangi',	'Makanza',	'Basankusu',	'Djombo',	'Bolomba',	'Lolanga Mampoko',
                            'Monieka',	'Ingende',	'Lotumbe',	'Bogosenubia',	'Bominenge',	'Bwamanda',	'Gemena',	'Tandala',	'Bangabola',	'Budjala',	'Bulu',	'Mbaya',	'Ndage',	'Bokonzi',	'Boto',	'Kungu',	'Libenge',	'Mawuya',	'Zongo',	'Gbadolite',	'Mobayi Mbongo',	'Abuzi',	'Wapinda',	'Wasolo',	'Yakoma',	'Businga',	'Karawa',	'Loko',	'Bili',	'Bosobolo',	'Binga',	'Boso Manzi',	'Lisala',	'Bumba',	'Lolo',	'Yamaluka',	'Yambuku',	'Yamongili',	'Bongandanga',	'Boso Mondanda',	'Bosondjo',	'Pimu',	'Boende',	'Wema',	'Befale',	'Mompono',	'Djolu',
                            'Lingomo',	'Ikela',	'Mondombe',	'Bokungu',	'Bosanga',	'Yalifafo',	'Monkoto',	'Kabondo',	'Lubunga',	'Makiso-Kisangani',	'Mangobo',	'Tshopo',	'Lowa',	'Ubundu',	'Wanierukula',	'Opala',	'Yaleko',	'Isangi',	'Yabaondo',	'Yahisuli',	'Yakusu',	'Yahuma',	'Basali',	'Basoko',	'Yalimbongo',	'Banalia',	'Bengamisa',	'Bafwagbogbo',	'Bafwasende',	'Opienge',	'Buta',	'Titule',	'Aketi',	'Likati',	'AAAAA',	'Bondo',	'Monga',	'Ango',	'Poko',	'Viadana',	'Isiro',	'Rungu',	'Niangara',	'Doruma',	'Dungu',	'Aba',	'Faradje',	'Makoro',	
                            'Gombari',	'Watsa',	'Boma-Mangbetu',	'Pawa',	'Wamba',	'Boga',	'Bunia',	'Gethy',	'Komanda',	'Nyakunde',	'Rwampara',	'Lolwa',	'Mambasa',	'Mandima',	'Nia-Nia',	'Bambu',	'Damas',	'Drodro',	'Fataki',	'Jiba',	'Kilo',	'Linga',	'Lita',	'Mangala',	'Mongbalu',	'Nizi',	'Rethy',	'Tchomia',	'Angumu',	'Aungba',	'Kambala',	'Logo',	'Mahagi',	'Nyarambe',	'Rimba',	'Adi',	'Adja',	'Ariwara',	'Aru',	'Biringi',	'Laybo',	'Goma',	'Karisimbi',	'Nyiragongo',	'Katoyi',	'Kirotshe',	'Masisi',	'Mweso',	'Itebero',	'Kibua',	'Pinga',
                            'Walikale',	'Alimbongo',	'Biena',	'Kayna',	'Lubero',	'Manguredjipa',	'Masereka',	'Musienene',	'Kalunguta',	'Kamango',	'Kyondo',	'Mabalako',	'Mutwanga',	'Oicha',	'Vuhovi',	'Beni',	'Butembo',	'Katwa',	'Bambo',	'Binza',	'Birambizo',	'Kibirizi',	'Rutshuru',	'Rwanguba',	'Bagira',	'Ibanda',	'Kadutu',	'Kabare',	'Kaniola',	'Katana',	'Miti-Murhesa',	'Nyantende',	'Kalole',	'Lulingu',	'Mulungu',	'Shabunda',	'Bunyakiri',	'Kalehe',	'Kalonge',	'Minova',	'Idjwi',	'Kaziba',	'Mubumbano',	'Nyangezi',	'Walungu',	'Hauts-Plateaux',	
                            'Lemera',	'Ruzizi',	'Uvira',	'Fizi',	'Kimbi Lulenge',	'Minembwe',	'Nundu',	'Itombwe',	'Kamituga',	'Kitutu',	'Mwana',	'Mwenga',	'Alunguli',	'Kindu',	'Kailo',	'Ferekeni',	'Punia',	'Lubutu',	'Obokote',	'Kalima',	'Kampene',	'Pangi',	'Kabambare',	'Lusangi',	'Saramabila',	'Kasongo',	'Kunda',	'Samba',	'Kibombo',	'Tunda',	'Kamalondo',	'Kampemba',	'Katuba',	'Kenya',	'Kisanga',	'Kowe',	'Lubumbashi',	'Mumbunda',	'Rwashi',	'Tshamilemba',	'Vangu',	'Kafubu',	'Kipushi',	'Sakania',	'Kambove',	'Kapolowe',	'Kilela Balanda',
                            'Manika',	'Panda',	'Likasi',	'Kasenga',	'Kikula',	'Lukafu',	'Kashobwe',	'Mitwaba',	'Mufunga Sampwe',	'Kilwa',	'Pweto',	'Dilala',	'Lualaba',	'Mutshatsha',	'Bunkeya',	'Fungurume',	'Kanzenze',	'Lubudi',	'Dilolo',	'Kasaji',	'Kafakumba',	'Sandoa',	'Kalamba',	'Kapanga',	'Baka',	'Kamina',	'Kinda',	'Songa',	'Kaniama',	'Kabongo',	'Kayamba',	'Kitenge',	'Malemba',	'Lwamba',	'Mukanga',	'Mulongo',	'Bukama',	'Butumba',	'Kabondo Dianda',	'Kinkondja',	'Kalemie',	'Nyemba',	'Kansimba',	'Moba',	'Ankoro',	'Kiyambi',	'Manono',	
                            'Kabalo',	'Kongolo',	'Mbulula',	'Nyunzu',	'Kabinda',	'Kalonda Est',	'Ludimbi Lukula',	'Makota',	'Mwene Ditu',	'Kalenda',	'Kanda Kanda',	'Luputa',	'Wikong',	'Kamiji',	'Kalambayi Kabanga',	'Mulumba',	'Ngandajika',	'Kamana',	'Lubao',	'Tshofa',	'Bipemba',	'Bonzola',	'Dibindi',	'Diulu',	'Kansele',	'Lubilanji',	'Lukelenge',	'Mpokolo',	'Muya',	'Nzaba',	'Kasansa',	'Tshilenge',	'Cilundu',	'Miabi',	'Kabeya Kamuanga',	'Mukumbi',	'Tshishimbi',	'Bibanga',	'Tshitenge',	'Lusambo',	'Ototo',	'Pania Mutombo',	'Lodja',	
                            'Omendjadi',	'Vanga Kete',	'Bena Dibele',	'Kole',	'Lomela',	'Tshudi Loto',	'Djalo Djeka',	'Katako Kombe',	'Wembo Nyama',	'Dikungu',	'Minga',	'Tshumbe',	'Bobozo',	'Kananga',	'Katoka',	'Lukonga',	'Ndesha',	'Tshikaji',	'Bunkonde',	'Dibaya',	'Lubondaie',	'Tshikula',	'Luambo',	'Luiza',	'Masuika',	'Yangala',	'Bilomba',	'Kalomba',	'Mikalayi',	'Ndekesha',	'Tshibala',	'Bena Leka',	'Demba',	'Mutoto',	'Bena Tshiadi',	'Katende',	'BBBBBBBBBB',	'Muetshi',	'Kalonda Ouest',	'Kamonia',	'Kamwesha',	'Kanzala',	'Kitangwa',	'Mutena',
                            'Nyanga',	'Tshikapa',	'Luebo',	'Ndjoko-Mpunda',	'Banga Lubaka',	'Ilebo',	'Mikope',	'Bulape',	'Kakenge',	'Mushenge',	'Mweka',	'Dekese']


                ZonneS=dict(zip(liste_code_zs,liste_noms_zs))
                df3['Localisation/ZS'].replace(ZonneS,inplace=True)


                liste_codes_AS=list(range(1,7158))
                liste_codes_AS=[str(i) for i in liste_codes_AS]
                liste_noms_AS=['Danga',	'Kopi',	'Kama',	'Nembisili',	'Lobuya',	'Cadelu',	'Bosombuki',	'Ndongo',	'Boboka',	'Bonginda',	'Bongwela',	'Fin-Terme',	'Likuba',	'Bokonzi',	'Lusengo',	'Malunza',	'Mobeka',	'Mission',	'Ndamana',	'Bokoyo',	'Mainika',	'Buye',	'Zamoyi',	'Banda',	'Mugalie',	'Sangwa',	'Samungu',	'Dakwa',	'Bandueli',	'Bondeko',	'Nzeret',	'Biasu',	'Kolo',	'Bella',	'Monga Ii',	'Monga I',	' ',	'Sombe',	'Mengi',	'Panzi',	'Maria',	'S.O.S',	'Ciriri',	'8Ã¨me CAPAC',	'CECA 40 Mweze',	'Neema',	'Uzima',	'Cimpunda-Maendeleo',	'Nyamulagira',	'Biname',	'Funu',	'Nyamugo',	'Labotte',	'Saio',	'CECA 40 Nguba',	'Nyawera',	'Croix -Rouge Nguba',	'Malkia wa amani',	'Muhungu Diocesain',	'Muhungu CELPA',	'Maman Mwilu',	'Gihamba',	'Cidasa',	'Chahi',	'Kabuye',	'Burhiba',	'Lumu',	'Beroya',	'Bagira',	'Mushekere',	'Kahero',	'Nyamuhinga',	'Ciguri',	'Buziba',	'Cowe',	'Kilambwigali',	'Kasika',	'Kilimbwe',	'Irangi',	'Kalambi',	'Ngando',	'Sungwe',	'Iganda',	'Kalole',	'Kitamba',	'Tuseswa',	'Kitagana',	'Bisembe',	'Mulombozi',	'Kibanda',	'Matebo',	'Kagelagela',	'Kazuza',	'Byonga',	'Kakolokelwa',	'Tukenga',	'Espoir',	'Mwangaza',	'Busakizi',	'Sugulu',	'Nyamibungu',	'Cobader-Mitobo',	'Mela',	'Kakemenge',	'Butetegele',	'Kabikokole',	'Mukemenge',	'Mapale',	'Makalanga',	'Nyakatulwa',	'Bakongo',	'Isogha',	'Cremetral',	'Isopo',	'Kigalama',	'Kankanga',	'Kibe',	'Bungalama',	'Ngolole',	'Mulambula',	'Ngambwa',	'Bigombe',	'Mboza',	'Kalingi',	'Kimbangu',	'Kele-SIDEM',	'Kele-CEPAC',	'Asuku',	'Asobaka',	'Luliba',	'Polyclinique-Afya',	'Katunga',	'Solu',	'Mero',	'Mungembe',	'Kalole',	'Kassa',	'Masanga-Sud',	'Miswaki',	'Tusisi',	'Kimbondi-Sud',	'Kikamba',	'Kipulu',	'Matili',	'Tuntungulu',	'Tukumbi',	'Lupimbi',	'Ngingi',	'Nyalubwe',	'Mbangayo',	'Dima',	'Makese',	'Tchombi',	'Bubila',	'Mutabo',	'Ishasha',	'Nyaruhange',	'Kiseguro',	'Katwiguro',	'Munyaga',	'Kisharo',	'Nyamitwitwi',	'Check Mamawahuruma',	'Kibirizi',	'Kabati',	'Nyanzale',	'Bwalanda',	'Kiyeye',	'Kirumba',	'Buhondwa',	'Singa',	'CBCA Bambo',	'CBCE Bambo',	'Faraja',	'Kishishe',	'Katsiru',	'Katuunda',	'Kabingu',	'Ufamandu',	'Bishange',	'Bitonga',	'Ruhegeri',	'Ngungu',	'Mumba',	'Rubaya',	'Mutumbala',	'Kabase',	'Karuba',	'Butale-Monkolo',	'Tambi',	'Kibarizo',	'Kirumbu',	'Katuna',	'Kalembe',	'Kashuga',	'Bweryu',	'Luhanga',	'Bibwe',	'Rugarama',	'Katuna',	'Bukama',	'Kivuye',	'Vuhoyo',	'Katala',	'Kauli',	'Bukununu',	'Mubana',	'Kisima',	'Vikendo',	'Kipese',	'Burusi',	'Kasongwere',	'Ngitse',	'Kyondo',	'Kalengehya',	'Vayana',	'Kasisi',	'Katiri',	'Ngeleza',	'Miringate',	'Vusitoro',	'Masereka',	'Mihake',	'Kaniyi',	'Kihindo',	'Muliki',	'Butare',	'Kanyangoy',	'JTN',	'Nyarubande',	'Luoto',	'Nyamitaba',	'Kanyatsi',	'Nyakariba',	'Muheto',	'Kalonge',	'Kahanga',	'Buguri',	'Kitsuli',	'Bihambwe',	'Kaniro',	'Kibabi',	'Bukumbirire',	'Katoyi',	'Luke',	'Mianja',	'Masisi',	'Loashi',	'Buabo',	'Maya',	'Langira',	'Ngomashi',	'Kimua',	'Kimo',	'Mbitsi',	'Muhanga',	'Ngenge',	'Nyabiondo',	'Kamonyi',	'Mandelya',	'Kaseke',	'Rombe I',	'Saint-Paul',	'Kabindula',	'Kalundu CEPAC',	'Kala SOS',	'Kavimvira',	'Kiyaya',	'Kasenga CEPAC',	'Mitumba',	'Kirungu',	'Kitumba',	'Rugezi',	'Kabingo',	'Kihunga',	'Bigaragara',	'Muliza',	'Kekenge',	'Kalonge',	'Kalingi',	'Nondjwa',	'Kahwela',	'Ilundu',	'Ibumba',	'Minembwe',	'Kinyokwe',	'Kisombe',	'Irumba',	'Kisanya',	'Mikenge',	'Lugabano',	'Bakura',	'Malingi',	'Ngomiano',	'Ngena',	'Kalonge',	'Kitibingi',	'Malanda',	'Tulambo',	'Kipupu',
                'Lubumba',	'Kitopo',	'Kabara',	'Tchakira',	'Aleba',	'Mikalati',	'Kanogo',	'Kanono',	'Mukumba',	'Muramvya',	'Kinyonyi',	'Masatha',	'Masango',	'Kahololo',	'Kitembe',	'Kirumba',	'Mugogo',	'Katanga',	'Bibangwa',	'Bijojo',	'Bijombo',	'Magunda',	'Kagogo',	'Chanzovu',	'Kitoga',	'Rubuga',	'Ishenge',	'Rubemba',	'Kateja',	'Makungu',	'Ngalula',	'Lubichako',	'Lubonja',	'Butale',	'Misisi',	'Mayimoto',	'Bibizi',	'Sanga',	'Lusilu',	'Katupu',	'Kilembwe',	'Lulimba',	'Namukala',	'Lumbwe',	'Nessani',	'Makola',	'Sungwe',	'Tchonwe',	'Kimaka',	'Kayumba',	'Kihungwe',	'Katala',	'Ndegu',	'Mulenge',	'Bushuju',	'Bulaga',	'Langala',	'Narunanga',	'Lemera',	'Kibungu',	'Bwegera',	'Ndolera',	'Nyamutiri',	'Luvungi II',	'Katogota',	'Mirungu',	'Kiringye',	'Luvungi I',	'Munanira',	'Busulira',	'Buheba',	'Kagaragara',	'Lubarika',	'Pungu',	'Abala',	'Nakiele',	'Kanguli',	'Kilumbi',	'Lutabura',	'Kaboke',	'Luberizi',	'Mutarule',	'Nazareno',	'Rusabagi',	'Kigurwe',	'Sange Etat',	'Sange CEPAC',	'Kigoma',	'Mangwa',	'Mugaja',	'Ndunda',	'Luhito',	'Runingu',	'Hongero',	'Sucki Etat',	'Kagando',	'Kiliba CEPAC',	'CBCA Kiliba',	'Mubere',	'Mahungubwe',	'Bunduki',	'Mombwasa',	'Atso',	'Molendo',	'Ngambele',	'Lengo',	'Banda',	'Mbele',	'Wozo',	'Kangalanga',	'Kpokoro',	'Gwi',	'GBagaembo',	'Baya',	'Kedza',	'Boduna',	'GBoko',	'Wodzo',	'Kongo',	'Boroto',	'GBangi',	'Durugu',	'Sidi',	'Boroko 1',	'Bili',	'Pandu',	'Baraga',	'MBele',	' ',	' ',	' ',	' ',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Binga',	'Balaw',	'Bokonzo',	'Tamozombe',	'Gemena III',	'Karagba',	'Libenge Moke',	'Lida',	'Salongo II',	'Kutu',	'Notre Dame',	'Djiba',	'CitÃ©',	'Nzeka',	'Salongo I',	'Kengele Ngbanvu',	'Ville',	'EvÃªchÃ©',	'Bolumbe',	'Bokala',	'Bozagba25',	'Ngwenze',	'Nguwenge',	'Bodeme',	'Zekefia',	'Bozoko',	'Bogwaka',	'Bongbada',	'Gbatikombo',	'Mbari',	'Mont Gila',	'Botela',	'Botuzu',	'Kombo',	'Mopela',	'Bominenge Kada',	'Bombisa',	'Bodenge',	'Bowazi',	'Bogbase',	'Bowakara',	'Bobisi',	'Bowara',	'Bodiawa',	'Bogamana',	'Boyademele',	'Bokuda',	'Boyambi',	'Wissika',	'Gbakata',	'Ngbulutu',	'Bodigia Moke',	'YETU',	'JAAMA',	'DE LA PAIX',	'BOYOMA',	'ST PIERRE',	'BANDUKU',	'Bombula',	'Betsaida',	'Kondima',	'Profession',	'Okapi',	'Famille',	'Anoalite',	'Mama Mwilu',	'Marie Antoinette',	'Salama',	'Siloe',	'Bondeko',	'Uzima',	'Tibata',	'Matete',	'Confiance',	'Segama',	'Fedi',	'Mc Millan',	'VILLE',	'MAKISO',	'COKIS',	'ROSARIA',	'NEEMA',	'LIBOTA',	'IMANI',	'MOKELA',	'KONGA KONGA',	'Museya',	'Bulambo',	'Vyakuno',	'Kyalumba',	'Kirindera',	'Vitumbi',	'Kalivuli',	'Kivuwe',	'Katama',	'Kiuli',	'Octobora',	'Lukaraba',	'Karete',	'Limangi',	'Usumbura',	'Kabamba',	'Musenge',	'Nyasi',	'SacrÃ© Coeur',	'8Ã©me CEPAC WALIKALE',	'Kumbwa',	'Mutakato',	'Mandje',	'Ntoto',	'Byungu',	'Malembe',	'Hombo Nord',	'Mianga',	'Biruwe',	'Obaye',	'Bilobilo',	'Osokari',	'Djingala',	'Mundundi',	'Ndofia',	'KATENDA',	'YASSA MIWUNU',	'KANGA',	'POMONGO',	'IWUNGU NSAMBA',	'KIMPATA EKU',	'BEMBELE',	'BUSONGO',	'MIKUNGU',	'BANGA SECTEUR',	'BANGA BANGA',	'KALANGANDA MUNKEN',	'MAYANDA',	'NDUNGU',	'MWILAMBONGO',	'MBANGI',	'MPOM',	'IMPANGA',	'PUNKULU',	'MANDING',	'EBAA',	'MAPELA',	'KIZITO',	'LWANGA',	'KINGAMBO',	'INIENDONGO',	'MUSENGE MPUTU',	'IMPINI INGUNDU',	'IFWANZONDO',	'BITSHAMBELE',	'BWALENGE',	'YASSA LOKWA',
                'INTSWEM CATHOLIQUE',	'KIMPATA NKOY',	'BUDJIMBILA',	'NIEKONGO',	'BUSHIBONGO',	'LUVUJI',	'INTSWEM LABWI',	'ISENGI',	'IYANGA',	'MIKANO',	'GOMBE',	'KASEMBE',	'MINGANDJI',	'YASSA PENDE',	'LUKA',	'BANDA',	'MADIMBI',	'MISANGI',	'LUENDE',	'MUNGAY',	'KINGUBA',	'NIOKA KAKESE',	'KILEMBE MC',	'MUKEDI',	'KINZAMBA I',	'KINZAMBA II',	'LOZO KAKESE',	'KILUNDU',	'LOZO MUNENE',	'DONGO',	'GUNGU II',	'MULWA',	'ATEN',	'ISBUMA',	'BONDO',	'INDELA',	'MALUNGA',	'LUKAMBA',	'BUSHI',	'KATEMBO',	'KILAMBA',	'NIEKENENE',	'KAKOBOLA',	'MUNGINDU I',	'MUNGINDU II',	'KIKANDJI',	'KITAMBWE',	'KINIAMA',	'PANAF',	'BITSHIAMBELE',	'LUKUNGA',	'MUNDUNDU',	'TOTSHI',	'KALUMBU',	'MBANGI',	'KANGU II',	'CMCO',	'GUNGU I',	'KINDJI MUSANGA',	'KASALA',	'MBANZA KIKAPA',	'KASANZA',	'KIPANDE',	'KINGWAYA',	'NSESE',	'NKAW',	'MIMIA',	'BISENGE BATWA',	'LOKOLAMA II',	'MANTANTALE',	'NGALI BENYENYE',	'BOLONGO WETI',	'NKOTO',	'BERONGE',	'BOKOLI WA BONGO',	'BOKALA',	'NGELEBEKE',	'LOKOLOLI',	'IBAMBA BOLONGO',	'NZOBE',	'BOBEKE',	'BEBONGO',	'BAAMBE',	'IBEKE',	'ILUNGU',	'NKILE',	'EBANZA',	'MAKANZA',	'NGELI BANDA',	'DUELO',	'MBE TENKOY',	'BOSAW',	'BOMPOMBO',	'IREKO',	'IKONGO',	'BENGOLO',	'IYEMBE EKONGO',	'IYEMBE MAKANZA',	'KOLOKOSO',	'MUKILA',	'MAKIOSI',	'KALENGE',	'SWABANGU',	'ST ESPRT',	'CBCO',	'KASOMBO',	'PONT WAMBA',	'GABIA',	'MISELE',	'KIMAFU',	'MAKIALA',	'MUNSANGUNSAI',	'BANGONGO',	'FASAMBA',	'KIKONGO LWASA',	'KOBO',	'BANGOMBE',	'KAPAY LONO',	'MUSAKA',	'MUKUMBI',	'BARRIERES',	'BUSEKE',	'LULAU',	'KITOY',	'BENGI',	'KINA KABOBA',	'DUNDA',	'BILILI',	'MBANZA GOBARI',	'KWAYA',	'LUWANGA',	'KIMBURI',	'KIAMFU',	'YASA',	'MBANZA WAMBA',	'KIMBWAYAMU',	'FULA',	'MBANZA MFUMU NKENTO',	'MANDONDO',	'PELO KUMBI',	'KIMBINGA',	'KIBANDA',	'KHINJI-LONGELE',	'KOBO',	'MUKUKU',	'KATELENGE',	'KINGELEMA',	'KANGU I',	'MUTOMBO KANGU',	'KASANZA PONDO',	'KAHELA',	'KIKOMBO',	'KIZUNGU NZADI',	'KINDEMBE',	'DUNGU LOSO',	'SESE KIDINDA',	'KULUNGU NZADI',	'KANGA NZADI',	'SONDJI',	'KIMBIMBI',	'BOMPONGO',	'ILANGOSONGO',	'MOLELE',	'MOMBOYO',	'IKOYO',	'MONIO',	'PENDJWA',	'LOKOKOLOKO',	'ITENDO',	'IMENGE',	'MBUNGA',	'NZALE',	'MOGERO',	'MALEBO',	'CBCO',	'IBOLE',	'CEBU',	'BONDEKO',	'BASOKO II',	'NSANGA NSANGA',	'BOKORO',	'ELOMBE',	'NDJAMPIE',	'NSEKESIRI',	'KEMPIMPI',	'MUSHUNI',	'LUKWEY',	'KIMBANDASAY',	'SEMENTOKO',	'ENKUTU',	'IKWALESA',	'BAMABA',	'SELEKOKO',	'TENELE',	'LIKWANGOLA',	'BOSOBE',	'TAMPIETE',	'MUKENGI',	'KIMPUTU',	'MBUSHIE',	'MBAMBA',	'MUWAKA',	'MOLIAMBO',	'ZABA KILUNDA',	'LUKALA',	'KINGALA',	'MUKINZI',	'KILUNDA',	'NSALU',	'NGANGA',	'BILILI',	'MOSIA',	'MAYOKO',	'GRAND PORT',	'BADIMUMBUMBA',	'FATIMA',	'KIBONGO BULUNGU',	'MILUNDU NSIAMA',	'KITABI',	'PUTUBONGO',	'KINZAMBI',	'BELEMIESE',	'KIMANU',	'MUPULU',	'MOBU',	'KIYOKO',	'BENGI',	'MUDIAMBU',	'MBANZA DIBUNDU',	'LUNIUNGU',	'ZABA LUNIUNGU',	'KIALU',	'NDUNGA',	'TERRE JAUNE',	'KIKONGO TANKU',	'KIMBUMBIDI',	'KIYAKA',	'MPO',	'NTO',	'PITA',	'MBAKA KASAI',	'KINKO',	'KINZIE',	'POKASAI',	'MABENGA',	'KIPALA',	'LUKINGA',	'KIBWADI LEY',	'NDANA',	'KIDZWEME',	'MBWASA',	'MBALIBI',	'MBALA',	'NGUDI',	'PANGA',	'NGELEBANGA',	'SIA',	'BULU',	'PANU',	'MUDIAMBU',	'TUMIKIA',	'YENZI',	'KITAMBO',	'MULUMA',	'MOSANGO',	'MUWANDA KOSO',	'KUMBI MBWANA',	'KASAY',	'KIPWANGA',	'KINZAMBA I',	'KINZAMBA II',	'MANGUNGU',	'KIPEMBE',	'KINZENZENGO',	'KINZANDA',	'EOLO',	'MAKANGA',	'PANU CBCO',	'PANU SUMBU',	'BIKOKO',	'NSEKIMPUTU',	'KALO',	'KINDWA',	'MBONGI',	'MATEKO KIVUVU',	'NSENGE NSENGE',	'MUSELE',	'MATEKO ETAT',	'JAKU',	'MOKALA',	'MBALA',	'MOBINI',	'LUNGWAMA',	'MUZO',	'KIO',	'NIANGA',	'KINKONO',	'PIO PIO',	'PANU CITE',	'SEDZO',
                'KIBALA',	'LWEM',	'NGOSO',	'MUSENGE MUNENE',	'IMPASI',	'LADZUM',	'KALANGANDA',	'LWELE IKUBI',	'MAYUNG',	'KINTSWA MFINDA',	'ZULUBANGA',	'NSIMANSIE',	'EBUBU',	'INTSWEM EBAY',	'TSHENE',	'BA NSIENGWON',	'ELANGA NENE',	'BULWEM',	'MBEO',	'ITERE MBANG',	'EBIALA KANDOLO',	'INTSWEM MUKONGO',	'MAKUBI',	'KIMPUTU',	'EBAY MUKUNGU',	'FATUNDU',	'FAKWILU',	'KIBWANGA',	'NKWAYA',	'LUNKUNI',	'NGI',	'KIMBAY',	'FAMBONDO',	'FANKANA',	'KINDONGOMBE',	'MUKULANZADI',	'MUMBUNDA',	'MBONGAMBANZA',	'MISAY',	'MBULUKUMBI',	'NSWE',	'KIKONGO',	'MBALA',	'MULASHI',	'MIKWI SECTEUR',	'LAREME',	'LWANO',	'DJUMA',	'KIMBATA',	'LUBIDI',	'LUZUBI',	'DWE NGANGA',	'KIMBANGULA',	'MOAKA',	'MUYELE TANGO',	'BUSALA',	'MOLILI',	'MIAH',	'PUKULU',	'SALA',	'MUYENE',	'NGUNU',	'MUBOLO',	'FUMUNDJOKO',	'MAYOKO',	'DWE MISSION CATHOLIQUE',	'LUNGAMA',	'ETO',	'KABALA',	'KIMPINI',	'LUBUNDJI',	'NSELE',	'MUYOMBO',	'CBCO',	'PINDI MISSION CATHOLIQUE',	'MPENE',	'NIADI',	'NDWIY',	'MUTOY',	'EBAY',	'EKUBI',	'YAMBAU',	'MBENI',	'NGWEME',	'MBIMBI',	'MITSHAKILA',	'MAYALA',	'NKARA',	'MUSENGE',	'KIA KIA',	'NTANDU',	'MAYOKO NIADI',	'KAZAMBA PINDI',	'KIYAKA MAFUTAMINGI',	'NGANDUNGALA',	'KIWUTU',	'BILOLO',	'MALUNGA',	'NKO',	'KIKIOR',	'LUMBU',	'MUSHIE PENTANE',	'BEKANE',	'MATAMBA',	'NDIKA NDIKA',	'LWANI',	'DISASI',	'MUSABA',	'BOYON',	'ISAKA MBOLE',	'SEMENDUA CITE',	'SEMENDUA CEBU',	'BIEN',	'MAKAW',	'IKONYA',	'LONIO',	'MALIBA',	'NSONDIA',	'BOKOLI',	'IBANDA',	'NTANDA II',	'EPOKENKASO',	'KIBAMBILI',	'LEBA',	'KIEMU',	'ANCIENS COMBATTANTS',	'INGA II',	'BOJI',	'INGA I',	'MUKASA',	'NGONGA',	'TRENTE JUIN',	'KAZAMBA',	'MISENGI',	'KAGGWA',	'KIMPWANZA',	'INFRA',	'KINDI',	'KIPABU',	'LUKUNI WAMBA',	'MUKULUTU',	'MOSAMBA',	'KIBWILA',	'KIDIMA',	'MUKATA',	'KIYENGA',	'MOTONI TOY',	'KIBENGELE',	'KABWITA',	'KIMBAU',	'TSAKU MALAFU',	'GANAKETI',	'MATARI',	'NGUDINKAMA',	'MAHUNGU',	'TSAKALA KUKU',	'MAFUTI',	'MWANABASILA',	'KANDILUKENI',	'KATAMBI',	'KINGUNGU',	'KISADI',	'NZASI MWADI',	'SWA MASANGU',	'KINKOLE',	'SUKA MBUNDU',	'KAPITA SUKA',	'TEMBO KUNTUALA',	'MAKENZI',	'KIMWAMBU',	'SWA KIBULA',	'FWANGONGO',	'KIMBWASA',	'BONDO POKOSO',	'BASOKO I',	'MONTERESIENE',	'BANGUMI',	'SAMPIER',	'BENO',	'KIBIMI',	'MBAYA',	'NTOBER',	'BAGATA I',	'SIEM SIEM',	'MANTIENE',	'MANZASAY',	'NDANA',	'KAMA',	'KINDONGO',	'NTA',	'CAMP LEMBA',	'IBOTO',	'DUNGU',	'MBIEN KASAI',	'MPANDA LUKENIE',	'SEMAZA',	'NDOJIME',	'SEBIE',	'SEMONDANI',	'BOBO CK',	'KILIMA',	'IPEKE',	'KUTU CENTRAL',	'KUTU LUMUMBA',	'KEMBA LELAW',	'BOMO',	'BOTEMOLA',	'LUNA',	'VUNA',	'TOLO I',	'MOTANGIRI',	'KEMBA SECTEUR',	'MOKILA',	'BOKUNGU',	'TOLO II',	'BAKELE',	'ISANGA BOKOTE',	'BOLIYANGUA',	'ITITO',	'MBUYE BOTOLA',	'NSAW',	'WETI BOLOLO',	'MBALA',	'IBEKE',	'MBELO',	'ISANGAIBALI',	'LOKANGA',	'LOMBE',	'BOKOTOKILI',	'ISONGO',	'NDONGESE',	'MBALE',	'NSELENGE',	'IBENGA',	'NGONGIYEMBE',	'KESENGE',	'LOBEKE',	'BELEMBE',	'BOTAKA',	'BETUMBE',	'BEENGO',	'NKOLOBEKE',	'LIKUANGOLA',	'MPOLO',	'MAMA YAKA',	'MOMBILANGA',	'MOMBOKONDA',	'MPANZA',	'MBUSEMPOTO',	'KUNDO',	'NTANDE NGOMO',	'GOMELENGE',	'BOONDO',	'NKALA',	'NTANDE MPENGE',	'IBAMBA',	'BOKOTE',	'BASIMBA',	'BANZOW-MOKE',	'MEKIRI',	'NTUMBE',	'BOLONDO',	'BANZOW-MONENE',	'MONGEMPONGO',	'NGONGO BASENGELE',	'MPILI',	'BOMBOLIMBOKA',	'NGOO',	'NGANYA',	'ILEBOMANGALA',	'MPOKO',	'BOKALAKALA',	'MONGAMA',	'MANSELE',	'BOPONGA',	'BONGENDE',	'KIMBEKE',	'MOLENDE',	'KIDIKI',	'MISSION CATH',	'NKOMBE',	'NKOLOYOKA',	'BOLU',	'LIKOLO',	'NTANDA I',	'BOYANGA',	'BOBANGI',	'MPENDA',	'NSINGI',	'ELONGO',	'MPOLE',	'MISILO',	'MIPALE',	'IKENZE',	'MANKAKITI',	'MOKIELI',	'KENGUBU',	'SABENA',	'CEBU',	'MABALA',
                'INUNU',	'FRIGO',	'MONGOBELE ETAT',	'MONGOBELE CITE',	'MONGOBELE BONDJON',	'ISAKA',	'ISAKA KIBAMBILI',	'KONKIA',	'LEBAMA',	'MABALA KASAY',	'BENDELA',	'NGIEVU',	'DUAKOMBE',	'NGOLO',	'NTSHUNI',	'IBAA',	'LOBOBI',	'NZINZI',	'SENDEKE',	'MUSHIE CITE',	'SACO',	'NDJOKELE',	'BOMPENSOLE',	'IZELI',	'BOSIKI',	'MASEKE',	'IBOLE',	'NSENU',	'ISALI',	'KENTALE',	'BOBALA',	'MBALI',	'VANI',	'BOLEBE',	'IKILI',	'MPEE',	'BISENGO',	'BOKALA',	'NGAMBOMI',	'MUTSHUETO',	'MENKWO',	'BUKUSU',	'MASIAKWA',	'MEKO',	'LIKANDA',	'MPOLI',	'ITUBI',	'CAMP BANKU',	'ENDALA',	'BONZONGO',	'MONTSUNDI',	'MOBUTU',	'BOYAMBOLO',	'MANKANZA',	'NDWA BATENDE',	'BOTANANKASA',	'MOSENO',	'BODZO',	'MBOMO',	'TSHUMA',	'MOMPULENGE',	'TSHUMBIRI',	'NDWA BATEKE',	'NKOO',	'ETEBE',	'MBEE',	'MANTUKA',	'EMBU',	'BIANGALA',	'OSAMOKOLO',	'LEDIBA',	'MOKELE',	'LEBO',	'KIZEFO',	'MASAMUNA',	'KINZENGA',	'MAYOYO',	'KIALU MIKUNZI',	'KIWAWA',	'NZOMBI',	'KINDINGA',	'BIBAMBA',	'KIMBODILA',	'KITSAMANGA',	'YOSHI',	'MUDINGONGO',	'LUMBI',	'LUNGA',	'LUKULA',	'BIMBEMBO',	'KANGAMIESI',	'BIBODI',	'KIFUNGA',	'MANGAI STE FAMILLE',	'MANGAI KIMBANGUISTE',	'NGULUNGU',	'BANSION',	'KINTSHWA',	'KASANGUNDA',	'MUKOKO',	'LAKAS',	'LABA IMPINI',	'KOREAMA',	'MANGAI II',	'MANGAI ETAT',	'MANGAI PAROISSE',	'DIBAYA PAROISSE',	'KIMVOLO',	'INONGO',	'WENZE',	'ETAC',	'MWANGA DIBAYA',	'OTT',	'KANZOMBI CFMC',	'KANZOMBI ETAT',	'KIBANGU',	'SACRE COEUR',	'MASAMBA I',	'MARCHE III',	'SABUKA',	'CBCO',	'LUNIA',	'PLATEAU I',	'MATERNITE PLATEAU',	'LUKOLELA',	'BONGISA',	'SAINT FRANCOIS',	'NZINDA II',	'NZINDA I',	'NZINDA III',	'SAINTE MARIE',	'KILOKOKO',	'SILWANU',	'PONT KWILU',	'MWANDEKE',	'CAMP BIKOBO',	'MASAMBA II',	'LUZOLO',	'KIMBINGA',	'BIPANGU',	'KINDUNDU',	'LOUIS PALAZZOLO',	'ZANGA',	'KISHIONGO',	'SAMBA',	'KWENGE KIMAFU',	'KWENGE PLC',	'DANDA',	'MOSENGE',	'BUMBA PUTA',	'KIPUKA',	'KASOMA',	'BUMBA KATOTO',	'MVUNDA',	'KISALA KAFUMBA',	'MAKUNGIKA',	'SOA',	'ISEME',	'KINZAMBI',	'KIKAMBA',	'KIMPUTU NSEKE',	'TANGO GOMENA',	'TANGO MANGO',	'IMBONGO',	'KAKOY',	'KINGANGA',	'KISALA MAYOKO',	'KWANGA',	'PAGANONI',	'EKWAYELO',	'BAYELO',	'POPOMBO',	'TAKETA',	'IKALA MB',	'LUANEMA',	'WAMBIA',	'DANZER',	'NONGENZALE',	'IKALA CB',	'NKOLE ETAT',	'MAHIEU',	'ILANGA NKOLE',	'CEBU OSHWE',	'NOTRE DAME FATIMA',	'BISENGE',	'ILONGO',	'IYENGA',	'MBAMBA',	'KINGULU',	'KAZAMBA NGWANGWA',	'KASOMA',	'KIMBWALU',	'KIPUNGU',	'KINGOLA',	'KIMBI',	'KISUMBU',	'PAY',	'KIPALANKA',	'KOLA',	'MUNGULU',	'KIBETI',	'KISAMBA',	'KIMBEKELE',	'KULUNGU SIKI',	'SUNGU',	'KIKUMBI',	'MINZIMBA',	'PESHI',	'KISALA',	'KINGUNGU',	'KIBWILA',	'KINGWENDI',	'KINGOLA',	'KABANDA',	'KITUBU',	'KINZIOTO',	'MALA',	'MUTUBU',	'VWANGA',	'MANGULU',	'BINDUNGI',	'MANIAMA',	'KINGONGO',	'KIBANGU',	'MBENGA',	'KIMWELA KWATI',	'KINGUNGI',	'MOSAMBO',	'KAMBUNDI BODILA',	'IBUMBU',	'MABUNDA',	'KINZAU PUTUKANDA',	'MUKUTU',	'KINKONGO',	'KIAMFU KINZADI',	'KASANDJI',	'MBINDA-TSEKE',	'LONZO',	'MUTOMBO',	'MUYALALA',	'KITATI',	'TSAKALA-MBEWA',	'KASINSI',	'INIANGI',	'INZIOKO',	'IKIALALA',	'MUKUKULU-TSEKE',	'DURI-MPANGI',	'DINGA',	'KENGE II',	'MUTSANGA',	'MAMBENGI',	'LUSANGA',	'CITE POPO',	'SECTEUR POPO',	'KENGE MUNIUNGU',	'INGASI',	'KABANGU',	'DENGO',	'KANGWENZI',	'IMBELA',	'INTENGA',	'KIAMFU KINZADI',	'IMWELA',	'MALUNDU',	'KIMBULU',	'KABANGAMUKEU',	'KINGONZI',	'SHAMWANA',	'POMBO',	'NGOMA',	'KITANDA',	'MUKOSO',	'KAMBONDO',	'KISENDA',	'MAFISHI',	'KIKOMBO',	'FESHI',	'UTADI',	'KAHOKA',	'MAZIAMO',	'KABUNDA',	'MBUMBA',	'MUTANGU',	'MUTSUNDA',	'LOBO',	'MUMBANDA',	'MABAYA',	'SHATUNGUSHI',	'ITADI',	'TONU',	'KASOMBO',	'MUBOSO',	'KABOLO',	'MUDIKALUNGA',	'SHAMATAHU',	'NZOFU',	'KAPINIPINI',	'SHAUYANGA',	'KAMBANGU',
                'KAJIJI',	'MUTETAMI',	'TSHANGATA',	'SHAKALONGO',	'BWANAMUTOMBO',	'KAMBASENGO',	'MWENDJILA',	'MUWANDA',	'KAMBAKADIMA',	'ESENGO',	'TSHITOYO',	'LWAKHONDA',	'NGUNDU MAYALA',	'SWA YAMFU',	'MAWANGU',	'KAHUNGULA',	'NGOMBE NTUMBA',	'YAMU KILUNGA',	'MWANA UTA',	'SEFU/SWATENDA',	'MUYAMBA',	'MAZEMBE',	'YENGA',	'MWEKA KASA',	'MIHALA',	'MUKONDO',	'MUKUNDJI',	'KITENDA',	'BAMBA',	'KAZEMBE/BARINGA',	'BUKA LUSENGI',	'MULUNDU',	'KIPANZU',	'MANZENGELE',	'KINGUNDA',	'KIMBEMBO',	'BANGI',	'MADIADIA',	'KIFUKA',	'MATAMBA SOLO',	'MWANA MUYOMBO',	'MAHUANGI',	'KISHIAMA',	'ZHINABUKETE',	'MWELA MBWANDU',	'MUNGANDA',	'KIKWATI',	'DIBULU',	'NZAKIMWENA',	'NTEMO',	'KAPATA',	'KINGULU',	'NZAMBA FUANGI',	'MWAKU YALA',	'BUKA PONGI',	'KABAKA MBANGI',	'MANENGA',	'MAIGO',	'MAWANGA',	'KIBINDA',	'WAMBA LUADI',	'PELENDE',	'MUKUMBI',	'MAHANNGA',	'KAPANGA',	'MUKALAKATA',	'KIBUNDA II',	'MWININGULU',	'KASANDJI',	'KIAMA',	'KABEYA MBAMBA',	'NZAMBA',	'BUKAKALAU',	'KIALAKAMBA',	'MUKANZA',	'TAMBU TSEKE',	'MANZENGELE',	'KIBUNDA I',	'KAMBUNDI',	'KAMBANZI',	'KINGWANGALA',	'SHABENGE',	'MAZINDA',	'KAWANA',	'PANZI/MAKITA',	'TSAKALA PANZI',	'CONGO',	'KWILU',	'KAKOBOLA II',	'NYANZALE',	'BONKONKO',	'BOLEKO',	'LOKOLAMA I',	'IPAKI',	'NONGEMPELA',	'IPOPE',	'MUNZA',	'NONGETURI',	'BOMBOLE',	'BONGIMBA ETAT',	'KANGARA',	'IPAMU',	'DIBAYA PORT',	'DIBAYA ETAT',	'YUKI',	'NKOLE NKEMA',	'KIBWADU',	'DIBAYA II',	'INDOLO',	'NSONG NTOR',	'PANGU',	'NSIM BAWONGO',	'LABA CENTRAL',	'NSONG MBUDI',	'MUSENGE BAWONGO',	'MWABO',	'KIPUKU',	'BALAKA',	'KALAPEMBE',	'ITUNDA',	'BENZI',	'MANGALA NGONGO',	'BOMBI KAPOKOTO',	'KOSHIBANDA',	'MUSENGE KIMBIMBI',	'BELO MC',	'MULOPO',	'MUKOSO II',	'KIEFU',	'KANDALE',	'MASEBA',	'MBONDO KIBALE',	'KIBABA',	'MUSANGA LUBUE',	'KALOMBO',	'NGASHI MC',	'KAKHOY',	'KONDO',	'MUJIMA',	'LUHELO',	'MATONDO',	'KILEMBE ETAT',	'KIPITA',	'NGUDI',	'KINGA',	'BUNDO',	'BELO SHIMUNA',	'BAMBA',	'MATSHI',	'NGASHI DIBAYA',	'KATAMBA',	'MASUIKA',	'MADIA MADIA',	'MUVUANU',	'KALALA DIBOKO',	'ULAMBA',	'MUSEFU',	'MALENDI',	'MUKALENGA',	'MUALA NTUMBA',	'SAKAZAJI',	'NTENDE',	'SAMADIA',	'SAMBUYI',	'MBANGU',	'MUTEGENI',	'MATA',	'KATENGA',	'MUKASA',	'TULUME',	'ULONGO',	'KAMOTO',	'YAMBA YAMBA',	'KAMBALA',	'KALOMBA',	'KABEYA  LUMBU',	'MULUMBA KABUYA',	'KAMUANDU',	'MPENGE',	'BITANDA KAKUNDA',	'BITANDA TSHIENDELA',	'TSHIMBAWU',	'TSHIKULA',	'TSHIALA BENYI',	'NKUFULU',	'MBUANYA',	'KAMUINA NSAPO',	'Isangi',	' ',	'Ibanga',	'Idipo',	'Bongobongo',	' ',	'BOKU',	'MASIAMBIO',	'TWA',	'MAIMPILI',	'EMPUNU',	'MFUMUNZALE',	'SALONGO',	'NKANA',	'LOANGO  CENTRE',	'BULA',	'MBALA',	'KHAMI',	'LOANGO BENDO',	'KHELE',	'KIKADULU',	'KIOLO',	'KIKUEMBO',	'KHESA',	'KILOANGO',	'LUKUAKUA',	'LUNGA',	'MBANZA NZUNGI',	'NDUNGA',	'NTIMANSI',	'SOMBALA',	'GOMBE MATADI',	'KINKUZU',	'MANILONDE',	'NKANKA MAWETE',	'NKAZU',	'NSANDA',	'YANDA',	'KAI DUANGA',	'KINIATI',	'LOANGU LU VUNGU',	'NGANDA TSUNDI',	'TSANGA MBAMBA',	'YENZI',	'TROUPE',	'KIBAMBA',	'NTEVA',	'BANANA',	'CECO',	'KIMBALA',	'VIAZA',	'LOVO',	'YANGA DIA SONGA',	'KIMBANGUISTE',	'KIKEBA ET LOVO',	'VILA',	'SONGA',	'VUNDA NSOLE',	'MALANGA',	'KASI',	'MUKIMBUNGU',	'MBANZA NSANDA',	'MBEMBA',	'BIENGA',	'MANGEMBO',	'SUNDI LUTETE',	'SUNDI MAMBA',	'BUONGO',	'KINIANGI',	'KINSUMBU',	'KINTETE',	'MBANZA-LELE',	'MIYAMBA',	'KIBUNZI',	'KINGOMA',	'KINZOLANI',	'NGOMBE MBEYA',	'ZELA',	'KINKENSE',	'LUANGU',	'NSUNDI NTOMBO',	'YANGALA',	'KIMVANKA',	'KAI MBAKU',	'KIOBO NGOYI',	'MADUDA',	'PALANGA',	'TSANGA NGOMA',	'KIFUMA',	'NKONDO',	'KIVALA TADI',	'KINKONZI',	'DIBINDU',	'DISTRICT',	'KIDUANGA',	'KIKHOKOLO',	'MINIONZI',	'NGANDA TSUNDI',	'THOTAMA',	'YEMA',	'NGANDA MBEMBA',	'BUENDE KASAMVU',	'DIZI MISSION',	'KAYI KUIMBA',	'KAYI TSANGA',	'YEMA NTENE',	'TSANGA NORD',	'NGANDA NDINGI',	'FUNDU NZOBE',	'KHODO',	'MBATA MINSINGA',	'SEBO NZOBE',	'KIVUNDA',
                'NIOLO',	'MINVANZA 1',	'KIZU',	'LUVU',	'MIMVANZA 2',	'TUIDI',	'LUILA',	'SONA BATA',	'LANGA',	'MBOMA NZENZE',	'NOKI 2',	'NSONA NKULU',	'VILLE HAUTE',	'MILITAIRE',	'CHRIST-ROI',	'KUMBI',	'LOMA',	'NGUNGU',	'TADILA',	'ATHENEE',	'KIBENTELE',	'KINSANG',	'LUFU TOTO',	'LUVITUKU',	'MAKUTA',	'POSTE 18',	'POSTE 13',	'POSTE 24',	'TUMBA MISSION',	'TUNGUA',	'VIAZA II',	'SASI',	'BETON',	'CILU',	'DISPENSAIRE CENTRAL',	'LULU',	'LUKALA CITE',	'BANDAKANI',	'BIDI KINDAMBA',	'KINGOYI',	'KINSEMI',	'LUOZI',	'MBANZA NGOYO',	'YANGA POMPE',	'YANGA',	'NKUNDI',	'MUZANZA',	'NGANDA NKULU',	'GOMBE SUD',	'KIMPANGU',	'KINLOMBO II',	'KIVALA',	'KONZO KIMPAN',	'LUVAKA',	'MBANZA MBATA',	'MPANGA',	'NGONGO',	'NKIENDE',	'SAVA',	'POSTE 19',	'CITE NSAMBU',	'KIMALUNDU',	'KIMBUBA',	'KIVANDABA',	'BOKO',	'DILA',	'KIASIKOLO',	'KIBUENZE',	'KIMAZA',	'KINGANGA',	'KINZUNDU',	'MBENGUA',	'MBANZA NSUNDI',	'MAWUNZI',	'LOVO',	'LUIDI',	'KOLO TAVA',	'NKOLO MISSION',	'KOLO KIDEZO',	'NDEMBO',	'CITE SELE',	'NSUMBA',	'KIVULU',	'NTAMPA',	'MASA',	'MAWETE',	'KIFUMA',	'KITSAKU',	'SEKE - BANZA',	'KILENGI',	'KINZAU  A',	'KINZAU  B',	'KINZAU  C',	'LUTALA-MBEKO',	'NKUKUTU',	'KIBUSU',	'LOLO NDAMVU',	'MBATA SIALA',	'MBENZA MUANDA',	'SUMBI',	'NDIMBA LOANGO',	'TEMBA',	'TIBU',	'KANGU',	'KUNGU MBAMBI',	'MBATA MBENGE',	'MLUNDU',	'NSIONI 1',	'NSIONI 2',	'KIMBANZA',	'MUANDA C',	'MUANDA A',	'MUANDA B',	'NSIAMFUMU',	'MALEKESE',	'KITONA VILLAGE',	'MAKASAMBA',	'YEMA',	'CSR TUMBA CITE',	'LUNGUANA',	'TUZOLANA',	'MAYENGA',	'BAKI VILLE',	'CAMP PERMANENT',	'WEKA',	'KINKONI',	'NGOMINA',	'MADIMBA',	'KAVUAYA',	'KIKONKA',	'NKANDU',	'NGEBA',	'LEMFU',	'KIPASA',	'KINTANU 1',	'KINTANU 2',	'KIMPEMBA',	'NGIDINGA',	'KIMPONGO',	'Kindompolo',	'SADI',	'MALELE',	'KINDONGO',	'LUNGI',	'MASIKILA',	'KINYENGO',	'ZOMFI',	'KINDUNDU',	'KINKUMBA',	'KINKOSI',	'KINZALA',	'KINZAU',	'NSONGO LUAFU',	'NSELO',	'MPESE',	'KIBAMBI',	'KILALU',	'NDEMBO',	'NSONA LEMBA',	'KIVUKA',	'AS KIMVUNZA',	'AS VANGA',	'AS KINDAMVU',	'AS VUNDA',	'AS SANZALA',	'MAYANGA',	'MBANZA NGOMBE',	'KINZOLANI',	'NTANDU',	'KINGANGA',	'MBANZA NKAZI',	'AS NZADI KONGO',	'AS KUIDI',	'Bangunza',	'Kai Mvemba',	'Khuvi Matanga',	'Kimbianga',	'Kisundi 1',	'Kisundi 2',	'Kinzinzi',	'Makungu Lengi',	'Mbambi',	'Mbata Lungu',	'Mfuiki',	'Mvuangu',	'Ngandu',	'Patu',	'Vungu Sabu',	'TSUNZA',	'KISOMA',	'NGASA',	'MBEMBELE',	'KIMVULA',	'LUBISI',	'IPONGI',	'IYIMBI',	'KINGUNZI',	'KALALA',	'KABAMA',	'KINGANGULA',	'MUTOMBO YAMFU',	'TSAKA',	'LULA LUMENE',	'KINKOSI BEN',	'MUTAY',	'KIVUNDA',	'MUKILA NDONDO',	'MPUTU',	'Kikimi',	'Hygiene B',	'Ngadi',	'Militaire',	'LUFU GARE',	'AS INGA',	'NSONA MPANGU',	'NGOMBE',	'MANTEKE',	'AS NSANDA',	'Mbuzi Mongo',	' ',	'AS MVUZI BUMBA',	'NKENGE',	'Mvuzi',	'Soyo-Luadi',	'Mposo',	'Hygiene A',	'Ndimba Antene',	'Salongo',	'NKAMUNA',	'LUANIKA',	'NDUIZI',	'PALABALA',	'AS KANZI',	'Ngomuila',	'Buanionzi',	'Kalamu',	'Bunzi',	'Kiveve',	'Seka Mbote',	'Rond Point',	'AS MVULA',	'AS KIONZO',	'KIZULU-NSANZI',	'AS MAO',	'Sinai',	'AS TSHUMBA',	'AS SEKE DI MANZADI',	'Lukula',	'Boma Ville',	'Kimbangu/B',	'AS LOVO',	'Kimbangu/A',	'AS KM8',	' ',	'Kitembe',	'Bukomu',	'Magherya',	'Lukanga',	'Ikuvula',	'Kitsuku',	'Rwese',	'Baraka',	'Kirikiri',	'Mulo',	'Kasima',	'Lubero',	'Masumo',	'Mabambi',	'Mukongo',	'Vughalihya',	'Vusayi',	'Lombi',	' ',	'Bamaria',	'Sukisa',	'Makala',	'Ecz',	'Yeme',	'Malikuta',	'Triangle',	' ',	'Lobi',	'Rive Gauche',	'Koteli',	'Mgbatala',	'Rubi',	'Bale',	'Yema',	'Bomea',	'Mobenge',	'Maselebende',	'Ngume',	'Popoka',	'Kumu',	' ',	'Agameto',	'Melume',	'Leluga',	'Malingwia',	'Gasende',
                'Andoma',	'Mbenge',	'Zobia',	'Titule1',	'Titule2',	'Gbantana',	'Ngbandea',	'Lebo',	'Assa',	'Makpoyo',	'Ebale',	' ',	' ',	' ',	'Molambi',	'Ganga',	'Yasa',	'Madodwo',	'Bayule',	'Disolo',	'Api',	'Digba',	' ',	'Baepulu',	'Mboti',	'Dambia',	'Mbibili',	'Mqwale',	'Dingila',	'Bambesa',	'Mongbaya',	'Mbabi',	'Mangindanginda',	'Andea',	'Ahaupa',	'Bonzengo',	'Pesana',	'Dulia',	'Nambwa',	'Mobenge',	'Mopendu',	'Ngbongade',	'Wela',	'Kulu',	'Muma',	'Bombogolo',	'Mabangu',	'Ngoy',	'Kilomni',	'Kasenga Etat',	'Mulongwe',	'Tanganyika',	'Kimanga',	'Nyamianda',	'Kalundu Etat',	'Catulundu Catholique',	'Kigongo',	'Kabimba',	'Makobola',	'Kabondozi',	'Iamba Makobola II',	'Munene',	'Swima',	'Ake',	'Abeka',	'Lweba',	'Bitobolo',	'Mukolwe',	'Lusenda',	'Kenya',	'Kabumbe',	'Nundu',	'Mboko',	'Bambay',	'Mutchaliko',	'Ongoka',	'Masiri',	'Matumaini',	'Litchomoya',	'Bavili',	'Lokani',	'Utiolio',	'Batiezue',	'MANDOMBE',	'Itondo',	'Bimbi',	'Mayunga',	'Manyanga',	'Botamba',	'Bolongo',	'Lobengo',	'Bosoasuka',	'Boyeka',	'Ikanza',	'Malele',	'Limbila',	'Ngendu',	'Paris',	'Konongo',	'Bolombo',	'Mampoko',	'KILENDA',	'YIMBI',	'KINKOKO',	'KIVUANGI',	'KIPAKO',	'KINZAMBI',	'LUKUNGA',	'KITUNDULU',	'NSATA',	'KIMUISI',	'Bwatsinge',	'Alimbongo',	'Bunyatenge',	'Kalimba',	'Kitsombiro',	'Ndoluma',	'Check Buyinga',	'Tongo',	'Kingi Buruha',	'Kashebere',	'Kausa',	'Matanda',	'Murambi',	'Kabizo',	'Birambizo',	'Mushababwe',	'Kamina',	'Rusekera',	'Rwindi',	'Kizimba',	'Ngoholo',	'Bishusha',	'Katale',	'Kabaya',	'Kazuba',	'Shangi',	' ',	'Rushovu',	'Matebe',	'Matebe',	'Bunagana',	'Rutsiro',	'Buyinga',	' ',	'Midede',	'Mabuo',	'Check Ombole',	'Check Bandulu',	'Check Malunguma',	'Butumbe',	'Kailenge',	'Besse',	'Lukala',	'Lwama',	'Bukonde',	'Lukweti',	'Rungo',	'Robe',	'Mutongo',	'Kibati',	'Misau',	'Nkimba',	'Tulizeni',	'Nyamalere',	'Kalonge',	'Birundele',	'Luofo',	'Busekera',	'Mriki',	'Kamango',	'Kahondo',	'Luanoli',	'MOHELI',	'MBULI',	'IYEMBE MONENE',	'BOKONGA',	'IKOKO BONGINDA',	'MAANGA',	'BIKORO',	'IYEMBE MOKE',	'MOKILI',	'NGELO MONZOI',	'BOTENDE',	'MOOTO',	'NKAKE',	'MAITA',	'NKALAMBA',	'BOBALA',	'PENZELE',	'MAINZENZE',	'IKENGO',	'ESOBE LIBULU',	'MPOMBO',	'IYONDA',	'WENDJI SECLI',	'BONGONDE',	'BONSOLE LOFOSOLA',	'IKENGELENGE',	'BALAKO',	'TELECOM',	'ITURI',	'BOSOMBA',	'LOSANGANYA',	'IPEKO',	'NGASHI',	'MAMA WA ELIKYA',	'LIBIKI',	'MAMBENGA 1',	'MOTEMBA PEMBE',	'BASOKO',	'Catholique',	'WIDJIFAKE',	'BOLAKA',	'DJOMBO',	'BAMANYA',	'BONSOLE RIVE',	'BOLENGE',	'WANGATA',	'DE LA RIVE',	'ARTISANAL',	'DE LA VILLE',	'MOTONGAMBALI',	'MAMBENGA 2',	'LIBAYA',	'BONDO',	'RUKI 2',	'INDJOLO',	'FLEUVE NSANGA',	'RUKI 1',	'LOKONGO',	'BOSOLO',	'BONDONGO',	'IBOKO',	'BUTELA',	'WENGA',	'LOPANZO',	'LOONGO',	'IKENGE',	'MPANGI',	'BOKONGO',	'LOONDO',	'ITIPO',	'MAPEKE',	'BUKONDO BUNA',	'IKOKO IMPENGE',	'LOKANGA',	'BUTULU KINSELE',	'PONT-KWANGO',	'MATELE',	'KINKOSI',	'FADIAKA',	'KIMANGUNU',	'KISIA',	'BITADI-LUASA',	'BUKANGA-LONZO',	'TAKUNDI',	'KINGAMAKUNI',	'KIMBATA TUDI',	'MAYINDA',	'NSUNDI',	'MANKUSU',	'KINGATOKO',	'KINGANA',	'KILOSO',	'MARIAL',	'NSANDA',	'BANNA',	'BINANGA',	'YONGO',	'MAKUNGA',	'KIMPAKASA',	'Kabuba',	'Bikindwe',	'Nduko',	'Ivatama',	'Katolo',	'Vusa',	'Ngoma',	'Vusamba',	'Bunyaka',	'Baraka',	'Bibogobogo',	'Buma',	'Dine',	'Bwala',	'Fizi',	'Kafulo',	'Kalundja',	'Kananda',	'Kandali',	'Katanga',	'Katenga',	'Kichula',	'Kikonde',	'Kilisha',	'Kizimia',	'Lumanya',	'Malinde',	'Mshimbakye',
                'Mukera',	'Mwangaza',	'Mwayenga',	'Nemba',	'Rubana',	'Sebele',	'Simbi',	'Some',	'Talama',	'Umoja',	'Yungu',	'Kanune',	'Mambowa',	'Mashuta',	'Bukumbirwa',	'Rusamambu',	'Munsanga',	'Luseke',	'Bingi',	'Kaseghe',	'Lubango',	'Anuarite',	'Mambowa',	'Masayi',	'Maeba',	'Musay',	'Katanga',	'Somea',	'Masingi',	'Kiragho',	'Kaheku',	'Biambwe',	'Mateto',	'Kirima',	'Musenge',	'Masoya',	'Mushebere',	'Soleniama',	'Kambau',	'Liboyo',	'Mbungwe',	'Mutendero',	'Lulinda',	'Isonga',	'Kibwe',	'Kighali',	'Vuhovi',	'Kitolu',	'Kyavinyonge',	'Vusorongi',	'Kyangendi',	'Kimbulu',	'Bweteta',	'Bughumirya',	'Nyabili',	'Kitsimba',	'Kashugo',	'Kakonze',	'Kagheri',	'Kisaka',	'Kasalaka',	'Vunyakondomi',	' ',	'Bulinda',	'Kikuvo',	'Kasando',	'Butsiri',	'Kamandi',	'Nyamindo',	'Vuvogho',	'Singamwambe',	'Mighobwe',	'Kayna',	'Kirumba',	'Kanyabayonga',	'Vitshumbi',	'Cepromi',	'Bulindi',	'Kibingo',	'Kashalira',	'Nyakakoma',	'Nyamilima',	'Buramba',	'Nyakahanga',	'Nyabanira',	'St Benoit',	'Yopa',	'Kichanga',	'Burungu',	'Kahe',	'Shinda',	'Nyarukwangara',	'Karambi',	'Rubavu',	'Tshengerero',	'Kabonero',	'Bugusa',	'Tanda',	'Rwanguba Kabindi',	'Rugari',	'Kakomero',	'Kinyandonyi',	'Kibutu',	'Umoja',	'Kiwanja',	'Buturande',	'Mabungo',	'Murambi',	'Mapendo',	'Rutshuru',	'Rubare',	'Kalengera',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	'Mudja',	'Buhumba',	'Kiziba',	'Mugunga',	'Baraka',	'Hebron',	'Ndosho',	'Mungano Resurrection',	'Albert Barthel',	'Lubanjo',	'Majengo',	'Bujovu',	'Rapha',	'Virunga',	'Katoyi',	'Amani',	'Mabanga',	'Murara',	'Kahembe',	'Kasika',	'Muungano SolidaritÃ©',	'Buhimba',	'CCLK',	'Keshero',	'Umoja',	'Himbi',	'Carmel',	'Katindo',	'Heal Africa',	'CASOP',	'Mapendo',	'Bweremana',	'Kirotshe',	'Sake',	'Kasuka',	'Lwibo',	'Kibua',	'Kishanga',	'Mushumbi',	'Limasa',	'Ngusua',	'Gbossa',	'Sanga',	'Ngalo',	'Mission',	'Simbala',	'Fulu',	'Maniko',	'Nwenenge',	'Sokoro',	'Katakoli',	'Zamba',	'Bassa',	'Vote',	'Satena',	'Mobayi',	'Nyaki',	'Mbui',	'Gbagabu',	'Sowa',	'Gbadogboketsa',	'Tongu',	'Gomba',	'Biasu',	'CitÃ©',	'Gbagi',	'Kanza',	'Loanga',	'Ekoto',	'Ikau',	'Ilodge(Ifomi)',	'Balangala',	'Bokolongo',	'Monzonzo',	'Lofoma (pilote)',	'Lifumba',	'Bokele',	'Waka',	'Bokeka',	'Bolimi toenga',	'Boyela',	'Bolombo mengi',	'Ndeke',	'Lilangi',	'Nsongo nkoy',	'Nsongo Ilinga',	'Lisafa',	'Bongilima',	'Bokala',	'Bafumba',	'Bokakata',	'Boboto',	'Kimbangu',	'Isampoka (Elikia)',	'Nkoko I',	'Salongo',	'St martyr',	'St therese',	'Kalemba',	'Tshiela',	'Tshikaji',	'Mbumba',	'Ntambue',	'Tshisenga',	'Katumba',	'Kalamba Mbuji',	'Kangambo secteur',	'Kasombo bishi',	'Makonde',	'Luambo',	'Kambongo',	'Ndolo',	'Minkolo',	'Muangala Ngoma',	'Kavueta',	'Lumpungu',	'Biaboko',	'Muzodi',	'Kangambo baka',	'Lueta',	'Mutenge',	'Ngovo',	'Tshikuni',	'Muanda Kalendu',	'Mbunze',	'Shakufwa',	'Mwamushiko',	'Kahemba',	'Sukisa Mobutu',	'Lutshima du Conseil',	'Muloshi',	'Kamabanga Lwapanga',	'Shamusenge',	'Ngwiya',	'Tshitambi',	'Bumba',	'Kambwela',	'Mwasenge',	'Tshiweka',	'Bangu',	'Shakungu',	'Shamalenge',	'Kamba Lwanzo',	'Kunganene',	'Kanuma',	'Tshifameso',	'Kabongo',	'Kamayala',	'Kabama',	'Kasasa',	'Napasa',	'Shamukwale',	'Bindu',	'MWAKATENDE',	'Katcha Mbuyu Kabange',	'Sambo',	'Katamba Kaboko',	'Malala',	'Kanteba',	'Nkanda',	'Kilembwe',	'Makena',	'Kilulwe',	'Kalole',	'Kibondwe',	'Lenge',	'Kahongo',	'Mbwele',	'Kaongo',	'Ngalula',	'Mpala',	'Nkuba',	'Mwindi',	'Kasokota',	'Lungulungu',	'Mwanza',	'Lambo',	'Kabwela',	'Kansabala',	'Mazonde',	'Malibu',
                'AS HGR',	'KATCHA MBUYU LL',	'KIZYUKI',	'KAULU MUNONO',	'Kiya',	'Kambi',	'Kivwa',	'ILUNGA NGOY',	'KAKAMBA',	'MUYUMBA 3',	'KATENGO',	'Kayombo',	'Kibao',	'MUYUMBA PORT',	'Kiluba',	'LUVWA',	'Mukomwenze',	'Kabimba',	'Bilila',	'Mtoa',	'Taba congo',	'Lubuye',	'Kituku',	'Undugu',	'Kyoko',	'Tundwa',	'Lukombe',	'Muleka',	'Lambo  Katenga',	'Lambo kilela',	'Mahila',	'Kabanga',	'Mulolwa',	'Kazumba',	'Wimbi',	'Rugumba',	'Kitoke',	'Kisongo',	'Makutano',	'Kasawa',	'Yenga',	'Ponda',	'Kateba',	'Kilenge',	'Buyovu',	'Kayanza',	'Kayenge',	'Kundu',	'Mpala',	'Bigobo',	'Mbulula',	'Ilunga',	'Nonge',	'Nyanga',	'Mwana Ngoy',	'Tambwe',	'Nkulula',	'Kahenga',	'Kabundi',	'Lubunda',	'Keba',	'Misisi',	'Masambi',	'Mugizya',	'Maria mama',	'Sola',	'Katele',	'Kalenga May',	'Ville',	'Kangoy',	'Kandolo',	'Mutakuya',	'Mukoko',	'Mukuma',	'Kabonzo',	'Lwaba',	'Soswa',	'Mambwe',	'Kabunda',	'Zongwe',	'Butondo',	'Lengwe',	'Kahinda',	'Mbeya',	'Lwizi',	'Mulongo',	'Masamba',	'Mangala',	'Tshangatshanga',	'Ngoy',	'Ngombe',	'Muhuya',	'Kanunu',	'Kabeyamayi',	'Sulumba',	'Kabeyamukena',	'Kilunga',	'Kampulu',	'Mukundi',	'Kankwala',	'Kitengetenge',	'Kalima',	'Kisengo',	'Makumbo',	'Mulimi',	'Kadima',	'Kitule',	'Kibula',	'Kihanga',	'Kashale',	'Mpongo',	'Lukundula',	'Kasu',	'Kasinge',	'Kamubangwa',	'Lwala',	'Muchungaji Mwema',	'katibili',	'Kimena',	'Katombo',	'Mpemba',	'Mulembwe',	'Mutakuya',	'Clinique',	'Kataki',	'Lutherien',	'Hewa Bora',	'Mulange',	'Tembwe',	'Fatuma',	'Katondo',	'Mai Baridi',	'Nyemba',	'Kiluba',	'HGR',	'Kifungo',	'Kasanga Nyemba',	'Muswaki',	'Lwanika',	'Makala',	'Kawama',	'Bwanakutcha',	'Kambu',	'LWAKATO',	'SHINDANO',	'Kabombo',	'Mukebo',	'Kabeke',	'Nsange',	'Mbayo',	'Kitentu',	'Mwenge',	'Kiambi',	'Kazingu',	'Kayumba',	'Mpiana',	'NZYONDO',	'LUBA',	'KATOLO',	'Muzovoy',	'Mutombo',	'Mbayo',	'Kyala',	'Ngongwe',	'Kisiko',	'Kyofwe',	'BUNDALA',	'TWITE',	'PANDA KUBOKO',	'KMINA LENGE',	'St JOSEPH',	'Kilengalele',	'Kanda',	'Kitanda',	'Kalenge',	'Ngwena May',	'Katutu',	'Kabanda',	'Kimungu',	'Kalolo',	'Kasumpa',	'Kamalenge',	'Kaye',	'Ngwena Gare',	'Kilambi',	'Kaseya',	'Mankoto',	'Mulonga',	'Kakuyu',	'Bena hamba',	'Pofu',	'Kilae',	'Kabwe',	'Kasheke',	'Katea',	'Loni Katenta',	'Matenta',	'Kilembi',	'Fube',	'Kirungu',	'Musosa',	'Mwange',	'Moliro',	'Livua',	'Kapote',	'Kiku',	'Pepa',	'Kipiri',	'Kampapa',	'Kizike',	'Lyapenda',	'Kasenga',	'Lumono',	'Liombe',	'Mulonde',	'Mutambala',	'Mulunguzi',	'Regeza',	'Moba Port',	'Kasama',	'Kapakwe',	'Kansenge',	'Mutonwa',	'Kayabala',	'Kampela',	'Kamena',	'Akwele',	' ',	'KITHEVYA',	'BUNZUMU',	'MABASELE',	'KAKUTAMA',	'MAMBAU',	'MAMOVE',	'APETINA',	'MALEKI',	'PAKANZA',	'MASOSI',	'MUSUKU',	'PASOLA',	'LIVA',	'TENAMBO',	'TOTOLITO',	'MBAU',	'MAMBABEKA',	'MAMBABIO',	'KOKOLA',	'ERINGETI',	'LUBIRIHA',	'KASANGA',	'KANGAHUKA',	'LOULO',	'KABALWA',	'MWENDA',	'KENEHAMBAORE',	'NZENGA',	'KALEMBO',	'MURAMBA',	'BULONGO',	'MANZANGA',	'KUDI 3',	'KITOKOLI',	'MASAMBO',	'RUGETSI',	'LUME',	'ALOYA',	'NGAZI',	'VUSAYIRO',	'BINGO',	'MANGODOMU',	'MABALAKO',	'LINZO',	'NGOYO',	'MANGINA',	'MUNUNZE',	'METAL',	'Kilueka',	'Kiansungua',	'Lukunga',	'Kizulu',	'Lufu-Nzola',	'Kisonga',	'Lombe',	'Songololo',	'Minkelo',	'Mbangu',	'Bolenge',	'Lingunda',	'Bolima',	'Djoa',	'Boso mbifa',	'Boso Djafo',	'Ligbalo',	'Bonyeka',	'Boso Isongo',	'Bolomba likolo',	'Yuli',	'Boso semodja',	'Bombimba',	'Bogbonga',
                'Boso likala',	'Boyenge',	'Monzambi',	'Libanga',	'Boso lombo',	'Wele',	'Belonga',	'Ikoli',	'Itotela',	'Djonori',	'Diwoko',	'Mbaka',	'Yombo',	'Tshodi',	'Kongoo',	'Onema Ototo',	'Nyama Lowo',	'Lodi Bangi',	'Ekolo',	'Okako nyombe',	'Shele',	'Ngembe',	'Okeke',	'Ngomo Lodi',	'Hotokodi',	'Dolo',	'Onema Lotane',	'Bomenge',	'Boso mondomba',	'Boso Nzala',	'Boso sebe',	'WANGATA',	'BAKANDJA',	'BOTEKA',	'BEMPUMBA',	'MPAKU',	'IKENGE',	'LOONGA',	'BOKAMBANGOMBE',	'BOKUMA',	'BOALANGOMBE',	'BATSINA LIFUMBA',	'BATSINA BAKAALA',	'LIFUMBA DJOLONGO',	'BOENDE ETOO',	'INCONNUE',	'MAKAKO',	'BOKATOLA',	'BONTOLE',	'LOSENGE',	'LOTUMBE',	'BOFANDJUA',	'WAKA',	'LOSAKO',	'BETSIMBOLA',	'IFOKU',	'EUNGU',	'IMBONGA',	'BESOMBO',	'BOLENA',	'BOYERA',	'NKASA',	'INGANDA',	'MOKOMU',	'BEFILI',	'BELONDO',	'BOKALA',	'MBALANKOLE',	'BOSSA',	'Bokote',	'Ilenga',	'Belolo',	'Bokolomongo',	'Bolanda',	'Bongale',	'Monieka',	'Bongila',	'Bokenyola',	'Penzele',	'Bokolongo',	'Bekungu',	'Bikondo',	'Bongazi',	'Buburu',	'Malanga',	'Moluka',	'Ngwanza',	'Mokolo',	'Bokondo',	'Iwondo',	'Bongenye',	'Ngondo',	'Boboke',	'Bomongo',	'Bomana',	'Bolebo',	'Bosobele',	'Lindika',	'BOBANGI',	'Popo kabaka',	'DJILI',	'MOLUMBU',	'LILANGA',	'Mobena',	'BOBANGA',	'LOKOLO MOKO',	'NDJONDO NGIRI',	'IPOMBO',	'Bokolomwaki',	'Mpoka',	'ILAMBASSA',	'SALONGO',	'Bosango',	'Ntondo',	'Mikaya',	'Ngombe',	'Botuni',	'Irebu',	'Malange',	'Ntondo',	'Mpa pole',	'Nkoso 1',	'Nkoso 2',	'Nzalezkenga',	'Mabinza',	'Ikoko motaka',	'Lohenge',	'Nkolo',	'Moebe',	'Boyoka',	'Tayoka',	'Bongonda',	'Itumba',	'Ilombola',	'Takili',	'Lukolela Plantation',	'Malualumba',	'Mokula',	'Botuali',	'Ndongo Bokoko',	'Desungu',	'Lokongo',	'Mpoka',	'Mbondo',	'Nkolo Lingamba',	'Nkondi',	'Bokangamoy',	'Monkoto',	'Imomampako',	'Isaka',	'Bongili',	'Emengeye',	'Nongelokwa',	'Mpengekaboko',	'Ndjafa',	'Bekili',	'Batanga',	'Bongoy',	'CDCC',	'Lifoku',	'Marie Louise',	'Motema mosantu',	'Yokelelu',	'Monkoy',	'Momboyo',	'Yangambo',	'Efekola',	'Bongemba',	'Lingomo',	'Yalifafu',	'Wamba',	'Isanga',	'Lotulo',	' ',	'Bokela',	'Boto',	'Ndotsi',	'Efekele',	'Lokoma',	'Elinga',	'Esongo',	'Bendjali',	'Efomi',	'Lukuku II',	'Nkembe',	'Etongoto',	'Isama',	'Malela',	'Likete',	'Ngombi isongu',	'Bokondji',	'Bekomi',	'Bokutu',	'Esangani',	'Bekila',	'Bosilia',	'Etata',	'Pi bofoka',	'Pilote wema',	'Boanga',	'Ibangalakata',	'Lolungu',	'Bolafa',	'Bonsombo',	'Nkoto',	'Bosenge',	'Yasola',	'Iyanga',	'Wanga',	'Lifanga',	'Yalokoli',	'Yofaka',	'Ilili',	'Yamboyo',	' ',	'Lyambo',	'Yoote',	'Yofili',	'Lokombo',	'Bongila',	'Yaikala',	'Djolu_muke',	'Bofola',	'Yoseki',	'Wamba',	' ',	'Yanyango_mbula',	'Nsema_biamba',	'Iyema',	'Yokwa',	'Befory',	'Yayangobula',	'Yambili',	'Lolanga',	'Yolonga',	'Bomoi',	'Yalokuli',	'Cedimo',	'Yalusaka',	'Mamba',	'Yaloola',	'Samanda',	'Ikomaloki',	'Watsi',	'Ekuku',	'Yalonga 3',	'Yaloketo',	'Yalola',	'Yalonga 1',	'Yalombo',	'Boyombe',	'Lokona',	'Ene',	'Boboto',	'Bokole',	'Bulukutu',	'Liyangola II',	'Yosasa',	'Bokolo',	'Lofima',	'Bokoka',	'Iyali',	'Bokau',	'Bokaindembe',	'Lotakamela',	'Yokamba',	'Liunga',	'Elongo',	'Lomama',	'Bompongo',	'Yemo',	'Basekaokoli',	'Ikengolaka II',	'Lendisa',	'Baringa',	'Djefera',	'Ekafera',	'Ikombe',	'Lileko',	'Ilolo',	'Ikela',	'Ekembela',	'Esangani',	'Likuanduamba',	'Lilanga',	'Lifanga',	'Ikelemba',	'Cadelu',	'Mbankoumola',	'Iyali',	'Yakaa',	'Ekukola',	'Djombo',	'Nsamba',	'Eandja iyondje',	'Kimbangu',	'Bokoli',	'Lomako',	'Lifumba',	'Lofuko',
                'Befale',	'Imbo nsamba',	'Iyaliboondde',	'Boende',	'Boonia',	'Lofukya',	'Engunda',	'Bolemba',	'Ilombe',	'Bokada pombo',	'Bomanza',	'Bokada mission',	'Bombe',	'Bogose',	'Mongo mono',	'Bubanda',	'Bosolindo II',	'Goyongo',	'Bososama',	'Komenge',	'Dula',	'Kelo',	'Boso moleke',	'Capsa bolo',	'Ndubulu',	'Kwala',	'Lombo',	'Pilote bobosolo',	'Modiri',	'Bobonganza',	'Takaya',	'Boya sebego',	'Bodokola',	'Boyawaza',	'Bombura',	'Bobasonga',	'Bodulungba',	'Bogosenubea',	'Boyamalanga',	'Ngbonge',	'Boyaseganu',	'Boyasemayi',	'Bodetoa',	'Bobangala',	'Nugaza',	'Gilinga',	'Bogose konu',	'Bodolowe',	'Botelenza',	'Bozokola 2',	'Bogwabe',	'Bobutu',	'Bozokola 1',	'Bodangabo',	'Bogbagi',	'Boyazamo 2',	'Bokarawa',	'Boyazamo 1',	'Bofulafu',	'Bowozo',	'Loko',	'Gbuda',	'Bobiti',	'Movangusa',	'Monveda',	'Bopili',	'Songbolo',	'Bogboan',	'CitÃ© 1',	'Edungu',	'Bombwa',	'Nbakpo',	'Centre urbain',	'Kondo',	'CitÃ© 2',	'Boso modjebo',	'Bongonza',	'Makao',	'Monzelenge',	'Bokapo',	'Bolombo',	'Boso dua',	'Boyange Motima',	'Boso libondo',	'Bomoye',	'Ebambe',	'Masanga',	'Mbangu',	'Gumba',	'Mongili',	'Boso manzi',	'Liboko',	'Yangbondu',	'Angbonga',	'Bondunga',	'Bilia',	'Ebata',	'Yamokoto',	'Yangome',	'Yasembe',	'Deki',	'Yamooko',	'Yalikombi',	'Bokoy Mputu',	'Bozogi',	'Yakombo Nkoy',	'Yalombo Swa',	'Yambuku',	'Yambawo',	'Yanzumba',	'Yamamba',	'Bauma',	'Lilongo',	'Yambongi',	'Bonkoy Bangenza',	'Yalitonda',	'Likau',	'Mobanda',	'Monzamboli',	'Yamwenga',	'Tshimbi',	'Bongelenza',	'Bangbokpale',	'Baisa',	'Yasoku',	'Egbongo',	'Bongolu',	'Yalosemba',	'Yambomi',	'Gongo',	'Yambonzo',	'Boningo',	'Aboso',	'Bondunga',	'Boganga',	'Makoko',	'Tobongisa',	'Difongo',	'Yakpa',	'sasa',	'Efolu',	'Kpakana',	'Eganda',	'Panzaka',	'Tomibikisa',	'Dekere',	'Gatanga',	'Kule',	'Baye',	'Dengu',	'Makpulu',	'Yakapo',	'Yahila',	'Liongelo',	'Yatutia',	'Mongali',	'Kuulu',	'Yamogbumia',	'Bolama',	'Yaolema',	'Moenge',	'Mombongo Elumba',	'Yamosia',	'Yamombo',	'Bolila',	'Sokinex',	'Bafamba',	'Lokumete',	'Lisalama',	'Bandu CitÃ©',	'Lokutu',	'Bandu CollectivitÃ©',	'Toyokana',	'Yamokanda',	'Libamba',	'Ambabe',	'Bokondo',	'Yalemba',	'Bolikango',	'Liambe',	'Mambandu',	'Bumaneh',	'Yawinawina',	'Yangbongbo',	'Yaonga',	'Boulo',	'Mokeke',	'Yaolema',	'Mombongo I',	'Mombongo II',	'Yalikito',	'Hembe 1',	'Mombole',	'Bondamba',	'Yalonde',	'Bolea',	'Lobolo',	'Yaosola',	'Koret',	'Yalongwa',	'Yaloola',	'Simba',	'Lisoku',	'Yahuma',	'Lieki',	'Hembe II',	'Lifumba',	'Yalombuka',	'Ngombo',	'Bongona',	'Irema',	'Lerema Kembe',	'Lohumoko',	'Yampete',	'MC Mondombe',	'Mpona',	'Letutu Simbele',	'Lerna Yalingo',	'\'Ekili',	'Kenake',	'Losokola',	'Lieke Lesole',	'Lokilo Etat',	'Lisanga',	'Lilanga Mongo',	'Lifulututu',	'Lolenga',	'Nongo Likenge',	'Songe Yomaie',	'Opala',	'Yokoko',	'Letutu Yakuma',	'Letakero',	'Yesse',	'Yaongenda',	'Yasongo',	'Lusanganya',	'Yahila',	'Yakamba',	'Itokela',	'Yalonga',	'Yalokundola',	'Saint Nicolas',	'Yatanda',	'Yatulia',	'Yakoko',	'Yalokombe',	'Likundu',	'Yaosio',	'Lisuma',	'Yatange',	'Yambela',	'Yatolema',	'Masimango',	'Banandkale',	'Bananguma',	'Ubundu',	'Batiamoyowa',	'Batiamane',	'Basua',	'Biaro',	'Obilo',	'Bandu',	'Babusoko',	'Yaongama',	'Yainelo',	'St Casmir',	'Bambole',	'Sncc',	'Pecheur d\'hommes',	'Mako',	'Uzima',	'losoko',	'Lando',	'Batiamendje',	'Yalisombo',	'Osio 16',	'Lukusa',	'Saint AndrÃ©',	'Masengo',	'Kubagu',	'Nhenengene',	'Osio 21',	'Isange Makutano',	'Biaro',	'Likolo',	'Yaeme',	'Mokombe',	'Yauta',	'Yaokoli',	'Ekondi',	'Yaolenga',	'Monoli',	'Litho',	'Yafala',	'Yafeta',	'Wenge Haut',	'Yaolombo',	'Wenge Bas',	'Yasunga',
                'Bolongo',	'Malinda',	'Bohuma',	'Yaomanga',	'yatumbo',	'Baluola',	'Yamohambe',	'Mumba Losuna',	'Ligasa Etat',	'Logoge',	'Yabwanza',	'Ligasa Ancien',	'Yaboseo',	'Yanfira',	'Yanguba',	'Yabolonga',	'Yabetuta',	'Imbolo',	'Botumanya',	'Yafenga',	'Itenge Haut',	'Ifulu',	'Yaenisa',	'Yaboila',	'Yalisingo',	'Yaesea',	'Yalanga',	'yaotike',	'ilota',	'Yasendu',	'yaokombo',	'Yawenda',	'Yaoseko',	'Yalolia',	'Yalotcha',	'Yalokombe',	'Yalongosa',	'yakungu',	'Lotokila',	'yaosenge',	'Bolongo',	'yanonge',	'Ikongo',	'Weko',	'Yaombole',	'Lilanda',	'Lusambila',	'Ekutsu',	'Inera',	'Yaelomba',	'Lomboto',	'Yalikina',	'Yafunga',	'Yalosase',	'Yambongengo',	'Ilambi',	'Yaokasanga',	'Yayaokwamu',	'Yanfole',	'Yalosuna',	'Yabotianong',	'Loholo',	'Yasanga',	'Yabasaloba',	'Baonga',	'Ilondo',	'Madula',	'Makana',	'Salambongo',	'Bambongena',	'Uma',	'Bafwaboli',	'Logale',	'Mobi',	'Basukwambao',	'Kipokoso',	'Parizi',	'Babongomnbe',	'Azambao',	'Babingi',	'Babagulu',	'Ndrekoko',	'Makalado',	'Babule',	'Nyasi',	'Opienge',	'Angemapasa',	'Balobe',	'Basaule',	'Elonga',	'Babukabe',	'Babomongo',	'Mangarai',	'Baego',	'Belika',	'Bafwandambo',	'Umodja',	'Bafwabanga',	'Lindi',	'Bafwagali',	'Kenge',	'Bafwabalinga',	'Boyulu',	'Bafwasana',	'Bafwabenze',	'Bakoroy',	'Bambodi',	'Bafwanduo',	'Bamoko',	'Wandugu',	'Muungano',	'Zawadi',	'Bon samaritain',	'Foyer',	'Ya biso',	'Mokili',	'Mukwango',	'Kandolo',	'Bolongue',	'Gloria',	'Kibibi st luc',	'Ngenengene',	'St camille',	'Umoja',	'Tshopo I',	'Tuungane',	'St Pierre',	'Tshopo II',	'Massina',	'Kumbakisaka',	'Pumuzika',	'Bon Samari',	'lobiko',	'Makutano',	'bavatete',	'Malkia',	'Bilinga',	'Batiakoko',	'kwetu',	'Merdi',	'Kandangwa',	'Bafwakozuo',	'Bangwambi',	'Bafwaziyo',	'Foret',	'Bafwadili',	'Bafwanane',	'Bafwagbobo',	'Bafwamate',	'Bomili',	'Bafwangbe',	'Bafwaseba',	'Bavandomo',	'Bafwambongo',	'Mapaza',	'Bavabu',	'Bafwamungu',	'Kondolole',	'Kabuka',	'Tele',	'Kole',	'Zambeke',	'Bopepe',	'Dr Sharpe',	'St Elisabeth',	'Bethsaida',	'Lukelo',	'Baloma',	'Bodela',	'Dikwa',	'Bongoza',	'Akuma',	'Panga',	'Alolo',	'Motoma',	'Mangala',	'Mosanda',	'Babise',	'Mangi',	'Mambo',	'Bakobo',	'Bambwe',	'Bandombila',	'Bambane',	'Bawi',	'Bavanguma',	'Pont Lindi',	'Bengamisa Cath',	'Abulakama',	'Nyonga',	'Bangbanye',	'Banjwade',	'Lokeli',	'Bangole',	'Bayangene',	'Kapalata',	'Bobiti??',	'Yelenge',	'Yubo',	'Yaselia',	'Banyungu',	'Bogbogbo',	'Bolika',	'Yangbulu',	'Bakere',	'Monganjo',	'Bangbe Tambi',	'Basali',	'Bunga',	'Lileko',	'Yambomba',	'Yambula?',	'Foret',	'Badengaido',	'Bafwakowa',	'CECCA-16',	'Afya ya wagonjwa',	'Bafwanakengele',	'Bafwambaya',	'Juhudi',	'Bafwabango',	'Mambati',	'Bolebole',	'Bakanja',	'Tshaka',	'Ceca 16 Wamba',	'Bayenga',	'Abanagomu',	'Bindani',	'Kayenga',	'Abiba',	'Bomana',	'Bakhita',	'Betongwe',	'Asamboa',	'Agbau',	'Maboma',	'Bavemo',	'Nambose',	'Boma-Mangbetu',	'Gombe',	'Bakangi',	'Adjangwe',	'Bevieseni',	'Bavamasiya',	'Bafwabaka',	'Badamoni',	'Obongoni',	'Yamo',	'Legu',	'Adedo',	'Mataku',	'Etakamokongo',	'Bachenze',	'Ibambi CECCA 16',	'Ibambi',	'Bamoka',	'Bavamabudu',	'Babia',	'Nebobongo',	'Matibika',	'Likasi',	'Babonde',	'Gatoa',	'Fungola',	'Budubudu',	'Abiangama',	'Pawa',	'Digi',	'Gbonzunzu',	'Nagwa',	'Medje',	'Arindru',	'Egbonde',	'Nembombi',	'Makpulu',	'Nangosina',	'Neisu',	'Nduka',	'Gossama',	'Nsele',	'Nolua',	'Bunie',	'Mbene',	'Mayogo(?)',	'Tuluba',	'Gamba',	'Telalingbi',	'Tely',	'Djambe',	'Viadana-Kobokobo',	'Akpudu',	'Manziada',	'Neru',	'Nagbo-Teli',	'Nalamu',	'Lokando',	'Nawiwi',	'Mbana',	'Vungba',
                'Limba',	'Mazulu',	'Diaba',	'vube',	'Nambunga',	'Nekalagba',	'Rungu',	'Kabome',	'Nangazizi',	'Nesira',	'Nepomeda',	'Nala',	'Bala',	'Bodjo',	'Badolo',	'Ngabi',	'Kpetele',	'Masombo',	'Gangala',	'Doruma',	'Naparka',	'Diebo',	'Bangadi',	'Diagbe',	'Napopo',	'Kana',	'Weneki',	'Ngilima',	'Kapili',	'Galagala',	'Ganga',	'Wamba Moke',	'Babagu',	'Arikaze',	'Makilingbo',	'Nangbama',	'Ndingba',	'Limpopo',	'Ligunza',	'Ekibondo',	'Wawe',	'Nambia',	'Tapili',	'Mangala',	'Mangalu',	'Bitima',	'Duru',	'Nango',	'Kosa',	'Sambia',	'Bamokand',	'Moussa',	'Mangese',	'Li-Pay',	'Wandote',	'Afu',	'Kpekpele',	'Ndedu',	'Mbadainga',	'Bakote',	'Biodi',	'Dungu Uye',	'Dungu May',	'P.Nat, de Garamba',	'Li-Uye',	'Kiliwa',	'Tora',	'Goria',	'Wanga',	'Madja ?',	'Ngazizi',	'Gombari',	'Tibodri',	'Abakudu',	'Apoko',	'Baitebi',	'Bakiri',	'Nepoko',	'Akpandau',	'Tangi',	'Bakaeku kenya',	'Molokay',	'Salate',	'Malembi',	'Epulu',	'Bongwupanda',	'Bandisende',	'Pede',	'Banana',	'Makoko 2',	'Tobola',	'Binase',	'Mambasa',	'Salama',	'Bukulani',	'Akokora',	'Nduye',	'Lwemba',	'Alima',	'Biakato-mine',	'Biakato-mayi',	'Katanga',	'Mandima',	'Mayuano',	'Teturi',	'Some',	'bella',	'Baiti',	'Ngubo',	'Makeke',	'Machebe',	'Lukaya',	'Bandiboli',	'Komanda',	'Beyi',	'Pinzili',	'Samboko',	'Luna',	'Katabey',	'Ndalya',	'Bwanasura',	'Idohu',	'Ofay',	'Mangusu',	'Bamande',	'Mandibe',	'Boga',	'Kyabhowe',	'Rubingo',	'Mugwanga',	'Zunguluka',	'Bikima',	'Burasi',	'Tondoli',	'Bwakadi',	'Tshabi',	'KAINAMA',	'Kagoro',	'Kagaba',	'Gety Etat',	'Aveba',	'Maga',	'Bukiringi',	'Bilima',	'Tchekele',	'Olongba',	'Nombe',	'Soke',	'Zitono',	'Isura',	'Kinyombaya',	'Mangiva',	'Tekele',	'Sota',	'Basunu',	'Marabo',	'Irumu',	'Kombokabo',	'Badiya',	'Tumbiabo',	'Ngbulanzabo',	'Birinyima',	'Nyankunde',	'Singo',	'Songolo',	'Balazana',	'Bahiana',	'Bogoro',	'Dele',	'Hoho',	'Kabarole',	'Kunda',	'Lengabo',	'Mwanga',	'Ntoma',	'Rwampara',	'Shari',	'Walu',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	' ',	'Yedi',	'Abelkozo',	'Ceca 20',	'Ituri',	'Pluto',	'Mongbwalu',	'Lodjo',	'Ngamau',	'Andisa',	'Sayo',	'Foret',	'Moku',	'Monama',	'Dilolo',	'Ngagazo',	'Dubele',	'Arumbi',	'Maitulu',	'Maba',	'Kokoro',	'Gatanga',	'Monya',	'Gambula',	'Toyota',	'Durba',	'Bethanie',	'Doko',	'Tandro',	'Sabuni',	'Djabir',	'Doya',	'Kurukwata',	' ',	'Koreri',	'Faradje CECA 20',	'Katanga?',	'Obii???',	'Kpodo',	'Tadu',	'Akua',	'Tadu Ceca 20',	'Nzopi',	'Sesenge',	'Tomati',	'Todro',	'Atadra',	'Kitambala',	'Baki',	'Massabe',	'Dramba',	'Tayo',	'Ataki',	'Kurukwata',	'Kamirhu',	'Aba',	'Nyalanya',	'Nyari',	'Lagabe',	'Bele',	'Garamba Parc',	'Lanza',	'Ndolomo',	'Bovi',	'Makoro',	'Ambarau',	'Abinva',	'Kamiro',	'Kiraka',	'Mariaba',	'Kilima',	'Kana',	'Ngili',	'Bhamo',	'Rangu',	'Maolo',	'Gaki',	'Etukaliri',	'Rikazu',	'Adi',	'Kanda',	'Drobukolo',	'Kumuru',	'Liku',	'Azu',	'Rumu',	'Agura',	'Ingbokolo',	'Gbondoko',	'Utru',	'Koloa',	'Midhu',	'Rodo',	'Iri',	'Loliga',	'Angalo',	'Mado',	'Laybo',	'Aloga',	'Didi',	'Tsinzi',	'Yangambi',	'konga',	'Langa?',	'Aubha',	'Azigi',	'Tadiri?',	'AYIFORO',	'PABIRI',	'NDERI',	'DONZU',	'ABEDJU',
                'ROGALE',	'TITI',	'ARIWARA',	'GOBIRI',	'APAA',	'KUKU',	'OMBAYI',	'OVUTSIRI',	'ANGIRIA',	'OVOA',	'ESSOKO',	'DEMA',	'KIKIA',	'EDIPI',	'WITSIRI',	'LEA',	'OMUNDATSI',	'Rau',	'Adhobea',	'Kayi',	'Atsinia',	'Yekia',	'Apinaka',	'Ombatale',	'Adua',	'Odroaze',	'Nono',	'Yetsu',	'Angonda',	'Laro',	'Abuguru',	'Abhava',	'Poni',	'Ekanga',	'Odranyi',	'Kumudhu',	'Yaba',	'Araba',	'Rodo',	'Alibha',	'Malinga',	'Eru Yofenyiri',	'Leri',	'Yebifu Ediofe',	'Ania',	'Oronzi',	'Ongoyi',	'Abiridio',	'Aru CitÃ©',	'Ayiko',	'Ondolea',	'Essebi',	'Ossada',	'Obitabo',	'Kandoy',	'Tururmu',	'Bholi',	'Rungu',	'Ngbeku',	'Ovison',	'Adranga',	'Dhuadhua',	'Kerekere',	'Azumba',	'Kumbuku',	'Sarasara',	'Mont Meyo',	'Biringi',	'Ngbiki',	'Wadaka',	'Ahologo',	'Alla Tukpa',	'Alotho',	'Anyara',	'Aterlembe',	'Avari',	'Djalasiga',	'Kusu',	'Ndama Centre',	'Mont Zeu',	'Luma',	'Yilo',	'Zani',	'Djaliga',	'Avu Vumba',	'Audha',	'Ameri',	'kaduma',	'Damas',	'Berunda',	'Ngazba',	'Dhego',	'Masikini',	'Mbidjo',	'Drugesi',	'Akwe',	'okere',	'Katanga',	'Kotho',	'Ndefu',	'Berunda',	'Lengbatsi',	'Kambala',	'Nioka',	'Yagu',	'Udju',	'Simbi',	'Rona',	'Rabu',	'Nyaleka',	'Ngb\'ur',	'Gulu',	'Amee',	'Avu',	'Gwoknyeri',	'Libi',	'Luga',	'Sii',	'Rimba',	'Panyabiu',	'Ngote',	'Vida',	'Uguro?',	'Unyebo?',	'Uwilo',	'Zavi',	'Adingi?',	'Schubert??',	'Ter Ususa?',	'Raa???',	'Paicing Keno',	'Mahagi Douane',	'Parombo Ambere',	'Pono Avar',	'Mahagi Etat',	'Mahagi Mission',	'Ulyeko',	'Mahagi Anglican',	'Alego',	'Avere',	'Kabasa',	'Jupudera',	'Jupawisa',	'Mungere',	'Tilal',	'Anjokani',	'Wi Rii',	'Jupudeba?',	'Kanga',	'Wala',	'Ambere',	'Wilii',	'Ulyeko',	'Buu',	'Jupahoy',	'Otha',	'Alla Wimoo',	'Thedeja',	'Gisigi',	'Ukebu Ngali',	'Bika',	'Jalusene',	'Nyaa',	'Beju',	'Ndrele',	'Djuru',	'Lenge',	'Alagi',	'Mere Appoline',	'Wighi',	'Draju',	'Rigo',	'Ajagi',	'kpana',	'Agudi Usoke',	'Pakulo Therango',	'Abira Areju',	'Jupagwey',	'Alla-CECA',	'Kasengu',	'Afoyo',	'Lelo',	'Kpanyi',	'Anyiko',	'Nyalebe',	'JupaDrogo',	'Ugwilo',	'Ambaki',	'Pudinga',	'MP Etat',	'MP Ceca',	'Lenju',	'Angaba',	'Djegu',	'Pathole',	'Pajaw',	'Nyarambe Mission',	'Udongo Abira',	'Anzika',	'Panyandong',	'Awasi',	'Cawa ANJU',	'Angumu Abia',	'Lanyi',	'ara',	'Apala ETAT',	'Dabu',	'Kudiweka',	'Langa',	'Bessi',	'Are',	'Ugudo Zii',	'Uyandu',	'Ndaru Muswa',	'Gengere',	'Jupakamu',	'Musongwa',	'Gudjo',	'Ngri Balo',	'Juru Kidigo',	'Libi',	'Mbr\'bu',	'Mandefu',	'Terali',	'Rassia',	'Aboro',	'Lokpa',	'Rethy',	'Kpandruma',	'Zau',	'Kokpa',	'Bale',	'Lailo',	' ',	'Mola',	'Djubate',	'Dz\'oo',	'Dissa',	'Keli',	'Dheyoluts',	'Dhebu',	'Buba',	'Godjoka',	'Noga',	'Sanduku',	'Dhekpaba',	'Lokema',	'Tchulu',	'Linga',	'Lodjo',	'Uma',	'Ndalo',	'Jina',	'Ndjale',	'Pimbo',	'Djugu',	'Bukachele',	'Salama',	'Lenga',	'Bule',	'Dhendro',	'Duvire',	'Ngolo',	'Fataki',	'Sombuso',	'Jiddha',	'Ndjala',	'Bassani',	'Ladyi',	'Gobunji',	'Okareba',	'Malo',	'Jiba',	'Gokpa',	'Djokaba',	'Ngadjoka',	'Laudjo',	' ',	'Petro',	'Dz\'Na Mbau',	'Paty',	'Passion',	'Kpau',	'Likopi',	'Budu',	'Tchele',	'Masikini',	'Mangambo',	'Tsili',	'Nyangaray',	'Nyarada',	'Petsi',	'Dihungo',	'Ngabula',	'Kobu',	'Bambu',	'Tchuda',	'Zengo',	'Lalo',	'Banana',
                'Dala',	'Baimani',	'Nizi',	'Luchay',	'Ce 39 Iga BarriÃ¨re',	'Heritage',	'Ndjanga',	'Lopa',	'Kambe',	'Lingo',	'Resto',	'Nyai Ndii',	'Blukwa Mbi',	'Dhedja',	'kpanga',	'Maze',	'Utcha',	'Blukwa Etat',	'Drodro',	'Logo Takpa',	'Kpalo',	'saliboko',	'Mulinga',	'Masumbuko',	'Tchatsikpa',	'Lomi',	'Mutumbi',	'Kparnganza',	'Loga',	'Lita',	'Katoto',	'Ndungbe',	'Lonyo',	'Vilo',	'Ezekere',	'D\'idjo',	'Mandro',	'Zumbe',	'Penyi',	'Bahwere',	'Risasi',	'Adventiste',	'Central',	'Areo',	'Bankoko',	'Bigo',	'Bora Uzima',	'Bunia Cite',	'Kindia',	'Lembabo',	'Mudzi Maria',	'Muhito',	'Ndibakodu',	'Ngezi',	'Nyakasanza',	'Nzere',	'Opas',	'Rwankole',	'Simbilyabo',	'CNCA Saio',	'Nyamavi',	'Kasenyi CitÃ©',	'Kasenyi Centre',	'Nyamusasi',	'Nana',	'Tchomia',	'Sabe',	'Nyamamba',	'Kakwa',	'Joo',	'Gbi',	'Torges',	'Bahaha',	'Pekele',	'Manya',	'Mabukulu',	'Bandibwame',	'Toly Toly',	'Mabangito',	'Lolwa',	'Dadaru',	'Mbunku',	'Tshitadi',	'Katshabala',	'Nsuana',	'Kalomba',	'Kasanga Luebo',	'Fuamba',	'Mutondo',	'Aigle Baddy',	'Mutetela',	'Kaseku',	'Kakungula',	'Tshibandama',	'Muendele',	'Kalendende',	'Kanzulinzuli',	'Tamende',	'Kasanga',	'Mabolio',	'Ngilinga',	'Butsili',	'Bundji',	'Mabakanga',	'Madrandele',	'Ngongolio',	'MBUTABA',	'MAVIVI',	'Malepe',	'Rwangoma',	'Kasabinyole',	'Boikene',	'Tuungane',	'Paida',	'HALUNGUPA',	'Mukulyia',	'Sayo',	'Supa',	'Vuvatsi',	'Vulamba',	'Vulindi',	'Vutike',	'Kyangike',	'Vutsundo',	'Munzambaye',	'Malende',	'Maman Musayi',	'Munoli',	'Makasi',	'Matanda',	'Vutetse',	'Katsya',	'Ngengere',	'Mondo',	'Kyambogho',	'Kyavisogho',	'Makoko',	'Mbilinga',	'Kanyihunga',	'Butuhe',	'Amani Kisungu',	'Rwahwa',	'Kahamba',	'Vurondo',	'Kalunguta',	'Mabuku',	'Maboya',	'Kivetya',	'Mataba',	'Lisasa',	'Kabasha',	'Kasebere',	'Mambingi',	'Kasitu',	'Buhesi',	'Katanda',	'KISIMA',	'BUHUMBANI',	'VISIKI',	'Muyisa',	'Wanamahika',	'Makerere',	'Rughenda',	'Masiki',	'Kihinga',	'Makangala',	'Vuhika',	'Tulizeni',	'Wayene',	'Vungi',	'Muchanga',	'Kivika',	'Mukuna',	'Irangya',	'Mitoya',	'Masuli',	'Musenda',	'Vighole',	'Kambuli',	'Katinga et sanzasili',	'Mengwe',	'Obelemba',	'Umubundje',	'Osso',	'Bitule',	'Obosango',	'Pene_aluta',	'Okoku',	'Mukwanyama',	'Kawe 1',	'Mungele',	'Nyakisende',	'Kilibatete',	'Amakonyo',	'Twabinga',	'Ayuza',	'Tenge tenge',	'Kasesa',	'Mashaka',	'Kalibonda',	'Kagulu',	'Muyombo',	'Mabanda',	'Mombese',	'Kilalaulu',	'Lengezi',	'Wagela',	'Penenyingi',	'Kipangula',	'Katala',	'Penesenga',	'Mukwanga',	'Katimba',	'Musongela',	'Ndeomanono',	'Fimbonyingi',	'Kalondakibuyu',	'Nyembo',	'Tchuki',	'Kabeya',	'Kiyanga',	'Malota',	'Kalunga mungabo',	'Biyungi',	'Sombe',	'Kayembe',	'Salumu',	'Matete',	'Kimbaseke i et machapano',	'Salamabila',	'Kimbaseke i',	'Kimbaseke ii',	'Asumani',	'Sous marin',	'Mwangundu',	'Wamaza',	'Kihonya',	'Kingombe',	'Kawaya',	'Kabeya',	'Kafyoto',	'Kankumba',	'Kauta',	'Kongolo',	'Lupaya',	'Mufala',	'Mulangabala',	'Muviringo',	'Mwana ndeke',	'Uzura',	'Olimba',	'Km 18',	'Limanga',	'Maringa',	'Maulumwanda',	'Nyanga',	'Kisesa',	'Mukangwa',	'Lotakasha',	'Lububula',	'Kahambwe',	'Luabao',	'Malela',	'Kavungu',	'Milobo',	'Bushiba',	'Lusangay',	'Kieshi',	'Kitete',	'Samba',	'Lweki',	'Bilundu',	'Difuma ii',	'Reference lowe',	'Kaswa',	'Lokenie',	'Kasuku',	'Kiyungi',	'Likeri reference',	'Ngenda',	'Methodiste kibombo',	'Lowe',	'Nganze',	'Losa olamba',	'Wenga',	'Utanga',	'Lusamba',	'Weta',	'Dembo',	'Dikululu',	'Kembeyule',	'Utshu',	'Amba',	'Saburi',	'Kapuli',	'Karomo',	'Rudika',	'Makangila',	'Marungu',	'Ngongo',
                'Lubamba',	'Kabonga',	'Bikenge',	'Mbutu',	'Mingana',	'Mwema',	'Mumba',	'Kimwanga',	'Kipaka',	'Kisandji',	'Kunda',	'Kasubi',	'Kaparangao',	'Kalongosola',	'Kabumbu',	'Saidi',	'Bakari',	'Sengamali',	'Kituta',	'Kamumba',	'Penengori',	'Biunkutu',	'Bukama',	'Kama',	'Kampene',	'Kibundila',	'Kisimba',	'Kitangi',	'Tchalumba',	'Kalongola',	'Katumpi',	'Kayuyu',	'Lumuna',	'Wambale',	'Pene  idomwa',	'Malikumu',	'Mwanankusu',	'Mabikwa',	'Ngoma',	'Sayabiaku',	'Itabala',	'Lutala',	'Ntombo',	'Kapela',	'Ngongo',	'Mulende',	'Mulamba',	'Misisi',	'Kyelu',	'Mukiti',	'Mabila',	'Penemagu',	'Kakaleka',	'Kagolomba',	'Kangela',	'Kakozwa',	'Lubile',	'Mukombe',	'Kagelya',	'Ndandalukala',	'Moga',	'Kamundala',	'Kakutya 3',	'Kakutya 2',	'Kamakozi',	'Kakutya 1',	'Bobela',	'Matongo',	'Mangobo',	'Mikonde',	'Mizeituni',	'Sokolo',	'Kamikunga',	'Alunguli',	'Idumba witamwino',	'Milanga',	'Mikelenge',	'Trois z',	'Brazza',	'Tokolote',	'Rva',	'Libenga',	'Kasiku i',	'Lwama',	'Kasiku ii',	'Basoko',	'Muyengo',	'Nyoka',	'Kailo i',	'Ulangate',	'Kasenga',	'Kailo ii',	'Elila',	'Lubao',	'Lokando',	'Kimiakimia',	'Pembeliba',	'Kipakata',	'Kapinda',	'Lubengele',	'Katako',	'Kampala',	'Yalombe',	'Kitamuna',	'Kabungulu',	'Fikiri',	'Kowe',	'Umba-umba',	'Kibeke-uru',	'Tubila',	'Ferekeni',	'Matengenya',	'Kibeleketa',	'Kibwana',	'Kalombenyama',	'Punia i',	'Minimbe',	'Belia',	'Obea',	'Matumba',	'Saulia',	'Kyolo',	'Kamukingi',	'Kabongola',	'Oku',	'Kasese',	'Tubile',	'Mpiala',	'Omauwa',	'Kabakaba',	'Ntufia',	'Omoyokani',	'Utiakumanga',	'Mangandu',	'Makondo',	'Tshamaka',	'Penedjali',	'Elimu',	'Ungandula',	'Maindombe',	'Makutano',	'Mokambo',	'Fma Mokambo',	'Fma Sakania',	'Hewa Bora',	'Kabunda',	'Kakyelo',	'Kasumba Lesa Douane',	'Kasumba Lesa Village',	'Katala',	'Kipilingo',	'Kipusha',	'Kitotwe',	'Muhona',	'Musumali',	'Mwenda',	'Tshinsenda',	'Adra 31',	'Adra 41',	'Kafubu',	'Kalunda',	'Kikanda',	'Kikwanda',	'Kinama',	'Kitanda',	'Kiwele',	'Makulo',	'Mulyashi',	'Sambwa',	'Shindaika',	'Kijiba 1',	'Baraka',	'Colorima',	'Kikunda',	'Mukulu',	'Notre dame',	'Kamasaka',	'TÃ©lÃ©cel',	'Congo 2',	'Kawama',	'Shindaika',	'Bendera',	'Congo 1',	'De la Mine',	'Kalukuluku',	'Kijiba 2',	'La VallÃ©e',	'Luano',	'Luwowoshi',	'Masangoshi',	'Neo Apostolique',	'Orphelinat',	'Orthodoxe',	'PolylumiÃ¨re',	'Stella',	'Mukaka',	'Kasapa',	'Kimbeimbe',	'Vangu',	'Boluo',	'Flotte',	'Genie',	'Marechal',	'Kakontwe',	'Mura',	'Nzilo',	'QG',	'Tingi Tingi',	'Kiwele',	'Kalubwe 2',	'Kasapa 2',	'Camp Assistant',	'CRAA',	'Gambela 1',	'Gambela 2',	'Iringi',	'Kalubwe 1',	'Kamatete',	'Kasapa 1',	'Kimbeimbe',	'Kiswishi',	'Lumumba',	'Makutano',	'RVA',	'St Esprit',	'Tshamalale',	'Tshombe',	'Circulaire',	'CitÃ© De Jeunes',	'Ecaset',	'EmmaÃ»s',	'Kabanga',	'Kabwela',	'Kakompe',	'Kamasaka',	'Kilobelobe',	'Lapofa',	'Mubindu',	'Njanja',	'RÃ©fÃ©rence',	'Sab',	'Safina',	'Savio',	'St Abraham',	'Suzanella',	'Triangle',	'Vap',	'Polyvalent',	'Werner',	'Hewa Bora 2',	'Rail',	'Hewa Bora 1',	'Agetraf',	'Cadastre',	'Camp PrÃ©fabriquÃ©',	'Ciment Kat',	'Foire',	'JÃ©sus Le Roc',	'Kabesha',	'Kigoma Est',	'Kigoma Ouest',	'Kinsense',	'Luano',	'Quartier Industriel',	'Dilala Kolwezi',	'DAC Kipushi',	'GMI',	'Kasapa',	'Kamalondo',	'Prefabrique',	'Kamalondo',	'Bumi',	'Serkali',	'Masikilizano',	'Kenya 2',	'Lubumbashi',	'Tingi Tingi',	'Kakompe',	'Dilungu',	'Kyubo',	'CASOP',	'Kalebuka',	'Kasungani',	'Kenya 1',	'Mabila',	'Malaika',	'Moba',	'Musofi',	'Munama',	'Kasamba',	'Kilenge',	'Trois C',	'Upemba',	'Golf MÃ©tÃ©o 2',	'Gbadolite 2',	'Tshamalale',	'Mampala 2',	'Basembe',	'Plateau 2',	'Lido Golf',
                'Gbadolite 1',	'Golf MÃ©tÃ©o 1',	'Kabulamenshi',	'Makomeno',	'Mampala 1',	'Mulao',	'Munua',	'Penga Penga',	'Plateau 1',	'Poleni',	'Maisha',	'Royale',	'Salama',	'Kasungami 2',	'Mimbulu',	'Triangle',	'Jamaa Yetu',	'Kasungami 1',	'Kiboko',	'Kilimasimba',	'Kimilolo',	'Maendeleo',	'Mama Wa Huruma',	'Mutuale',	'Ntanda',	'Peage',	'Somika',	'Wantanshi',	'Kafubu',	'Bangwelo',	'Ceba',	'Gemena',	'Golgotha',	'Kantumbwi',	'Kayelele',	'Kisaho',	'Kyubo',	'MarchÃ©',	'Marungu',	'Sandoa',	'Tangu Hapo',	'Tingi Tingi',	'Tujikaze',	'Betty',	'GÃ©camine',	'Kawama',	'Kinsevere',	'Mukoma',	'Kipopo',	'Lumata',	'Lumwana',	'Mabaya',	'Mimbulu',	'Musoshi',	'Mwawa',	'Sainte Famille',	'Saint Raphael',	'Sapin',	'Tumbwe',	'Lupidi 2',	'Kyembe 2',	'Kapolowe Gare',	'Kapulwa',	'Katanga',	'Katobio',	'Lupidi 1',	'Kibangu',	'Kidimudilo',	'Koni',	'Kyembe 1',	'Lwisha',	'Mulandi',	'Ndakata',	'Ditengwa',	'Kaluwe',	'Kamikolo',	'Mission',	'Kikuyo',	'Mwabesa',	'Ngalu',	'Mwana Kulema',	'Mubambe',	'Shamalenge',	'Lupaji',	'Kakontwe',	'Kiwele',	'Kamilopa',	'Kilima',	'Kimpulande',	'Mivuka',	'Muchanga',	'Nguya',	'Panda Mayi',	'Disanga 1',	'Disanga 2',	'Dikula',	'Disanga 3',	'Kambove',	'Kampemba',	'Kiwewe',	'Kyaba',	'Mpande',	'Mukumbi',	'Mulungwishi',	'Mission',	'Centre Ville',	'Dac',	'Kamatanda',	'Kampupi',	'Kitabataba',	'Mapatano',	'Simba',	'Six Sapins',	'SNCC',	'Kyubo',	'Kampemba',	'Kalipopo',	'Kanona',	'Kapenda',	'Kaponona',	'Kibadi',	'Mafuta',	'Musumba',	'Nkolomoni',	'Okito',	'Petwe',	'Ntondo',	'Kyenge',	'Lubanda',	'Lubuko',	'Lukafu',	'Lutandula Lwalala',	'Malambwe',	'Minga',	'Mukebo',	'Mupanda Mukenge',	'Mwemena',	'Nkonko',	'Chalwe',	'Chibambo',	'Kaboka',	'Kabyasha',	'Kasomeno',	'Kikungu',	'Kinika',	'Kisamamba',	'Mfuta',	'Mission',	'Mwaba',	'Nkambo',	'Sapwe',	'kashobwe',	'Kawama',	'Mukoshi',	'Kabimbi',	'Walya',	'Lukeka',	'Mulumbwa',	'Nkole',	'Ntonge',	'Kaindu',	'Kabambankuku',	'Lupembe',	'Dikulwe',	'Kalera',	'Kanfwa',	'Kapoya',	'Kasungami',	'Katala',	'Kimungu',	'Kipanga',	'Kitobo',	'Kyubo',	'Lwika',	'Lwishi',	'Mpwaki',	'Mufunga',	'Mukana',	'Mushiza',	'Muvule',	'Nsangwa',	'Sumpwa',	'Tomombo',	'Toyota',	'Mungomba',	'Mwalamuna',	'Kilwa',	'Dikulushi',	'Dubie',	'Kabangu',	'Kakinga',	'Kampangwe',	'Kamutrombe',	'Kapufi',	'Kasolo',	'Kasongo Mwana',	'Katenge',	'Kato',	'Kyaka',	'Kyona',	'Lukonzolwa',	'Lusalala',	'Lwanza',	'Mubanga',	'Mukupa',	'Mulangale',	'Mulendwa',	'Mulinde',	'Mwepu Ntanda',	'Nsonga',	'Kabambe',	'Tompwe',	'Kilenge',	'Kasungeshi 2',	'Dilenge',	'Kabanda',	'Kanshimba',	'Kasungeshi 1',	'Kibula',	'Kintya',	'Kisele',	'Kwiyongo',	'Lusinga',	'Mitwaba',	'Mubidi',	'Mumbolo',	'Muombe',	'Mwema',	'Nkonga',	'Nsokelwa',	'Kapulo',	'SantÃ©',	'Kabilele',	'Boma',	'Chalanshi',	'Chamfubu',	'Kakonona',	'Kamakanga',	'Kapondo',	'Kasama',	'Kasongo Kamulumbi',	'Katonta',	'Kinkalangu',	'Kizabi',	'Mumbalanga',	'Mwela',	'Mwenge',	'Bibanga',	'Bufua',	'Cibila',	'Cikuyi',	'Ciluila',	'Kabala 1',	'Kabala 2',	'Kalunda',	'Kaponji',	'Katabua',	'Katanda 1',	'Katanda 2',	'Katshiampanga',	'Lukangu',	'Manja',	'Molola',	'Station',	'Adventiste',	'Ciombela',	'Commune',	'Inga',	'Inkisi',	'Kabuacia',	'Kalundu',	'Kanjiya',	'Kankelenge',	'Kimbangu',	'Lubuebue',	'MarchÃ©',	'Mission',	'Mpandisha',	'Plaine',	'Salongo',	'Schekina',	'Sengamines',	'Tatu Kanyinda',	'Bimpe',	'Camp Nsele',	'Camp Nyongolo PNC',	'Centre de mission',	'Ciaciacia',	'Cikisha',	'Dubai',	'Kasamayi',	'Kashala Bonzola',	'Lubilanji',	'Mudiba',	'Nyongolo',	'Solola Bien',	'Tubondo 1',	'Tubondo 2',	'Tubondo 3',	'Bakua Kamba',
                'Kalunda_Musoko',	'Kande',	'Kanyukua',	'_Tshileo',	'Mbao_Lubiji',	'Kasandwe',	'Kabanga',	'Mbao_Lubimbi',	'Kabiji',	'Tshikala',	'Itondo_G',	'Kabue',	'Tshilundu',	'Ngoy_Band',	'Tshimung',	'Kalenda_G',	'Kangala',	'Makena',	'Nyemba',	'Tshimanda',	'Tshinzoboyi',	'Katangela',	'Tshiamba',	'Lubambala',	'Lubunza',	'Kapaku',	'Tshikumbu',	'Mukanda',	'Malukasamba',	'Kaha',	'Bk_Tshieleng',	'Muanamuzang',	'Mulundu',	'Tshilomba',	'Mbaya_Museng',	'Museng_G',	'Kipangie',	'Matembo',	'Bakoma',	'Mbayo',	'Eyombo',	'Kipushya',	'Kasendu',	'Lufuanka',	'Tshiambue',	'Kasamba',	'Mbo',	'Mbendele',	'Kafuku',	'Ngombe',	'Tshiseshi',	'Lulungu',	'Kipoke',	'Mpitshi',	'Nkeba',	'Kalonda',	'Ngievu lulu',	'Tshibue',	'Kabula',	'Mpemba_Ndala',	'Kimabue',	'Musangie',	'Ebondo_Kape',	'Lubala',	'Kasolo',	'Ndjibu_Ebambi',	'Lualaba_Ndaba',	'Mbutu',	'Mulenda',	'Kamana_1',	'Kamana_2',	'Kabue_Lomami',	'Sankia',	'Kasonguele',	'Muamuayi',	'Tshungu',	'Mambu',	'Bakunda',	'Kipinda',	'Lualaba_Nsangua',	'Eshilu',	'Kele',	'Muasa',	'Cipuka',	'Nyoka',	'Muadi',	'Kasanga',	'Kamaziya',	'Kamiji',	'Miketa',	'Lubi',	'Katongo',	'Malenga',	'Mbala Tshinyanga',	'Tshiamvi',	'Kapangu',	'Matamba',	'Mulaji Kanumbi',	'Bakwa Bowa',	'lm Kabuela',	'Kambayi',	'Kanda Kanda',	'Kabila',	'Mbala Cotongo',	'Lulamba',	'Kalunga',	'Kayemba Ngomba',	'Katobo',	'Kamanda Kadila',	'Mukola Kabongo',	'Mutembue',	'Csmi',	'Mumbo',	'Kamueno',	'Lupongo',	'Kisengwa',	'Kafumbe',	'Sangwa',	'Lumumba',	'Kangoyi',	'Lubamba',	'Kabao',	'Malungu',	'Maloba',	'Seke',	'Yemba',	'Bemane',	'Kiasame',	'Lukolela',	'Mukomayi',	'Kitengie Muana Kialu',	'Miombe Etale',	'Bashimikie',	'Kifuenkiese 1',	'Kengie',	'Basase',	'Bakile',	'Kabue',	'Luanga Etambayi',	'Mpengie',	'Miombe Muavi',	'Katshia',	'Triangle',	'Tshibikosa',	'Museng_Droite',	'Tshilonda',	'Tshiabobo_Revelation',	'Tshiabobo_Etat',	'Congo',	'Lusuku',	'Munvuyi',	'Ilengele',	'Kombo_Tshitonga',	'Kasakayi',	'Christ_Sauveur',	'Nvlle Ville',	'Conscience',	'Baseka',	'Katshisungu',	'Katshisamba',	'Kazadi _A_ Ngoyi',	'Bajika',	'Kabusanga',	'Ste_Anne',	'Lokobo',	'Kasha',	'Hamba',	'Kamukungu',	'Masonzo',	'Nkulu',	'Kankinda',	'Ditu_Ilunga',	'Mbamvu',	'Katoka',	'Tshitonkonyi',	'Katshisungu',	'Kasanza',	'Ditu_Bukasa',	'Mutonji_Matanda',	'Mukanza',	'Kabwe_Muzembe',	'Matshionyi',	'Nkuna',	'Kaseyi_Kabuyi',	'Kanana',	'Kamisangi',	'Kantendele',	'Makota',	'Kabanda',	'Mande_Intarieur',	'Mulunda_Muimpe',	'Mukendi_Luboya',	'Mpiana_Ntita',	'Ditalala',	'Luanga',	'Nsona',	'Fasi_Yetu',	'Kakona',	'Tshiasasa',	'Relais_Mpumbwa',	'Ngambua',	'Mukubi',	'Mpiana_Mbinga',	'Ntita_Mushiya',	'Ndiadia',	'Tshileu',	'Kanyana',	'Lukole',	'BIK',	'Bondoyi',	'Regideso',	'Katabaie',	'Ciput',	'Mpinga',	'Kanda_Kanda',	'Musaula',	'Macici',	'Prison',	'Kamabue',	'Mandam',	'Cishinji',	'Kalubeya',	'Deux_Collines',	'Matobo',	'Musadi',	'Kanintshin',	'Kabamba_K',	'Cindundu',	'Munsampi',	'Tshibangu_Mpata',	'Lunga',	'Lusambo',	'Kaseki',	'Kalubanda',	'Mpata',	'Heritage',	'Mulamba 2',	'Relais Mpongo',	'Mpemba Nzeo',	'Deux Samaritains',	'Cioji',	'Ngandajika Central',	'Mpunga',	'Musakatshi',	'Kanyaka Inera',	'Mpoyi',	'Mande Central',	'Mpasu',	'Inabanza',	'Kolobeyi',	'Kabue_Kakiele',	'Lukombe',	'Lupambwe',	'Mitombe',	'Eonyi',	'Kibulu',	'Baunga',	'Mankamba',	'Kitengie_Ngu',	'Ebindjiri',	'Kitengie-ngu',	'Kilungie',	'Lumba_Lupata',	'Lomami',	'Ngandu',	'Lutobo',	'Muinkand',	'Ntikit',	'Jesus_De_Nazareth',	'Kakang',	'CarriÃ¨re',	'Kayind',	'Kananganan',	'Nsang Tshibal',	'Tshiyeng',	'NDG',	'Tshipond',	'Ishiy',	'Tshiawut',	'Mbangom',	'Kanin Tshin',	'Muamb\'a_Rangas',	'TSHIAWU',	'Monga',	'Shamwana',	'Nkonkole',	'Kishale',	'Kalamata',	'Mupanga',	'Kasenga Nganye',	'Kabele',	'Kibiziwa',	'Selembe',	'Tabora',	'Kalunga',	'Ntobo',	'Lumwe',	'Sheleshele',	'Mukulakulu',	'SNCC',
                'Gecamine',	'Methodiste',	'Mbala',	'Katobwe',	'Ngoya Lulu',	'Maka',	'Kibanda',	'Kazele',	'Muchanga',	'Makala',	'Byowa',	'Kisanga Wa Byoni',	'Kabwe',	'Katentamine',	'Kabamoma',	'Medico Social',	'Kapando',	'Katondo',	'Mabwe',	'Misebo',	'Byandala',	'Lweya',	'Kintobongo',	'Capitale',	'Butumba',	'Kisamba',	'Kisungi',	'Kilumbe',	'Kakole',	'Balongo',	'Missa',	'Congo',	'CPCO',	'Mpambwe',	'Kayeye',	'Kapako',	'Vumbi',	'Nkimba',	'Kibwe',	'Ntwale',	'Nyembo',	'Kadibwe',	'Mulenda',	'Kyabu',	'Kaleka',	'Kizanga',	'Kakoma',	'Mpanda',	'Kamashi',	'Uzima',	'Kelenge',	'Kahungwe',	'Kasele',	'Kihumba',	'Nyembo',	'Mpasu',	'Kabunda',	'Kaloba',	'Kamwenze',	'Djombo',	'Nsele',	'Mwambayi',	'Kyondo',	'Nyundo',	'Mwanya',	'Kimambwe',	'Lukaya',	'Kina',	'Lubyay',	'Lenge',	'Kamungu',	'Bukunga',	'Lwakidi',	'Kavula Kifitu',	'Ngoya',	'Kime',	'Bushimbi',	'Elisabeth',	'Kambo',	'Kamusenga',	'Ngonzo',	'Kampako',	'Buleya',	'Katuba 1',	'Katuba 2',	'Katuba 3',	'Q 14',	'Katuba 4',	'RVA',	'Q Base',	'PMI/SNCC',	'Q 82',	'Kiabukwa',	'Kasania',	'Kinkunki',	'Kingo',	'Nsungu',	'Mwitobwe',	'Congo',	'Kasende',	'Lwembe',	'Kibula',	'Luvwa',	'Q 53',	'Q 52',	'Busangu',	'Centre Urbain',	'Kimpanga',	'Tshibamba',	'Musanji',	'Kaniama 3',	'Kaniama 4',	'Kaniama 2',	'Musaka',	'Kaniama 1',	'Muleba',	'Maniamuna',	'Mutoyo',	'Kasenji',	'Mwadi Kayembe 2',	'Kisamba',	'Mwadi Kayembe 1',	'Kapata',	'Kimanda',	'Mpanda',	'Kasese',	'Kasengayi',	'Ngombe',	'Kalundwe',	'Kayeye',	'Pastoral',	'Tshiahona',	'Mombela',	'Mwala',	'Kahako',	'Kisaho',	'Kayi',	'Lufwishi',	'Kafuku',	'Kalamba',	'Lwamba Sakadi',	'Mudindwa',	'Nsulo A Lowa',	'Kibila',	'Yamba',	'Kamayi',	'Mukaya Nkumba',	'Luabo',	'Kalalo',	'Kanene',	'Kinda',	'Kalele',	'Mpweji',	'Sokele',	'Lupweji',	'Kavwaya',	'Katula',	'Kamishipa',	'Kitembo',	'Kalombo 1',	'Kibila',	'Ntwadi',	'Mwaba',	'Yolo',	'Mpungwe',	'Kaleba',	'Kadia',	'Masangu',	'Kalombo 2',	'Kipamba 1',	'Kibondo',	'Kabenga',	'Muyumbwe',	'Lufira',	'Mangi 4',	'Kipamba 4',	'Kipamba 3',	'Mangi 3',	'Mangi 2',	'Mangi 1',	'Kipamba 2',	'Nyonga',	'Kayombo',	'Lubonge',	'Kibula',	'Makwidi',	'Kashukulu',	'Kitenge',	'Kabulo Kisanga',	'Kasongo Musule',	'Lulenge',	'Kayambi',	'Nkombe',	'Kamunza',	'Komba Komba',	'Budi',	'Kasenga Mpetshi',	'Sohe',	'Kaloko',	'Kyunga',	'Kileo',	'Kalulu',	'Kalungu',	'Mwadi Ngoy',	'Kansele',	'Bekisha',	'Amani',	'Anuarite',	'Mwine Ngoy',	'Fwila',	'Lubinda',	'Kikose',	'Kimbalama',	'Kilumba Ngoy',	'Kabumbulu',	'Kabwe Ndalewe',	'Kamwenze',	'Lwamba',	'Umba Nongo',	'Banza Mbuyu',	'Kyapwa',	'Katyimpwe',	'Kayashingo',	'Kalongo',	'Kisanga',	'Kivukuta',	'Musao',	'Kisula',	'Kakongolo',	'Songwe',	'Manga',	'Kabishi',	'Seya',	'Sope',	'Kasulwa',	'Nyoka',	'Kyamakanza',	'Lwandwe',	'Kabwe Mulongo',	'Kakombo Mushimba',	'Kabuya',	'Twite Mwanza',	'Lubondoy',	'Nkole',	'Kabozya',	'Tuba',	'Kamete Mete',	'Kabala',	'Butombe',	'Mutombo Lupisthi',	'Muko Mutombo',	'Ndala',	'Kansonge',	'Kimwenze',	'Kasenga 2',	'Shele',	'Bangwe',	'Mukubu 2',	'Nambia',	'Kibindi',	'Kantambo',	'Kasenga 1',	'Kyolo 2',	'Kyolo 1',	'Mukanga 1',	'Kina de Mukanga',	'Mukubu 1',	'Kyamona',	'Ilunga',	'Mukanga 2',	'Benze',	'Mpemba',	'Mulongo 1',	'Kalume',	'Kumbula',	'Kabamba',	'Musumba',	'Mpangwe',	'Mulongo 2',	'Kiya',	'Kipuzi',	'Ngoya',	'Kamudilo',	'Kibambo',	'Kafumbe',	'Kaunga',	'Kyabo',	'Kabi',	'Kala Commune',	'Bukena',	'Kanunka',	'Kyadi',	'Kyabombo',	'Lumbule',	'Kongolo',	'Grelka',	'Kamome',	'Kimungu',	'Kabulo',	'Kafumbe',
                'Télévision',	'Tshiangu',	'Congo',	'Pelende',	'Kasai',	'Kivu',	'Lokari',	'Lubamba',	'Mafuta kizola',	'Mandiangu',	'Mapela',	'Matadi',	'Tshuenge',	'Lukunga',	'Lumumba',	'Dondo',	'Loeka',	'Lubefu',	'Lunionzo',	'Malemba',	'Maziba',	'Mbomb Ipoko',	'Sankuru',	'Sumbuku',	'Totaka',	'Vivi',	'Manenga',	'Fongo',	'Kimbondo',	'Kimwenza Mission',	'Kimwenza Rural',	'Kindele',	'Mama Yemo',	'Kinkuemi',	'Manionzi',	'Masanga Mbila',	'Mitendi',	'Mazamba',	'Matadi Mayo',	'Ndjili Kilambu',	'Ngansele',	'Plateaux',	'Pumbu',	'Maman mobutu',	'Ngombe',	'Mitendi',	'Kimbondo',	'Antenne Lobiko',	'Don Bosco',	'Dumez',	'Kimbwala',	'Mambre',	'Matadi Kibala',	'Matokama',	'Mazal',	'Mbudi',	'Sans Fil',	'Quartier 10',	'Quartier 11',	'Quartier 12',	'Quartier 13 A',	'Quartier 13 B',	'Quartier 1',	'Quartier 2',	'Quartier 3',	'Quartier 4',	'Quartier 5',	'Quartier 6',	'Quartier 7',	'Quartier 8',	'Quartier 9',	'Mukulua',	'Baoba',	'Luyi 2',	'Mateba',	'Bulambemba',	'Luyi 1',	'Mpila',	'Mukulua 1',	'Assossa',	'44889',	'Diangienda',	'Diomi',	'Elengesa',	'Karthoum',	'Peti Peti',	'Saio',	'Fleuve',	'Mikondo',	'Bahumbu 2',	'Badara',	'Bahumbu 1',	'Bibwa',	'Buma',	'Dingidingi',	'Kindobo',	'Mikala',	'Mikonga',	'Mpasa 1',	'Mpasa 2',	'Nsele',	'Pecheur',	'Tshangu',	'Badara',	'Kabila',	'Lufungula',	'PIR Kimbondo',	'Badiadingi',	'Molende',	'Lubudi',	'Liberation',	'CitÃ© Verte',	'Herady',	'Inga',	'Kalunga',	'Konde',	'Madiata',	'Mbala',	'Muana Ntunu',	'Ndobe',	'Ngafani',	'Nkingu',	'Nkombe',	'Nkulu',	'Pululu Mbambu',	'Banga Banneux',	'Banyanga',	'Biponga',	'Kanyunyu',	'Lunduba',	'Mashashana',	'Mayamba',	'Mayimbi',	'Nganda 2',	'Pungu 2',	'Shandala',	'Banga Lubaka',	'Ibombo Iyeye',	'Ipunda',	'Kalunga',	'Vatican',	'Mamanya',	'Mbondjare',	'Bambalaie',	'Bangombe',	'Bangombe 2',	'Batanga',	'Bukwek',	'Bulape',	'Bulape communautaire',	'Bungongo 1',	'Bungongo 2',	'Bupole',	'Dikolo',	'Ebampoma',	'Ingongo',	'Luayi Bushongo',	'Maluku',	'Mbelo',	'Misumba',	'Misumba Ebende',	'Misumba Ã©tat',	'Mpatambamba',	'Mpianga',	'Muemasongo',	'Pombo',	'Yoolo',	'Anga',	'Bambakfu',	'Basenga',	'Bololo',	'Bolonga',	'Bongondo',	'Bosenge',	'Dekese Bobo',	'Dekese Etat',	'Djombo',	'Djongo Port',	'Dumba',	'Idumbe',	'Imbombolongo',	'Ipoka',	'Isandja',	'Isolu',	'Itunga',	'Longa',	'Mbanga Sud',	'Mvusengando',	'Ngoyolo',	'Nkongo',	'Yasa',	'Yoso',	'Bambange',	'Bena Mulumba',	'Bikuku',	'Jerusalem',	'Kabote',	'Kalina',	'Kasai',	'Kasavubu',	'Kimbangu',	'Kinkole',	'Lutshuadi',	'Malumalu',	'Mpuntshia',	'Nsele',	'Pilote',	'Populaire',	'Sfi',	'Sncc',	'Yolo',	'Bakua Kenge',	'Batua Ishama',	'Batua Kadimba',	'Bolempo1',	'Dengamongo 2',	'Dengamongo Katshiabala',	'Enanga',	'Etapanya Camp',	'Etapanya Village',	'Itungampende',	'Kakenge Centre',	'Kalamba',	'Kamenji',	'Kinda 1',	'Kinda 2',	'Lukombe',	'Lukubu',	'Lushiku',	'Matambi',	'Matumba',	'Mpianga (Kakenge)',	'Tete Kalamba',	'Tshiaboshobe',	'Tshinongo',	'Bakilisto',	'Dienzalayi',	'Ditekemena',	'Inga',	'Kabambayi',	'Kabeya Lumbu',	'Kabuyi',	'Kalonda',	'Kasai 1',	'Kasai 2',	'Kasala',	'Katalushi',	'Katoka',	'Kele Kasai',	'Lungundi',	'Lunkamba',	'Mairie',	'Makumbi',	'Mbawu',	'Mbumba',	'Mukuaya',	'Mulamba Tshionza',	'Mungenda',	'Trois Z',	'Tshimbinda 2',	'Tshimbinda 1',	'Tshindemba',	'Tujukayi',	'Tukunyema',	'Kabangu',	'Kabilengu',	'Kabungu',	'Kamabonza',	'Kamako 1',	'Kamako 2',	'Kamonia',	'Kandjaji',	'Kasai Lumbembe',	'Kasekue',	'Katopa',	'Luangashimo',	'Lubami',	'Luyembe',	'Mayanda',	'Mpasu',	'Mudiadia',	'Mukuadjanga',	'Mungamba',	'Nsokombe',	'Nsumbula',	'Ntambue Kabongo',	'Tshimeya',	'Tshinota',	'Tshitambeji',	'Biakabomba',	'Dibala',	'Dikole',	'Kabelekese',	'Kakumba',	'Kalumbu',	'Kamba Nkuvu',	'Kamuesha 1',	'Kamuesha 2',	'Kasanzu',	'Ks Kasonga Tshinyam',
                'Katalayi',	'Katanda',	'Katshimu',	'Luenda Basanga',	'Lungonzo',	'Ks Lunyeka Etat',	'Lunyeka Faubourg',	'Lutshimu',	'Masangu Anayi',	'Mayi Munene',	'Mbolondo',	'Mpampa',	'Mukambu',	'Muladila',	'Mutumba',	'Mwila Mbuambua',	'Ntumba Kapangu',	'Tshiela Mata',	'Aeroport',	'Clinique',	'Kabungu',	'Kankala',	'Kanzala',	'Lunyanya',	'Mennonite',	'Mutshi',	'Muyombo',	'Nzambe Malamu',	'Salambote',	'Sami 1',	'Sami 2',	'Stade 1',	'Stade 2',	'Tshibemba',	'Tshikapa',	'Kakhumu',	'Kamatoma',	'Kamungindu',	'Kimbangu Teteji',	'Kitangwa',	'Kitembo',	'Kombo Kiboto',	'Kuyi TetejiÂ Aire de Santao',	'Mbuambua',	'Mbuji',	'Mukala',	'Ndjindji',	'Nyangu',	'Shakafulu',	'Shambuanda',	'Tshingila',	'Tshiwanda Wanda',	'Tundu',	'Kayongo Etat',	'Shayitengo',	'Kayongo CMCO',	'Tshitepa',	'Malundu',	'Kandumba',	'Kabunda',	'Sashila',	'Ngulungu',	'Ngoya',	'Bajila Kapumbu',	'Bakua Dishi',	'Dinyunyi',	'Kabemba',	'Kabeya Tshinyama',	'Kakulu 1',	'Kakulu 2',	'Kakungula',	'Kambangoma',	'Kanyinganyinga',	'Konyi 1',	'Konyi 2',	'Ks Luebo CitÃ© 1',	'Luebo Dilolo',	'Luebo Lulengele',	'Luebo Wedi',	'Lumpembe',	'Lunkelu',	'Malangu',	'Mukuandjanga',	'Ndumba',	'Ndungu',	'Nyengele Nkoshi',	'Shambuambua',	'Sheppard',	'Tshiombe Bululu',	'Bashipanga',	'Biyenge Makekele',	'Dibanga',	'Domay Kashosho',	'Ilebo Ndjare',	'Lenga',	'Mc Mikope',	'Mitshibu',	'Nyamandele',	'Tshilomba',	'Kabwanga',	'Ibowa',	'Shanga Lumbondji',	'Mc Bushongo',	'Domay Munene',	'Kabamba',	'Kabombo',	'Mc Mwembe',	'BANKUMUNA',	'Mapangu Etat',	'Mc Mapangu',	'Kumiyulu',	'Basongo',	'Yamba Yamba',	'MALEMBE',	'BENABENDI',	'Bena Makima',	'Bishanga',	'Bongo 1',	'Bongo 2',	'Bupu',	'Butala',	'Bwaya',	'Domiongo 1',	'Domiongo 2',	'Domiongo 3',	'Ikeke',	'Ilenge',	'Imambumba',	'Ipanga',	'Kabwe',	'Lodi',	'Mbima',	'Mwentshi',	'Ngoto',	'Nkoshi',	'Nono',	'Pembeangu',	'Pilote',	'Shongamba',	'Sonkatshi',	'Tuleo',	'Yeke',	'Diboko',	'HÃ´pital',	'Kampengele',	'Katshiloba',	'Kola Moyo',	'Mutena',	'Tshipata',	'Tshisenge',	'Mukuku',	'Kamabanje',	'Muamuengo',	'Lombe',	'Mutshima',	'Tshisuabantu',	'Ndala Kalunga',	'Tshibangu',	'Tshitande',	'Luvula',	'Ndambi',	'Mutetela',	'Tshisangombe',	'Bakatombi',	'Banongo',	'Benalongo',	'Benasamba',	'Bulangu Kapimbi',	'Bulangu Tshimbulu',	'Bulongo',	'Bungamba',	'Congo',	'Ifaf',	'Ikit',	'Ishamandongo',	'Kalombayi',	'Kaluamba',	'Kampungu',	'Lubanga',	'Makonoko',	'Malongo 1',	'Malongo 2',	'Mapeyi',	'Muanyika',	'Muteba',	'Mweka 1',	'Mweka 2',	'Mweka 3',	'Nsungi Munene',	'Pilote',	'Tshikuluka',	'Bangamba',	'Bashi Biyenge',	'Bena Lumba',	'Kangombe',	'Kapata',	'Kapemba',	'Kapindula',	'Kayenda Nkumbu',	'Kimbanguiste',	'Luama Kabambayi',	'Malu Malu',	'Mbayi Kamonji',	'Mputa',	'Mukanga',	'Mukuadjanga',	'Ndjoko Adventiste',	'Ndjoko Catholique',	'Ndjoko Etat',	'Tshialupemba',	'Tshikuma',	'Kabola',	'Kayala',	'Khoma',	'Kindamba',	'Mbamba',	'Mbango',	'Muhaku',	'Lukaka',	'Kikunga Tembo',	'Nzadi',	'Tukondo',	'Luangue Video',	'KANGUMBA',	'Abattoir',	'Bakuba',	'Bel\'air',	'HÃ\´pital',	'Kabikabi',	'Kabuatu',	'Kabudila centre',	'Kabudila Samba',	'Kalupombe',	'Kamankonde',	'Kasanji',	'Kashimba',	'Katanga',	'Katshiongo',	'Khajama',	'Kibulungu',	'Kizito',	'La Paix',	'Malongo',	'Masangu',	'Matshibola',	'Mbulamputu',	'Muyeji',	'Ngombe',	'Tite',	'Tshidimbu',	'Tshisele',	'Tshitangu',	'Obenge',	'Kalindula',	'Mamboleo',	'Kinkenda',	'Congo'							
                ]


                AS=dict(zip(liste_codes_AS,liste_noms_AS))
                df3['Localisation/AS'].replace(AS,inplace=True)


                # Base de donnes enquete menage
                df1=df3[df3['consentement']=="1"]
                df1=df1[df1['Type_Enquete']=='menage']
                df1=df1[df1.columns[2:]]

                # Base de données enquetes coopératives
                # df2=df3[df3['consentement']=="1"]
                df2=df3[df3['Type_Enquete']=='cooperative']
                df2=df2.loc[:,df2.columns.str.startswith('state_name')|df2.columns.str.startswith('Localisation') | df2.columns.str.startswith('gCV') | df2.columns.str.startswith('periode') | df2.columns.str.startswith('semestre')]
                df2.loc[:,df2.columns.str.contains('nbre') | df2.columns.str.contains('chiffre') ]=df2.loc[:,df2.columns.str.contains('nbre') | df2.columns.str.contains('chiffre') ].apply(pd.to_numeric)

                df2['Nbre Membres']=pd.to_numeric(df2['gCV/nbredehomme'])+ pd.to_numeric(df2['gCV/nbredefemme'])
                df2['Nbre Salaries']=pd.to_numeric(df2['gCV/nbres_salaries_hommes'])+ pd.to_numeric(df2['gCV/nbres_salaries_femmes'])
                df2['Nbre Commite de gestion']=pd.to_numeric(df2['gCV/nbredehommegest'])+ pd.to_numeric(df2['gCV/nbredefemmegest'])


                df2['Pourcentage de femmes membres de cooperatives']= pd.to_numeric(df2['gCV/nbredefemme'])/pd.to_numeric(df2['Nbre Membres'])*100
                df2['Pourcentage de femmes salariées  de cooperatives']= pd.to_numeric(df2['gCV/nbres_salaries_femmes'])/pd.to_numeric(df2['Nbre Salaries'])*100
                df2['Pourcentage de femmes dans les organes de decision']= pd.to_numeric(df2['gCV/nbredefemmegest'])/pd.to_numeric(df2['Nbre Commite de gestion'])*100

                df2.rename(columns={'periode':'year',"Localisation/Territoire": "Territoire"}, inplace=True)
                year1=[]
                for row in df2['year']:
                    date = row
                    datem = datetime. datetime. strptime(date, "%Y-%m-%d")
                    year1.append(datem.year)
                df2['year']=year1
                ##### END CONSENTEMENT


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

                ## SCORE DE CONSOMMATION ALIMENTAIRE
                df1.loc[:,df1.columns.str.startswith('gCA/gSCA')]=df1.loc[:,df1.columns.str.startswith('gCA/gSCA')].apply(pd.to_numeric) 
                # df1['Score de Consommation Alimentaire']=3*df1['gCA/gSCA/cerealtubercul']+2*df1['gCA/gSCA/oleagineuxetleg']+2*df1['gCA/gSCA/legume']+df1['gCA/gSCA/fruits']+4*df1['gCA/gSCA/proteinesanimal']+0.5*df1['gCA/gSCA/sucreprodsucr']+df1['gCA/gSCA/produitslaitiers']+0.5*df1['gCA/gSCA/huilegraisse']


                ####################################ENQUETE RELATIVE AU MENAGE###############################################
                # Indice de score de consommation
                # df1.loc[:, df1.columns.str.startswith('gCA/gSCA')].columns
                df1['Score de Consommation Alimentaire']=3*df1['gCA/gSCA/cerealtubercul']+2*df1['gCA/gSCA/oleagineuxetleg']+2*df1['gCA/gSCA/legume']+df1['gCA/gSCA/fruits']+4*df1['gCA/gSCA/proteinesanimal']+0.5*df1['gCA/gSCA/sucreprodsucr']+df1['gCA/gSCA/produitslaitiers']+0.5*df1['gCA/gSCA/huilegraisse']

                # Indice de Strategie de Survie
                df1.rename(columns={'gCA/Indice_Strategie_Survie': 'Indice de Strategie de Survie'}, inplace=True)
                df1['Indice de Strategie de Survie']=pd.to_numeric(df1['Indice de Strategie de Survie'])
                # st.write(df1['Indice de Strategie de Survie'])
                # # Score de faim dans le ménage
                df1['Indice de Faim dans de menage']=df1[['gCA/gIDF/NombreAAlim','gCA/gIDF/nbrefdormaff','gCA/gIDF/nbrejnsansmang']].sum(axis=1)

                # Indice de participation de la femme dans le ménage
                df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')]=df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')].replace([1.0,2.0,3.0,4.0],[1,0,0.5,0])
                df1['Indice_Participation_femme']=df1.loc[:, df1.columns.str.startswith('Genre/gIPF/')].sum(axis=1)/7

                ## SCORE DE FAIM DANS LE MENAGE
                df1['gCA/gIDF/NombreAAlim'].replace([1,2,3],['rarement','parfois','souvent'], inplace=True)
                df1['gCA/gIDF/nbrefdormaff'].replace([1,2,3],['rarement','parfois','souvent'], inplace=True)
                df1['gCA/gIDF/nbrejnsansmang'].replace([1,2,3],['rarement','parfois','souvent'], inplace=True)

                df1.loc[:,df1.columns.str.startswith("'gCA/gIDF/n")].replace(['rarement','parfois','souvent'],[1,1,2], inplace=True)

                df1['gCA/gIDF/NombreAAlim'].replace(['rarement','parfois','souvent'],[1,1,2],inplace=True)
                df1['gCA/gIDF/nbrefdormaff'].replace(['rarement','parfois','souvent'],[1,1,2],inplace=True)
                df1['gCA/gIDF/nbrejnsansmang'].replace(['rarement','parfois','souvent'],[1,1,2],inplace=True)
                df1[['gCA/gIDF/NombreAAlim','gCA/gIDF/nbrefdormaff','gCA/gIDF/nbrejnsansmang']]=df1[['gCA/gIDF/NombreAAlim','gCA/gIDF/nbrefdormaff','gCA/gIDF/nbrejnsansmang']].apply(pd.to_numeric)
                df1['Indice de Faim dans de menage']=df1[['gCA/gIDF/NombreAAlim','gCA/gIDF/nbrefdormaff','gCA/gIDF/nbrejnsansmang']].sum(axis=1)


                ## GENRE ET INCLUSION DE LA FEMME
                # Indice de participation de la femme dans le ménage
                df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')]=df1.iloc[:,df1.columns.str.startswith('Genre/gIPF/')].replace(['1','2','3','4'],[1,0,0.5,0])
                df1['Indice_Participation_femme']=df1.loc[:, df1.columns.str.startswith('Genre/gIPF/')].sum(axis=1)/7


                # AUTONOMISATON DE LA FEMME
                Auto=df1.loc[:,df1.columns.str.startswith('Genre/gASE/')]
                #Auto

                for column in Auto.columns:
                    Auto.loc[Auto[column]=='oui', column]=1
                    Auto.loc[Auto[column]=='non', column]=0
                    Auto.loc[Auto[column]=='daccc_asser_1', column]=1
                    Auto.loc[Auto[column]=='daccc_asser_2', column]=0
                    Auto.loc[Auto[column]=='beaucoup_de_temps', column]=3
                    Auto.loc[Auto[column]=='dutemps', column]=2
                    Auto.loc[Auto[column]=='trespeudetemps', column]=1
                    Auto.loc[Auto[column]=='pasdetemps', column]=0
                Auto['Genre/gASE/quidecidesirevfem']=np.where(Auto['Genre/gASE/gain6lastmont']==0,0,Auto['Genre/gASE/quidecidesirevfem'])
                Auto=Auto.dropna(axis=0)
                def Converter_to_numeric(dataframe):
                    for column in dataframe.columns:
                        dataframe[column]=pd.to_numeric(dataframe[column])
                    return dataframe

                Auto=Converter_to_numeric(Auto)
                Auto[['Genre/gASE/quidecidesirevfem','Genre/gASE/decisiontypetrav','Genre/gASE/qudeciderevhom']]=Auto[['Genre/gASE/quidecidesirevfem','Genre/gASE/decisiontypetrav','Genre/gASE/qudeciderevhom']].replace({1:1,2:0,3:0.5,4:0})
                Auto['Indice de participation Socioéconomique']=Auto.sum(axis=1)/9

                df1['Genre/gASE/gain6lastmont'].replace({'oui':1,'non':0}, inplace=True)
                df1['Genre/gASE/utilisationdesourcefemme'].replace({'oui':1,'non':0}, inplace=True)
                df1['Genre/gASE/competencedefemme'].replace({'daccc_asser_1':1,'daccc_asser_2':0}, inplace=True)
                df1['Genre/gASE/disponibinitefemme'].replace(['beaucoup_de_temps','dutemps','trespeudetemps','pasdetemps'],[1,1,0,0], inplace=True)
                df1['Genre/gASE/quidecidesirevfem'].replace([1,2,3,4], [1,0,0.5,0], inplace=True)
                df1['Genre/gASE/decisiontypetrav'].replace([1,2,3,4], [1,0,0.5,0], inplace=True)
                df1['Genre/gASE/qudeciderevhom'].replace([1,2,3,4], [1,0,1,0], inplace=True)
                df1['Indice d\'autonominsationn de la femme']=df1.loc[:,df1.columns.str.startswith('Genre/gASE/')].sum(axis=1,numeric_only=True)/9 

                ## ENVIRONNEMENT ET  WASH
                ### CHARBON ET BIOCHAR

                df1['unite_charbon']=df1['gEEHA/quantitecharbon/gQcharbon/unite_braise'].replace(['sac','sachet','bassin','seau'],[1,1/50,1/15,1/18])
                df1['unite_biochar']=df1['gEEHA/quantitecharbon/gQcharbon/unite_biochar'].replace(['sac','sachet','bassin','seau'],[1,1/50,1/15,1/18])

                df1[['unite_charbon','gEEHA/quantitecharbon/gQcharbon/Quantite_braise_consommee','unite_biochar','gEEHA/quantitecharbon/gQcharbon/Quantite_biochar']]=df1[['unite_charbon','gEEHA/quantitecharbon/gQcharbon/Quantite_braise_consommee','unite_biochar','gEEHA/quantitecharbon/gQcharbon/Quantite_biochar']].apply(pd.to_numeric)

                df1['Quantite de Charbon']=df1['unite_charbon']*df1['gEEHA/quantitecharbon/gQcharbon/Quantite_braise_consommee']*60
                df1['Quantite de Biochar']=df1['unite_biochar']*df1['gEEHA/quantitecharbon/gQcharbon/Quantite_biochar']*40

                ### ACCES A L'EAU
                df1['accès à une source d’eau potable à moins de 30 min']=df1['IPM/IPM_6'].replace([0,1],[1,0])
                df1['accès à une source d’eau potable à moins de 30 min']=pd.to_numeric(df1['accès à une source d’eau potable à moins de 30 min'])

                ## LAVAGE DE MAIN
                mains=[]
                for row in df1['gEEHA/lavagedemains']:
                    mains.append(row.split(' '))
                df1['gEEHA/lavagedemains']=mains
                lav1=[]
                for row in df1['gEEHA/lavagedemains']:
                    if len(row)>=3:
                        lav1.append(1)
                    else:
                        lav1.append(0)
                df1['Indice de Lavage de mains au moins à trois moments'] =lav1


                ## ECONOMIE ET RESILIENCE
                # Index de Résilience
                # df1.loc[:, df1.columns.str.startswith(('Exposition_Choc/Recuperartion','Exposition_Choc/urgence'))]
                df1['Exposition_Choc/Recuperartion']=df1['Exposition_Choc/Recuperartion'].replace(['a','b','c','d'],[1,2,3,4])
                df1['Exposition_Choc/urgence']=df1['Exposition_Choc/urgence'].replace(['a','b','c','d','e','f'],[3,2,1,0,0,0])
                df1.loc[:, df1.columns.str.startswith(('Exposition_Choc/Recuperartion','Exposition_Choc/urgence'))].fillna(0)
                df1['Indice de résilience']=df1.loc[:, df1.columns.str.startswith(('Exposition_Choc/Recuperartion','Exposition_Choc/urgence'))].sum(axis=1)



                #EXPOSITION AU CHOCS 

                df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')]=df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')].fillna(0)
                df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')]=df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')].apply(pd.to_numeric)
                df1["Indice d'exposition aux chocs"]=df1.loc[:, df1.columns.str.startswith('Exposition_Choc/Impact_de_chocs/')].sum(axis=1)/32


                # Indice de Pauvrété Multidimentionnelle

                GroupeIPM=df1.loc[:,df1.columns.str.startswith('IPM')]

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

                df1['Source energie eclairage']=df1['IPM/Nature_energie_eclairage'].replace(['a','b'],['Lampe à pile/ pétrole/ bougie/ lampe a pétrole, Coleman','Electricité/ groupe électrogène/ gaz/ système solaire'])
                df1['IPM/Nature_energie_eclairage']=np.where(df1['IPM/Nature_energie_eclairage']=='a', 1/24,0)

                Actifs_Bien_de_base=[]
                for row in df1['IPM/Actifs_Bien_de_base']:
                    Actifs_Bien_de_base.append(row.split(' '))
                df1['IPM/Actifs_Bien_de_base']=Actifs_Bien_de_base
                Act1=[]
                for row in df1['IPM/Actifs_Bien_de_base']:
                    Act1.append(len(row))
                df1["Assets_base"]=Act1

                Actifs_Bien_de_luxe=[]
                for row in df1['IPM/Actifs_Bien_de_distinction']:
                    Actifs_Bien_de_luxe.append(row.split(' '))
                
                df1["Assets_distinction"]=Actifs_Bien_de_luxe
                Act2=[]
                for row in df1["Assets_distinction"]:
                    if "d" in row:
                        Act2.append(0)
                    else:
                        Act2.append(len(row))
                df1["Assets_distinction"]=Act2
                df1['Assets']=np.where((df1['Assets_base']>=2) & (df1['Assets_distinction']>=1),1/24,0)

                df1['IPM/Nature_energie_eclairage']=np.where(df1['IPM/Nature_energie_eclairage']=='a',1/24,0)
                df1['IPM/IPM_6']=np.where(df1['IPM/IPM_6']=='1',1/24,0)
                df1['Acces eau potable par le ménage']=df1['IPM/IPM_6']
                df1['IPM/Plancher']=np.where(df1['IPM/Plancher']=='a',1/24,0)
                df1['IPM/mur']=np.where(df1['IPM/mur']=='a',1/24,0)
                df1['IPM/mur']=np.where(df1['IPM/mur']=='a',1/24,0)

                df1['Energie_cuisson']=df1['gEEHA/sourcedenergie']
                df1['Energie_cuisson']=df1['Energie_cuisson'].replace({'braise':1/24,'bois':1/24,'biochar':0,'electricite':0,'gas':0})


                # df1['Energie_cuisson']=df1['gEEHA/sourcedenergie']
                # df1['Source energe cuisson']=df1['gEEHA/sourcedenergie']
                # df1['Energie_cuisson']=df1['Energie_cuisson'].replace({'braise':1/24,'bois':1/24,'biochar':0,'electricite':0})


                df1[['IPM/eau/nbre_bidons_2_5_litres_utilises','IPM/eau/nbre_bidons_5_litres_utilises','IPM/eau/nbre_bidons_10_litres_utilises','IPM/eau/nbre_bidons_20_litres_utilises','renseignement_generaux/Taille_menage']]=df1[['IPM/eau/nbre_bidons_2_5_litres_utilises','IPM/eau/nbre_bidons_5_litres_utilises','IPM/eau/nbre_bidons_10_litres_utilises','IPM/eau/nbre_bidons_20_litres_utilises','renseignement_generaux/Taille_menage']].apply(pd.to_numeric)

                df1['IPM/eau/nbre_bidons_2_5_litres_utilises']=df1['IPM/eau/nbre_bidons_2_5_litres_utilises']*2.5
                df1['IPM/eau/nbre_bidons_5_litres_utilises']=df1['IPM/eau/nbre_bidons_5_litres_utilises']*5
                df1['IPM/eau/nbre_bidons_10_litres_utilises']=df1['IPM/eau/nbre_bidons_10_litres_utilises']*10
                df1['IPM/eau/nbre_bidons_20_litres_utilises']=df1['IPM/eau/nbre_bidons_2_5_litres_utilises']*20

                df1.loc[:,df1.columns.str.endswith('_litres_utilises')]=Converter_to_numeric(df1.loc[:,df1.columns.str.endswith('_litres_utilises')])

                df1['Quantite_eau_par_personne']=df1.loc[:,df1.columns.str.endswith('_litres_utilises')].sum(axis=1)
                df1['Taille_menage']=df1['renseignement_generaux/Taille_menage']
                df1['Quantite_eau_par_personne']=df1['Quantite_eau_par_personne']/df1['Taille_menage']
                df1['Acces_eau_qte_suffisante']=np.where(df1['Quantite_eau_par_personne']<20,1/24,0)

                #IPM
                df1['Indice de Pauvrete Multidimentionnelle']=df1.loc[:,df1.columns.str.contains('IPM_')].sum(axis=1) +df1[['Acces_eau_qte_suffisante','IPM/Plancher','IPM/mur','Energie_cuisson','Assets']].sum(axis=1,numeric_only=True)
                # df1['Indice de Pauvrete Multidimentionnelle']

                ### COHESION SOCIAL & STABILISATION

                ## SCORE IDENTIFICATION 
                df1['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se'].replace([4,3,2,1,1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/Relation_interpersonnelles/membre_de_votre_groupe_ethniuqe'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/Relation_interpersonnelles/membre_des_autres_groupes_ethniques'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/frequentation_interpersonnelle/Participer_a_des_ceremonies_culturelles'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/frequentation_interpersonnelle/Se_rendre_a_la_meme_eglise_ou_autre_lieu_de_culte'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/frequentation_interpersonnelle/Se_marier_entre_eux'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/Perception_interperonnelles/niveau_violence'].replace(['4','3','2','1'],['1','2','3','4'], inplace=True)
                df1['CS/Dim1/Perception_interperonnelles/niveau_violence'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)
                df1['CS/Dim1/Perception_interperonnelles/niveau_paresse'].replace(['4','3','2','1',1,99,'99'],[1,1,0,0,0,np.NaN,np.NaN], inplace=True)



                df1['Score Identification']=df1[['CS/Dim1/Relation_interpersonnelles/Parent_enfants_epoux_se','CS/Dim1/Relation_interpersonnelles/membre_de_votre_groupe_ethniuqe',
                                                'CS/Dim1/Relation_interpersonnelles/membre_des_autres_groupes_ethniques','CS/Dim1/frequentation_interpersonnelle/Participer_a_des_ceremonies_culturelles',
                                                'CS/Dim1/frequentation_interpersonnelle/Se_rendre_a_la_meme_eglise_ou_autre_lieu_de_culte',  'CS/Dim1/frequentation_interpersonnelle/Se_marier_entre_eux',
                                                'CS/Dim1/Perception_interperonnelles/niveau_violence','CS/Dim1/Perception_interperonnelles/niveau_paresse'
                                                ]].sum(axis=1,numeric_only=True)

                df1['Score Identification1']=df1['Score Identification']/8/9

                ## CONFIANCE MUTUELLE

                df1['CS/Confiance_mutuelle/Membre_de_votre_famille'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Confiance_mutuelle/Membre_de_votre_communaute'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)

                df1['Score Confiance Mutuelle']=df1.loc[:,df1.columns.str.contains('CS/Confiance_mutuelle/')].sum(axis=1)
                df1['Score Confiance Mutuelle1']=df1['Score Confiance Mutuelle']/9/3

                ## CONFIANCE INSTITUTION

                df1['CS/Confiance_institutions/Autorites_locales'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Confiance_institutions/Autorites_provinciales'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Confiance_institutions/Autorites_nationales'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['Score Confiance Institution']=df1.loc[:,df1.columns.str.startswith('CS/Confiance_institutions')].sum(axis=1)
                df1['Score Confiance Institution1']=df1['Score Confiance Institution']/3/9

                ## SENTIMENT CORRECT REPRESENTATION 

                df1['CS/Sentiment_Correcte_Representation/nationale'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Sentiment_Correcte_Representation/provinciale'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN],inplace=True)
                df1['CS/Sentiment_Correcte_Representation/locale'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN],inplace=True)
                df1['Score Correcte Representation']=df1.loc[:,df1.columns.str.startswith('CS/Sentiment_Correcte_Representation/')].sum(axis=1)
                df1['Score Correcte Representation1']=df1['Score Correcte Representation']/3/9

                ##ABESENCE DE CORRUPTION

                df1['CS/Absence_de_corruption/nationale_001'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Absence_de_corruption/provinciale_001'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Absence_de_corruption/locale_001'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['Score Absence Corruption']=df1.loc[:,df1.columns.str.startswith('CS/Absence_de_corruption')].sum(axis=1)
                df1['Score Absence Corruption1']=df1['Score Absence Corruption']/3/9


                ## PARTICIPATION CITOYENNE

                df1['CS/Participation_Citoyenne/Participation_Manifestation_publique'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Participation_Citoyenne/Participation_Activite_Developpement'].replace(['1','0','99'],[1,0,np.NaN], inplace=True)
                df1['CS/Participation_Citoyenne/membre_organisation_SOCIV'].replace(['0','1','99'],[0,1,np.NaN],inplace=True)
                df1['Score Participation_Citoyenne']=df1.loc[:,df1.columns.str.startswith('CS/Participation_Citoyenne')].sum(axis=1,numeric_only=True)
                df1['Score Participation_Citoyenne1']=df1['Score Participation_Citoyenne']/3/9

                ## SECURITE HUMAINE

                df1['CS/Securite_humaine/Niveau_accord_que_Excombatants_insecurise'].replace(['a','b','c','d','e'],[5,4,3,2,1], inplace=True)
                df1['CS/Securite_humaine/Perspective_securite_future'].replace(['1','2','3','99'],[3,1,2,np.NaN], inplace=True)
                df1['CS/Securite_humaine/crainte_attaque'].replace(['1','2','3','4','99'],[4,3,2,1,np.NaN])

                df1['CS/Securite_humaine/Jour'].replace(['5','4','3','2','1','99'],[1,1,0,0,0,np.NaN], inplace=True)
                df1['CS/Securite_humaine/Aller_Quartier_a_un_autre'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN], inplace=True)
                df1['CS/Securite_humaine/niveau_violence_001'].replace(['5','4','3','2','1','99'],[1,1,0,0,0,np.NaN],inplace=True)
                df1['CS/Securite_humaine/crainte_attaque'].replace(['4','3','2','1','99'],[1,1,0,0,np.NaN],inplace=True)

                df1['Score Securite humaine']=df1[['CS/Securite_humaine/Jour','CS/Securite_humaine/Aller_Quartier_a_un_autre',
                                                'CS/Securite_humaine/niveau_violence_001','CS/Securite_humaine/crainte_attaque'
                                                ]].sum(axis=1)
                df1['Score Securite humaine1']=df1['Score Securite humaine']/4/9

                ## SATISFACTION VIE CIVIQUE 

                df1['CS/Satisfaction_Vie_Civique/Acces_physique_tribunaux'].replace('99',np.NaN, inplace=True)
                df1['CS/Satisfaction_Vie_Civique/Accees_systeme_judiciaire'].replace(['99'],[np.NaN], inplace=True)
                df1['CS/Satisfaction_Vie_Civique/Niveau_Accord_Equite_Justice'].replace(['a','b','c','d','e',],[5,4,3,2,1], inplace=True) 
                df1['CS/Satisfaction_Vie_Civique/Niveau_de_confiance_dans_la_justice'].replace(['a','b','c','d','e','f','g'],[6,5,4,3,2,1,np.NaN], inplace=True) # revision de la codification
                df1['CS/Satisfaction_Vie_Civique/Securite'].replace(['4','3','2','1'],[1,1,0,0], inplace=True) 
                df1['CS/Satisfaction_Vie_Civique/Niveau_Accord_Equite_Justice'].replace(['5','4','3','2','1'],[1,1,0,0,0], inplace=True) 
                df1['CS/Satisfaction_Vie_Civique/Resolution_conflit'].replace(['4','3','2','1'],[1,1,0,0], inplace=True) 
                df1['CS/Satisfaction_Vie_Civique/SSP'].replace(['4','3','2','1'],[1,1,0,0], inplace=True) 

                df1['Score satisfaction vie civique']=df1[['CS/Satisfaction_Vie_Civique/Securite','CS/Satisfaction_Vie_Civique/Niveau_Accord_Equite_Justice',
                                                        'CS/Satisfaction_Vie_Civique/Resolution_conflit','CS/Satisfaction_Vie_Civique/SSP'
                                                        ]].sum(axis=1)
                df1['Score satisfaction vie civique1']=df1['Score satisfaction vie civique']/4/9

                ## SATISFACTION VIE PERSONNELLE

                df1['CS/satisfaction_vie_personnelle/vie_professionnelle'].replace(['4','3','2','1'],[1,1,0,0], inplace=True)
                df1['CS/satisfaction_vie_personnelle/etat_de_sante'].replace(['4','3','2','1'],[1,1,0,0], inplace=True)
                df1['CS/satisfaction_vie_personnelle/acces_nourriture'].replace(['4','3','2','1'],[1,1,0,0], inplace=True)
                df1['CS/satisfaction_vie_personnelle/acces_eau'].replace(['4','3','2','1'],[1,1,0,0], inplace=True)
                df1['Score satisfaction vie personnelle']=df1[['CS/satisfaction_vie_personnelle/vie_professionnelle','CS/satisfaction_vie_personnelle/etat_de_sante',
                                                            'CS/satisfaction_vie_personnelle/acces_nourriture','CS/satisfaction_vie_personnelle/acces_eau'
                                                            ]].sum(axis=1)
                df1['Score satisfaction vie personnelle1']=df1['Score satisfaction vie personnelle']/4/9
                df1['Index de Cohesion Sociale']=df1[['Score satisfaction vie personnelle1','Score satisfaction vie civique1','Score Securite humaine1',
                                                    'Score Participation_Citoyenne1','Score Confiance Institution1','Score Absence Corruption1',
                                                    'Score Correcte Representation1','Score Identification1','Score Confiance Mutuelle1'
                                                    ]].sum(axis=1)

                #####Stabilisation
                yeara=[]
                for row in df1['periode']:
                    date = row
                    datem = datetime. datetime. strptime(date, "%Y-%m-%d")
                    yeara.append(datem.year)
                df1['periode']=yeara

                # Pourcentage de personnes qui se sente en sécurité en exerçant leurs activitées quotidiennes
                df1['Sécurité en exerçant leurs activitées quotidiennes']=df1['CS/Securite_humaine/Jour'].replace(['5','4','3','2','1'],[1,1,0,0,0])
                # Pourcentage de personnes qui ont confiance en la justice
                df1['Confiance en la justice']=df1['CS/Satisfaction_Vie_Civique/Niveau_de_confiance_dans_la_justice'].replace(['5','4','3','2','1','f',5,4,3,2,1],[1,1,0,0,0,pd.NA,1,1,0,0,0])
                # Pourcentage de personnes qui pensent que les FARDC contribuent à la sécurité du milieu
                df1['Contribution de FARDC à la securite']=df1['CS/Securite_humaine/Contribution_FARDC_securite'].replace(['5','4','3','2','1'],[1,1,0,0,0])
                # Pourcentage de personnes qui pensent que la Police Contribue à la sécurisation du milieu
                df1['Contribution de la PNC à la securite']=df1['CS/Securite_humaine/Contribution_PNC_securite'].replace(['5','4','3','2','1'],[1,1,0,0,0])
                # Pourcentage de personnes qui pensent que les démobilisées contribuent à insécuriser le milieu
                df1['Les excombatants insecurisent le milieu']=df1['CS/Securite_humaine/Niveau_accord_que_Excombatants_insecurise'].replace([5,4,3,2,1],[1,1,0,0,0])
                # Pourcentage de personnes optimistes quand à la perpective d'amélioraion de condititons sécuritaires dans leur milieu
                df1['Perspectives desecurite']=df1['CS/Securite_humaine/Perspective_securite_future'].replace(['3','2','1','99',3,2,1,99],[1,0,0,pd.NA,1,0,0,np.NaN])
                # Pourcentage de personnes qui pensent que les projets de consolidation de la paix adressent les vrais problemes de la population
                df1['Projets de consolidation adressent les vaix problemes']=df1['CS/satisfaction_vie_personnelle/propjet_consolidation_paix_vrais_problemes'].replace(['5','4','3','2','1'],[1,1,0,0,0])
                # Paiement de taxes
                df1['Paiement taxe pour le securite']=df1['CS/Securite_humaine/Payer_taxe_6_derniers_mois'].replace('99',np.NaN)
                # Pourcentage de personnes qui pensent que la justice est rendue de manière équitable
                df1['Justice rendue de maniere equitable']=df1['CS/Satisfaction_Vie_Civique/Equite_justice'].replace(['4','3','2','1'],[1,1,0,0])
                # pourcentage de personnes qui percoivent que les autorités locales represnetent leurs interets
                df1['autorites locales reprensent les interets de la population']=df1['CS/Sentiment_Correcte_Representation/locale']
                # % de personnes qui pensent que les points de la population est pris en compte dans la gestion de la chose publique
                df1['Pensez-vous que vos opinions sont prises en compte dans la gestion de la chose publique']=df1['Genre/Prisen_en_compte_opinion_solution_consolidation_de_la_paix'].replace([5,4,3,2,1,99],[1,1,0,0,0,np.NaN])
                # % des personnes qui perçoivent que la gestion de leur ETD est inclusive et transparente
                df1['La gestion de ETD est transparente et inclusive']=df1['gCA/Transparence_gestion_ressources_naturelles'].replace(['5','4','3','2','1','99'],[1,1,0,0,0,np.NaN])
                # % de personnes qui perçoivent qu’ils ont un bon ou très bon accès à la terre 
                df1['Acces à la terre est bonne']=df1['gCA/Evaluation_acces_a_la_terre'].replace(['5','4','3','2','1','99','Pas bon (Pas facile);'],[1,1,0,0,0,np.NaN,0])
                # % des personnes qui perçoivent que la gestion des ressources naturelles (minières et autres) de leurs zones est transparente et bénéfique au développement de leurs milieux
                df1['La gestion de ressources naturelle est transparente']=df1['CS/Satisfaction_Vie_Civique/Gestion_ressouces_miniere_pour_le_developpement'].replace(['5','4','3','2','1','99'],[1,1,0,0,0,np.NaN])
                # % d'anciens combattants précédemment retournés dans leur communauté dans le cadre d'une activité de réintégration officielle qui ont quitté leur communauté avant un an 
                # -----------------------------------------------------------------------------------------------------------------
                # % des personnes qui ont une perception positive vis-à-vis des anciens combattants réintégrés dans la communauté 
                df1['Opinions positives vis à vis des ex combattants']=df1['CS/Securite_humaine/Niveau_accord_que_Excombatants_insecurise'].replace([5,4,3,2,1],[0,0,0,1,1])
                #  % des femmes estiment que leurs opinions se reflètent dans les solutions participatives mise en œuvre dans le cadre du processus de consolidation de la paix 
                # -----------------------------------------------------------------------------------------------------------------
                # % des femmes dans les institutions (Sénat, gouvernement, parlement) au niveau national, provincial et local.
                # -----------------------------------------------------------------------------------------------------------------
                # securite rencontre les membres d'utres groupes éthniques
                df1["securite rencontre autre groupe ethnique"]=df1['CS/Securite_humaine/Niveau_secu_rencontre_autre_groupe_ethnique'].replace(['5','4','3','2','1','99'],[1,1,0,0,0,np.NaN])
                # Pourcentage de femmes qui  sont membres de structures de resolution de confits

                # df1['gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits'] 


                df1['gCA/Poste_occupe_dans_la_structure_de_resolutuion_de_conflits'].replace(["Présidente","Vice-président","Secrétaire", "Caissière",
                                                                                            "Trésorières", "Autre à préciser" ],  [1,1,0,0,0,0], inplace=True)

                # Pilier 5 (Femme, paix et sécurité) --------------------------------------------------------------------------------------------------------------
                # Pourcentage de femmes qui sont membre d'une strcuture communautaire de résolution de conflit
                df_p5=df1[df1['gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits']=='1']
                #Pourcentage de femmes qui pensent qu'elles  sont représentées dans les instances de prise de décision et comité de structures de paix et résolution de conflit dans  leur zone zone
                df_p5['Perception de femme sur leur representation dans les instances de decision  et structures communautaires']=df_p5['gCA/Opinions_sur_representation_de_femmes_dans_les_instances_de_decision'].replace(['Moins de 15%' ,'15 à 29 %' ,'30 à 49 %', 'plus de 49%','s'],[0,0,1,1,1])
                #df_p5['gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits'].replace(['1','0','99'],[1,0,np.NaN],inplace=True)
                df_p5['Femme membre Structure Communautaire res conflit']=0
                df_p5.loc[(df_p5['renseignement_generaux/Sexe']=='F') & (df_p5['gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits']=="1"),'Femme membre Structure Communautaire res conflit']=1
                # df_p5['Femme membre Structure Communautaire res conflit']
                # Pourcentage de femmes membres de commité d'une strcuture communautaire de resolution de conflit
                df_p51=df_p5[df_p5["gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits_commite"]=="1"]
                df_p51['Femme membre du comite dans structure res conflit']=0
                # Prise en compte des opitnions de femmmes dans les solutions participatives de consolidation de la paix

                df_p51.loc[(df_p5['renseignement_generaux/Sexe']=='F') & (df_p51["gCA/Appartenance_a_une_structure_communautaire_de_resolution_de_conflits_commite"]=="1"),'Femme membre du comite dans structure res conflit']=1
                f1=pd.DataFrame(df_p5.groupby(['state_name','Localisation/Territoire','periode','semestre']).aggregate({'Femme membre Structure Communautaire res conflit':'mean',
                                                                                                                                'Genre/Prisen_en_compte_opinion_solution_consolidation_de_la_paix':'mean',
                                                                                                                                'Perception de femme sur leur representation dans les instances de decision  et structures communautaires':'mean'}))

                f1['enrolement de femmes comme membre de structure']=0
                f1.loc[f1['Femme membre Structure Communautaire res conflit']>=0.3,'enrolement de femmes comme membre de structure']=1

                f1['representation de femmes dans les strucures de prise de decision']=0
                f1.loc[f1['Perception de femme sur leur representation dans les instances de decision  et structures communautaires']>=0.3,'representation de femmes dans les strucures de prise de decision']=1

                f2=pd.DataFrame(df_p51.groupby(['state_name','Localisation/Territoire','periode','semestre']).aggregate({'Femme membre du comite dans structure res conflit':'mean'}))
                f2['representation de femmes dans les comité de structure']=0
                f2.loc[f2['Femme membre du comite dans structure res conflit']>=0.3,'representation de femmes dans les comité de structure']=1
                f=pd.concat([f1,f2],axis=1)
                f.rename(columns={'Genre/Prisen_en_compte_opinion_solution_consolidation_de_la_paix': 'Prise en compte opinions femmes solutions participatives consolidation de la paix'}, inplace=True)
                f['Pilier 5: Femme, paix et sécurité']=(f['representation de femmes dans les comité de structure']/3+f['enrolement de femmes comme membre de structure']/3+f['representation de femmes dans les strucures de prise de decision']/3)/5
                stab=['Sécurité en exerçant leurs activitées quotidiennes','Confiance en la justice','Contribution de FARDC à la securite',
                    'Contribution de la PNC à la securite','Les excombatants insecurisent le milieu','Perspectives desecurite',
                    'Projets de consolidation adressent les vaix problemes','Paiement taxe pour le securite','Justice rendue de maniere equitable',
                    'autorites locales reprensent les interets de la population','Pensez-vous que vos opinions sont prises en compte dans la gestion de la chose publique',
                    'La gestion de ETD est transparente et inclusive','Acces à la terre est bonne','La gestion de ressources naturelle est transparente',
                    'Opinions positives vis à vis des ex combattants',"securite rencontre autre groupe ethnique"
                    ]

                ids=list(df1.loc[:,df1.columns.str.startswith('renseignement_generaux/')|df1.columns.str.startswith('renseignement_generaux/Sexe') |df1.columns.str.startswith('state_name')|  df1.columns.str.startswith('Localisation')| 
                                df1.columns.str.contains('semestre') | df1.columns.str.contains('periode')].columns)
                for i in stab:
                    ids.append(i)
                output = []
                def reemovNestings(l):
                    for i in l:
                        if type(i) == list:
                            reemovNestings(i)
                        else:
                            output.append(i)
                
                reemovNestings(ids)
                all_stab=output
                Indicateurs_Stabilisation=df1[all_stab]
                Indicateurs_Stabilisation[['Projets de consolidation adressent les vaix problemes','autorites locales reprensent les interets de la population','La gestion de ressources naturelle est transparente',
                'Pensez-vous que vos opinions sont prises en compte dans la gestion de la chose publique','Perspectives desecurite','Sécurité en exerçant leurs activitées quotidiennes','Contribution de FARDC à la securite','Contribution de la PNC à la securite','Paiement taxe pour le securite','La gestion de ETD est transparente et inclusive']]=Indicateurs_Stabilisation[['Projets de consolidation adressent les vaix problemes','autorites locales reprensent les interets de la population','La gestion de ressources naturelle est transparente',
                'Pensez-vous que vos opinions sont prises en compte dans la gestion de la chose publique','Perspectives desecurite','Sécurité en exerçant leurs activitées quotidiennes','Contribution de FARDC à la securite','Contribution de la PNC à la securite','Paiement taxe pour le securite','La gestion de ETD est transparente et inclusive']].apply(pd.to_numeric)
                Indicateurs_Stabilisation['Pilier 1 : DIALOGUE DEMOCRATIQUE']=Indicateurs_Stabilisation['Projets de consolidation adressent les vaix problemes']/5
                Indicateurs_Stabilisation['Pilier 2 : SECURITE']=(Indicateurs_Stabilisation['Perspectives desecurite']/5+Indicateurs_Stabilisation['Sécurité en exerçant leurs activitées quotidiennes']/5+Indicateurs_Stabilisation['Contribution de FARDC à la securite']/5+Indicateurs_Stabilisation['Contribution de la PNC à la securite']/5+Indicateurs_Stabilisation['Paiement taxe pour le securite']/5)/5
                Indicateurs_Stabilisation['Pilier-3 : RAE-Justicce']=((Indicateurs_Stabilisation['Confiance en la justice']/2+Indicateurs_Stabilisation['Justice rendue de maniere equitable']/2)/3)/5
                Indicateurs_Stabilisation['Pilier-3 : RAE-Gouvernance']=((Indicateurs_Stabilisation['autorites locales reprensent les interets de la population']/3+Indicateurs_Stabilisation['Pensez-vous que vos opinions sont prises en compte dans la gestion de la chose publique']/3+Indicateurs_Stabilisation['La gestion de ETD est transparente et inclusive']/3)/3)/5
                Indicateurs_Stabilisation['Pilier-3 : RAE-Ressources naturelles']=((Indicateurs_Stabilisation['Acces à la terre est bonne']/2+Indicateurs_Stabilisation['La gestion de ressources naturelle est transparente']/2)/3)/5
                Indicateurs_Stabilisation['Pilier 3 : RAE']=Indicateurs_Stabilisation.loc[:,Indicateurs_Stabilisation.columns.str.startswith('Pilier-3')].sum(axis=1)
                Indicateurs_Stabilisation['Pilier 4 : RETOUR, RÉINTÉGRATION ET RELÈVEMENT SOCIOÉCONOMIQUE (RRR)']=((Indicateurs_Stabilisation['Opinions positives vis à vis des ex combattants']/2+Indicateurs_Stabilisation["securite rencontre autre groupe ethnique"]/2)/3)/5
                # Indicateurs_Stabilisation['Pilier 5 : FEMMES, PAIX ET SECURITE']
                Indicateurs_Stabilisation.rename(columns={'Localisation/Province': 'state_name'},inplace=True)
                Indicateurs_Stabilisation["periode"]=Indicateurs_Stabilisation["periode"].astype(str)
                a=pd.DataFrame(Indicateurs_Stabilisation.groupby(['state_name','Localisation/Territoire','periode','semestre'],
                                                as_index=True)['Sécurité en exerçant leurs activitées quotidiennes'].count())    # Nombre des individus pas territore pour une période donnée
                a.rename(columns={'Sécurité en exerçant leurs activitées quotidiennes':'Effectifs'}, inplace=True)
                # Indicateurs_Stabilisation["periode"]=Indicateurs_Stabilisation["periode"].astype(str)
                b=pd.DataFrame(Indicateurs_Stabilisation.groupby(['state_name','Localisation/Territoire','periode','semestre'],
                                                as_index=True).aggregate('mean',numeric_only=True))
                code=pd.concat([a,b],axis=1)
                d=pd.concat([code,f],axis=1)
                d['Indice de Stabilisation']=d.loc[:,d.columns.str.contains('Pilier ')].sum(axis=1) # Calcul de l'index de stabilisation au niveau de territoires
                d.reset_index(inplace=True)
                d.rename(columns={"Localisation/Territoire":"Territoire","periode":"year"},inplace=True)
                d["year"]=d["year"].astype(int)
                # d

                # st.write(Indicateurs_Stabilisation.head())
                # st.write(df1.head())
                # st.write(df1.head())




                # st.write(df1.head())
                # ASSEMBLAGE DES INDICATEUR  base de données UNIQUES POUR LES MENAGES
                Indicateurs_Data=df1.loc[:, df1.columns.str.startswith('periode')|df1.columns.str.startswith('semestre')|df1.columns.str.startswith('renseignement_generaux/') | df1.columns.str.startswith('Score') | df1.columns.str.startswith('Score') | df1.columns.str.startswith('Indice') | df1.columns.str.startswith('Index') | df1.columns.str.startswith('Quantit') | df1.columns.str.startswith('Localisation') | df1.columns.str.startswith('state')|df1.columns.str.startswith('accès à une source d’eau potable à moins de 30 min')|df1.columns.str.startswith('Indice de Strategie de Survie')|df1.columns.str.startswith('Score de Consommation Alimentaire')]
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
                # st.write(Indicateurs_Data.columns.to_list())
                # year=[]
                # for row in Indicateurs_Data['year']:
                #     date = row
                #     datem = datetime. datetime. strptime(date, "%Y-%m-%d")
                #     year.append(datem.year)
                # Indicateurs_Data['year']=year
                Indicateurs_Data["Territoire"]=Indicateurs_Data["Territoire"].values.astype(str)
                # Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=np.where(Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=='non',0,1)
                Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"]=Indicateurs_Data["Indice de Lavage de mains au moins à trois moments"].replace(['Oui','Non'],[1,0])
                Indicateurs_Data["Sexe"]=Indicateurs_Data["Sexe"].replace(['F','M'],['Femme','Homme'])
                # A augmenter 
                Indicateurs_Data['Profession'].replace([1,2,3,4,5,6,7,8,9,10,11],["Agri-Peche-Elev","Commerce","Act. Minier","Agent Hum",'Menager','enseignant','Agent etat','Inf,Med,jurist', 'LR','Autres','Aucune'],inplace=True)
                # Indicateurs_Data["Profession"].replace([1,2],["Agri-Peche-Elev","Commerce"],inplace=True)

                Indicateurs_Data['Etat Civil'].replace([1,2,3],["Celibataires","Marié(e)s","Divorcés"],inplace=True)
                # Indicateurs_Data['semestre']=Indicateurs_Data["semestre"].replace(['Semestre1','Semestre2'],['S1','S2'])s
                df20=Indicateurs_Data
                # st.write(df20)
                Indicateurs_Data['Score de Consommation Alimentaire']=pd.to_numeric(Indicateurs_Data['Score de Consommation Alimentaire'])
                #### CHAINE DE VALEUR PAR SPECULATION
                dfparchain=Indicateurs_Data.loc[:,Indicateurs_Data.columns.str.startswith('year')|Indicateurs_Data.columns.str.startswith('semestre')|Indicateurs_Data.columns.str.startswith('state_name')|Indicateurs_Data.columns.str.startswith('Chaine de Valeur Principale')|Indicateurs_Data.columns.str.startswith('Indice de Pauvrete Multidimentionnelle')]
                dfparchain=dfparchain.groupby(['year','semestre','state_name','Chaine de Valeur Principale'])['Indice de Pauvrete Multidimentionnelle'].mean()
                dfparchain=pd.DataFrame(dfparchain)
                dfparchain.reset_index(inplace=True)
                nn={'Indice de Pauvrete Multidimentionnelle':"IPM PAR SPECULATION"}
                dfparchain.rename(columns=nn, inplace=True)

                def Compute_mean(df_col):
                    return df_col.mean()
                #############################
                ###################Creating the dataset for Household study
                # ############################################??????????????????<>
                dfinal=df20.drop(['Zone de Santé', 'Aire de Santé', 'Residence', 'Qualite du repondant','Chaine de Valeur Principale'],axis=1)

                dfinal[['year', 'state_name', 'Etat Civil','Tranche d\' age']] = dfinal[['year', 'state_name', 'Etat Civil','Tranche d\' age']]. astype(str)


                menage=dfinal.groupby(['semestre','Territoire','year','state_name'])['Taille du menage'].sum()
                # menage.values

                # Get FInal data to Be used
                df_transf1=dfinal.groupby(['semestre','Territoire','year','state_name']).mean(1)
                df_transf1.reset_index(inplace=True)
                new_order=[2,0,3,1]
                new_order.extend(range(4,len(df_transf1.columns.tolist())))
                df_transf1=df_transf1[df_transf1.columns[new_order]]
                df_transf1['Taille du menage']=menage.values

                df=df_transf1.round(decimals = 2)
                df['year']=df['year'].astype(int)
                df["Quantite de Charbon"]=df1["Quantite de Charbon"]/df["Taille du menage"]
                df['Quantite de Biochar']=df['Quantite de Biochar']/df["Taille du menage"]
                # st.write(df)

                var_drop=list(df22.loc[:,df22.columns.str.startswith('_')].columns)
                df22.drop(var_drop, axis=1, inplace=True)
                df22.drop('meta/instanceID', axis=1, inplace=True)

                # Relation avec les fournisseurs de l'aide

                df22['Le % des personnes  qui sentent que les acteurs humanitaires les traitent avec respect']=df22['Relation_Fournisseur/Traiter_avec_respect'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                        [0,0,0,1,1])
                #df22['rf1']=np.where(df22['Le % des personnes  qui sentent que les acteurs humanitaires les traitent avec respect']==1,1/15,0)
                df22['rf1']=df22['Le % des personnes  qui sentent que les acteurs humanitaires les traitent avec respect'].replace([1,0],[1/15,0])
                df22['Le % des personnes affectées qui pensent que leurs opinions sont prises en compte dans les prises de décisions humanitaires']=df22['Relation_Fournisseur/Prise_en_compte_de_points_de_vue'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                                        [0,0,0,1,1])
                df22['rf2']=df22['Le % des personnes affectées qui pensent que leurs opinions sont prises en compte dans les prises de décisions humanitaires'].replace([1,0],[1/15,0])
                df22['Le % des personnes satisfaites par le comportement des agents humaniataires']=df22['Relation_Fournisseur/Satisfaction_comportement_de_travailleurs_humanitaires'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['rf3']=df22['Le % des personnes satisfaites par le comportement des agents humaniataires'].replace([1,0],[1/15,0])
                df22['i-relation avec le fournissaire aide humanitaire']=df22.loc[:,df22.columns.str.startswith('rf')].sum(axis=1)

                # Qualité d'assistance hummanitaire
                df22['Le % des personnes affectées qui considèrent que leurs besoins essentiels sont couverts par l’assistance']=df22['Qualite_de_l_assistance/Couverture_besoins'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['qah1']=df22['Le % des personnes affectées qui considèrent que leurs besoins essentiels sont couverts par l’assistance'].replace([1,0],[1/15,0])
                df22['Le % des personnes affectées qui considèrent que l’assistance arrive au moment où elles en ont le plus besoin']=df22['Qualite_de_l_assistance/Bon_moment_arrive_de_l_aide'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])

                df22['qah2']=df22['Le % des personnes affectées qui considèrent que l’assistance arrive au moment où elles en ont le plus besoin'].replace([1,0],[1/15,0])
                df22['Le % des personnes affectées qui vendent des biens reçus des organisations humanitaires afin de couvrir leurs besoins essentiels']=df22['Qualite_de_l_assistance/Vente_de_biens_recu_par_les_membre_de_la_communaute'].replace(['Oui','Non',"Ne sait pas"],[0,1,np.NaN])
                df22['qah3']=df22['Le % des personnes affectées qui vendent des biens reçus des organisations humanitaires afin de couvrir leurs besoins essentiels'].replace([1,0],[1/15,0])
                df22['i-qualite assistance humanitaire']=df22.loc[:,df22.columns.str.startswith('qah')].sum(axis=1,skipna=False)

                # resilience et retablissement de moyens de subsistances
                df22['Le % des personnes affectées qui pensent que l’assistance qu’elles reçoivent leur permet d’améliorer leurs conditions de vie']=df22['Resilience/Amelioration_conditions_de_vie_grace_assistance'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['rrms1']=df22['Le % des personnes affectées qui pensent que l’assistance qu’elles reçoivent leur permet d’améliorer leurs conditions de vie'].replace([1,0],[1/25,0])
                df22['Le % des personnes affectées qui sentent que l’assistance qu’elles reçoivent les prépare à l’autonomie']=df22['Resilience/Perception_autonomisation_suite_assistance'].replace(['Oui',"Non","Ne sait pas"],[1,0,np.NaN])
                df22['rrms2']=df22['Le % des personnes affectées qui sentent que l’assistance qu’elles reçoivent les prépare à l’autonomie'].replace([1,0],[1/20,0])
                df22['% des personnes interrogées pensent qu’elles peuvent gagner leurs vies en travaillant dans l’économie locale.']=df22['Resilience/Gagner_la_vie_en_exercant_une_activite_economique_local'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['rrms3']=df22['% des personnes interrogées pensent qu’elles peuvent gagner leurs vies en travaillant dans l’économie locale.'].replace([1,0],[1/20,0])
                df22['% de personnes affectées qui déclarent que l’aide humanitaire reçue n’a pas provoqué de hausse de prix considérable sur le marché local1']=df22['Resilience/Consideration_inflation'].replace(['Très considérable','Considérable','Pas considérable'],
                                                                                                                                                                                                                [0,0,1])
                df22['rrms41']=df22['% de personnes affectées qui déclarent que l’aide humanitaire reçue n’a pas provoqué de hausse de prix considérable sur le marché local1'].replace([1,0],[1/20,0])
                df22['% de personnes affectées qui déclarent que l’aide humanitaire reçue n’a pas provoqué de hausse de prix considérable sur le marché local2']=df22['Resilience/Consideration_deflation'].replace(['Très considérable','Considérable','Pas considérable'],
                                                                                                                                                                                                                [0,0,1])
                df22['rrms42']=df22['% de personnes affectées qui déclarent que l’aide humanitaire reçue n’a pas provoqué de hausse de prix considérable sur le marché local2'].replace([1,0],[1/20,0])
                df22['i-resilience retablissemnt de moyens de subsistance']=df22.loc[:, df22.columns.str.startswith('rrms')].sum(axis=1, skipna=True)
                # Information et communication
                df22['Le % des personnes affectées qui se sentent informées au sujet de l’aide qu’elles peuvent recevoir']=df22['Information_et_communication/Appreciation_informatique'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['ic1']=df22['Le % des personnes affectées qui se sentent informées au sujet de l’aide qu’elles peuvent recevoir'].replace([1,0],[1/10,0])
                df22['Le % des personnes affectées qui pensent que les leaders communautaires partagent l’information nécessaires sur les activités humanitaires']=df22['Information_et_communication/Appreciation_partage_information_leaders_communautaires'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['ic2']=df22['Le % des personnes affectées qui pensent que les leaders communautaires partagent l’information nécessaires sur les activités humanitaires'].replace([1,0],[1/10,0])
                df22['i-information et communication']=df22.loc[:,df22.columns.str.startswith('ic')].sum(axis=1,skipna=False)
                # Protection  
                df22['Le % des personnes affectées qui ont une meilleure connaissance du processus de ciblage']=df22['protection/Connaissance_du_choix_de_beneficaire_par_les_agences_humanitaire'].replace(['Oui','Non'],[1,0])
                df22['pn1']=df22['Le % des personnes affectées qui ont une meilleure connaissance du processus de ciblage'].replace([1,0],[1/25,0])

                df22['Le % des personnes affectées qui pensent que l’assistance touche ceux qui ont le plus besoin']=df22['protection/Appreciation_aide_atteint_les_necessiteux'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['pn2']=df22['Le % des personnes affectées qui pensent que l’assistance touche ceux qui ont le plus besoin'].replace([1,0],[1/25,0])
                df22['Le % des personnes affectées qui se sentent en sécurité au quotidien']=df22['protection/Appreciation_sentiment_de_securite_activites_quotidienne'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['pn3']=df22['Le % des personnes affectées qui se sentent en sécurité au quotidien'].replace([1,0],[1/25,0])
                df22['Le % des personnes affectées qui se sentent en sécurité quand elles accèdent à l’assistance humanitaire']=df22['protection/Appreciation_securite_lors_reception_de_l_aide'].replace(['Pas du tout','Pas vraiment','Entre les deux','Plutôt oui','Tout à fait'],
                                                                                                                                                                                                [0,0,0,1,1])
                df22['pn4']=df22['Le % des personnes affectées qui se sentent en sécurité quand elles accèdent à l’assistance humanitaire'].replace([1,0],[1/25,0])
                df22['Le % des personnes affectées qui savent comment faire des suggestions ou soumettre des plaintes aux acteurs humanitaires']=df22['protection/Connaissance_du_mechanisme_MGP'].replace(['Oui','Non'], [1,0])
                df22['pn5']=df22['Le % des personnes affectées qui savent comment faire des suggestions ou soumettre des plaintes aux acteurs humanitaires'].replace([1,0],[1/25,0])
                df22['i-protection']=df22.loc[:,df22.columns.str.startswith('pn')].sum(axis=1,skipna=False)
                df22['adequation aide humanitaire']=df22.loc[:,df22.columns.str.startswith('i-')].sum(axis=1,skipna=False)
                df22.rename(columns={'Province':'state_name'}, inplace=True)
                df22.rename(columns={'Le % des personnes  qui sentent que les acteurs humanitaires les traitent avec respect':"perc personne respecter par les act. hum", "Le % des personnes affectées qui pensent que leurs opinions sont prises en compte dans les prises de décisions humanitaires":"Pers. Affect. opprise en com" })
                df22.rename(columns={"date_de_l_enquete":"year"},inplace=True)
                df22.rename(columns={'Information_et_communication/Appreciation_partage_information_leaders_communautaires':"Info_com"},inplace=True)

                # df22["Info_com"]
                # year1=[]
                # for row in df22['year']:
                #     date = row
                #     if row == "<NA>":
                #         date= '2021-12-24'
                #         # datem = datetime.datetime.strptime(date, "%Y-%m-%d")
                #         year1.append(date)
                #     else:
                #         datem = datetime.datetime.strptime(date, "%Y-%m-%d")
                #         year1.append(datem.year)

                # df22['year']=year1
                df23=df22
                # st.write(df23)
                dfg=deepcopy(df)
                # st.write(dfg.head())
                # st.write(dfg[dfg.columns[5:7]])


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
                new_title = '<p style="font-family:sans-serif; color:#21662f; font-size: 42px;">Indicators Visualisation</p>'
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
                                    WHERE u.id = p.userId AND p.id = s.partnerId AND s.sectorId = se.id AND s.status='Active' AND u.username = %s"""
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
                            y_val1=st.selectbox("Selectionne l'indicateur",options=[df.columns[36],d['Indice de Stabilisation'].name])
                         
                        elif domain_name =='RÉSILIENCE ET ECONOMIE':
                            y_val1=st.selectbox("Selectionne l'indicateur",options=[df.columns[14],df.columns[15],df.columns[17],dfparchain.columns[4]])
                            
                        elif domain_name =='SÉCURITÉ ALIMENTAIRE ET NUTRITION':
                            y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[5:8])

                        elif domain_name =='ENVIRONNEMENT ET WASH':
                            y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[10:14])
                            
                        elif domain_name =="GENRE":
                            y_val1=st.selectbox("Selectionne l'indicateur",options=df.columns[9:11])

                        elif domain_name =="CHAINE DE VALEUR":
                            y_val1=st.selectbox("Selectionne l'indicateur",options=df2.columns[27:])

                        elif domain_name =="FINANCES":
                            y_val1=st.selectbox("Selectionne l'indicateur",options=donnsecond.columns[1:18])

                        elif domain_name == "AIDE HUMANITAIRE":
                            y_val1=st.selectbox("Selectionne l'indicateur",options=df22.columns[119:])
                        
                        else :
                            st.markdown("<h4 style='text-align: center; font-familly:work; color: red;'>Dear Partner, We unfortunately release that all your subsciptions to our sectors and indicators have been expired! So, We encourage you to renew your subscriptions by contacting us on <a href='mailto:info@iescongo.com?Subject=Renewal of subscription to Congo Big Data'>info@iescongo.com</a>. Kind regards! </h4>", unsafe_allow_html=True)

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
                def display_map(df, year,semester, province,spec=NONE):
                # def display_map(df, year, province):
                    if domain_name=="RÉSILIENCE ET ECONOMIE" and y_val1=="IPM PAR SPECULATION":
                        df = df[(df['year'] == year)&(df['semestre'] == semester) & (df['state_name'] == province)&(df['Chaine de Valeur Principale'] == spec)]
                        # df = df[(df['year'] == year)& (df['state_name'] == province)]

                        map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                        
                        choropleth = folium.Choropleth(
                                geo_data='./geojson/rdcongo.geojson',
                                data=df,
                                columns=['state_name', y_val1],
                                key_on='feature.properties.name',
                                line_opacity=0.8,
                                highlight=True,
                                legend_name=y_val1,
                                # fill_color='YlOrRd',
                                color=y_val1

                            )
                        choropleth.geojson.add_to(map)
                        df_indexed = df.set_index('state_name')
                        
                        for feature in choropleth.geojson.data['features']:
                                state_name = feature['properties']['name']
                                # feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'Population'][0]) if state_name in list(df_indexed.index) else ''
                                feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),4)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Popul'] = 'Population: ' + '{:,}'.format(round(df_indexed.loc[state_name]['Population'].sum(),1)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['TailleMen'] = 'Taille du Menage: ' + '{:,}'.format(df_indexed.loc[state_name]['Taille du menage'].mean()) if state_name in list(df_indexed.index)else ''
                                
                        
                        choropleth.geojson.add_child(
                                # folium.features.GeoJsonTooltip(['name', 'Indicateur','Popul'], labels=False)
                                folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                            )
                    
                    
                        st_map = st_folium(map, width=700, height=450)

                        
                        state_name = ''
                        if st_map['last_active_drawing']:
                            state_name = st_map['last_active_drawing']['properties']['name']
                        return state_name


                    elif domain_name in ['STABILISATION ET COHÉSION SOCIALE',"RÉSILIENCE ET ECONOMIE", "SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] and y_val1!="Indice de Stabilisation":
                        df = df[(df['year'] == year)&(df['semestre'] == semester) & (df['state_name'] == province)]
                        # df = df[(df['year'] == year)& (df['state_name'] == province)]

                        map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                        
                        choropleth = folium.Choropleth(
                                geo_data='./geojson/rdcongo.geojson',
                                data=df,
                                columns=['state_name', y_val1],
                                key_on='feature.properties.name',
                                line_opacity=0.8,
                                highlight=True,
                                legend_name=y_val1,
                                # fill_color='YlOrRd',
                                color=y_val1
                            )
                        choropleth.geojson.add_to(map)
                        df_indexed = df.set_index('state_name')
                        
                        for feature in choropleth.geojson.data['features']:
                                state_name = feature['properties']['name']
                                # feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'Population'][0]) if state_name in list(df_indexed.index) else ''
                                feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),4)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Popul'] = 'Population: ' + '{:,}'.format(round(df_indexed.loc[state_name]['Population'].sum(),1)) if state_name in list(df_indexed.index)else ''
                                
                        
                        choropleth.geojson.add_child(
                                folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                            )
                    
                    
                        st_map = st_folium(map, width=700, height=450)

                        
                        state_name = ''
                        if st_map['last_active_drawing']:
                            state_name = st_map['last_active_drawing']['properties']['name']
                        return state_name

                    elif domain_name=="STABILISATION ET COHÉSION SOCIALE" and y_val1=="Indice de Stabilisation":
                        df=d
                        df = df[(df['year'] == year)&(df['semestre'] == semester) & (df['state_name'] == province)]
                        # df = df[(df['year'] == year)& (df['state_name'] == province)]

                        map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                        
                        choropleth = folium.Choropleth(
                                geo_data='./geojson/rdcongo.geojson',
                                data=df,
                                columns=['state_name', y_val1],
                                key_on='feature.properties.name',
                                line_opacity=0.8,
                                highlight=True,
                                legend_name=y_val1,
                                # fill_color='YlOrRd',
                                color=y_val1
                            )
                        choropleth.geojson.add_to(map)
                        df_indexed = df.set_index('state_name')
                        
                        for feature in choropleth.geojson.data['features']:
                                state_name = feature['properties']['name']
                                # feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'Population'][0]) if state_name in list(df_indexed.index) else ''
                                feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),4)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Popul'] = 'Population: ' + '{:,}'.format(round(df_indexed.loc[state_name]['Population'].sum(),1)) if state_name in list(df_indexed.index)else ''
                                
                        
                        choropleth.geojson.add_child(
                                folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                            )
                    
                    
                        st_map = st_folium(map, width=700, height=450)

                        
                        state_name = ''
                        if st_map['last_active_drawing']:
                            state_name = st_map['last_active_drawing']['properties']['name']
                        return state_name

                    
                    elif domain_name=="CHAINE DE VALEUR": 
                        df = df[(df['year'] == year) & (df['semestre'] == semester)& (df['state_name'] == province)]
                        map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                        
                        choropleth = folium.Choropleth(
                                geo_data='./geojson/rdcongo.geojson',
                                data=df,
                                columns=['state_name', y_val1],
                                key_on='feature.properties.name',
                                fill_color='YlOrRd',
                                line_opacity=0.8,
                                highlight=True,
                                legend_name=y_val1,
                                color=y_val1
                                # fill_color = 'YlOrRd'
                                # fill_color="YlGn",
                                # fill_opacity=0.7,
                                # line_opacity=.8
                                # highlight=True
                            )
                        choropleth.geojson.add_to(map)
                        df_indexed = df.set_index('state_name')
                        
                        for feature in choropleth.geojson.data['features']:
                                state_name = feature['properties']['name']
                                # feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'Population'][0]) if state_name in list(df_indexed.index) else ''
                                feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),3)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Popul'] = 'Population: ' + '{:,}'.format(round(df_indexed.loc[state_name]['Population'].sum(),1)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Members'] = 'Membres: ' + '{:,}'.format(df_indexed.loc[state_name]['Nbre Membres'].sum()) if state_name in list(df_indexed.index)else ''
                                
                        
                        choropleth.geojson.add_child(
                                # folium.features.GeoJsonTooltip(['name', 'Indicateur','Popul'], labels=False)
                                folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                            )
                    
                    
                        st_map = st_folium(map, width=700, height=450)

                        
                        state_name = ''
                        if st_map['last_active_drawing']:
                            state_name = st_map['last_active_drawing']['properties']['name']
                        return state_name 
                    elif domain_name =="FINANCES":
                        st.write("MAP NOT AVAILABLE")

                    elif domain_name=="AIDE HUMANITAIRE":
                        df = df[df['state_name'] == province]
                        map = folium.Map(location=[-4.0383, 21.7587], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

                        
                        choropleth = folium.Choropleth(
                                geo_data='./geojson/rdcongo.geojson',
                                data=df,
                                columns=['state_name', y_val1],
                                key_on='feature.properties.name',
                                fill_color='YlOrRd',
                                line_opacity=0.8,
                                highlight=True,
                                legend_name=y_val1,
                                color=y_val1
                                # fill_color = 'YlOrRd'
                                # fill_color="YlGn",
                                # fill_opacity=0.7,
                                # line_opacity=.8
                                # highlight=True
                            )
                        choropleth.geojson.add_to(map)
                        df_indexed = df.set_index('state_name')
                        
                        for feature in choropleth.geojson.data['features']:
                                state_name = feature['properties']['name']
                                # feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'Population'][0]) if state_name in list(df_indexed.index) else ''
                                feature['properties']['Indicateur'] = 'Indicateur moyen: ' + '{:,}'.format(round(df_indexed.loc[state_name][y_val1].mean(),3)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Popul'] = 'Population: ' + '{:,}'.format(round(df_indexed.loc[state_name]['Population'].sum(),1)) if state_name in list(df_indexed.index)else ''
                                # feature['properties']['Members'] = 'Membres: ' + '{:,}'.format(df_indexed.loc[state_name]['Nbre Membres'].sum()) if state_name in list(df_indexed.index)else ''
                                
                        
                        choropleth.geojson.add_child(
                                # folium.features.GeoJsonTooltip(['name', 'Indicateur','Popul'], labels=False)
                                folium.features.GeoJsonTooltip(['name', 'Indicateur'], labels=False)
                            )
                    
                    
                        st_map = st_folium(map, width=700, height=450)

                        
                        state_name = ''
                        if st_map['last_active_drawing']:
                            state_name = st_map['last_active_drawing']['properties']['name']
                        return state_name 

                def interactiveplot(dataframe):
                    x_val=st.selectbox("Selectionne l'indicateur X",options=df.columns[4:])
                    y_val=st.selectbox("Selectionne l'indicateur Y",options=df.columns[4:])
                    plot=px.scatter(dataframe, x=x_val, y=y_val,size='Population', color="Territoire",hover_name="Territoire",log_x=True)
                    st.plotly_chart(plot)
                    # st.color_picker("select color")

                # USED FUCTION FOR THE PLOT ON IES STREAMLIT
                def interactivehist(dataframe):
                    # x_val1=st.selectbox("Selectionne l'indicateur x1",options=dataframe.columns)
                    x_val1=dataframe.columns[3]
                    # y_val1=st.selectbox("Selectionne l'indicateur y1",options=dataframe.columns[4:])
                    # fig = px.histogram(dataframe,x_val1,y_val1)
                    # fig= px.bar(dataframe,x_val1,y_val1,color="Territoire",hover_name="Territoire",title="Province du {} {} ".format(state_name, df[y_val1].name))
                    # st.plotly_chart(fig)
                    if (domain_name== "STABILISATION ET COHÉSION SOCIALE") or (y_val1 in ["Indice de Pauvrete Multidimentionnelle","Indice de Participation de la femme","Indice d'autonominsationn de la femme","Indice de Lavage de mains au moins à trois moments","Indice d'exposition aux chocs"]) :
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,1], range_color=[0,1])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    elif y_val1=="Indice de résilience":
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,7], range_color=[0,7])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)
                    elif y_val1=="Indice de Faim dans de menage":
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,6], range_color=[0,6])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    elif y_val1=="Indice de Strategie de Survie":
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,55], range_color=[0,55])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    
                    elif y_val1=="Score de Consommation Alimentaire":
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,112], range_color=[0,112])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    else:
                        fig= px.bar(dataframe,x_val1,y_val1,color=y_val1,hover_name="semestre",title="Province du(de) {} : {} ".format(state_name, df[y_val1].name),range_y=[0,max(df[y_val1])],range_color=[0,max(df[y_val1])])
                        fig.data[-1].text = dataframe[y_val1]
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)


                def interactivepie(dataframe):
                    # colors = ['gold', 'mediumturquoise']
                    # colors=['blue','darkblue']
                    # colors=['lightcyan','cyan']
                    colors=["red", "blue"]
                    fig2 = px.pie(dataframe, values=dataframe['Sexe'].value_counts(), names=dataframe['Sexe'].unique(),color_discrete_map={'F':'darkblue','M':'cyan'},hole=.3,title=("Répartition des Participants par sexe"))
                    fig2.update_traces(hoverinfo='label+percent',  textfont_size=20,
                            marker=dict(colors=dataframe['Sexe'].value_counts(), line=dict(color='#000000', width=2)))
                    # textinfo='value'/100,
                    st.plotly_chart(fig2)

                def interactiveprovinceval(dataframe):
                    d1=dataframe.loc[state_name][y_val1]
                    # fig1= px.scatter(dataframe,d1,color="Territoire",hover_name="Territoire")
                    fig1= px.scatter(d1)

                    st.plotly_chart(fig1)


                def main(df):    
                    return interactivehist(df)


                def Evolutionplot(dataframe):
                    # import plotly.io as pio
                    if domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"] and y_val1!="IPM PAR SPECULATION":
                        dataframe['semestre']=dataframe["semestre"].replace(['Semestre1','Semestre2'],['S1','S2'])
                        a2=dataframe.loc[dataframe['state_name']==state_name]
                        a1=a2.groupby(['year','semestre'])[y_val1].mean()
                        # a1=a2.groupby('year')[y_val1].mean()
                        # a1=dataframe.loc[state_name].groupby('year')[y_val1].mean()# to get annual mean by province
                        prov1=pd.DataFrame(a1)
                        prov1.reset_index(inplace=True)
                        # prov1
                        
                        
                        Repub=dataframe.groupby(['year','semestre'])[y_val1].mean()
                        Repub=pd.DataFrame(Repub)
                        Repub.reset_index(inplace=True)
                        # Repub

                        ###################
                        X=pd.Series(list(Repub.index))
                        Y=Repub[y_val1]
                        B11=estimate_coef(X,Y)
                        # st.write(B11)
                        X1=pd.Series(range(len(Repub.index),len(Repub.index)+6))
                        Y1=B11[0]+B11[1]*X1
                        
                        
                        Xp=pd.Series(list(prov1.index))
                        Yp=prov1[y_val1]
                        B21=estimate_coef(Xp,Yp)
                        # st.write(B21)
                        Xp1=pd.Series(range(len(prov1.index),len(prov1.index)+6))
                        Yp1=B21[0]+B21[1]*Xp1
                    
                        fig1=go.Figure()
                        fig1.add_trace(go.Scatter(
                            # x=[Repub['year'], Repub['semestre']], 
                            # y=Repub[y_val1],
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

                        fig1.update_layout(legend_title_text='Region', title_text="{} au {} et en RDC(Tendance)".format(Repub[y_val1].name,state_name),xaxis_title="Années", yaxis_title="{}".format(Repub[y_val1].name),yaxis=dict(range=[0, max(Yp1)]))
                            
                        st.plotly_chart(fig1)

                    
                    if domain_name == 'CHAINE DE VALEUR':
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
                        fig.update_layout(legend_title_text="Tendance {}".format(Repub[y_val1].name), title_text="{} au {} et en RDC (Tendance)".format(Repub[y_val1].name,state_name),xaxis_title="Années", yaxis_title="{}".format(Repub[y_val1].name))
                        
                        st.plotly_chart(fig)

                col1, col2 = st.columns([0.5, 0.5])
                with col1:  
                    if domain_name=="RÉSILIENCE ET ECONOMIE" and y_val1=="IPM PAR SPECULATION":
                        # st.write("IPM waiting...")
                        # st.write(dfparchain)
                        df_indexed1 = dfparchain.set_index('state_name')
                        spec=st.selectbox("Choose speculation",options=dfparchain['Chaine de Valeur Principale'].unique().tolist())
                        # dfparchain=dfparchain[dfparchain['Chaine de Valeur Principale']==spec]
                        MapDRC = display_map(dfparchain, year,semester, list(df_indexed1.index),spec)

                    if (domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]) and (y_val1!="IPM PAR SPECULATION")and (y_val1!='Indice de Stabilisation'):
                        df_indexed = df.set_index('state_name')
                        MapDRC = display_map(df, year,semester, list(df_indexed.index),spec=None)
                        # MapDRC = display_map(df, year,list(df_indexed.index))
                    if (domain_name in ['STABILISATION ET COHÉSION SOCIALE']) and (y_val1=='Indice de Stabilisation'):
                        df_indexed11 = d.set_index('state_name')
                        MapDRC = display_map(d, year,semester, list(df_indexed11.index),spec=None)
                    if domain_name=="CHAINE DE VALEUR":
                        df_indexed1 = df2.set_index('state_name')
                        # st.write(df2.head())
                        MapDRC = display_map(df2, year,semester, list(df_indexed1.index),spec=None)

                    if domain_name=="AIDE HUMANITAIRE":
                        df_indexed1 = df22.set_index('state_name')
                        # st.write(df2.head())
                        MapDRC = display_map(df22, year,semester, list(df_indexed1.index),spec=None)
                    
                    

                    # ## Select State: One should set the obtion and the the selection type, like (radio,checkbox,selectbox,...)
                    if domain_name=="RÉSILIENCE ET ECONOMIE" and y_val1=="IPM PAR SPECULATION":
                        state_option = dfparchain['state_name'].unique().tolist()
                        # state_name = st.selectbox("Choisir la province", state_option)
                        # state_name=st.sidebar.radio('Select the province:', state_option)
                        # state_name=st.sidebar.selectbox('Select the province:', state_option)
                        # state_name=st.multiselect('choisir province',state_option)
                        dfparchain = dfparchain[dfparchain['state_name']==state_name]

                    elif (domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]) and (y_val1!="IPM PAR SPECULATION") and(y_val1!='Indice de Stabilisation'):
                        state_option = df['state_name'].unique().tolist()
                        # state_name = st.selectbox("Choisir la province", state_option)
                        # state_name=st.sidebar.radio('Select the province:', state_option)
                        # state_name=st.sidebar.selectbox('Select the province:', state_option)
                        # state_name=st.multiselect('choisir province',state_option)
                        df = df[df['state_name']==state_name]
                    
                    elif domain_name in ['STABILISATION ET COHÉSION SOCIALE'] and y_val1=='Indice de Stabilisation':
                        state_option = d['state_name'].unique().tolist()
                        # state_name = st.selectbox("Choisir la province", state_option)
                        # state_name=st.sidebar.radio('Select the province:', state_option)
                        # state_name=st.sidebar.selectbox('Select the province:', state_option)
                        # state_name=st.multiselect('choisir province',state_option)
                        d = d[d['state_name']==state_name]

                    
                    elif domain_name=="CHAINE DE VALEUR":
                        state_option = df2['state_name'].unique().tolist()
                        # state_name = st.selectbox("Choisir la province", state_option)
                        # state_name=st.sidebar.radio('Select the province:', state_option)
                        # state_name=st.sidebar.selectbox('Select the province:', state_option)
                        # state_name=st.multiselect('choisir province',state_option)
                        df2 = df2[df2['state_name']==state_name]

                    elif domain_name=="AIDE HUMANITAIRE":
                        state_option = df22['state_name'].unique().tolist()
                        # state_name = st.selectbox("Choisir la province", state_option)
                        # state_name=st.sidebar.radio('Select the province:', state_option)
                        # state_name=st.sidebar.selectbox('Select the province:', state_option)
                        # state_name=st.multiselect('choisir province',state_option)
                        df22 = df22[df22['state_name']==state_name]
                    

                #### PLOTING FUNCTIONS 
                with col2:
                    if domain_name== "RÉSILIENCE ET ECONOMIE" and y_val1=='IPM PAR SPECULATION':

                        fig16=px.bar(round(dfparchain,2), x='Chaine de Valeur Principale', y='IPM PAR SPECULATION',color='IPM PAR SPECULATION',title="Province du {}, {} ".format(state_name, dfparchain['IPM PAR SPECULATION'].name),range_y=[0,1],range_color=[0,1])
                        fig16.data[-1].text = round(dfparchain[y_val1],2)
                        fig16.update_traces(textposition='inside')
                        st.plotly_chart(fig16)
                    elif (domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]) and (y_val1!='IPM PAR SPECULATION')and (y_val1!="Indice de Stabilisation"):
                        main(df)
                    elif domain_name=="STABILISATION ET COHÉSION SOCIALE" and y_val1=="Indice de Stabilisation":
                        # d['year']=d['year'].astype(int)
                        d = d[(d['state_name']==state_name)&(d['semestre']==semester)]
                        fig=px.bar(d,d.columns[1],y_val1,color=y_val1,hover_name="semestre",range_y=[0,1],range_color=[0,1] )
                        # fig= px.bar(df2,df2.columns[3],y_val1,color=y_val1,hover_name="semestre",title="\{} indicateur {} ".format(state_name, df[y_val1].name))
                        fig.data[-1].text = round(d[y_val1],2)
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    elif domain_name=="CHAINE DE VALEUR":
                        df2 = df2[(df2['state_name']==state_name)&(df2['semestre']==semester)]
                        fig=px.bar(df2,df2.columns[3],y_val1,color=y_val1,hover_name="semestre" )
                        # fig= px.bar(df2,df2.columns[3],y_val1,color=y_val1,hover_name="semestre",title="\{} indicateur {} ".format(state_name, df[y_val1].name))
                        fig.data[-1].text = round(df2[y_val1],2)
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)

                    elif domain_name=="AIDE HUMANITAIRE":
                        df22 = df22[df22['state_name']==state_name]
                        df22=df22.groupby("Territoire")[y_val1].mean()
                        df22=pd.DataFrame(df22)
                        df22.reset_index(inplace=True)
                        fig=px.bar(round(df22,3),df22.columns[0],y_val1,color=y_val1,hover_name="Territoire",range_y=[0,1],range_color=[0,1]  )
                        # fig= px.bar(df2,df2.columns[3],y_val1,color=y_val1,hover_name="semestre",title="\{} indicateur {} ".format(state_name, df[y_val1].name))
                        fig.data[-1].text = round(df22[y_val1],2)
                        fig.update_traces(textposition='inside')
                        st.plotly_chart(fig)
                    
                    # #### This part allows the  visualisation of the indicators evolution in the State and the Whole country
                    ### In fact The trend of means of indicators is the one plotted.
                
                
                    
                if (domain_name in ['STABILISATION ET COHÉSION SOCIALE', "RÉSILIENCE ET ECONOMIE","SÉCURITÉ ALIMENTAIRE ET NUTRITION","ENVIRONNEMENT ET WASH","GENRE"]) and (y_val1!="IPM PAR SPECULATION") and (y_val1!="Indice de Stabilisation"):
                    col11, col22 = st.columns([0.5, 0.5])
                    with col11:
                        Evolutionplot(dfg)
                    with col22:
                        df20 = df20[df20['state_name']==state_name]
                        interactivepie(df20)
                        # st.write(df20.head())
                        # st.write(df20['Sexe'].value_counts())

                elif domain_name in ['STABILISATION ET COHÉSION SOCIALE'] and y_val1=="Indice de Stabilisation":
                    Evolutionplot(d)

                
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
                        # textinfo='value'/100,
                        st.plotly_chart(fig2)
                        # interactivepie(df2)

                elif domain_name == "FINANCES":
                    donnsecond["Années d'Exercice"]=donnsecond["Années d'Exercice"].values.astype(str)

                    if y_val1 in ["Part du Budget: Justice","Part du Budget: défense","Part du Budget: Santé","Part du Budget: Enseignement","Part du Budget: Agriculture","Part du Budget: Commerce","Part du Budget: Environnement","Part du Budget: Genre et Famille","Part du Budget: Entrepreneuriat et PME"]:
                        fig3 =px.bar(donnsecond, x="Années d'Exercice",y=y_val1, color=y_val1, title="CREDITS BANCAIRES OU PART DU BUDGET NATIONAL",range_y=[0,100], range_color=[0,100])
                        fig3.data[-1].text = round(donnsecond[y_val1],2)
                        fig3.update_traces(textposition='inside')
                        st.plotly_chart(fig3)

                    else :
                        fig3 =px.bar(donnsecond, x="Années d'Exercice",y=y_val1, color=y_val1, title="CREDITS BANCAIRES OU PART DU BUDGET NATIONAL",range_y=[0,max(donnsecond[y_val1])], range_color=[0,max(donnsecond[y_val1])])
                        fig3.data[-1].text = round(donnsecond[y_val1],2)
                        fig3.update_traces(textposition='inside')
                        st.plotly_chart(fig3)     
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
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: visible;}
                header {visibility: hidden;}
                .egzxvld0{color:white;}
                footer:after{
                    content: 'Copyright © DML Congo & IES Congo, All rights reserved';
                    display: block;
                    position: relative;
                    color: tomato;
                    text-align:center;
                }
                .egzxvld1{visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
