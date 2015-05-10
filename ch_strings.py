
# -*- coding: utf-8 -*-

import re


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
    else:
        result = Regulars(text)
        if result != None:
            return result.encode("utf-16")+b"\0\0"
        

   
    return None


WORD_AND_NUM_IN_COMMONS = re.compile(r"[\w/]+?\s\(\d+?\)$") #Citizens (7) | Pets/Livestock (16)
SKILLS = re.compile(r"(Novice|Adequate|Proficient|Legendary)\s\w+?") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL = re.compile(r"(Stray)\s\w+?\s\((Tame)\)$") #Stray Hen (Tame)
#TWO_WORDS = re.compile(r"\w+?\s\w+?") 
#THREE_WORDS = re.compile(r"\w+\s\w+\s\w+") 




def GET_TRANSLATE(original):
    translate = InstanceStrings.get(original)
    if translate == None:
        return original
    else:
        return translate

def PROC_WORD_AND_NUM_IN_COMMONS(text):
    tmp = text.split(" ") #Делим строку делителем
    trans = GET_TRANSLATE(tmp[0]) #Запрашиваем перевод первой части
    return trans + " " + tmp[1]


def PROC_SKILLS(text):
    tmp = text.split(" ")
    quality = GET_TRANSLATE(tmp[0])
    skill  = GET_TRANSLATE(" ".join(tmp[1:]))
    ret = quality + " " + skill
    return ret

def PROC_STRAY_ANIMAL(text):
    tmp = text.split(" ")
    

#Словарь регулярных выражений, состоит из самого выражения и функции-обработчика дла нее
expressions = {
WORD_AND_NUM_IN_COMMONS:PROC_WORD_AND_NUM_IN_COMMONS,
SKILLS:PROC_SKILLS,
STRAY_ANIMAL:PROC_STRAY_ANIMAL
}    
    

def Regulars(text):
    result = None
    for exp in expressions:
        if exp.match(text):                 #Фраза соответствует шаблону
            result = expressions[exp](text) #Передаём текст на обработчик этого шаблона
            break

    return result


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
        

        
if __name__ != "__main__":
    InstanceStrings.update(load_trans_mo("./libs/trans.mo"))
    

def dictToPo(some_dict):
    for item in some_dict:
        print("msgid \"%s\"\nmsgstr \"%s\"\n" % (item, some_dict[item]))


if __name__ == "__main__":
    pass
    dictToPo(InstanceStrings)

    
