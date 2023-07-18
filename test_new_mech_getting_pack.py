import os
import socket
import time 
import datetime
import pandas as pd
import logging

# Логирование работы программы логирования ^_^
logging.basicConfig(filename="Rose_Wind__logger_program.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s') 

class Wind_Rose_logger:
    def __init__(self, ip_adress='192.168.54.123', port=8001, timeout=1):
        self.address_to_server = (ip_adress, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address_to_server)
        logging.info('logger initialized')



def save_to_csv(self, string, name_addition=''):
    logger_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    date_now = time_now.split()[0]
    writepath = logger_path + date_now  + '_Wind_Rose' + '.csv'

    mode = 'a' if os.path.exists(writepath) else 'w'

    with open(logger_path + name_addition + date_now + '.csv', mode) as file:
        if mode == 'w':
            file.write('Datetime, WindSpeed, WindGust_10min, WindSpeed_10min, WindSpeed_1min, WindDir_1min, WindDir_10min  \n')
            print('file created with name ' + date_now + name_addition + '.csv')
            logging.info('file created')
            file.close()
        elif mode == 'a':
            file.write(time_now + ',' + string)
            logging.info('string written to file')
            print('WRITE: ', time_now + ',' + string)
            file.close()


def unpack_message(received_data):
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


def send_messsage_get_esponse():
    buffer = b''
    message = b'\x01\x03\x00\x00\x00\x07\x04\x08'
    client.send(message)
    logging.info('message has sent')

    while True:
        input_data = client.recv(10)  # Читаем небольшой фрагмент данных
        logging.info('get batch')
        buffer += input_data

        if buffer.startswith(b'\x01\x03\x0e') and len(buffer) >= 19:
            received_data = buffer[:19]
            buffer = buffer[19:] 
            logging.info('batch is ready')
            data_dict, string = unpack_message(received_data)
            try:
                save_to_csv(string)
                #print(data_dict)
                #print()
            except:
                print('Сначала закройте файл записи!')
            break       
         
        time.sleep(0.3)

while True:
    send_messsage_get_esponse()
    

