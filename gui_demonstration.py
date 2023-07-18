import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import random

# Создаем объект приложения Dash
app = dash.Dash(__name__)

# Создаем подложку для графиков

# Определяем макет (layout) приложения
app.layout = html.Div(
    [
        html.H1("Динамическая Колонка № 1 "),

        # Выводим три графика с использованием компонента dcc.Graph для отображения графических данных
        dcc.Graph(id="polar-plot1"),
        dcc.Graph(id="polar-plot2"),
        dcc.Graph(id="polar-plot3"),

        # Устанавливаем интервал обновления в 1 секунду
        dcc.Interval(
            id="interval-component",
            interval=1000,  # Обновление каждую секунду
            n_intervals=0,
        ),
    ]
)

# Определяем функцию-колбэк для обновления графиков
@app.callback(
    [Output("polar-plot1", "figure"),
     Output("polar-plot2", "figure"),
     Output("polar-plot3", "figure")],
    [Input("interval-component", "n_intervals")]
)
# Генерируем случайные значения для графиков
def update_polar_plots(n):
    fig1 = update_polar_plot(device_number=1)  # Передаем номер устройства в функцию
    fig2 = update_polar_plot(device_number=2)
    fig3 = update_polar_plot(device_number=3)
    return fig1, fig2, fig3

# Функция для создания графика с случайными значениями
def update_polar_plot(device_number):
    r = [random.uniform(0, 20)]  # Радиусы
    theta = [random.uniform(0, 360)]  # Углы

    # Создаем объект графика в полярной системе координат
    fig = go.Figure(go.Barpolar(
        r=r,
        theta=theta,
        width=8,
        base=0,
        offset=-4,
        marker_line_width=0,
        hovertext=["Скорость ветра: {:.1f}, БББ: {:.0f}".format(r[0], theta[0])],
        hovertemplate="Скорость ветра: %{r:.1f} м/с <br> БББ: %{theta:.0f}°<extra></extra>",
        hoverlabel=dict(font=dict(size=14, color='white')),
        showlegend=True,
        name="Скорость ветра: {:.1f} м/с<br>Направление: {:.0f}°".format(r[0], theta[0])))
    
    fig.update_layout(title='Устройство №: {:d}'.format(device_number), width=800, height=520, 
                      polar=dict(
                          angularaxis=dict(direction="clockwise",
                                                  tickvals=np.arange(0, 360, 22.5),
                                                  ticktext=["С", "ССВ", "СВ", "ВСВ",
                                                            "В", "ВЮВ", "ЮВ", "ЮЮВ",
                                                            "Ю", "ЗЗЮ", "ЗЮ", "ЗЮЗ",
                                                            "З", "ЗСЗ", "СЗ", "ССЗ"],
                                                    ),
                                 radialaxis=dict(range=[0, 20])),
                                 legend=dict(font=dict(size=16),
        x=0.31, y=-0.3,
        title=dict(font=dict(size=16)),  # Размер шрифта заголовка легенды
        traceorder="normal",  # Порядок отображения легенды
        itemsizing="constant",  # Размер элементов легенды всегда одинаковый
    ),
)

    fig.update_traces(marker=dict(color='rgb(30, 136, 229)',  # Устанавливаем цвет маркера
                                  line=dict(color='rgb(30, 136, 229)',
                                  width=1)),  # Устанавливаем цвет линии маркера
                                  opacity=0.75)  # Устанавливаем непрозрачность маркера

    return fig

# Запускаем сервер Dash
if __name__ == '__main__':
    app.run_server(debug=False)
