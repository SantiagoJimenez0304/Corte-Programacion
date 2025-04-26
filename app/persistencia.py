from actor import ActorActriz
from serie import Serie

class Persistencia:
    def __init__(self):
        self.actores = []
        self.series = []

        self.actor_adiciona(78, "Ana María Orozco", "nm0650450", "Colombia", "1973-07-04", ["Premio TVyNovelas"])
        self.actor_adiciona(81, "Laura Londoño", "nm2256810", "Colombia", "1988-02-13", [])
        self.actor_adiciona(84, "Carolina Ramírez", "nm1329835", "Colombia", "1983-06-20", [])
        self.actor_adiciona(93, "Catherine Siachoque", "nm0796171", "Colombia", "1972-01-21", ["Premio Tu Mundo"])
        self.actor_adiciona(98, "Carmenza González", "nm1863990", "Colombia", "1961-07-16", [])
        self.actor_adiciona(99, "Andrés Londoño", "nm2150265", "Colombia", "1996-12-19", [])
        self.actor_adiciona(101, "Sebastián Martínez", "nm1101968", "Colombia", "1983-01-07", [])
        self.actor_adiciona(102, "Majida Issa", "nm2449973", "Colombia", "1981-06-27", [])
        self.actor_adiciona(103, "Julián Román", "nm0739814", "Colombia", "1977-11-23", ["Premio India Catalina"])
        self.actor_adiciona(104, "Paola Rey", "nm0721140", "Colombia", "1979-12-19", [])
        self.actor_adiciona(105, "Mario Duarte", "nm0239119", "Colombia", "1965-06-17", [])
        self.actor_adiciona(106, "Lina Tejeiro", "nm4813048", "Colombia", "1991-10-08", [])
        self.actor_adiciona(107, "Alejandra Borrero", "nm0097356", "Colombia", "1962-04-25", ["Premio India Catalina"])



        self.series.append(Serie(16, "Yo soy Betty, la fea", "tt0233127", "Comedia", 1999, 1))
        self.series.append(Serie(43, "La reina del flow", "tt8560918", "Drama", 2018, 2))
        self.series.append(Serie(60, "Café con Aroma de Mujer", "tt14471346", "Romance", 2021, 1))
        self.series.append(Serie(62, "Los Briceño", "tt10348478", "Drama", 2019, 1))
        self.series.append(Serie(70, "Distrito Salvaje", "tt8105958", "Acción", 2018, 2))
        self.series.append(Serie(72, "Mil Colmillos", "tt9701670", "Terror", 2021, 1))
        self.series.append(Serie(83, "Perdida", "tt10064124", "Thriller", 2020, 1))
        self.series.append(Serie(90, "Rosario Tijeras", "tt6340304", "Acción", 2010, 3))
        self.series.append(Serie(91, "La Ley del Corazón", "tt6311902", "Drama", 2016, 2))
        self.series.append(Serie(92, "El Capo", "tt1527368", "Acción", 2009, 4))
        self.series.append(Serie(94, "Pasión de Gavilanes", "tt0387763", "Romance", 2003, 2))
        self.series.append(Serie(95, "Amar y Vivir", "tt2268749", "Romance", 2020, 1))


        self.serie_asocia(16, 78)
        self.serie_asocia(16, 93)
        self.serie_asocia(16, 98)
        self.serie_asocia(83, 78)
        self.serie_asocia(70, 78)
        self.serie_asocia(43, 84)
        self.serie_asocia(43, 101)
        self.serie_asocia(60, 81)
        self.serie_asocia(60, 105)
        self.serie_asocia(62, 99)
        self.serie_asocia(62, 106)
        self.serie_asocia(72, 102)
        self.serie_asocia(72, 107)
        self.serie_asocia(90, 102)
        self.serie_asocia(90, 103)
        self.serie_asocia(91, 104)
        self.serie_asocia(91, 101)
        self.serie_asocia(92, 103)
        self.serie_asocia(92, 105)
        self.serie_asocia(94, 104)
        self.serie_asocia(94, 107)
        self.serie_asocia(95, 106)
        self.serie_asocia(95, 84)

    def actor_adiciona(self, codigo, nombre, url, nacionalidad="", fecha_nacimiento="", premios=None):
        if any(a.codigo == codigo for a in self.actores):
            return False
        self.actores.append(ActorActriz(codigo, nombre, url, nacionalidad, fecha_nacimiento, premios))
        return True

    def actor_edita(self, codigo_actor, nombre, url, nacionalidad="", fecha_nacimiento="", premios=None):
        for actor in self.actores:
            if actor.codigo == codigo_actor:
                actor.nombre = nombre
                actor.url_imdb = f"https://www.imdb.com/name/{url}"
                actor.nacionalidad = nacionalidad
                actor.fecha_nacimiento = fecha_nacimiento
                actor.premios = premios if premios is not None else []
                return True
        return False

    def actor_en_serie(self, codigo_actor):
     """Verifica si un actor está asociado a alguna serie"""
     return any(codigo_actor in s.actores for s in self.series) 

    def actor_borra(self, codigo_actor):
        if not self.actor_en_serie(codigo_actor):
            self.actores = [a for a in self.actores if a.codigo != codigo_actor]
            return True
        return False

    def nombre_actor(self, codigo_actor):
        for actor in self.actores:
            if actor.codigo == codigo_actor:
                return actor.nombre
        return "N/A"

    def actor_trabaja(self, codigo_actor):
        return [s.nombre for s in self.series if codigo_actor in s.actores]

    def serie_adiciona(self, codigo_serie, nombre, url, genero="", anio_estreno=0, num_temporadas=1):
        if any(s.codigo == codigo_serie for s in self.series):
            return False
        self.series.append(Serie(codigo_serie, nombre, url, genero, anio_estreno, num_temporadas))
        return True

    def serie_edita(self, codigo_serie, nombre, url, genero="", anio_estreno=0, num_temporadas=1):
        for serie in self.series:
            if serie.codigo == codigo_serie:
                serie.nombre = nombre
                serie.url_imdb = f"https://www.imdb.com/title/{url}"
                serie.genero = genero
                serie.anio_estreno = anio_estreno
                serie.num_temporadas = num_temporadas
                return True
        return False

    def serie_borra(self, codigo_serie):
        self.series = [s for s in self.series if s.codigo != codigo_serie]
        return True

    def serie_actores(self, codigo_serie):
        serie = self.get_serie(codigo_serie)
        if serie:
            return [f"[{c}] {self.nombre_actor(c)}" for c in serie.actores]
        return []

    def serie_asocia(self, codigo_serie, codigo_actor):
        serie = self.get_serie(codigo_serie)
        if serie and codigo_actor not in serie.actores:
            serie.actores.append(codigo_actor)
            return True
        return False

    def serie_disocia(self, codigo_serie, codigo_actor):
        serie = self.get_serie(codigo_serie)
        if serie and codigo_actor in serie.actores:
            serie.actores.remove(codigo_actor)
            return True
        return False

    def get_serie(self, codigo_serie):
        return next((s for s in self.series if s.codigo == codigo_serie), None)