import imp
from time import time
from os.path import getmtime
import ch_strings


global last_modified_time
last_modified_time = getmtime('ch_strings.py')

global last_answer
global last_ask

last_answer = None
last_ask = None


def ChangeText(s):
    global last_modified_time
    global last_answer
    global last_ask

    try:
        modtime = getmtime('ch_strings.py')
        if (modtime != last_modified_time):
           last_modified_time = modtime
           print("Перезагрузка модуля ch_strings.py")
           imp.reload(ch_strings)
    except:
        print("Ошибка при перезагрузке модуля")
           
    if last_ask == s:
        return last_answer
    else:
        last_ask = s
    
    decoded = s.decode("utf-16")

    try:
        result = ch_strings.GetTranslate(s)
    except:
        print("Ошибка при получении перевода")
        result = None
    
    if result != None:
        last_answer = result
        return result
    else:
        if ch_strings.MAKE_OUTPUT:
            print('\"%s\"' % decoded)
        last_answer = None
        return None

def test(text):
    a = ChangeText(text.encode("utf-16"))
    if a != None:
        print(a[:-2].decode("utf-16"))
    else:
        print("Not Found")
