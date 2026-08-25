class Triangulo:
    def __init__(self):
        self.b = 0
        self.h = 0 
    def calcular_area(self):
        return self.b * self.h / 2
x = Triangulo() 
print(x.b, x.h)
x.b = 10
x.h = 20
print(x.calcular_area())