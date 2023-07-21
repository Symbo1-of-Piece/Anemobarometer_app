import random
import os
import logging
from Wind_Rose_logger import Wind_Rose_logger

# Установка библиотек при первом запуске программы, если это необходимо
try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np

try:
    import pandas as pd
except:
    os.system('pip install pandas')
    import pandas as pd

try:
    import plotly.graph_objects as go
except:
    os.system('pip install plotly')
    import plotly.graph_objects as go

try:
    import dash
    from dash import dcc
    from dash import html
    from dash.dependencies import Input, Output
except:
    os.system('pip install dash')
    import dash
    from dash import dcc
    from dash import html
    from dash.dependencies import Input, Output

try:
    import webbrowser
except:
    os.system('pip install webbrowser')
    import webbrowser

import datetime
logger_WR = Wind_Rose_logger()

# Создаем объект приложения Dash
app = dash.Dash(__name__)
logging.info('app created')

app.layout = html.Div(
    [
        html.H1("Флюгер_Анемометр "),

        # Выводим три графика с использованием компонента dcc.Graph для отображения графических данных
        dcc.Graph(id="polar-plot1"),
        dcc.Graph(id="polar-plot2"),
        dcc.Graph(id="polar-plot3"),
        dcc.Graph(id="polar-plot4"),

        # Устанавливаем интервал обновления в 1 секунду
        dcc.Interval(
            id="interval-component",
            interval=1000,
            n_intervals=0,
        ),
    ]
)
logging.info('layout created')

# устанавливаем цвет и прозрачность стрелки
marker_style = dict(color='rgb(30, 136, 229)', line=dict(color='rgb(30, 136, 229)', width=1))
opacity = 0.75

# Определяем функцию-колбэк для обновления графиков
@app.callback(
    [Output("polar-plot1", "figure"),
     Output("polar-plot2", "figure"),
     Output("polar-plot3", "figure"),
     Output("polar-plot4", "figure")],
    [Input("interval-component", "n_intervals")],
    prevent_initial_callbacks=True)

# Генерируем случайные значения для графиков
def update_polar_plots(n):
    fig1 = update_polar_plot(device_number=1)  # Передаем номер устройства в функцию
    fig2 = update_polar_plot(device_number=2)
    fig3 = update_polar_plot(device_number=3)
    fig4 = update_polar_plot(device_number=4)
    logging.info('update_polar_plots')
    return fig1, fig2, fig3, fig4

# Функция для создания графика с случайными значениями
def create_random_data_for_plot():
    r_random = [round(random.uniform(0, 20),1)]  # Сила ветра
    theta_random = [round(random.uniform(0, 360),0)]  # Угол ветра
    df_random = pd.DataFrame({'speed': [r_random], 'direction': [theta_random]})
    logging.info('df_random created')
    return df_random

def get_random_data():
    df_random = create_random_data_for_plot()
    r_random = df_random['speed'].values[0]  # Сила ветра
    theta_random = df_random['direction'].values[0]  # Угол ветра
    logging.info(f'random values received: {r_random}, {theta_random}')
    return r_random, theta_random

def get_data_from_RW_class():
    try:
        df_WR = logger_WR.get_data()
        r_WR = [df_WR['WindSpeed'].values[0]]         # скорость ветра
        theta_WR = [df_WR['WindDir_1min'].values[0]]  # угол направления ветра
        logging.info(f'r, theta received: {r_WR}, {theta_WR}')
        return r_WR, theta_WR
    except Exception as e:
        logging.warning(f'r, theta did not received. {e}')
        print("Произошла ошибка", str(e))

def update_polar_plot(device_number):
    
    if device_number == 1:
        r, theta = get_data_from_RW_class() 
    else:
        r, theta = get_random_data()
    logging.info('random and real data received')

    # Создаем объект графика в полярной системе координат
    fig = go.Figure(go.Barpolar(
        r=r,
        theta=theta,
        width=8,
        base=0,
        offset=-4,
        marker_line_width=0,
        hovertemplate="speed: %{r:.1f} m/s <br> direction: %{theta:.0f}°<extra></extra>",
        hoverlabel=dict(font=dict(size=14, color='white')),
        showlegend=True,
        name = f"Скорость ветра: {r[0]:.1f} м/с<br>Направление: {theta[0]:.0f}°"))
    logging.info('Barpolar plot created')

    fig.add_annotation(
        xref='paper',          # Относительно ширины холста (в процентах)
        x=1.05,       
        y=1,
        text="ВНИМАНИЕ<br>сильный ветер!",
        showarrow=False,
        #arrowhead='arrow',
        font=dict(size=25, color='red'),
        align='center',
        visible=True,
        width=450 
    )

    try:
        fig.update_layout(title= f'Устройство №: {device_number}', width=800, height=520, 
                        polar=dict(
                                    angularaxis=dict(direction="clockwise",
                                                tickvals=np.arange(0, 360, 22.5),
                                                ticktext=["С", "ССВ", "СВ", "ВСВ",
                                                            "В", "ВЮВ", "ЮВ", "ЮЮВ",
                                                            "Ю", "ЗЗЮ", "ЗЮ", "ЗЮЗ",
                                                            "З", "ЗСЗ", "СЗ", "ССЗ"]),
                                    radialaxis=dict(range=[0, 6])),
                        legend=dict(font=dict(size=16),
                        x=0.31, y=-0.3,
                        title=dict(font=dict(size=16)),  # Размер шрифта заголовка легенды
                        traceorder="normal",  # Порядок отображения легенды
                        itemsizing="constant"))  # Размер элементов легенды всегда одинаковый                
                        
        fig.update_traces(marker=marker_style, opacity=0.75) # Устанавливаем цвет линии маркера и непрозрачность
        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)  # Убираем оси и метки на графике
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
        logging.info('figure returned')                              
        return fig
    except Exception as e:
        logging.warning(f'Barpolar plot did not created. {e}')

# Запускаем сервер Dash
if __name__ == '__main__':
    url = 'http://localhost:8025'
    webbrowser.open_new(url)
    app.run_server(debug=False, port = 8025)
    logging.info('server is launched')