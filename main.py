import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import requests
from streamlit_echarts import st_echarts
from bs4 import BeautifulSoup


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
    st.write("Можно наблюдать, что большая часть мирового счастья принадлежит Австралии и Новой Зеландии. "
             "Меньшая часть принадлежит Африке")
    happyre = d[['HappinessScore', 'Region']]
    d['HappinessScore'] = d['HappinessScore'].round(decimals=0)
    region_count = happyre["Region"].value_counts()
    happyre = happyre.groupby(["Region"]).agg('sum')
    happyre_count = happyre.join(region_count)
    happyre_count["HappinessScore"]=happyre_count["HappinessScore"]/happyre_count["Region"]
    happyre_count.rename(columns={'Region': 'Количество стран'}, inplace=True)
    meow = happyre_count.sort_values("HappinessScore", ascending=False)



    value1 = meow["HappinessScore"].loc[meow.index[0]]
    value2 = meow["HappinessScore"].loc[meow.index[1]]
    value3 = meow["HappinessScore"].loc[meow.index[2]]
    value4 = meow["HappinessScore"].loc[meow.index[3]]
    value5 = meow["HappinessScore"].loc[meow.index[4]]
    value6 = meow["HappinessScore"].loc[meow.index[5]]
    value7 = meow["HappinessScore"].loc[meow.index[6]]
    value8 = meow["HappinessScore"].loc[meow.index[7]]
    value9 = meow["HappinessScore"].loc[meow.index[8]]


    options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "1%", "left": "center"},
    "series": [
        {"name": "Уровень счастья", "type": "pie", "radius": ["30%", "70%"],
         "avoidLabelOverlap": False,
         "itemStyle": {"borderRadius": 15,
                       "borderColor": "#fff",
                       "borderWidth": 3},
         "label": {"show": False, "position": "center"},
         "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
         "labelLine": {"show": False},
         "data": [{"value": value1, "name": "Australia and New Zealand"},
                  {"value": value2, "name": "North America"},
                  {"value": value3, "name": "Western Europe"},
                  {"value": value4, "name": "Latin America and Caribbean"},
                  {"value": value5, "name": "Eastern Asia"},
                  {"value": value6, "name": "Central and Eastern Europe"},
                  {"value": value7, "name": "Southeastern Asia"},
                  {"value": value8, "name": "Middle East and Northern Africa"},
                  {"value": value9, "name": "Sub-Saharan Africa"}]}]}

    st_echarts(options=options, height="600px")

    hidre = d[['HDI', 'Region']]
    region_count = hidre["Region"].value_counts()
    hidre = hidre.groupby(["Region"]).agg('sum')
    hidre_count = hidre.join(region_count)
    hidre_count["HDI"] = hidre_count["HDI"] / hidre_count["Region"]
    hidre_count.rename(columns={'Region': 'Количество стран'}, inplace=True)
    lala = hidre_count.sort_values("HDI", ascending=False)
    st.write("По графику ниже можно понять, что счастливее люди там, где они более развитые, а не там, где больше баров!")

    valu1 = lala["HDI"].loc[lala.index[0]]
    valu2 = lala["HDI"].loc[lala.index[1]]
    valu3 = lala["HDI"].loc[lala.index[2]]
    valu4 = lala["HDI"].loc[lala.index[3]]
    valu5 = lala["HDI"].loc[lala.index[4]]
    valu6 = lala["HDI"].loc[lala.index[5]]
    valu7 = lala["HDI"].loc[lala.index[6]]
    valu8 = lala["HDI"].loc[lala.index[7]]
    valu9 = lala["HDI"].loc[lala.index[8]]

    option = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "1%", "left": "center"},
        "series": [
            {"name": "Уровень человеческого развития", "type": "pie", "radius": ["30%", "70%"],
             "avoidLabelOverlap": False,
             "itemStyle": {"borderRadius": 15,
                           "borderColor": "#fff",
                           "borderWidth": 3},
             "label": {"show": False, "position": "center"},
             "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
             "labelLine": {"show": False},
             "data": [{"value": valu1, "name": "Australia and New Zealand"},
                      {"value": valu2, "name": "North America"},
                      {"value": valu3, "name": "Western Europe"},
                      {"value": valu4, "name": "Latin America and Caribbean"},
                      {"value": valu5, "name": "Eastern Asia"},
                      {"value": valu6, "name": "Central and Eastern Europe"},
                      {"value": valu7, "name": "Southeastern Asia"},
                      {"value": valu8, "name": "Middle East and Northern Africa"},
                      {"value": valu9, "name": "Sub-Saharan Africa"}]}]}

    st_echarts(options=option, height="600px")
    st.subheader("А вообще сейчас мы сдали последний проект на втором курсе и мы счастливы! Так что можно отметить!")
    img = Image.open("photo_.jpg")
    st.image(img, width=700)

