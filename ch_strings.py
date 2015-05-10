
# -*- coding: utf-8 -*-

import re

MAKE_OUTPUT = True


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


MENU_U_TITLE = re.compile(r"(Citizens|Pets/Livestock|Others|Dead/Missing)\s(\(\d+\))") #Citizens (7) | Pets/Livestock (16)
SKILLS = re.compile(r"(Novice|Adequate|Proficient|Legendary)\s") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL = re.compile(r"Stray\s((\w+\s)+)") #Stray Hen (Tame) | Stray Yak Cow (Tame)
STRAY_ANIMAL_GENDER = re.compile(r"Stray\s(\w+?),\s(♀|♂)\s\((\S+?)\)") #"Stray Dog, ♀♂ (Tame)"
#TWO_WORDS = re.compile(r"\w+?\s\w+?") 
#THREE_WORDS = re.compile(r"\w+\s\w+\s\w+") 




def GET_TRANSLATE(original):
    """Функция проверяет наличие перевода строки, если его нет, возвращает запрашиваему назад"""
    translate = InstanceStrings.get(original)
    if translate == None:
        return original
    else:
        return translate

def TEST_GENDER(word):
    """Проверяет какой пол у существительного"""
    if word[-1] in ['а', 'я']:
        return "FEMALE"
    else:
        return "MALE"
    

def PROC_MENU_U_TITLE(text):
    """Функция обработки выражений типа: Citizens (7)"""
    tmp = MENU_U_TITLE.split(text) #Делим строку делителем
    trans = GET_TRANSLATE(tmp[1])    #Запрашиваем слова
    return trans + " " + tmp[2]


def PROC_SKILLS(text):
    """Функция обработки выражений типа: Novice Miner"""
    tmp = SKILLS.split(text)
    quality = GET_TRANSLATE(tmp[1])
    skill  = GET_TRANSLATE(tmp[2])
    ret = quality + " " + skill
    return ret


def PROC_STRAY_ANIMAL(text):
    """Функция обработки выражений типа: Stray Hen (Tame)"""
    TEMPLATE = {"MALE":"Ничей %s (Ручной)", "FEMALE":"Ничья %s (Ручная)"}

    animal = STRAY_ANIMAL.split(text)[1].strip()
    transl = GET_TRANSLATE(animal)
    gender = TEST_GENDER(transl)
    return TEMPLATE[gender] % transl

def PROC_STRAY_ANIMAL_GENDER(text):
    """Функция обрабатывает выражения типа: Stray Dog, ♀ (Tame)"""
    TEMPLATE = {"MALE":"Ничей %s, %s (Ручной)", "FEMALE":"Ничья %s, %s (Ручная)"}

    tmp = STRAY_ANIMAL_GENDER.split(text)
    transl = GET_TRANSLATE(tmp[1].strip())
    gender = TEST_GENDER(transl)
    return TEMPLATE[gender] % (transl, tmp[2])

    

#Словарь регулярных выражений, состоит из самого выражения и функции-обработчика дла нее
expressions = {
MENU_U_TITLE:        PROC_MENU_U_TITLE,
SKILLS:              PROC_SKILLS,
STRAY_ANIMAL:        PROC_STRAY_ANIMAL,
STRAY_ANIMAL_GENDER: PROC_STRAY_ANIMAL_GENDER
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

    
