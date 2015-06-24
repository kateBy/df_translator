# -*- coding: utf-8 -*-
import regulars
import imp

imp.reload(regulars) #Необходимо для ребилда модуля регулярных выражений. Для отладки

#Разрешает или запрещает вывод непереведённого текста в консоль
MAKE_OUTPUT = True

#Строки, которые не нужно отображать. Для отладки
DO_NOT_SHOW = [
               "  Dwarf Fortress  ",
               "ESC",
               "Enter",
               "Alt+b",
               ": ",
               "Shift+Enter",
               "Tab"
               ]


def GET_TRANSLATE(original):
    """Функция проверяет наличие перевода строки, если его нет, возвращает запрашиваему назад"""
    if original == "":
        return original
    
    translate = InstanceStrings.get(original)
    if translate != None:
        return translate

    print("TRANSL --->\"%s\"" % original)
    return original

#Передаём модулю обработчик перевода, потому что нет возможности перекрестного импорта
regulars.GET_TRANSLATE = GET_TRANSLATE 


#Сюда вносятся новые строки для теста
InstanceStrings = {

}


#Проверка на пустые строки, иначе будет вылет
checked = True
for i in InstanceStrings:
    if InstanceStrings[i] == "":
        checked = False
        print("---->",i)
        
#Cоздадим исключение, чтобы модуль не загрузился
assert(checked)




def load_trans_mo(fn):
    '''Загрузка перевода из файла .mo с помощью библиотеки polib'''
    import polib
    result = {}
    mofile = polib.mofile(fn)
    for i in mofile:
        if i.msgid.startswith(": "):
            result[i.msgid[2:]] = i.msgstr[2:]
        
        result[i.msgid] = i.msgstr

    return result

toUTF16 = lambda x: x.encode("utf-16")+b"\0\0"
        

def GetTranslate(_text):
    """Функция принимает текст в виде UTF-16"""
    text = _text.decode("utf-16")

    fromInstance = InstanceStrings.get(text)

    if fromInstance != None:
        return toUTF16(fromInstance)

    if len(text) > 1:
        """Если слово не найдено в словаре пробуем искать его с маленькой буквы"""
        if text[0].isupper():
            fromInstance = InstanceStrings.get(text[0].lower() + text[1:])
        else:
            """Вторая попытка поиска слова с большой буквы"""
            fromInstance = InstanceStrings.get(text[0].upper() + text[1:])
            
        if fromInstance != None:
            return toUTF16(fromInstance)

    """Запускаем поиск через регулярные выражения"""
    result = regulars.Regulars(text)
    if result != None:
        return toUTF16(result)

    #Если никак не получилось получить перевод
    return None 
        

        
if __name__ != "__main__":
    InstanceStrings.update(load_trans_mo("./libs/trans.mo"))
    

def dictToPo(some_dict):
    for item in some_dict:
        print("msgid \"%s\"\nmsgstr \"%s\"\n" % (item, some_dict[item]))


if __name__ == "__main__":
    pass
    dictToPo(InstanceStrings)

    
