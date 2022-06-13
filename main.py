import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import re
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)



def intro():
    st.header("Happiness Death and Alcohol Consumption")
    st.subheader("Анализ данных, посвященных потреблению алкоголя, счастью и смертности")

if __name__ == "__main__" :
    intro()

img = Image.open("photo.jpg")
st.image(img, width=700)

with st.echo(code_location='below'):
    @st.experimental_singleton()


    def get_file():
        return pd.read_csv('HappinessAlcoholConsumptions.csv')
    d = get_file()
    st.dataframe(d)
    print(d)

    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")

    df_age_alco = d.groupby('Region', as_index=False).agg({'HappinessScore': 'mean', 'HDI': 'mean'})

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_age_alco['Region'], y=df_age_alco['HappinessScore'], name='Happiness'))
    fig.add_trace(go.Bar(x=df_age_alco['Region'], y=df_age_alco['HDI']/100, name='HDI'))
    fig.update_layout(legend_title_text="Показатель", title="Индекс счастья и человеческого развития в зависимости от региона")
    fig.update_xaxes(title_text="Регион")
    fig.update_yaxes(title_text="Индексы")
    st.plotly_chart(fig)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.subheader("Среднее потребление алкоголя на душу населения в разных странах")
    click = st.selectbox("Статистика среди",
                         ['Обоих полов', 'Женщин', 'Мужчин'])
    url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D1%80%" \
          "D0%B0%D0%BD_%D0%BF%D0%BE_%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E_%" \
          "D0%B0%D0%BB%D0%BA%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F_%D0%BD%D0%B0_%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA%D0%B0"
    country = st.text_input(label="Введите страну")

    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    tab = soup.table

    try:
        me = soup.table.find(attrs={"data-sort-value": country})
        th = me.parent.parent
        all = str(th.find_next_sibling('td')).replace('<td>', ' ').replace('</td>', ' ')
        mal = str(th.find_next_siblings('td')[1]).replace('<td>', ' ').replace('</td>', ' ')
        fem = str(th.find_next_siblings('td')[2]).replace('<td>', ' ').replace('</td>', ' ')

        if click=="Обоих полов":
            st.write("Среднее потребление алкоголя в год "
                    "(в литрах чистого этилового спирта) на душу среди всего населения в стране",
                    country, "равно", all)

        elif click=="Мужчин":
            st.write("Среднее потребление алкоголя в год "
                     "(в литрах чистого этилового спирта) на душу среди мужчин в стране",
                     country, "равно", mal)

        elif click=="Женщин":
            st.write("Среднее потребление алкоголя в год "
                     "(в литрах чистого этилового спирта) на душу среди женщин в стране",
                     country, "равно", fem)

    except:
        st.text("Что-то пошло не так, введите другую страну")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.subheader("Немного про уровень смертности в странах")
    coun = st.text_input(label="Bведите страну")
    url = "https://nonews.co/directory/lists/countries/death"
    re = requests.get(url)
    soups = BeautifulSoup(re.text)
    tabl = soups.tbody
    meow = tabl.find_all(class_="column-2")
    places = []
    death_rates = []
    for element in meow:
        al = element.find_next_sibling('td')
        place = str(element).replace('</td>', '').replace('<td class="column-2">', '')
        places.append(place)
        death_rate = str(al).replace('</td>', '').replace('<td class="column-3">', '')
        death_rates.append(death_rate)
    death = dict(zip(places, death_rates))
    try:
        st.write("Уровень смертносте в стране", coun, "равен", death[coun], "на 1000 человек")
    except:
        st.text("Введите другую страну")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.subheader("Поищем бары в разных регионах")
    click1 = st.selectbox("Искать",
                         ['Все бары', 'Пивные бары', 'Винные бары'])
    place1 = st.text_input("Введите нужный регион")

    if click1=="Пивные бары":
        sear = place1+" пивной бар"
    elif click1=="Винные бары":
        sear = place1 + " винный бар"
    elif click1=="Все бары":
        sear = place1 + " бар"

    entrypoint = "https://nominatim.openstreetmap.org/search"
    params = {'q': sear,
              'format': 'json'}
    r = requests.get(entrypoint, params=params)
    data = r.json()
    count = 0
    for item in data:
        count += 1
    st.write("По данным сайта в регионе", place1, "найдено", count, "бара(ов)")
    if st.checkbox( "Показать список баров" ):
        for item in data:
            st.write(item['display_name'])
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.subheader("Еще немного про счастье")
    happyre = d[['HappinessScore', 'Region']]
    d['HappinessScore'] = d['HappinessScore'].round(decimals=0)
    region_count = happyre["Region"].value_counts()
    happyre = happyre.groupby(["Region"]).agg('sum')
    happyre_count = happyre.join(region_count)
    happyre_count["HappinessScore"]=happyre_count["HappinessScore"]/happyre_count["Region"]
    happyre_count.rename(columns={'Region': 'Количество стран'}, inplace=True)
    meow = happyre_count.sort_values("HappinessScore", ascending=False)
    st.write(meow)

    happyre.to_sql(name="Happiness level", con=engine, schema=None, if_exists='fail', index=True,
                   index_label=None, chunksize=None, dtype=None, method=None)
    engine.execute("SELECT * FROM Happiness level").fetchall()

    region_count.to_sql(name="Number of regions", con=engine, schema=None, if_exists='fail', index=True,
                   index_label=None, chunksize=None, dtype=None, method=None)


    
