# Anemobarometer interface
## I.А Описание проекта
Разработка интерфейса для анеморумбометра Сокол-А, предназначенного для измерения и оценки направления и скорости ветра - завершена

Разработка велась на русском и английском языке.

Цель проекта:

1. Визуализация полученных данных о направлении и скорости ветра, полученных с помощью TSP-соединения между анеморумбометром Сокол-А и компьютером.
2. Предупреждение через графический интерфейс пользователя об изменении погодных условий и выведение экрана предупреждения о сильных порывах ветра.

## I.B Project Description
The development of the Sokol-A anemobarometer, designed for measuring and assessing wind direction and speed, is complete.

The development was conducted in Russian and English languages.

Project purposes:

Visualization of the wind direction and speed data obtained through the TSP connection between the Sokol-A anemobarometer and the computer.
Alerting the user through a graphical interface about changes in weather conditions and displaying a warning screen for strong wind gusts.



## II.А Программа

Sokol-A anemobarometer interface
Программа предназначена для получения и распаковки данных с устройства Сокол-А с последующей визуализацией требуемых параметров

Технологии и библиотеки
- Python: язык программирования, на котором написана программа.
- os: модуль Python для работы с операционной системой.
- datetime: модуль Python для работы с датой и временем.
- pandas: библиотека для обработки и анализа данных в Python.
- random: библиотека для генерации случайных чисел
- logging: модуль Python для логирования действий программы на разном уровне
- socket: библиотека для взаимодействия с внешними устройствами по сети
- dash: фреймворк Python для создания графического интерфейса

Модули программы
- Anemobarometer_logger.py - модуль для получения и расшифровки данных с устройства
- Alarm_mode.py - модуль, актвирующий/дезактивирующий окно предупреждения о сильном ветре
- main.py: главный модуль программы, который инициализирует и запускает графическое приложение.

Программа содержит папку INSTRUCTION, в которой файлы с инструкцией на Русском и Английском языке.
Внутри файла:
1. Инструкция по запуску программы
2. Пояснение к графическому интерфесу, записи логов, окну предупреждения

Программа содержит файл отладки программы: Anemobarometer_debug_logs.log, который содержит информацию о прошедших за время итераций событиях



## II.B Program

Sokol-A Anemobarometer
The program is designed to receive and unpack data from the Sokol-A device with the following visualization of requiring parameters.

Technologies and Libraries
- Python: the programming language used to develop the program.
- os: Python module for interacting with the operating system.
- datetime: Python module for working with date and time.
- pandas: a data manipulation and analysis library in Python.
- random: a library for generating random numbers.
- logging: Python module for logging program actions at different levels.
- socket: a library for interacting with external devices over the network.
- dash: Framework Python for creating graphical interface.

Program Modules
- Anemobarometer_logger.py: a module for receiving and decoding data from the device.
- Alarm_mode.py: a module that activates/deactivates the warning window about strong winds.
- main.py: the main program module that initializes and launches the graphical application.

The program contains the INSTRUCTION folder, which includes files with instructions in Russian and English languages.
Inside the file:
1. Instructions for running the program.
2. Explanation of the graphical interface, log recording, and warning window.

The program contains the debugging file: Anemobarometer_debug_logs.log, which contains information about events that occurred during iterations.



## III.a Контактная информация
- Telegram: https://t.me/wondermain, https://t.me/igor_mtrfnv
- E-Mail: tim.yakushev.01@gmail.com, i.v.mitrofanov@ya.ru

## III.B Contact Information
- Telegram: https://t.me/wondermain, https://t.me/igor_mtrfnv
- E-Mail: tim.yakushev.01@gmail.com, i.v.mitrofanov@ya.ru