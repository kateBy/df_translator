
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


InstanceStrings = {#Главное меню
                    "Visit Bay 12 Games":"Посетите Bay 12 Games",
                    "Programmed by Tarn Adams":"Программирование: Тарн Адамс",
                    "Slaves to Armok:  God of Blood":"Рабы Амрока: Бога крови",
                    "Designed by Tarn and Zach Adams":"Дизайн: Тарн и Зак Адамс",
                    "Chapter II: Dwarf Fortress":"Часть II: Крепость Дварфов",
                    "Dwarf Fortress":"Крепость Дварфов",

                   #Запасы
                    "raw fish":"свежая рыба",
                    "drinks":"напитки",
                    "weapons":"оружие",
                    "books":"книги",
                    "traction benches":"тракционные столы",
                    "ballista arrow heads":"наконечники стрел баллисты",
                    "totems":"тотемы",
                    "corpses":"трупы",
                    "body parts":"части тела",
                    "small rock":"малый камень",
                    "splints":"шины",
                    "crutches":"костыли",
                    "boxes and bags":"контейнеры",
                    "bins":"ящики",
                    "barrels":"бочки",
                    "buckets":"вёдра",
                    "trap components":"механизмы",
                    "flasks":"фляги",
                    "goblets":"кубки",
                    "toys":"игрушки",
                    "tools":"инструменты",
                    "musical instruments":"музыкальные инструменты",
                    "figurines":"статуэтки",
                    "amulets":"амулеты",
                    "scepters":"скипетры",
                    "crowns":"короны",
                    "rings":"кольца",
                    "earrings":"серьги",
                    "bracelets":"браслеты",
                    "large gems":"большие самоцветы",
                    "coins":"монеты",
                    "small tame animals":"небольшое ручное животное",
                    "small live animals":"небольшое животное",
                    "hatch covers":"крышка люка",
                    "grates":"решетки",
                    "querns":"ручная мельница",
                    "millstones":"жернова",
                    "windows":"окна",
                    "animal traps":"силки",
                    "chains":"цепи",
                    "cages":"клетки"
                    

                   
                   
                   
                   
                   
    }


InstanceStrings.update(load_trans_mo("./libs/trans.mo"))





    
