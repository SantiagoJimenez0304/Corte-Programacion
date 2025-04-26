class ActorActriz:
    def __init__(self, codigo, nombre, url_imdb, nacionalidad="", fecha_nacimiento="", premios=None):
        self.codigo = codigo
        self.nombre = nombre
        self.url_imdb = f"https://www.imdb.com/name/{url_imdb}"
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.premios = premios if premios is not None else []