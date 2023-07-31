import datetime


class AlarmMode:
    """
    Описание класса: Предназначен для активации окна add_annotation в Dash.
    Если скорость ветра превышает установленный лимит, то в окне Dash активируется окно предупреждения на 5 сек.

    Атрибуты:
    - alarm_off_time (datetime) - время, в которое будет отключаться окно предупреждения
    - visible (boolean) - флаг, принимающий исходное состояние окна предупреждения
    - warning_speed (float) - скорость ветра, при которой загорелось окно

    Методы:
    - __init__(self): конструктор класса.
    - alarm_label(self, r): возвращает видимость окна предупреждения.
    """     
    def __init__(self):
        self.alarm_off_time = datetime.datetime.now().replace(microsecond=0)
        self.visible = False
        self.warning_speed = None

    def alarm_label(self, r):
        """
        В зависимости от значения скорости ветра возвращает True или False для переменной visible
 
        Параметры: 
        - r (list):  список со значением скорости ветра.

        Возвращает:
        - visible (boolean)
        - warning_speed (float)
        """
        datetime_now = datetime.datetime.now().replace(microsecond=0)
        turn_off_time = datetime_now + datetime.timedelta(seconds=5)
        
        if self.alarm_off_time <= datetime_now:
            if r[0] >= 17.5:
                self.visible = True
                #logging.info('alarm is occurred')
                self.alarm_off_time = turn_off_time
                self.warning_speed = r[0] # Сохраняем  r[0] при котором сработал alarm
            else:
                self.visible = False
        else:
            self.visible = True

        return self.visible, self.warning_speed
    
# TODO: предлагаю длительность появления аларма сделать настраиваемым параметром, а не хардкодом. т.е. добавить в инициализацию или функцию alarm_label.
# Тоже самое касается порога скорости ветра для аларма - введи константу WIND_SPEED_THRESHOLD.
# Названия имен классов принято делать верблюжим кейсом, перед и после класса пропускают 2 пустые строки