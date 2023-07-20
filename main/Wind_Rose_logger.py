import os
import logging
import pandas as pd

try:
    import re
except:
    os.system('pip install re')
    import re

try:
    import socket
except:
    os.system('pip install socket')
    import socket

try:
    import datetime
except:
    os.system('pip install datetime')
    import datetime



# Логирование работы программы логирования ^_^
logging.basicConfig(filename="Rose_Wind__logger_program.log", level=logging.DEBUG,
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

                except Exception as e:
                    # Обработка исключения
                    print("Произошла ошибка:", str(e))
                    #print('Сначала закройте файл записи!')
                break       
        

        df = pd.DataFrame(data=data_dict, index=[0])
        return df