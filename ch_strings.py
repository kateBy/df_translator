

def GetTranslate(_text):
    """Функция принимает текст в виде UTF-16"""
    text = _text.decode("utf-16")

    fromInstance = InstanceStrings.get(text)

    if fromInstance != None:
        return fromInstance.encode("utf-16")+b"\0\0"

    processed = ProcessText(text)

    if processed != None:
        return processed.encode("utf-16")+b"\0\0"
    
    return None


InstanceStrings = {"Adventurer":"Приключения",
                   "Dwarf Fortress":"Крепость дварфов",
                   "Legends":"Легенды",
                   "Visit Bay 12 Games":"Посетите Bay 12 Games",
                   "Programmed by Tarn Adams":"Программирование: Тарн Адамс",
                   "Slaves to Armok:  God of Blood":"Рабы Амрока: Бога крови",
                   "Histories of Greed and Toil":"Истории о жадности и тяжком труде",
                   "Designed by Tarn and Zach Adams":"Дизайн: Тарн и Зак Адамс",
                   "Chapter II: Dwarf Fortress":"Часть II: Крепость Дварфов",
                   "N":"C"}



def ProcessText(text):
    return None



def DetectPartOfSpeech(word):
    particles = ["из"]

    
