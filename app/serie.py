class Serie:
    def __init__(self, codigo, nombre, url_imdb, genero="", anio_estreno=0, num_temporadas=1):
        self.codigo = codigo
        self.nombre = nombre
        self.url_imdb = f"https://www.imdb.com/title/{url_imdb}"
        self.genero = genero
        self.anio_estreno = anio_estreno
        self.num_temporadas = num_temporadas
        self.actores = []