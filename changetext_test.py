import imp
from time import time
from os.path import getmtime
import ch_strings


global last_modified_main
global last_modified_regul
last_modified_main = getmtime('ch_strings.py')
last_modified_regul = getmtime('regulars.py')

global last_answer
global last_ask

last_answer = None
last_ask = None


def ChangeText(s):
    global last_modified_main
    global last_modified_regul
    global last_answer
    global last_ask

    try:
        modtime_main = getmtime('ch_strings.py')
        if (modtime_main != last_modified_main):
           last_modified_main = modtime_main
           print("Перезагрузка модуля ch_strings.py")
           imp.reload(ch_strings)
    except:
        print("Ошибка при перезагрузке модуля ch_strings.py")


    try:
        modtime_regul = getmtime('regulars.py')
        if (modtime_regul != last_modified_regul):
           last_modified_regul = modtime_regul
           print("Перезагрузка модуля regulars.py")
           imp.reload(ch_strings)
    except:
        print("Ошибка при перезагрузке модуля regulars.py")







        
           
    if last_ask == s:
        return last_answer
    else:
        last_ask = s
    
    decoded = s.decode("utf-16")

    try:
        result = ch_strings.GetTranslate(s)
    except:
        print("Ошибка при получении перевода", decoded)
        result = None
    
    if result != None:
        last_answer = result
        return result
    else:
        if ch_strings.MAKE_OUTPUT:
            if len(decoded) > 1:
                if not (decoded in ch_strings.DO_NOT_SHOW):
                    print('\"%s\"' % decoded)
        last_answer = None
        return None

def test(text):
    a = ChangeText(text.encode("utf-16"))
    if a != None:
        print(a[:-2].decode("utf-16"))
    else:
        print("Not Found")
