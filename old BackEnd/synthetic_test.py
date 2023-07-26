
def find_match_at_beginning(data, pattern):
    if data.startswith(pattern):
        print("Найдено совпадение в начале строки")
    else:
        print("Совпадение не найдено в начале строки")

pattern = b'\x01\x03\x0e'
string1 = b'\x01\x03\x0e'  # Совпадение в начале строки
string2 = b'Something \x01\x03\x0e something else'  # Нет совпадения в начале строки

find_match_at_beginning(string1, pattern)
find_match_at_beginning(string2, pattern)



'''
def bytes_to_hex_string(input_str):
    # Переводим байтовую строку в шестнадцатеричное представление
    hex_string = input_str.hex()

    # Выводим полученную шестнадцатеричную строку и её длину
    print("строка:", hex_string)
    print("Длина шестна строки:", len(hex_string))

    # Возвращаем шестнадцатеричную строку и её длину в виде кортежа
    return hex_string, len(hex_string)

# Пример использования функции
input_str = b'\x00\x00\x00\x00\xa4\x00\xa4\xb0\xa8\x00\x00\x00\x00\xa4\x00\xa4\xb0\xa8\x01\x03\x0e\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x00\xa4\xb0\xa8'
bytes_to_hex_string(input_str)
'''