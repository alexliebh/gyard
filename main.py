import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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
    fig = go.Figure(data=[go.Pie(labels=["Section " + s.upper() for s in section_counted.index.tolist()], values=section_counted)])
    fig.update_layout(margin=dict(pad=0, l=0, r=0, b=0, t=0))
    return fig

def generate_gender_graph(data):
    women_data = data["femme"]
    women_counted = women_data.value_counts(dropna=False)
    fig = go.Figure(data=[go.Pie(labels=["Hommes", "Femmes"], values=women_counted)])
    fig.update_layout(margin=dict(pad=0, l=0, r=0, b=0, t=0))
    return fig

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
    line_chart.update_layout(margin=dict(pad=0, l=0, r=0, b=0, t=10))
    return line_chart

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
    col1.plotly_chart(generate_section_graph(data), use_container_width=True)
    col2.subheader('Répartition par genre')
    col2.plotly_chart(generate_gender_graph(data), use_container_width=True)

    st.plotly_chart(generate_age_graph(data))

data = init()
display(data)
