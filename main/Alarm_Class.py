import datetime
import logging

class Alarm_Class:
    """
    Описание класса Alarm_Class. Предназначен для активации окна add_annotation в Dash
    Если скорость ветра превышает установленный лимит, то в окне Dash активируется окно предупреждения на 3 сек.

    Атрибуты:
    - alarm_off_time (datetime) - время, в которое будет отключится окно предупреждения
    - visible (boolean) - флаг, принимающий исходное состояние окна предупреждения
    Методы:
    - __init__(self): конструктор класса.
    - alarm_label(self, r) 
    
    """     
    def __init__(self):
        self.alarm_off_time = datetime.datetime.now().replace(microsecond=0)
        self.visible = False

    def alarm_label(self, r):
        """
        В зависимости от значения скорости ветра возвращает True или False для переменной visible
 
        Параметры:
        - r (list):  список со значением скорости ветра.

        Возвращает:
        - visible (boolean)
        """
        datetime_now = datetime.datetime.now().replace(microsecond=0)
        turn_off_time = datetime_now + datetime.timedelta(seconds=3)

        if self.alarm_off_time <= datetime_now:
            if r[0] >= 18:
                self.visible = True
                #logging.info('alarm is occurred')
                self.alarm_off_time = turn_off_time
            else:
                self.visible = False
        else:
            self.visible = True

        return self.visible
