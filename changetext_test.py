"""
Модуль используется во время отладки, для интерактивной перезагрузки
модуля перевода и регулярных выражений, что существенно помогает при создании
перевода, при этом не требуется перезапуск самой игры.
"""
import imp
from time import time
from os.path import getmtime
import ch_strings


global last_modified_main
global last_modified_regul
last_modified_main = getmtime('ch_strings.py')
last_modified_regul = getmtime('regulars.py')

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
