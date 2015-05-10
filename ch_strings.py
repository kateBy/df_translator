
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
        

def GetTranslate(_text):
    """Функция принимает текст в виде UTF-16"""
    text = _text.decode("utf-16")

    fromInstance = InstanceStrings.get(text)

    if fromInstance != None:
        return fromInstance.encode("utf-16")+b"\0\0"

   
    return None



#Сюда вносятся новые строки для теста
InstanceStrings = {}


InstanceStrings.update(load_trans_mo("./libs/trans.mo"))

def dictToPo(some_dict):
    for item in some_dict:
        print("msgid \"%s\"\nmsgstr \"%s\"\n" % (item, some_dict[item]))



    
