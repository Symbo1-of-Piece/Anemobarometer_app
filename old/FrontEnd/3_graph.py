import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import numpy as np
import random
import pandas as pd
import os
import socket
import time 
import datetime
import logging
import re
import webbrowser



# Логирование работы программы логирования ^_^
logging.basicConfig(filename="Rose_Wind__logger_program3.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s') 

class Wind_Rose_logger:
    """
    Описание класса Wind_Rose_logger. Предназначен для логирования работы флюгера-анемометра (далее ФА) и записи логов в формате CSV
    Получает на входе байтовую строку, содержащую информацию о силе и направлении ветра, зарегистрированных датчиками устройства.
    на выходе возвращает df (pandas.DataFrame), содержащий значения каждого параметра и файл csv

    Атрибуты:
    - ip_adress (str) - адрес, по которому связаны устройство и компьютер
    - port (int) - порт связывающий компьютер и устройство
    Методы:
    - __init__(self, port, baudrate, timeout): конструктор класса.
    - save_to_csv(self, string, name_addition=''): метод, выполняющий сохранение строки данных в файл csv. 
    - unpack(self, received_data): метод, распаковывающий полученную байтовую строку из Флюгера-Анемеметра по параметрам.
    - get_data(self, name_addition=''): Основной метод класса который:
         1. Осуществляет отправку сообщения через сокет на с TSP-сервер и получает ответ, содержащий байтовую строку 
         2. Распаковывает данные и сохраняет их в формате CSV
         3. Возвращает обхект DataFrame для последующей визуализации параметров
    """
    def __init__(self, ip_adress='192.168.54.123', port=8001):
        """
        Конструктор класса Wind_Rose_logger.
        Создает объект класса socket. Тип сокета - TSP-клиент. 
        Происходит подключение к серверу по указанным адресом и портом по протоколу IPv4 

        Параметры:
        - port (str): название COM-порта устройства, к которому подключается ГА.
        """
        self.address_to_server = (ip_adress, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address_to_server)
        logging.info('logger initialized')
        


    def save_to_csv(self, string, name_addition=''):
        """
        Создает csv файл с именем в формате: приставка_имени+дата+.csv , или добавляет строку данных в существующий с таким именем файл csv.
        
        Параметры:
        - string (str): строка данных, которая будет записана в файл.
        - name_addition (str): приставка к имени файла для тестов и отладки.
        """
        logger_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        date_now = time_now.split()[0]
        writepath = logger_path + date_now  + name_addition + '.csv'

        mode = 'a' if os.path.exists(writepath) else 'w'

        with open(logger_path + name_addition + date_now + '.csv', mode) as file:
            if mode == 'w':
                file.write('Datetime, WindSpeed, WindGust_10min, WindSpeed_10min, WindSpeed_1min, WindDir_1min, WindDir_10min  \n')
                print('file created with name ' + name_addition + date_now + '.csv')
                logging.info('file created')
                file.close()
            elif mode == 'a':
                file.write(time_now + ',' + string)
                logging.info('string written to file')
                print('WRITE: ', time_now + ',' + string)
                file.close()


    def unpack_message(self, received_data):
        """
        Распаковывает байтовую строку из ФА по параметрам.
        
        Параметры:
        - received_data (str): байтовая строка, которая будет распакована.
        
        Возвращает:
        - data_dict (dict): словарь с данными.
        - string (str): строка данных, которая была распакована.
        """
        try:
            SokolAnswer = received_data.hex()  

            Device_Type = SokolAnswer[6:10]
            WindSpeed = (int(SokolAnswer[10:14],16)/10)
            WindGust_10min = (int(SokolAnswer[14:18],16)/10)
            WindSpeed_10min = (int(SokolAnswer[18:22],16)/10)
            WindSpeed_1min = (int(SokolAnswer[22:26],16)/10)
            WindDir_1min = int(SokolAnswer[26:30],16)
            WindDir_10min = int(SokolAnswer[30:34],16)

            list_for_string = [WindSpeed, WindGust_10min,
                            WindSpeed_10min, WindSpeed_1min,
                            WindDir_1min, WindDir_10min]
            string = ','.join(str(item) for item in list_for_string) + '\n'

            data_dict = {
                    'datetime': pd.Timestamp(datetime.datetime.now().replace(microsecond=0)).timestamp(),
                    'WindSpeed': WindSpeed,
                    'WindGust_10min': WindGust_10min,
                    'WindSpeed_10min': WindSpeed_10min,
                    'WindSpeed_1min': WindSpeed_1min,
                    'WindDir_1min': WindDir_1min,
                    'WindDir_10min': WindDir_10min}
            logging.info('data is unpacked')
            return data_dict, string

        except socket.error as e:
            logging.warning(f'data do not unpacked: {e}')
            print("Произошла ошибка, что грустно", str(e), len(received_data))


    def get_data(self, name_addition=''):
        """
        Получает данные из ФА и сохраняет их в csv файл.
        
        Параметры:
        - name_addition (str): приставка к имени файла для тестов и отладки.
        
        Возвращает:
        - df (pandas.DataFrame): данные из ФА.
        """
        buffer = b''
        message = b'\x01\x03\x00\x00\x00\x07\x04\x08'
        pattern = re.compile(rb'\x01\x03\x0e') # Паттерн для определения начала пакета
        self.client.send(message)
        logging.info('message has sent')

        while True:
            input_data = self.client.recv(10)  # Читаем небольшой фрагмент данных
            logging.info(f'get batch {buffer}')
            buffer += input_data

            if re.match(pattern, buffer) and len(buffer) >= 19:
                received_data = buffer[:19]
                buffer = buffer[19:] 
                logging.info(f'batch is ready  {buffer}')
                data_dict, string = self.unpack_message(received_data)
                try:
                    self.save_to_csv(string, name_addition)
                    print(data_dict)
                    print()
                except Exception as e:
                    # Обработка исключения
                    print("Произошла ошибка:", str(e))
                    #print('Сначала закройте файл записи!')
                break       
        
            #time.sleep(0.3)

        df = pd.DataFrame(data=data_dict, index=[0])
        return df


logger_WR = Wind_Rose_logger()


# Создаем объект приложения Dash
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Флюгер_Анемометр "),

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

marker_style = dict(color='rgb(30, 136, 229)',
                    line=dict(color='rgb(30, 136, 229)', width=1))
opacity = 0.75

# Определяем функцию-колбэк для обновления графиков
@app.callback(
    [Output("polar-plot1", "figure"),
     Output("polar-plot2", "figure"),
     Output("polar-plot3", "figure")],
    [Input("interval-component", "n_intervals")],
    prevent_initial_callbacks=True
)
# Генерируем случайные значения для графиков
def update_polar_plots(n):
    fig1 = update_polar_plot(device_number=1)  # Передаем номер устройства в функцию
    fig2 = update_polar_plot(device_number=2)
    fig3 = update_polar_plot(device_number=3)
    return fig1, fig2, fig3

# Функция для создания графика с случайными значениями
def get_random_data_for_plot():
    r_random = [random.uniform(0, 20)]  # Сила ветра
    theta_random = [random.uniform(0, 360)]  # Угол ветра
    df_random = pd.DataFrame({
        'speed': [r_random],
        'direction': [theta_random]})
    logging.info('random data created and return')
    return df_random

def update_polar_plot(device_number):
    try:
        df = logger_WR.get_data()
        r = [df['WindSpeed'].values[0]]  # скорость ветра
        theta = [df['WindDir_1min'].values[0]] # угол направления ветра
        logging.info(f'r, theta received: {r}, {theta}')
    except Exception as e:
        logging.warning('r, theta did not received. {e}')
        print("Произошла ошибка", str(e))

    df_random = get_random_data_for_plot() 
    r_random = df_random['speed'].values[0]
    theta_random = df_random['direction'].values[0]

    # Создаем объект графика в полярной системе координат
    fig = go.Figure(go.Barpolar(
        r=r,
        theta=theta,
        width=8,
        base=0,
        offset=-4,
        marker_line_width=0,
        hovertext = [f"Скорость ветра: {r[0]:.1f}, БББ: {theta[0]:.0f}"], # отображение информации при наведении курсора
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
                                                         "З", "ЗСЗ", "СЗ", "ССЗ"]),
                                radialaxis=dict(range=[0, 6])),
                      legend=dict(font=dict(size=16),
                      x=0.31, y=-0.3,
                      title=dict(font=dict(size=16)),  # Размер шрифта заголовка легенды
                      traceorder="normal",  # Порядок отображения легенды
                      itemsizing="constant"))  # Размер элементов легенды всегда одинаковый                
                       
    fig.update_traces(marker=marker_style, opacity=0.75) # Устанавливаем цвет линии маркера и непрозрачность
                                  
    return fig

# Запускаем сервер Dash
if __name__ == '__main__':
    url = 'http://localhost:8025'
    webbrowser.open_new(url)
    app.run_server(debug=False, port = 8025)
    logging.info('server is launched')
    
    
