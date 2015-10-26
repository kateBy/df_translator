
# -*- coding: utf-8 -*-
"""Модуль содержит все регулярные выражение и функции их обработки, для большей структурированности"""

import re
#Должен быть уставновлен из вызывающего модуля
GET_TRANSLATE = None

_MATERIALS = {
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

#Добавляем в словарь те же материалы, только с заглавной буквы
MATERIALS = dict(_MATERIALS)
for x in _MATERIALS:
	MATERIALS[x[0].upper() + x[1:]] = _MATERIALS[x]

MATS_DIVIDED = "|".join([x for x in MATERIALS]) #Материалы, разделенные | для вставки в регулярные выражения


MAIN_MENU_TITLE     = re.compile(r"Histories of (\w+) and (\w+)") #Меняющийся заголовок главного меню
WORDS_AND_NUMBER    = re.compile(r"(\w+.*(?: \w+)*) (\(\d+\))") #Mason's Workshop (1) | Pets/Livestock (16)
SKILLS              = re.compile(r"(Dabbling|Novice|Adequate|Competent|Proficient|Legendary) ") #Novice Miner #Adequate Fish Cleaner
STRAY_ANIMAL        = re.compile(r"\s*Stray ((\w+ )+)") #Stray Hen (Tame) | Stray Yak Cow (Tame)
STRAY_ANIMAL_GENDER = re.compile(r"Stray (\w+?), (♀|♂) \((\S+?)\)") #"Stray Dog, ♀♂ (Tame)"
NAME_AND_PROFESSION = re.compile(r"(\w+? \w+?),\s(\w+(?: \w+)*)$")#Zuglar Reggikut, Fisherdwarf
WATER_COVERING      = re.compile(r"water covering \((\w+(?: \w+)*.(?: \w+)*)\)")#water covering (upper body)
YOU_HAVE_STRUCT     = re.compile(r"You have struck (\w+(?: \w+)*)!") #"You have struck blue jade!"
NEEDS               = re.compile(r"Needs (\w+(?: \w+)*)")# "Needs millstone"
ORE_OF              = re.compile(r"Ore of (\w+)")#Ore of iron
WORLD_SIZE_STRING   = re.compile(r"This controls the size of the world map.  Current: (.+)")
WORLD_HISTORY       = re.compile(r"This is the length of pre-generated history.  Current: (\d+) years")
YEAR_NUM            = re.compile(r"Year (\d+)") # Year 1150
COVER_MATERIAL      = re.compile(r"(\w+(?: \w+)*) (Downward\ Slope|Upward\ Slope|Cavern\ Floor|Downward\ Stairway|Up/Down Stairway|Wall)") #chalk Cavern Floor
NO_CHESTS           = re.compile(r"(No|\d+) (\w+(?: \w+)*)")#No Chests "5 Cabinets"
NOTHING_TO_CATCH    = re.compile(r"There is nothing to catch in the (\w+) swamps")
WEALTH              = re.compile(r"  The Wealth of (\w+(?: \w+)*)") # "  The Wealth of НазваниеКрепости

WOOD_LOGS           = re.compile(r"(\w+(?: \w+)*) wood logs") # bitter orange logs
TREES               = re.compile(r"(\w+(?: \w+)*) trees") # bitter paradise nut trees
TREE_ROOTS          = re.compile(r"(\w+) tree roots")# apple tree roots
LEATHER             = re.compile(r"(.+(?: \w+)*) Leather") # Giant Jackal Man Leather
MEAT                = re.compile(r"(.+(?: \w+)*) (?:meat|Meat)") # guineafowl meat
FISH                = re.compile(r"(Unprepared Raw )*(\w+(?: \w+)*), (♀|♂)") #FIXME!


MAKE                = re.compile(r"\s*(make|Make|Construct|Extract) ("+ MATS_DIVIDED +") (\w+(?: \w+)*)") #Construct wooden Armor Stand
WEAR                = re.compile(r"\(*(\w+(?: \w+)*) (silk|wool|leather|fiber) (\w+(?: \w+)*)") # cave spider silk trousers
WEAPON              = re.compile(r"\(*(" + MATS_DIVIDED + ") (\w+(?: \w+)*)( \[\d\])*\)*") # copper Battle Axe

FIRST_IN_MINDS      = re.compile(r'"(.+)"') # "I don't like being obligated to anybody."
THE_NOBLES          = re.compile(r"\s*The Nobles and Administrators of (\w+(?: \w+)*)\s*") #The Nobles and Administrators of Mosusvod
THE_NOBLES_INFO     = re.compile(r"\s*(\w+(?: \w+)*), \"(\w+(?: \w+)*)\", (\w+(?: \w+)*)") #Name, "Alias Alias", должность
CHOOSE_THE          = re.compile(r"  Choose the (\w+(?: \w+)*) of (\w+(?: \w+)*)") #Choose the manager of Mosusvod


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
    """Возвращает форму материала в соответствии с нужной формой"""
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

def PROC_CHOOSE_THE(text):
    tmp = CHOOSE_THE.findall(text)[0]
    transl = GET_TRANSLATE(tmp[0])

    return "Выбирите " + transl + " крепости " + tmp[1]
    
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

def PROC_FISH(text):
    print(text)
    tmp = FISH.findall(text)[0]
    
    name = GET_TRANSLATE(tmp[1])
    gender = tmp[2]
    
    if tmp[0] == "Unprepared Raw ":
        return "Неприготовленый сырой " + name + ", " + gender
    else:
        return name + ", " + gender
    

#========== G ==========
#========== H ==========
#========== I ==========
#========== J ==========
#========== K ==========
#========== L ==========

def PROC_LEATHER(text):
    tmp = LEATHER.findall(text)[0]
    transl = GET_TRANSLATE(tmp)
    return "Кожа " + transl

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

def PROC_MEAT(text):
    tmp = MEAT.findall(text)[0]
    transl = GET_TRANSLATE(tmp)

    return "мясо " + transl

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
    """При просмотре запасов показываем руду чего-либо,
    используется 'Руда:' для того, чтобы не крутиться с падежами"""
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

def PROC_THE_NOBLES(text):
    """Администрация и знать"""
    tmp = THE_NOBLES.findall(text)[0]
    return "Знать и Администрация " + tmp

def PROC_THE_NOBLES_INFO(text):
    """Заголовок о знати и администрации"""
    name, alias, post = THE_NOBLES_INFO.findall(text)[0]
    return "%s, \"%s\", %s" % (name, alias, GET_TRANSLATE(post))

def PROC_TREES(text):
    """Обрабатываются строки в настройках склада, например: banana trees"""
    tmp = TREES.findall(text)[0]
    transl = GET_TRANSLATE(tmp)

    return "древесина " + transl

def PROC_TREE_ROOTS(text):
    tmp = TREE_ROOTS.findall(text)[0]
    transl = GET_TRANSLATE(tmp)

    return "корни " + transl

    
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

def PROC_WEALTH(text):
    """Эта строчка появляется вверху, при просмотре запасов"""
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

def PROC_WOOD_LOGS(text):
    """Строки при выборе материала постройки: abaca logs"""
    tmp = WOOD_LOGS.findall(text)[0]
    trans = GET_TRANSLATE(tmp)
    return "бревна " + trans 


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









#Создание словаря автоматически, по началу функций PROC
all_procs = [x for x in dir() if x.startswith("PROC_")] #Получаем имена всех объектов, начинающихся с PROC_
globs = globals() #Получаем словарь всех объектов модуля
RegularExpressions = {} 
for i in all_procs:
    RegularExpressions[globs[i[5:]]] = globs[i] #Устанавливаем соответствие между объектом-регулярным выражением и функцией-обработчиком

def Regulars(text):
    """Запускает цикл перебора на соответствие регулярным выражениям"""
    result = None
    for exp in RegularExpressions:
        if exp.match(text):                        #Фраза соответствует шаблону
            result = RegularExpressions[exp](text) #Передаём текст на обработчик этого шаблона
            break

    return result
