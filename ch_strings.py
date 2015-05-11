
# -*- coding: utf-8 -*-

import re

#Разрешает или запрещает вывод непереведённого текста в консоль
MAKE_OUTPUT = True

#Строки, которые не нужно отображать. Для отладки
DO_NOT_SHOW = [
               "  Dwarf Fortress  ",
               "ESC"
               ]



MAIN_MENU_TITLE = re.compile(r"Histories of (\w+) and (\w+)")
MENU_U_TITLE = re.compile(r"(Citizens|Pets/Livestock|Others|Dead/Missing) (\(\d+\))") #Citizens (7) | Pets/Livestock (16)
SKILLS = re.compile(r"(Novice|Adequate|Proficient|Legendary) ") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL = re.compile(r"\s*Stray ((\w+ )+)") #Stray Hen (Tame) | Stray Yak Cow (Tame)
STRAY_ANIMAL_GENDER = re.compile(r"Stray (\w+?), (♀|♂) \((\S+?)\)") #"Stray Dog, ♀♂ (Tame)"
NAME_AND_PROFESSION = re.compile(r"(\w+? \w+?),\s(\w+(?: \w+)*)$")#Zuglar Reggikut, Fisherdwarf
WATER_COVERING = re.compile(r"water covering \((\w+(?: \w+)*.(?: \w+)*)\)")#water covering (upper body)

def GET_TRANSLATE(original):
    """Функция проверяет наличие перевода строки, если его нет, возвращает запрашиваему назад"""
    translate = InstanceStrings.get(original)
    if translate == None:
        return original
    else:
        return translate

def TEST_GENDER(word):
    """Проверяет какой пол у существительного"""
    if word[-1] in ['а', 'я', 'ь']:
        return "FEMALE"
    else:
        return "MALE"

def PROC_WATER_COVERING(text):
    """Функция обрабатывает строки типа: water covering (upper body)"""
    TEMPLATE = {"MALE":"водой покрыт (%s)", "FEMALE":"водой покрыта (%s)"}
    tmp = WATER_COVERING.findall(text)[0]
    trans = GET_TRANSLATE(tmp)
    gender = TEST_GENDER(trans)
    return TEMPLATE[gender] % trans                              
          
    

def PROC_MENU_U_TITLE(text):
    """Функция обработки выражений типа: Citizens (7)"""
    tmp = MENU_U_TITLE.split(text) #Делим строку делителем
    trans = GET_TRANSLATE(tmp[1])    #Запрашиваем слова
    return trans + " " + tmp[2]

def PROC_NAME_AND_PROFESSION(text):
    """Функция обработки строк в виде имени и профессии через запятую"""
    tmp = NAME_AND_PROFESSION.split(text)
    trans = GET_TRANSLATE(tmp[2])
    return tmp[1] + ", " + trans


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

def PROC_MAIN_MENU_TITLE(text):
    """Обрабатывает заголовок в главном меню: Histories of Greed and Industry"""
    TEMPLATE = "Истории о%s и %s"
    tmp = MAIN_MENU_TITLE.split(text)
    transl1 = GET_TRANSLATE(tmp[1])
    transl2 = GET_TRANSLATE(tmp[2])
    return TEMPLATE % (transl1, transl2)

    

#Словарь регулярных выражений, состоит из самого выражения и функции-обработчика дла нее
expressions = {
MAIN_MENU_TITLE:     PROC_MAIN_MENU_TITLE,
MENU_U_TITLE:        PROC_MENU_U_TITLE,
SKILLS:              PROC_SKILLS,
STRAY_ANIMAL:        PROC_STRAY_ANIMAL,
STRAY_ANIMAL_GENDER: PROC_STRAY_ANIMAL_GENDER,
NAME_AND_PROFESSION: PROC_NAME_AND_PROFESSION,
WATER_COVERING:      PROC_WATER_COVERING
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
        

        
if __name__ != "__main__":
    InstanceStrings.update(load_trans_mo("./libs/trans.mo"))
    

def dictToPo(some_dict):
    for item in some_dict:
        print("msgid \"%s\"\nmsgstr \"%s\"\n" % (item, some_dict[item]))


if __name__ == "__main__":
    pass
    dictToPo(InstanceStrings)

    
