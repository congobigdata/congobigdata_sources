import pandas as pd
import mysql.connector as connection
import streamlit as st
import streamlit_authenticator as stauth
import toml
from streamlit_option_menu import option_menu
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid
import streamlit.components.v1 as components

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
img1 = Image.open(r"./images/capture 1.JPG")
img2 = Image.open(r"./images/Capture2.JPG")
img3 = Image.open(r"./images/Capture3.png")

def page_about():
    st.markdown
    components.html(
        """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <div class="accordion m-2 p-2" id="accordionExample"style="height: 95vh; overflow: scroll;">
            <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
                <button class="accordion-button h5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                Context & Method
                </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                <p><strong>Congo Big data</strong> is an important tool to guide managers in <b>decision making</b>. It produces integrated and disaggregated data for the formulation, monitoring/evaluation of development policies and programs.</p>
                <p><strong>Congo Big data</strong> is based on multi-sectoral raw data from biannual surveys to enable subscribing development actors (Government, Donors, Non-Governmental Organizations, Companies, Universities, etc.) 
                    to monitor in real time the level of performance of their actions and/or the context by geographical area in DRC. This allows them to make necessary adjustments based on the evidence (Adaptive and Results Based Management).
                    In a rigorous and innovative way, data is collected periodically from participants in different territories and cities of 26 Congolese provinces Other data is collected from accredited secondary sources.
                    From data collection to analysis, a rigorous, systematic, ethical and deontological methodological protocol is followed for Quality assurance. Any cleaning or modification made to the collected data is documented and provided to users for reliability and accountability.</p>
                </div>
            </div>
            </div>
            <div class="accordion-item">
            <h2 class="accordion-header" id="headingTwo">
                <button class="accordion-button collapsed h5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                Sectors & Indicators
                </button>
            </h2>
            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                    <div class="card" style="height: 95vh; overflow: scroll;">
                        <div class="card-header">
                            Since our indicators are composite (index), each of our indicators is made up of several sub-indicators. Therefore, for each indicator in a given sector, a given partner could identify ten or so that help calculate the composite (index) indicator and that constitute for them performance indicators for a specific program. The report for each sector provides more details.
                            Apart from the specific themes addressed at the request of partners, data on impact indicators are collected every six months for the sectors listed bellow.
                        </div>
                        <div class="card-body">
                        <table class="table table-bordered table-condensed table-responsive table-sm">
                                <thead>
                                <tr>
                                    <th class="h4">#</th>
                                    <th class="h4">Sectors</th>
                                    <th class="h4">Index/Indicators</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>1</td>
                                    <td><b>STABILISATION AND SOCIAL COHESION</b> </td>
                                    <td>
                                    <ul>
                                        <li>Social Cohesion Index</li>
                                        <li>Social Capital Index</li>
                                    </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td><b>RESILIENCE AND ECONOMICS</b></td>
                                    <td>
                                    <ul>
                                        <li>Household Shock Exposure Index</li>
                                        <li>Shock Resilience Index</li>
                                        <li>Multidimensional Poverty Index (MPI)</li>
                                        <li>Breakdown of credits by sector of activity* (in millions of dollars)</li>
                                        <li>Breakdown of the national budget by sector of activity</li>
                                    </ul>
                                    
                                    </td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td><b>FOOD SAFETY AND NUTRITION</b></td>
                                    <td>
                                    <ul>
                                        <li>Food Consumption Score (FCS)</li>
                                        <li>Reduced Survival Strategy Index (rCSI)</li>
                                        <li>Global Acute Malnutrition Rate (GAM)</li>
                                        <li>Household Hunger Index (HHI)</li>
                                    </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>4</td>
                                    <td><b>ENVIRONMENT AND WASH</b></td>
                                    <td>
                                    <ul>
                                        <li>Quantity of charcoal (in Kg) used per person in the household</li>
                                        <li>Quantity of biochar (Eco-braise) used in kg per person in the household</li>
                                        <li>% of households with access to a safe water source within 30 minutes</li>
                                        <li>% of people practicing handwashing at least 3 key times</li>
                                    </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>5</td>
                                    <td><b>AGRICULTURAL VALUE CHAIN AND MARKET SYSTEMS DEVELOPMENT</b></td>
                                    <td>
                                    <ul>
                                        <li>Multidimensional Poverty Index (MPI) of farmers (disaggregated by main CVA)</li>
                                        <li>Average turnover of agricultural cooperatives (disaggregated by CVA)</li>
                                        <li>% of women employed in agricultural cooperatives</li>
                                        <li>% of women members of agricultural cooperatives</li>
                                        <li>% of women in agricultural decision-making bodies</li>
                                    </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>6</td>
                                    <td><b>GENDER</b></td>
                                    <td>
                                    <ul>
                                        <li>Women's participation in household decision-making index (WPI)</li>
                                        <li>Women's socio-economic empowerment index (WEI)</li>
                                    </ul>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                
                </div>
            </div>
            </div>
            <div class="accordion-item">
            <h2 class="accordion-header" id="headingThree">
                <button class="accordion-button collapsed h5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                Copyright
                </button>
            </h2>
            <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                <strong>Congo Big Data</strong> is an online platform for viewing statistical data relating to various sectors of the DR Congo, designed by two consulting firms, namely Innovations et Entrepreneuriat Social (www.iescongo.com) and Data Mining Lab (www.dmlcongo.com).
                It is All rights reseved!
                </div>
            </div>
            </div>
            <div class="accordion-item">
            <h2 class="accordion-header" id="headingFour">
                <button class="accordion-button collapsed h5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseThree">
                Help Center
                </button>
            </h2>
            <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                To get help, please contact us on +243 975 554 248 or email us on <a href="mailto:help@dmlcongo.com?Subject=Help Congo Big Data">help@dmlcongo.com</a> 
                </div>
            </div>
            </div>
        </div>  
    """,
    height=600,)
    
def page_home():
    
    # datahome = {
    #     'Sector': ['STABILISATION AND SOCIAL COHESION', 'RESILIENCE AND ECONOMICS', 'FOOD SAFETY AND NUTRITION', 'ENVIRONMENT AND WASH', 'AGRICULTURAL VALUE CHAIN AND MARKET SYSTEMS DEVELOPMENT', 'GENDER'],
    #     'Indicators': ['Social Cohesion Index,\n Social Capital Index', 'Household Shock Exposure Index,\n Shock Resilience Index,\n Multidimensional Poverty Index (MPI),\n Breakdown of credits by sector of activity* (in millions of dollars),\n Breakdown of the national budget by sector of activity', 'Food Consumption Score (FCS),\n Reduced Survival Strategy Index (rCSI),\n Global Acute Malnutrition Rate (GAM)*,\n Household Hunger Index (HHI)', "Quantity of charcoal (in Kg) used per person in the household,\n Quantity of biochar (Eco-braise) used in kg per person in the household,\n % of households with access to a safe water source within 30 minutes,\n % of people practicing handwashing at least 3 key times", 'Multidimensional Poverty Index (MPI) of farmers (disaggregated by main CVA),\n Average turnover of agricultural cooperatives (last semester) (disaggregated by CVA),\n % of women employed in agricultural cooperatives,\n % of women members of agricultural cooperatives,\n % of women in agricultural decision-making bodies', "Women's participation in household decision-making index (WPI),\n Women's socio-economic empowerment index (WEI)"]
    # }
    # dfhome = pd.DataFrame(datahome)

    # gb = GridOptionsBuilder.from_dataframe(dfhome)

    # gridOptions = gb.build()
    # st.write('### Sectors and indicators we analyze')
    # AgGrid(
    #             dfhome,
    #             gridOptions=gridOptions,
    #             height=250,
    #             fit_columns_on_grid_load=True
    #         )

    components.html(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <div class="card" style="height: 95vh; overflow: scroll;">
    <div class="card-header">
        Since our indicators are composite (index), each of our indicators is made up of several sub-indicators. Therefore, for each indicator in a given sector, a given partner could identify ten or so that help calculate the composite (index) indicator and that constitute for them performance indicators for a specific program. The report for each sector provides more details.
        Apart from the specific themes addressed at the request of partners, data on impact indicators are collected every six months for the sectors listed bellow.
    </div>
    <div class="card-body">
      <table class="table table-bordered table-condensed table-responsive table-sm">
            <thead>
              <tr>
                <th class="h4">#</th>
                <th class="h4">Sectors</th>
                <th class="h4">Index/Indicators</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td><b>STABILISATION AND SOCIAL COHESION</b> </td>
                <td>
                  <ul>
                    <li>Social Cohesion Index</li>
                    <li>Social Capital Index</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td>2</td>
                <td><b>RESILIENCE AND ECONOMICS</b></td>
                <td>
                  <ul>
                    <li>Household Shock Exposure Index</li>
                    <li>Shock Resilience Index</li>
                    <li>Multidimensional Poverty Index (MPI)</li>
                    <li>Breakdown of credits by sector of activity* (in millions of dollars)</li>
                    <li>Breakdown of the national budget by sector of activity</li>
                  </ul>
                  
                </td>
              </tr>
              <tr>
                <td>3</td>
                <td><b>FOOD SAFETY AND NUTRITION</b></td>
                <td>
                  <ul>
                    <li>Food Consumption Score (FCS)</li>
                    <li>Reduced Survival Strategy Index (rCSI)</li>
                    <li>Global Acute Malnutrition Rate (GAM)</li>
                    <li>Household Hunger Index (HHI)</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td>4</td>
                <td><b>ENVIRONMENT AND WASH</b></td>
                <td>
                  <ul>
                    <li>Quantity of charcoal (in Kg) used per person in the household</li>
                    <li>Quantity of biochar (Eco-braise) used in kg per person in the household</li>
                    <li>% of households with access to a safe water source within 30 minutes</li>
                    <li>% of people practicing handwashing at least 3 key times</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td>5</td>
                <td><b>AGRICULTURAL VALUE CHAIN AND MARKET SYSTEMS DEVELOPMENT</b></td>
                <td>
                  <ul>
                    <li>Multidimensional Poverty Index (MPI) of farmers (disaggregated by main CVA)</li>
                    <li>Average turnover of agricultural cooperatives (disaggregated by CVA)</li>
                    <li>% of women employed in agricultural cooperatives</li>
                    <li>% of women members of agricultural cooperatives</li>
                    <li>% of women in agricultural decision-making bodies</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td>6</td>
                <td><b>GENDER</b></td>
                <td>
                  <ul>
                    <li>Women's participation in household decision-making index (WPI)</li>
                    <li>Women's socio-economic empowerment index (WEI)</li>
                  </ul>
                </td>
              </tr>
            </tbody>
          </table>
    </div>
  </div>
    """,
    height=400,
)

    col1, col2, col3 = st.columns([3.33,3.33,3.33])
    img1 = Image.open(r"./images/capture 1.JPG")
    img2 = Image.open(r"./images/Capture2.JPG")
    img3 = Image.open(r"./images/Capture3.png")
    with col1:
        st.write('##### Data Collection and analysis')
        st.write('Every six months, we collect data from all the indicators listed in all sectors above. Then data collected are automatically controled and analyzed using Python machine learning approaches.')
        st.image(img1)
        

        with col2:
            st.write('##### Data vizualisation and report generation')
            st.write('Results from Data Analysis are interpreted and visualized on the map, bar-charts, pie-charts, etc, to inform the real time data evolution of different indicators in geographic areas')
            st.image(img2)

        with col3:
            st.write('##### Future Tendancy prediction')
            st.write('According to the evolution of indicators, their tendancies are predicted in the future using machine learning and artificial intelligence techniques')
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

def update_status(status, subscription):
    c.execute("""UPDATE subscription SET status = %s WHERE id = %s""", (status, subscription))
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