import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import util

st.title('Données du Cimetière du Dieweg')

EXCEL_URL = ('./_cu.xlsx')
DEATH_COLUMN = "décès"
BIRTH_COLUMN = "naissance"

def init():
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text("")
    return data

@st.cache
def load_data():
    data = pd.read_excel(EXCEL_URL, index_col=0)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DEATH_COLUMN] = pd.to_datetime(data[DEATH_COLUMN])
    return data

def generate_stats(data):
    st.subheader("Statistiques générales")
    functionning_time = max(data[DEATH_COLUMN].dt.year) - min(data[DEATH_COLUMN].dt.year)
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de gens enterrés", str(len(data)) + " pers.")
    col2.metric("Personnes avec épitaphe", str(data["épitaphe"].value_counts(dropna=False)[1]) + " pers.")
    col3.metric("Temps de fonctionnement", str(functionning_time) + " ans")

def generate_section_graph(data):
    section_data = data["section"]
    section_counted = section_data.value_counts(dropna=False)
    fig = go.Figure(data=[go.Pie(labels=["Section " + s.upper() for s in section_counted.index.tolist()], values=section_counted)])
    fig.update_layout(title_text="Répartition par section", margin=dict(pad=2, l=0, r=0, b=0, t=25))
    return fig

def generate_gender_graph(data):
    women_counted = data["femme"].value_counts(dropna=False)
    men_counted = data["homme"].value_counts(dropna=False)
    gender_unavailable_data = data.loc[(data["femme"] == False)].loc[data["homme"] == False]
    fig = go.Figure(data=[go.Pie(labels=["Femme", "Homme", "Inconnu"], values=[women_counted[True], men_counted[True], len(gender_unavailable_data)])])
    fig.update_layout(title_text="Répartition par genre", margin=dict(pad=2, l=0, r=0, b=0, t=25))
    return fig

def generate_age_graph(data):
    available_data = data.loc[(data["âge"] >= 1)]["âge"]
    women_available_data = data.loc[(data["âge"] >= 1)].loc[data["femme"]]["âge"]
    men_available_data =   data.loc[(data["âge"] >= 1)].loc[data["homme"]]["âge"]
    line_chart = go.Figure()
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
    y = available_data.value_counts(dropna=False, sort=False).sort_index(), name="Tous"))
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
        y = women_available_data.value_counts(dropna=False, sort=False).sort_index(), name="Femmes"))
    line_chart.add_trace(go.Scatter(x = [x for x in range(min(available_data), max(available_data)+1)],
        y = men_available_data.value_counts(dropna=False, sort=False).sort_index(), name="Hommes"))
    line_chart.update_layout(title_text="Âge de mort", margin=dict(pad=2, l=0, r=0, b=0, t=35))
    return line_chart

def generate_nationalities_graph(data):
    nationalities = util.find_group_nationalities(data)
    
    fig = go.Figure(data=[go.Pie(labels=[n for n in nationalities.keys() if nationalities[n] > 0], values=[n for n in nationalities.values() if n > 0])])
    fig.update_layout(title_text="Répartition par nationalité", margin=dict(pad=2, l=0, r=0, b=0, t=25))
    return fig

def display_family_analyser(data):
    st.subheader("Données par famille")
    names_data = data["nom"]
    names_counted = names_data.value_counts(dropna=False)
    popular_names = names_counted.index.tolist()
    selected_name = st.selectbox("Family to analyse", popular_names[:50])
    selected_family = data.loc[(data["nom"] == selected_name.upper())]

    col1, col2 = st.columns(2)
    fig = generate_nationalities_graph(selected_family)
    col1.plotly_chart(fig, use_container_width=True)
    fig = generate_gender_graph(selected_family)
    col2.plotly_chart(fig, use_container_width=True)


def display(data):
    if st.sidebar.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    generate_stats(data)

    col1, col2 = st.columns(2)
    col1.plotly_chart(generate_section_graph(data), use_container_width=True)
    col2.plotly_chart(generate_gender_graph(data), use_container_width=True)

    st.plotly_chart(generate_age_graph(data), use_container_width=True)

    display_family_analyser(data)

data = init()
display(data)
