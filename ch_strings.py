
# -*- coding: utf-8 -*-

import re

#Разрешает или запрещает вывод непереведённого текста в консоль
MAKE_OUTPUT = True

#Строки, которые не нужно отображать. Для отладки
DO_NOT_SHOW = [
               "  Dwarf Fortress  ",
               "ESC"
               ]



MAIN_MENU_TITLE     = re.compile(r"Histories of (\w+) and (\w+)")
WORDS_AND_NUMBER    = re.compile(r"(\w+.*(?: \w+)*) (\(\d+\))") #Mason's Workshop (1) | Pets/Livestock (16)
SKILLS              = re.compile(r"(Dabbling|Novice|Adequate|Proficient|Legendary) ") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL        = re.compile(r"\s*Stray ((\w+ )+)") #Stray Hen (Tame) | Stray Yak Cow (Tame)
STRAY_ANIMAL_GENDER = re.compile(r"Stray (\w+?), (♀|♂) \((\S+?)\)") #"Stray Dog, ♀♂ (Tame)"
NAME_AND_PROFESSION = re.compile(r"(\w+? \w+?),\s(\w+(?: \w+)*)$")#Zuglar Reggikut, Fisherdwarf
WATER_COVERING      = re.compile(r"water covering \((\w+(?: \w+)*.(?: \w+)*)\)")#water covering (upper body)
YOU_HAVE_STRUCT     = re.compile(r"You have struck (\w+(?: \w+)*)!") #"You have struck blue jade!"
NEEDS               = re.compile(r"Needs (\w+(?: \w+)*)")# "Needs millstone"
ORE_OF              = re.compile(r"Ore of (\w+)")

#Мастерские мастерская
MAKE = re.compile(r"\s*(Make|Construct) (wooden|rock|steel|pig\ iron|clay) (\w+(?: \w+)*)") #Construct wooden Armor Stand



def GET_TRANSLATE(original):
    """Функция проверяет наличие перевода строки, если его нет, возвращает запрашиваему назад"""
    if original == "":
        return ""
    translate = InstanceStrings.get(original)
    if translate == None:
        print("TRANSL --->\"%s\"" % original)
        return original
    else:
        return translate

def TEST_GENDER(word):
    """Проверяет какой пол у существительного"""
    F = "FEMALE"
    T = "MIDDLE"
    S = "MULTI"
    
    SUFFIXES = {
                "а":F, "я":F, "ю":F, "ь":F, #Женские окончания
                "о":T, "ё":T,               #Окончания среднего рода
                "и":S, "ы":S                #Окончания множественного числа
                }
    
    #Если окончание не найдено, вернется MALE
    return SUFFIXES.get(word[-1],"MALE")

def PROC_ORE_OF(text):
    tmp = ORE_OF.findall(text)[0]
    return "Руда: " + GET_TRANSLATE(tmp)


def PROC_MAKE(text):
    """Обрабатывает строки в запросах мастерских: Construct wooden Armor Stand"""
    tmp = MAKE.findall(text)[0]
    action = GET_TRANSLATE(tmp[0])
    thing = GET_TRANSLATE(tmp[2])
    gender = TEST_GENDER(thing)

    MATERIALS = {
                 "wooden":   {"MALE":"деревянный", "FEMALE":"деревянную", "MIDDLE":"деревянное", "MULTI":"деревянные"},
                 "rock":     {"MALE":"каменный",   "FEMALE":"каменную",   "MIDDLE":"каменное",   "MULTI":"каменные"},
                 "steel":    {"MALE":"стальной",   "FEMALE":"стальную",   "MIDDLE":"стальное",   "MULTI":"стальные"},
                 "pig iron": {"MALE":"чугунный",   "FEMALE":"чугунную",   "MIDDLE":"чугунное",   "MULTI":"чугунные"},
                 "clay":     {"MALE":"глиняный",   "FEMALE":"глиняную",   "MIDDLE":"глиняное",   "MULTI":"глиняные"},
                 }
    #Меняем последнюю букву слов женского рода
    FEMALE_SUFFIXES = {"а":"у", "я":"ю"}
    if gender == "FEMALE":
        thing = thing[:-1] + FEMALE_SUFFIXES.get(thing[-1],thing[-1]) #Если окончание не присутствует в списке, то возвращается оригинальное

    material = MATERIALS.get(tmp[1]).get(gender)

    return " ".join([action, material, thing])
    

def PROC_YOU_HAVE_STRUCT(text):
    """Функция обрабатывает строки типа: You have struck blue jade!"""
    tmp = YOU_HAVE_STRUCT.findall(text)[0]
    return "Вы нашли " + GET_TRANSLATE(tmp)

def PROC_WATER_COVERING(text):
    """Функция обрабатывает строки типа: water covering (upper body)"""
    TEMPLATE = {"MALE":"водой покрыт (%s)",
                "FEMALE":"водой покрыта (%s)",
                "MIDDLE":"водой покрыто (%s)",
                "MULTI":"водой покрыты (%s)"}
    tmp = WATER_COVERING.findall(text)[0]
    trans = GET_TRANSLATE(tmp)
    gender = TEST_GENDER(trans)
    return TEMPLATE[gender] % trans                              
    

def PROC_WORDS_AND_NUMBER(text):
    """Функция обработки выражений типа: Citizens (7)"""
    tmp = WORDS_AND_NUMBER.findall(text)[0]
    trans = GET_TRANSLATE(tmp[0])    
    return trans + " " + tmp[1]

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
    TEMPLATE = {"MALE":"Ничей %s (Ручной)",
                "FEMALE":"Ничья %s (Ручная)",
                "MIDDLE": "Ничьё %s (Ручное)",
                "MULTI":"Ничьи %s (Ручные)"}

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
WORDS_AND_NUMBER:    PROC_WORDS_AND_NUMBER,
SKILLS:              PROC_SKILLS,
STRAY_ANIMAL:        PROC_STRAY_ANIMAL,
STRAY_ANIMAL_GENDER: PROC_STRAY_ANIMAL_GENDER,
NAME_AND_PROFESSION: PROC_NAME_AND_PROFESSION,
WATER_COVERING:      PROC_WATER_COVERING,
YOU_HAVE_STRUCT:     PROC_YOU_HAVE_STRUCT,
MAKE:                PROC_MAKE,
ORE_OF:              PROC_ORE_OF
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

    
