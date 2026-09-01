class Triangulo:
    def __init__(self):
        self._b = 0
        self._h = 0 

    def set_base(self, v):
        if v >= 0: 
            self._b = v
        else: 
            raise ValueError('Base deve ser positiva')

    def set_altura(self, v):
        if v >= 0: 
            self._h = v
        else: 
            raise ValueError('Altura deve ser positiva')

    def get_base(self):
        return self._b

    def get_altura(self):
        return self._h

    def calcular_area(self): 
        return (self._b * self._h) / 2


class UI:
    @staticmethod
    def main():
        x = Triangulo()
        print(f"Base inicial: {x.get_base()} | Altura inicial: {x.get_altura()}")
        
        # Define os novos valores usando os métodos modificadores (setters)
        x.set_base(10)
        x.set_altura(20)
        
        print(f"Base atualizada: {x.get_base()} | Altura atualizada: {x.get_altura()}")
        print(f"Área do triângulo: {x.calcular_area()}")


if __name__ == "__main__":
    UI.main()
