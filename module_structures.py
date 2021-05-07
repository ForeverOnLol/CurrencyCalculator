

def nameOfMonth(num_m):
    return {
            1:'январь' ,
            2:'февраль',
            3:'март',
            4:'апрель',
            5:'май',
            6:'июнь',
            7:'июль',
            8:'август',
            9:'сентябрь', 
            10:'октябрь',
            11:'ноябрь',
            12:'декабрь'
    }[num_m]

def nameOfQuart(num_k):
    return {
        1:"первый квартал",
        2:"второй квартал",
        3:"третий квартал",
        4:"четвёртый квартал",
    }[num_k]
    
def setvalues(i):
    values = {
        2: 'weeks',
        3:'months',
        4:'quarts',
        5:'years'
    }
    return values[i]
    


class POINT:
    def __init__(self, price, name, data=None, count=None):
        self.price = price #цена
        self.name = name
        self.data = data #дата
        self.count = count