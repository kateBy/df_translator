
# -*- coding: utf-8 -*-
"""Модуль содержит все регулярные выражение и функции их обработки, для большей структурированности"""

import re
#Должен быть уставновлен из вызывающего модуля
GET_TRANSLATE = None

MATERIALS = {
         "wooden":    {"MADEOF":"из дерева", "MALE":"деревянный", "FEMALE":"деревянную", "MIDDLE":"деревянное", "MULTI":"деревянные"},
         "rock":      {"MADEOF":"из камня",  "MALE":"каменный",   "FEMALE":"каменную",   "MIDDLE":"каменное",   "MULTI":"каменные"},
         "steel":     {"MADEOF":"из стали",  "MALE":"стальной",   "FEMALE":"стальную",   "MIDDLE":"стальное",   "MULTI":"стальные"},
         "pig iron":  {"MADEOF":"из чугуна", "MALE":"чугунный",   "FEMALE":"чугунную",   "MIDDLE":"чугунное",   "MULTI":"чугунные"},
         "clay":      {"MADEOF":"из глины",  "MALE":"глиняный",   "FEMALE":"глиняную",   "MIDDLE":"глиняное",   "MULTI":"глиняные"},
         "plaster":   {"MADEOF":"из гипса",  "MALE":"гипсовый",   "FEMALE":"гипсовую",   "MIDDLE":"гипсовое",   "MULTI":"гипсовые"},
         "copper":    {"MADEOF":"из меди",   "MALE":"медный",     "FEMALE":"медная",     "MIDDLE":"медное",     "MULTI":"медные"},
         "gabbro":    {"MADEOF":"из габбро", "MALE":"габбровый",  "FEMALE":"габбровая",  "MIDDLE":"габбровое",  "MULTI":"габбровые"}, #Мне было нечего делать :)
         "sand":      {"MADEOF":"из песка",  "MALE":"песчаный",   "FEMALE":"песчаная",   "MIDDLE":"песчаное",   "MULTI":"песчаные"},
         "fire clay": {"MADEOF":"из огнеупорной глины",   "MALE":"огнеупорная глина",     "FEMALE":"огнеупорная глина",     "MIDDLE":"огнеупорная глина", "MULTI":"огнеупорная глина"},
         "adamantine":{"MADEOF":"из адамантина",  "MALE":"адамантиновый",   "FEMALE":"адамантиновую",   "MIDDLE":"адамантиновое",   "MULTI":"адамантиновые"}
         
         }

MATS_DIVIDED = "|".join([x for x in MATERIALS]) #Материалы, разделенные | для вставки в регулярные выражения


MAIN_MENU_TITLE     = re.compile(r"Histories of (\w+) and (\w+)") #Меняющийся заголовок главного меню
WORDS_AND_NUMBER    = re.compile(r"(\w+.*(?: \w+)*) (\(\d+\))") #Mason's Workshop (1) | Pets/Livestock (16)
SKILLS              = re.compile(r"(Dabbling|Novice|Adequate|Proficient|Legendary) ") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL        = re.compile(r"\s*Stray ((\w+ )+)") #Stray Hen (Tame) | Stray Yak Cow (Tame)
STRAY_ANIMAL_GENDER = re.compile(r"Stray (\w+?), (♀|♂) \((\S+?)\)") #"Stray Dog, ♀♂ (Tame)"
NAME_AND_PROFESSION = re.compile(r"(\w+? \w+?),\s(\w+(?: \w+)*)$")#Zuglar Reggikut, Fisherdwarf
WATER_COVERING      = re.compile(r"water covering \((\w+(?: \w+)*.(?: \w+)*)\)")#water covering (upper body)
YOU_HAVE_STRUCT     = re.compile(r"You have struck (\w+(?: \w+)*)!") #"You have struck blue jade!"
NEEDS               = re.compile(r"Needs (\w+(?: \w+)*)")# "Needs millstone"
ORE_OF              = re.compile(r"Ore of (\w+)")#Ore of iron
WORLD_SIZE_STRING   = re.compile(r"This controls the size of the world map.  Current: (.+)")
WORLD_HISTORY       = re.compile(r"This is the length of pre-generated history.  Current: (\d+) years")
YEAR_NUM            = re.compile(r"Year (\d+)")
COVER_MATERIAL      = re.compile(r"(" + MATS_DIVIDED + ") (Downward\ Slope|Upward\ Slope|Cavern\ Floor|Downward\ Stairway|Up/Down Stairway)") #chalk Cavern Floor
NO_CHESTS           = re.compile(r"(No|\d+) (\w+(?: \w+)*)")#No Chests "5 Cabinets"
NOTHING_TO_CATCH    = re.compile(r"There is nothing to catch in the (\w+) swamps")
WEALTH              = re.compile(r"  The Wealth of (\w+(?: \w+)*)") # "  The Wealth of НазваниеКрепости 

MAKE                = re.compile(r"\s*(make|Make|Construct|Extract) ("+ MATS_DIVIDED +") (\w+(?: \w+)*)") #Construct wooden Armor Stand
WEAR                = re.compile(r"\(*(\w+(?: \w+)*) (silk|wool|leather|fiber) (\w+(?: \w+)*)") # cave spider silk trousers
WEAPON              = re.compile(r"\(*(" + MATS_DIVIDED + ") (\w+(?: \w+)*)( \[\d\])*\)*") # copper Battle Axe

FIRST_IN_MINDS      = re.compile(r'"(.+)"') # "I don't like being obligated to anybody."



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




def GET_MATERIAL(word, form_type):
    if not form_type in ["MALE", "FEMALE", "MIDDLE", "MULTI", "MADEOF"]:
        return word

    mat_dict = MATERIALS.get(word)
    if mat_dict != None:
        return mat_dict.get(form_type)
    else:
        return word

#========== A ==========
#========== B ==========
#========== C ==========
    
def PROC_COVER_MATERIAL(text):
    """Функция обрабатывает строки вида: chalk Cavern Floor"""
    tmp = COVER_MATERIAL.findall(text)[0]
    wat = GET_TRANSLATE(tmp[1])
    mat = GET_MATERIAL(tmp[0], "MADEOF")
    return wat + " " + mat

#========== D ==========
#========== E ==========
#========== F ==========
    
def PROC_FIRST_IN_MINDS(text):
    tmp = FIRST_IN_MINDS.findall(text)[0]
    return '"' + GET_TRANSLATE(tmp) + '"'

#========== G ==========
#========== H ==========
#========== I ==========
#========== J ==========
#========== K ==========
#========== L ==========
#========== M ==========

def PROC_MAIN_MENU_TITLE(text):
    """Обрабатывает заголовок в главном меню: Histories of Greed and Industry"""
    TEMPLATE = "Истории о %s и %s"
    tmp = MAIN_MENU_TITLE.split(text)
    transl1 = GET_TRANSLATE(tmp[1])
    transl2 = GET_TRANSLATE(tmp[2])
    return TEMPLATE % (transl1, transl2)


def PROC_MAKE(text):
    """Обрабатывает строки в запросах мастерских: Construct wooden Armor Stand"""
    tmp = MAKE.findall(text)[0]
    action = GET_TRANSLATE(tmp[0])
    thing = GET_TRANSLATE(tmp[2])
    gender = TEST_GENDER(thing)

    #Меняем последнюю букву слов женского рода
    FEMALE_SUFFIXES = {"а":"у", "я":"ю"}
    if gender == "FEMALE":
        thing = thing[:-1] + FEMALE_SUFFIXES.get(thing[-1],thing[-1]) #Если окончание не присутствует в списке, то возвращается оригинальное

    material = GET_MATERIAL(tmp[1], gender)

    return " ".join([action, material, thing])

#========== N ==========

def PROC_NAME_AND_PROFESSION(text):
    """Функция обработки строк в виде имени и профессии через запятую"""
    tmp = NAME_AND_PROFESSION.split(text)
    trans = GET_TRANSLATE(tmp[2])
    return tmp[1] + ", " + trans


def PROC_NO_CHESTS(text):
    """Функция для обрабоки строки запросов знати, где сказано, что что-то отсутствует No Chests"""
    tmp = NO_CHESTS.findall(text)[0]
    if tmp[0] == "No":
        return "Нет " + GET_TRANSLATE(tmp[1])
    else:
        return tmp[0] + " " + GET_TRANSLATE(tmp[1])

def PROC_NOTHING_TO_CATCH(text):
    tmp = NOTHING_TO_CATCH.findall(text)[0]
    return "Ничего не ловится в " + GET_TRANSLATE(tmp) + " болотах."

#========== O ==========

def PROC_ORE_OF(text):
    tmp = ORE_OF.findall(text)[0]
    return "Руда: " + GET_TRANSLATE(tmp)

#========== P ==========
#========== Q ==========
#========== R ==========
#========== S ==========

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

#========== T ==========
#========== U ==========
#========== V ==========
#========== W ==========

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

def PROC_WEALTH(text):#==
    tmp = WEALTH.findall(text)[0]
    return "  Запасы крепости " + tmp + "  "

def PROC_WEAPON(text):
    tmp = WEAPON.findall(text)[0]
    mat = GET_MATERIAL(tmp[0], "MADEOF") #Берем перевод материала, если такой есть
    wat = GET_TRANSLATE(tmp[1])
    cnt = tmp[2]
    return " ".join([wat, mat, cnt])

def PROC_WEAR(text):
    """Функция обрабатывает строки вида: cave spider silk trousers"""
    mats = {"silk":"из шелка",  #Из чего
            "wool":"из шерсти",
            "leather":"из кожи",
            "fiber":"из нити"}

    tmp = WEAR.findall(text)[0]
    who = GET_TRANSLATE(tmp[0]) #Чьё
    wat = GET_TRANSLATE(tmp[2]) #Что

    return "%s %s %s" % (wat, mats.get(tmp[1], "НЕТ ПЕРЕВОДА"), who)


def PROC_WORDS_AND_NUMBER(text):
    """Функция обработки выражений типа: Citizens (7)"""
    tmp = WORDS_AND_NUMBER.findall(text)[0]
    trans = GET_TRANSLATE(tmp[0])    
    return trans + " " + tmp[1]


def PROC_WORLD_HISTORY(text):
    tmp = WORLD_HISTORY.findall(text)
    return "Этот параметр отвечает за предысторию мира. Она составит: %s лет" % tmp[0]

def PROC_WORLD_SIZE_STRING(text):
    tmp = WORLD_SIZE_STRING.findall(text)
    return "Этот параметр отвечает за размер мира. Текущий размер: " + tmp[0]

#========== X ==========
#========== Y ==========

def PROC_YEAR_NUM(text):
    """При генерации мира есть строка Year: 125"""
    tmp = YEAR_NUM.findall(text)
    return "Год " + str(tmp[0])

def PROC_YOU_HAVE_STRUCT(text):
    """Функция обрабатывает строки типа: You have struck blue jade!"""
    tmp = YOU_HAVE_STRUCT.findall(text)[0]
    return "Вы нашли " + GET_TRANSLATE(tmp)

#========== Z ==========











#Словарь регулярных выражений, состоит из самого выражения и функции-обработчика дла нее
RegularExpressions = {
MAIN_MENU_TITLE:     PROC_MAIN_MENU_TITLE,
WORDS_AND_NUMBER:    PROC_WORDS_AND_NUMBER,
SKILLS:              PROC_SKILLS,
STRAY_ANIMAL:        PROC_STRAY_ANIMAL,
STRAY_ANIMAL_GENDER: PROC_STRAY_ANIMAL_GENDER,
NAME_AND_PROFESSION: PROC_NAME_AND_PROFESSION,
WATER_COVERING:      PROC_WATER_COVERING,
YOU_HAVE_STRUCT:     PROC_YOU_HAVE_STRUCT,
MAKE:                PROC_MAKE,
ORE_OF:              PROC_ORE_OF,
WORLD_SIZE_STRING:   PROC_WORLD_SIZE_STRING,
WORLD_HISTORY:       PROC_WORLD_HISTORY,
YEAR_NUM:            PROC_YEAR_NUM,
NO_CHESTS:           PROC_NO_CHESTS,
NOTHING_TO_CATCH:    PROC_NOTHING_TO_CATCH,
WEALTH:              PROC_WEALTH,
COVER_MATERIAL:      PROC_COVER_MATERIAL,
WEAR:                PROC_WEAR,
WEAPON:              PROC_WEAPON,
FIRST_IN_MINDS:      PROC_FIRST_IN_MINDS
}

def Regulars(text):
    result = None
    for exp in RegularExpressions:
        if exp.match(text):                        #Фраза соответствует шаблону
            result = RegularExpressions[exp](text) #Передаём текст на обработчик этого шаблона
            break

    return result
