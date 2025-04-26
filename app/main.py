from persistencia import Persistencia
from visual import Visual

if __name__ == "main":
    datos = Persistencia()
    vista = Visual(datos)
    vista.menu()