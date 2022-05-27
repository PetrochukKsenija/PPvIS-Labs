
import random
import pickle

# сад
class Garden:

    """
    по умочанию создается пустой сад
    аттрибуты: количество деревьев, количество грядок, списки с деревьями и грядками
               булевая переменная, обозначающая, полит ли наш сад
               переменная, обозначающая, сколько времени он уже не полит
               время жизни сада
               список деревьев, на которые нападает жук
               список деревьев, которые больные
               собственно жук и болезнь собственными персонами

    """
    def __init__(self):
        self.__tree_count = 0
        self.__garden_bed_count = 0
        self.tree_list = []
        self.garden_bed_list = []
        self.__water = True
        self.__drought_time = 0
        self.__time = 0
        self.__pested_list = []
        self.__diseased_list = []
        self.bug = Pest()
        self.disease = Disease()


    @property
    def water(self):
        return self.__water

    @property
    def drought_time(self):
        return self.__drought_time

    @water.setter
    def water(self, status):
        if self.__water == status:
            if not status:
                self.__drought_time += 1
        else:
            self.__water = status
            self.__drought_time = 0

    """
    Метод регулирования уровня засушенности растений
    Если больше 4 дней не идет дождь и сад не поливается, то наступает засуха, которая всем вредит
    """
    def WaterRegulate(self):
        if self.__drought_time > 2:
            drought = Drought()

            for i in self.tree_list:
                drought.Plant_Infuence(i)

            for i in self.garden_bed_list:
                drought.Plant_Infuence(i)

    """
    Метод посадки дерева
    """
    def Plant_Tree(self, name="яблоня"):
        self.__tree_count+=1
        self.tree_list.append(Tree(name))

    """
    Метод удаления одного дерева по наименованию фруктов, что на нем растут
    """
    def Remove_OneTree(self, name="яблоня"):
        if self.__tree_count:
            for i in self.tree_list:
                if i.name == name:
                    self.tree_list.remove(i)
                    self.__tree_count -= 1
                    print("Дерево удалено")
                    break
        else:
            print("В саду еще нет деревьев")

    """
    Медод распечатки деревьев
    """
    def PrintTree(self):
        if len(self.tree_list) == 0:
            print("В саду еще нет деревьев")
        else:
            for i in self.tree_list:
                print(i.name, end=" ")
            print("")

    """
    Метод создания грядки
    """
    def Make_GardenBed(self, name="картофель"):
        self.__garden_bed_count+=1
        self.garden_bed_list.append(Garden_Bed(name))

    """
    Метод удаления грядки
    удаляет грядку с меньшим количетсвом полезных растений 
    """
    def Remove_OneGardenBed(self):
        if self.__garden_bed_count:
            min = -1
            index = -1
            for i in self.garden_bed_list:
                if i.vegetable_count + i.seeds_count < min:
                    min = i.vegetable_count + i.seeds_count
                    index = i

            if index != -1:
                print("Удаление грядки", self.garden_bed_list[index].name)
                self.garden_bed_list.remove(index)
            else:
                print("Удаление грядки", self.garden_bed_list[self.__garden_bed_count-1].name)
                self.garden_bed_list.pop()

            self.__garden_bed_count -= 1
        else:
            print("В саду нет грядок")

    """
    Метод роста сада
    """
    def Growth(self):

        self.__time += 1

        # рост деревьев
        for i in self.tree_list:
            i.Growth()

        # рост на грядке
        for i in self.garden_bed_list:
            i.Growth()

        self.WaterRegulate()

        if not self.__time % 7:
            if self.__tree_count:
                number = random.randint(0, self.__tree_count-1)
                self.__pested_list.append(self.tree_list[number])

        for i in self.__pested_list:
            self.bug.Plant_Influence(i)

        if not self.__time % 10:
            if self.__tree_count:
                number = random.randint(0, self.__tree_count - 1)
                self.__diseased_list.append(self.tree_list[number])

        for i in self.__diseased_list:
            self.disease.Plant_Influence(i)

    """
    Метод удобрения 
    """
    def ToFertilize(self, name="яблоня"):
        fert = Fertilizer()
        for i in self.tree_list:
            if i.name == name:
                fert.ToFertilize(i)

    """
    Метод прополки 
    """
    def Bed_Wedding(self):
        wedding = Weeding()
        for i in self.garden_bed_list:
            wedding.ToWeed(i)

    """
    Метод посадки растения
    """
    def ToPlant(self, name="картофель"):
        plant = False
        for i in self.garden_bed_list:
             if i.name == name and i.IsPossible_ToPlant():
                 i.ToPlant(name)
                 plant = True

        if not plant:
            print("Создается новая грядка, на которой будет расти", name)
            garden_bed = Garden_Bed(name)
            garden_bed.ToPlant(name)
            self.__garden_bed_count += 1
            self.garden_bed_list.append(garden_bed)

    """
    Метод сбора всех фруктов со всех деревьев
    """
    def Pick_Fruits(self):
        if self.__tree_count:
            fruits = False
            for i in self.tree_list:
                if i.count_fruit:
                    fruits = True
                    break
            if fruits:
                for i in self.tree_list:
                    i.Pick_Fruits()
            else:
                print("На деревьях еще не выросли фрукты")
        else:
            print("В саду еще нет деревьев")


    """
    Метод сбора всех овощей со всех грядок
    """
    def Pick_Vegetable(self):
        if self.__garden_bed_count:
            veg = False
            for i in self.garden_bed_list:
                if i.vegetable_count:
                    veg = True
                    break
            if veg:
                for i in self.garden_bed_list:
                    i.Pick_Vegetable()
            else:
                print("На грядках еще не выросли овощи - подождите или посадте семена!")
        else:
            print("В саду еще нет грядок!")

    @property
    def tree_count(self):
        return self.__tree_count

    def Get_FruitsCount(self):
        for i in self.tree_list:
            print(i.name, "неспелые:", i.young, "спелые:", i.okay, "гнилые:", i.old)

    @property
    def garden_bed_count(self):
        return self.__garden_bed_count

    def Get_VegetableCount(self):
        for i in self.garden_bed_list:
            print(i.name, "неспелые:", i.young, "спелые:", i.okay, "гнилые:", i.old)

    def Get_WeedCount(self):
        for i in self.garden_bed_list:
            print(i.name, i.weed_count)

    def Get_SeedCount(self):
        for i in self.garden_bed_list:
            print(i.name, i.seeds_count)

    # Как мы будем "сохранять" класс
    def __getstate__(self) -> dict:
        state = {}
        state["tree_count"] = self.__tree_count
        state["garden_bed_count"] = self.__garden_bed_count
        state["water"] = self.__water
        state["drought_time"] = self.__drought_time
        state["time"] = self.__time

        state["tree_list"] = self.tree_list
        state["garden_bed_list"] = self.garden_bed_list
        state["pested_list"] = self.__pested_list
        state["diseased_list"] = self.__diseased_list

        state["bug"] = self.bug
        state["disease"] = self.disease
        return state

    # Как мы будем восстанавливать класс из байтов
    def __setstate__(self, state: dict):
        self.__tree_count = state["tree_count"]
        self.__garden_bed_count = state["garden_bed_count"]
        self.__water = state["water"]
        self.__drought_time = state["drought_time"]
        self.__time = state["time"]

        self.tree_list = state["tree_list"]
        self.garden_bed_list = state["garden_bed_list"]
        self.__pested_list = state["pested_list"]
        self.__diseased_list = state["diseased_list"]

        self.bug = state["bug"]
        self.disease = state["disease"]

# грядка
class Garden_Bed:

    """
    аттрибуты:
    максимальное количество растений на грядке - она же не резиновая
    количество сорняков - при создании грядки 5
    количество овощей 0
    количество посаженных семян 0
    списки семян и овощей
    список сорняков
    время жизни грядки
    """
    def __init__(self, name="картофель"):
        self.__name = name
        self.__max_size = 10

        self.__weed_count = 5
        self.__weed_list = []
        i = 0
        while i<5:
            self.__weed_list.append(Weed())
            i += 1

        self.__vegetable_count = 0
        self.__vegetable_list = []

        self.__young = 0
        self.__okay = 0
        self.__old = 0

        self.__seeds_list = []
        self.__seeds_count = 0

        self.__time = 0

    """
    Метод, описывающий возможность посадки еще дного растения на грядку 
    """
    def IsPossible_ToPlant(self):
        if self.__vegetable_count + self.__weed_count + self.__seeds_count < self.__max_size:
            return True
        else:
            return False

    """
    метод для посадки растения
    """
    def ToPlant(self, name="картофель"):
        self.__seeds_count += 1
        self.__seeds_list.append(Seeds(name))

    @property
    def name(self):
        return self.__name

    @property
    def vegetable_count(self):
        return self.__vegetable_count

    @property
    def seeds_count(self):
        return self.__seeds_count

    @property
    def weed_count(self):
        return self.__weed_count

    @weed_count.setter
    def weed_count(self, count):
        self.__weed_count = count

    @property
    def weed_list(self):
        return self.__weed_list

    @weed_list.setter
    def weed_list(self, list):
        self.__weed_list = list

    @property
    def young(self):
        return self.__young

    @property
    def okay(self):
        return self.__okay

    @property
    def old(self):
        return self.__old

    """
    Метод роста
    """
    def Growth(self):
        self.__time += 1
        if not self.__time % 5 and self.IsPossible_ToPlant():
            self.__weed_list.append(Weed())
            self.__weed_count += 1
        for i in self.__seeds_list:
            i.Growth()
            if i.time == 5:
                self.__seeds_list.remove(i)
                self.__seeds_count -= 1
                self.__vegetable_count += 1
                self.__vegetable_list.append(Vegetable())
        for i in self.__vegetable_list:
            i.Growth()
        if self.Vegetable_Status() == -1:
            raise ValueError('Error in Vegetable Status')

    def Vegetable_Status(self):
        self.__old = 0
        self.__young = 0
        self.__okay = 0
        for i in self.__vegetable_list:
            status = i.Status()
            if status == "неспелый":
                self.__young += 1
            elif status == "спелый":
                self.__okay += 1
            elif status == "гнилой":
                self.__old += 1
        if self.__old + self.__okay + self.__young == self.__vegetable_count:
            return 1
        else:
            return -1


    def Hinder_Growth(self):
        for i in self.__seeds_list:
            i.Hinder_Growth()

    """
    Метод сбора овощей с грядки
    """
    def Pick_Vegetable(self):
        if self.__vegetable_count:
            for i in self.__vegetable_list:
                if i.Status != "неспелый":
                    self.__vegetable_list.remove(i)
                    self.__vegetable_count -= 1
        else:
            print("Ничего пока не созрело, подождите либо посадите семена")

# растение
class Plant:

    """
    Аттрибуты:
    имя - по умолчанию сорняк
    время жизни
    статус - удобрено/не удобрено
    """
    def __init__(self, name="сорняк", time=0):
        self.__name = name
        self.time = time



    @property
    def name(self):
        return self.__name

    def Growth(self):
        self.time += 1

    def Hinder_Growth(self):
        self.time -= 1


# дерево
class Tree(Plant):

    """
    аттрибуты:
    количество фруктов
    список фруктов
    """
    def __init__(self, name="яблоня", time=0):
        super().__init__(name, time)
        self.__count_fruit = 0
        self.__young = 0
        self.__okay = 0
        self.__old = 0
        self.list_fruits = []
        self.__fertilized = False

    def Fruits_Status(self):
        self.__old = 0
        self.__young = 0
        self.__okay = 0
        for i in self.list_fruits:
            status = i.Status()
            if status == "неспелый":
                self.__young += 1
            elif status == "спелый":
                self.__okay += 1
            elif status == "гнилой":
                self.__old += 1
        if self.__old + self.__okay + self.__young == self.__count_fruit:
            return 1
        else:
            return -1

    def Growth(self):
        super().Growth()
        if self.time > 9 and not self.time % 5:
            self.__count_fruit += 1
            if self.name == "яблоня":
                name = "яблоко"
            else:
                name = self.name
            self.list_fruits.append(Fruits(name))
        for i in self.list_fruits:
            i.Growth()
        if self.Fruits_Status() == -1:
            raise ValueError('Error in Fruits Status')

    @property
    def young(self):
        return self.__young

    @property
    def okay(self):
        return self.__okay

    @property
    def old(self):
        return self.__old

    @property
    def count_fruit(self):
        return self.__count_fruit

    @property
    def fertilized(self):
        return self.__fertilized

    @fertilized.setter
    def fertilized(self, status):
        self.__fertilized = status

    """
    Метод сбора фруктов
    """
    def Pick_Fruits(self):
        if self.__count_fruit:
            for i in self.list_fruits:
                if i.Status != "неспелый":
                    self.list_fruits.remove(i)
                    self.__count_fruit -= 1

class Result:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.__young = True
        self.__okay = False
        self.__old = False

    def Growth(self):
        self.time += 1
        if self.time == 5:
            self.__young = False
            self.__okay = True
        if self.time == 10:
            self.__okay = False
            self.__old = True

    def Status(self):
        if self.__young:
            return "неспелый"
        elif self.__okay:
            return "спелый"
        elif self.__old:
            return "гнилой"

# фрукты
class Fruits(Result):
    def __init__(self, name="яблоко"):
        super().__init__(name)

# овощи
class Vegetable(Result):
    def __init__(self, name="картофель"):
        super().__init__(name)

# семена
class Seeds(Plant):
    def __init__(self, name="картофель"):
        super().__init__(name, 0)

# сорняк
class Weed(Plant):
    def __init__(self):
        super().__init__()

# удобрения
class Fertilizer:
    def __init__(self):
        pass

    def ToFertilize(self, object):
        if type(object) is Tree:
            object.fertilized = True
            object.Growth()
            print("Дерево", object.name, "удобрено")
        else:
            print("Некорректные данные")

# прополка
class Weeding:
    def __init__(self):
        pass

    def ToWeed(selfself, object):
        if type(object) is Garden_Bed:
            object.weed_count = 0
            object.weed_list = []
            print("Грядка", object.name, "прополота")
        else:
            print("Некорректные данные")

# вредитель
class Pest:
    def __init__(self, name="жук"):
        self.name = name

    def Plant_Influence(self, object):
        if type(object) is Tree:
            if not object.fertilized:
                object.Hinder_Growth()
                print("\nВНИМАНИЕ!!", self.name, "вредит дереву", object.name)
                print("Рекомендуется удобрить")
        else:
            print("Некорректные данные")

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["name"] = self.name
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.name = state["name"]

# болезнь
class Disease:

    def __init__(self):
        pass

    def Plant_Influence(self, object):
        if type(object) is Tree:
            if not object.fertilized:
                object.Hinder_Growth()
                print("\nВНИМАНИЕ!! Болезнь вредит дереву", object.name)
                print("Рекомендуется удобрить")
        else:
            print("Некорректные данные")

# погода
class Weather:
    def __init__(self):
        pass

    def Define_Weater(self, object):
        if type(object) is Garden:
            a = random.randint(0, 1)
            if a:
                sun = Sun()
                sun.Influence(object)
            else:
                rain = Rain()
                rain.Influence(object)
        else:
            print("Некорректные данные")

# солнце
class Sun:
    def __init__(self):
        print("Сегодня солнечно")

    def Influence(self, object):
        if type(object) is Garden:
            object.water = False
            print("Рекомендуется полить сад")
        else:
            print("Некорректные данные")

# дождь
class Rain:
    def __init__(self):
        print("Сегодня идет дождь")

    def Influence(self, object):
        if type(object) is Garden:
            object.water = True
        else:
            print("Некорректные данные")

# засуха
class Drought:
    def __init__(self):
        print("\nВНИМАНИЕ!! Засуха вредит растениям")
        print("Рекомендуется полить сад")

    # влияние на растения
    def Plant_Infuence(self, object):
        if type(object) is Garden_Bed or isinstance(object, Plant):
            object.Hinder_Growth()
        else:
            print("Некорректные данные")


# полив
class Watering:
    def __init__(self, object):
        if type(object) is Garden:
            object.water = True
            print("Сад полит")
        else:
            print("Некорректные данные")


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def begin_input(inp):
    if inp == "создать":
        return 1
    elif inp == "выгрузить":
        return 2
    else:
        return -1

list_one_word = ["полить", "вывести_информацию_деревья", "вывести_информацию_грядки",
                 "собрать_фрукты", "собрать_овощи", "количество_деревьев", "количество_грядок", "убрать_грядку", "прополка", "сохранить_выйти", "помощь"]

list_two_words = ["посадить_дерево", "удобрить", "вырубить", "посадить_семена", "новая_грядка"]

def work_input(inp):
    num = 1
    for i in list_one_word:
        if i == inp:
            return num
        num += 1
    list = inp.split()
    if len(list) == 2:
        for i in list_two_words:
            if i == list[0]:
                if num < 15:
                    if find_in_tree_seedling(list[1]):
                        return num
                    else:
                        print_tree_seedlings()
                        return -1
                if num >= 15:
                    if find_in_seed(list[1]):
                        return num
                    else:
                        print_seeds()
                        return -1
            num += 1
    return -1

def find_in_tree_seedling(seedling):
    for i in list_tree_seedling:
        if i == seedling:
            return True

def find_in_seed(seed):
    for i in list_seeds:
        if i == seed:
            return True

list_tree_seedling = ["абрикос", "вишня", "груша", "слива", "черешня", "яблоня"]
list_seeds = ["картофель", "морковь", "редис", "капуста", "свекла", "помидор", "огурец", "перец", "тыква", "кабачок", "баклажан"]

def print_tree_seedlings():
    print("Возможно работать только с этими деревьями: ")
    for i in list_tree_seedling:
        print(i, end=" ")
    print()

def print_seeds():
    print("Есть семена только для этих культур: ")
    for i in list_seeds:
        print(i, end=" ")
    print()

def print_info():
    print("Инструкция по формату ввода:")
    print("полить - для полива сада")
    print("вывести_информацию_деревья - для вывода информации для каждого дерева про фрукты")
    print("вывести_информацию_грядки - для вывода информации для каждой грядки про овощи, семена и сорняки")
    print("собрать_фрукты - для сбора спелых и гнилых фруктов")
    print("собрать_овощи - для сбора спелых и гнилых овощей")
    print("количество_деревьев - для вывода количетсва деревьев")
    print("количество_грядок - для вывода количества грядок")
    print("убрать_грядку - для того, чтобы убрать грядку с наименьшим количеством овощей и семян")
    print("прополка - для прополки грядок")
    print("сохранить_выйти - для сохранения в файл и выхода из игры")

    print("\nпосадить_дерево название_дерева - для посадки дерева. Вводите название дерева в именительном падеже")
    print("удобрить название_дерева - для удобрения дерева. Вводите название дерева в именительном падеже")
    print("вырубить название_дерева - для вырубки дерева. Вводите название дерева в именительном падеже")
    print("посадить_семена название_культуры - для посадки семян. Вводите название культуры в именительном падеже")
    print(
        "новая_грядка название_культуры - для создания новой грядки, на которой будет расти введенная культура. Вводите название культуры в именительном падеже")
    print("\nпомощь - чтобы получить инструкцию по формату ввода")


def console_application():

    # |||||||||||||||||||||||||||||||||||||| BEGIN |||||||||||||||||||||||||||||||||||||||||
    print("Здравствуйте! \nДля создания нового сада введите создать \nДля того, чтобы выгрузить сад из файла, введите выгрузить")
    kod = begin_input(input())
    match kod:
        case 1:
            garden = Garden()
            flag = True
        case 2:
            try:
                with open("inform.pkl", "rb") as fp:
                    garden = pickle.load(fp)
                    flag = True
            except FileNotFoundError:
                print("Ошибка в работе с файлом")
        case -1:
            raise ValueError('Неверный ввод!')

    print_info()
    weather = Weather()
    time = 0

    while flag:
        time += 1

        if not time % 3 or time == 1:
            print("\n~~~~~~~~~~~~~~~~ О ПОГОДЕ В РЕГИОНАХ ~~~~~~~~~~~~~~~~~~")
            weather.Define_Weater(garden)

        garden.Growth()

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Введите действие:")
        inp = input()
        kod1 = work_input(inp)

        match kod1:
            case -1:
                print("Неверный ввод!")

            # полить
            case 1:
                Watering(garden)

            # информация про деревья
            case 2:
                garden.Get_FruitsCount()

            # информация про грядки
            case 3:
                if garden.garden_bed_count:
                    print("\nКоличество сорняков:")
                    garden.Get_WeedCount()
                    print("\nКоличество семян:")
                    garden.Get_SeedCount()
                    print("\nКоличество овощей:")
                    garden.Get_VegetableCount()
                else:
                    print("В саду еще нет грядок")

            # собрать фрукты
            case 4:
                garden.Pick_Fruits()

            # собрать овощи
            case 5:
                garden.Pick_Vegetable()

            # количество деревьев
            case 6:
                if garden.tree_count == 1:
                    print("В саду растёт только 1 дерево")
                elif garden.tree_count > 1 and garden.tree_count < 5:
                    print("В саду растёт", garden.tree_count, "дерева")
                else:
                    print("В саду растёт", garden.tree_count, "деревьев")

            # количество грядок
            case 7:
                if garden.garden_bed_count == 1:
                    print("В саду только 1 грядка")
                elif garden.garden_bed_count > 1 and garden.garden_bed_count < 5:
                    print("В саду", garden.garden_bed_count, "грядки")
                else:
                    print("В саду", garden.garden_bed_count, "грядок")

            # убрать грядку
            case 8:
                garden.Remove_OneGardenBed()

            # прополка
            case 9:
                garden.Bed_Wedding()

            # сохранить и выйти
            case 10:
                with open("inform.pkl", "wb") as fp:
                    pickle.dump(garden, fp)
                flag = False

            case 11:
                print_info()

            # посадить дерево
            case 12:
                list = inp.split()
                garden.Plant_Tree(list[1])
                print("Дерево", list[1], "посажено")

            # удобрить
            case 13:
                list = inp.split()
                garden.ToFertilize(list[1])

            # вырубить
            case 14:
                list = inp.split()
                garden.Remove_OneTree(list[1])

            # посадить семена
            case 15:
                list = inp.split()
                garden.ToPlant(list[1])

            # сделать новую грядку
            case 16:
                list = inp.split()
                garden.Make_GardenBed(list[1])


if __name__ == '__main__':
    console_application()


