import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Source Sans Pro"

st.title('Données du Cimetière du Dieweg')

EXCEL_URL = ('./_cu.xlsx')
CSV_URL = ('./_cu.csv')
DEATH_COLUMN = "décès"
BIRTH_COLUMN = "naissance"

def init():
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text("")
    return data

@st.cache
def load_data():
    data = pd.read_excel(EXCEL_URL)
    # data = pd.read_csv(CU_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DEATH_COLUMN] = pd.to_datetime(data[DEATH_COLUMN])
    # data[BIRTH_COLUMN] = pd.to_datetime(data[BIRTH_COLUMN])
    return data

def generate_section_graph(data):
    section_data = data["section"]
    section_counted = section_data.value_counts(dropna=False)
    fig1, ax1 = plt.subplots()
    ax1.pie(section_counted, startangle=20, autopct='%1.3f%%', labels=["Section " + s.upper() for s in section_counted.index.tolist()])
    ax1.axis('equal')  
    return fig1

def generate_gender_graph(data):
    women_data = data["femme"]
    women_counted = women_data.value_counts(dropna=False)
    fig1, ax1 = plt.subplots()
    ax1.pie(women_counted, startangle=20, autopct='%1.1f%%', labels=["Hommes", "Femmes"])
    ax1.axis('equal')
    return fig1

def generate_age_graph(data):
    st.subheader("Âge de mort par genre")
    available_data = data.loc[(data["âge"] >= 1)]["âge"]
    women_available_data = data.loc[(data["âge"] >= 1)].loc[data["femme"]]["âge"]
    men_available_data =   data.loc[(data["âge"] >= 1)].loc[data["homme"]]["âge"]
    # st.write(available_data.value_counts(dropna=False, sort=False).sort_index())
    line_chart = go.Figure()
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
    y = available_data.value_counts(dropna=False, sort=False).sort_index(), name="All"))
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
        y = women_available_data.value_counts(dropna=False, sort=False).sort_index(), name="Women"))
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
        y = men_available_data.value_counts(dropna=False, sort=False).sort_index(), name="Men"))
    st.plotly_chart(line_chart)

def generate_stats(data):
    st.subheader("Statistiques générales")
    functionning_time = max(data[DEATH_COLUMN].dt.year) - min(data[DEATH_COLUMN].dt.year)
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de gens enterrés", str(len(data)) + " pers.")
    col2.metric("Personnes avec épitaphe", str(data["épitaphe"].value_counts(dropna=False)[1]) + " pers.")
    col3.metric("Temps de fonctionnement", str(functionning_time) + " ans")


def display(data):
    if st.sidebar.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    generate_stats(data)

    col1, col2 = st.columns(2)
    col1.subheader('Tombes par section')
    col1.pyplot(generate_section_graph(data))
    col2.subheader('Répartition par genre')
    col2.pyplot(generate_gender_graph(data))

    generate_age_graph(data)

data = init()
display(data)
