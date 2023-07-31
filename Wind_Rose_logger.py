import os
import logging
import pandas as pd
import socket

try:
    import re
except:
    os.system('pip install re')
    import re

try:
    import datetime
    from datetime import timedelta
except:
    os.system('pip install datetime')
    import datetime
    from datetime import timedelta




# Логирование работы программы логирования ^_^
logging.basicConfig(filename="Rose_Wind_logger_program.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s') 

class Wind_Rose_logger:
    """
    Описание класса Wind_Rose_logger: Предназначен для логирования работы флюгера-анемометра (далее ФА) и записи логов в формате CSV
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
        Происходит подключение к серверу по указанным адресу и порту по протоколу IPv4 

        Параметры:
        - port (str): название COM-порта устройства, к которому подключается ГА.
        """
        self.address_to_server = (ip_adress, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address_to_server)
        logging.info('logger initialized')

    def unpack_message(self, received_data):
        """
        Распаковывает байтовую строку из ФА по параметрам.
        
        Параметры:
        - received_data (str): байтовая строка, которая будет распакована.
        
        Возвращает:
        - data_dict (dict): словарь с данными.
        - string (str): строка данных, которая была распакована.
        """

        # Получим все необходимые для программы переменные времени
        datetime_now = datetime.datetime.now().replace(microsecond=0)
        time_for_csv = datetime_now.strftime('%Y-%m-%d %H:%M:%S')
        
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
                    'datetime_now': datetime_now,
                    'WindSpeed': WindSpeed,
                    'WindGust_10min': WindGust_10min,
                    'WindSpeed_10min': WindSpeed_10min,
                    'WindSpeed_1min': WindSpeed_1min,
                    'WindDir_1min': WindDir_1min,
                    'WindDir_10min': WindDir_10min}
            logging.info('data is unpacked')
            return data_dict, string, time_for_csv

        except socket.error as e:
            logging.warning(f'data do not unpacked: {e}')
            print("Произошла ошибка, что грустно", str(e), len(received_data))

    def save_to_csv(self, string, time_for_csv, name_addition=''):
        """
        Создает csv файл с именем в формате: приставка_имени+дата+.csv , или добавляет строку данных в существующий с таким именем файл csv.
        
        Параметры:
        - string (str): строка данных, которая будет записана в файл.
        - name_addition (str): приставка к имени файла для тестов и отладки.
        - time_for_csv (str): текущие дата и время
        """
        logger_path = os.path.dirname(os.path.realpath(__file__)) + '/logs/'
        date_for_name = time_for_csv.split()[0]
        writepath = logger_path + date_for_name  + name_addition + '.csv'
        mode = 'a' if os.path.exists(writepath) else 'w'

        with open(logger_path + name_addition + date_for_name + '.csv', mode) as file:
            if mode == 'w':
                file.write('Datetime, WindSpeed, WindGust_10min, WindSpeed_10min, WindSpeed_1min, WindDir_1min, WindDir_10min  \n')
                print('file created with name ' + name_addition + date_for_name + '.csv')
                logging.info('file created')
                file.close()
            elif mode == 'a':
                file.write(time_for_csv + ',' + string)
                logging.info('string written to file')
                print('Записана строка: ', time_for_csv + ',' + string)
                file.close()

    def get_data(self, name_addition=''):
        """
        Получает данные из ФА и сохраняет их в csv файл.
        
        Параметры:
        - name_addition (str): приставка к имени файла для тестов и отладки.
        
        Возвращает:
        - df (pandas.DataFrame): данные из ФА.
        """
        buffer = b'' # Инициализируем пустой буфер
        message = b'\x01\x03\x00\x00\x00\x07\x04\x08' # Сообщение устройству, для получения от него данных 
        pattern = b'\x01\x03\x0e' # Паттерн для определения начала пакета
        self.client.send(message)
        logging.info('message has sent')

        while True:
            input_data = self.client.recv(19)  # Читаем пакет данных
            logging.info(f'get batch {input_data}, length: {len(input_data)}')
            buffer += input_data
            logging.info(f'buffer: {buffer}, length: {len(buffer)}')

            if buffer.startswith(pattern) and len(buffer) == 19:
                logging.info(f'we in  {buffer}')
                received_data = buffer[:19]
                buffer = buffer[19:] 
                logging.info(f'buffer is ready  {buffer}, length: {len(buffer)}')
                data_dict, string, time_for_csv = self.unpack_message(received_data)
                try:
                    self.save_to_csv(string, time_for_csv, name_addition)

                except Exception as e:
                    #print("Произошла ошибка:", str(e))
                    logging.warning('written error: ', str(e))
                    print('Сначала закройте файл записи!')
                    buffer = b''
                    data_dict = {'datetime_now': datetime.datetime.now().replace(microsecond=0),
                                 'WindSpeed': 0,
                                 'WindGust_10min': 0,
                                 'WindSpeed_10min': 0,
                                 'WindSpeed_1min': 0,
                                 'WindDir_1min': 0,
                                 'WindDir_10min': 0}
                    # если произойдет ошибка, то вернется пустой Df и программа не упадет
                    df = pd.DataFrame(data_dict, index=[0]) 
                break   
            else:
                logging.warning('buffer is bad: {buffer}')
                buffer = b''    
        
        df = pd.DataFrame(data=data_dict, index=[0])
        logging.info(f'df returned to Dash')
        return df