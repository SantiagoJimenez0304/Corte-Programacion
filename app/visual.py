import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from persistencia import Persistencia
from actor import ActorActriz
from serie import Serie

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Series y Actores")
        self.p = Persistencia()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.frame_series = ttk.Frame(self.notebook)
        self.frame_actores = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_series, text='Series')
        self.notebook.add(self.frame_actores, text='Actores')

        self.setup_series()
        self.setup_actores()
    
    def mostrar_info_serie(self):
        seleccion = self.tree_series.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una serie para ver su información")
            return
        
        codigo_serie = int(seleccion[0])
        serie = self.p.get_serie(codigo_serie)
        if not serie:
            messagebox.showerror("Error", "Serie no encontrada")
            return
        
        # Crear ventana de información
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Información de {serie.nombre}")
        
        # Frame principal
        main_frame = ttk.Frame(info_window)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Información básica
        ttk.Label(main_frame, text=f"Nombre: {serie.nombre}", font=('Arial', 10, 'bold')).pack(anchor='w')
        ttk.Label(main_frame, text=f"Género: {serie.genero}").pack(anchor='w')
        ttk.Label(main_frame, text=f"Año de estreno: {serie.anio_estreno}").pack(anchor='w')
        ttk.Label(main_frame, text=f"Número de temporadas: {serie.num_temporadas}").pack(anchor='w')
        
        # Actores asociados
        actores = self.p.serie_actores(codigo_serie)
        if actores:
            ttk.Label(main_frame, text="\nActores:", font=('Arial', 9, 'bold')).pack(anchor='w')
            for actor in actores:
                ttk.Label(main_frame, text=f"- {actor.split('] ')[1]}").pack(anchor='w')
        else:
            ttk.Label(main_frame, text="\nNo hay actores asociados", font=('Arial', 9, 'italic')).pack(anchor='w')
        
        # Botón para cerrar
        ttk.Button(info_window, text="Cerrar", command=info_window.destroy).pack(pady=10)

    def mostrar_info_actor(self):
        seleccion = self.tree_actores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un actor para ver su información")
            return
        
        codigo_actor = int(seleccion[0])
        actor = next((a for a in self.p.actores if a.codigo == codigo_actor), None)
        if not actor:
            messagebox.showerror("Error", "Actor no encontrado")
            return
        
        # Crear ventana de información
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Información de {actor.nombre}")
        
        # Frame principal
        main_frame = ttk.Frame(info_window)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Información básica
        ttk.Label(main_frame, text=f"Nombre: {actor.nombre}", font=('Arial', 10, 'bold')).pack(anchor='w')
        ttk.Label(main_frame, text=f"Nacionalidad: {actor.nacionalidad}").pack(anchor='w')
        ttk.Label(main_frame, text=f"Fecha de nacimiento: {actor.fecha_nacimiento}").pack(anchor='w')
        
        # Premios
        if actor.premios:
            ttk.Label(main_frame, text="\nPremios:", font=('Arial', 9, 'bold')).pack(anchor='w')
            for premio in actor.premios:
                ttk.Label(main_frame, text=f"- {premio}").pack(anchor='w')
        else:
            ttk.Label(main_frame, text="\nNo tiene premios registrados", font=('Arial', 9, 'italic')).pack(anchor='w')
        
        # Series en las que trabaja
        series = self.p.actor_trabaja(codigo_actor)
        if series:
            ttk.Label(main_frame, text="\nSeries:", font=('Arial', 9, 'bold')).pack(anchor='w')
            for serie in series:
                ttk.Label(main_frame, text=f"- {serie}").pack(anchor='w')
        else:
            ttk.Label(main_frame, text="\nNo está asociado a ninguna serie", font=('Arial', 9, 'italic')).pack(anchor='w')
        
        # Botón para cerrar
        ttk.Button(info_window, text="Cerrar", command=info_window.destroy).pack(pady=10)

    def setup_series(self):
        self.tree_series = ttk.Treeview(self.frame_series, columns=("Nombre", "IMDB"), show='headings')
        self.tree_series.heading("Nombre", text="Nombre")
        self.tree_series.heading("IMDB", text="IMDB")
        self.tree_series.pack(fill='both', expand=True)

        frame_botones_series = ttk.Frame(self.frame_series)
        frame_botones_series.pack(pady=5)

        self.btn_ver_serie = ttk.Button(frame_botones_series, text="Ver en IMDb", command=self.abrir_link_serie)
        self.btn_ver_serie.pack(side='left', padx=5)

        self.btn_agregar_serie = ttk.Button(frame_botones_series, text="Agregar Serie", command=self.agregar_serie)
        self.btn_agregar_serie.pack(side='left', padx=5)

        self.btn_editar_serie = ttk.Button(frame_botones_series, text="Editar Serie", command=self.editar_serie)
        self.btn_editar_serie.pack(side='left', padx=5)

        self.btn_borrar_serie = ttk.Button(frame_botones_series, text="Borrar Serie", command=self.borrar_serie)
        self.btn_borrar_serie.pack(side='left', padx=5)
        
        self.cargar_series()
        self.btn_info_serie = ttk.Button(frame_botones_series, text="Ver Información", command=self.mostrar_info_serie)
        self.btn_info_serie.pack(side='left', padx=5)
        self.tree_series.bind("<Double-1>", lambda e: self.mostrar_info_serie()) 
        self.btn_gestionar_actores = ttk.Button(frame_botones_series, 
                                          text="Gestionar Actores", 
                                          command=self.gestionar_actores_serie)
        self.btn_gestionar_actores.pack(side='left', padx=5) 

    def setup_actores(self):
        self.tree_actores = ttk.Treeview(self.frame_actores, columns=("Nombre", "IMDB"), show='headings')
        self.tree_actores.heading("Nombre", text="Nombre")
        self.tree_actores.heading("IMDB", text="IMDB")
        self.tree_actores.pack(fill='both', expand=True)

        frame_botones_actores = ttk.Frame(self.frame_actores)
        frame_botones_actores.pack(pady=5)

        self.btn_ver_actor = ttk.Button(frame_botones_actores, text="Ver en IMDb", command=self.abrir_link_actor)
        self.btn_ver_actor.pack(side='left', padx=5)

        self.btn_agregar_actor = ttk.Button(frame_botones_actores, text="Agregar Actor", command=self.agregar_actor)
        self.btn_agregar_actor.pack(side='left', padx=5)

        self.btn_editar_actor = ttk.Button(frame_botones_actores, text="Editar Actor", command=self.editar_actor)
        self.btn_editar_actor.pack(side='left', padx=5)

        self.btn_borrar_actor = ttk.Button(frame_botones_actores, text="Borrar Actor", command=self.borrar_actor)
        self.btn_borrar_actor.pack(side='left', padx=5)

        self.cargar_actores()
        self.btn_info_actor = ttk.Button(frame_botones_actores, text="Ver Información", command=self.mostrar_info_actor)
        self.btn_info_actor.pack(side='left', padx=5)
        self.tree_actores.bind("<Double-1>", lambda e: self.mostrar_info_actor()) 

    def cargar_series(self):
        for item in self.tree_series.get_children():
            self.tree_series.delete(item)
        for serie in self.p.series:
            self.tree_series.insert('', 'end', iid=str(serie.codigo), values=(serie.nombre, serie.url_imdb))

    def cargar_actores(self):
        for item in self.tree_actores.get_children():
            self.tree_actores.delete(item)
        for actor in self.p.actores:
            self.tree_actores.insert('', 'end', iid=str(actor.codigo), values=(actor.nombre, actor.url_imdb))

    def abrir_link_serie(self):
        seleccion = self.tree_series.selection()
        if seleccion:
            item = self.tree_series.item(seleccion)
            url = item['values'][1]
            webbrowser.open(url)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una serie para ver en IMDb")

    def abrir_link_actor(self):
        seleccion = self.tree_actores.selection()
        if seleccion:
            item = self.tree_actores.item(seleccion)
            url = item['values'][1]
            webbrowser.open(url)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un actor para ver en IMDb")

    def agregar_serie(self):
        ventana_serie = tk.Toplevel(self.root)
        ventana_serie.title("Agregar Nueva Serie")

        tk.Label(ventana_serie, text="Código").pack(pady=5)
        entry_codigo = tk.Entry(ventana_serie)
        entry_codigo.pack(pady=5)

        tk.Label(ventana_serie, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(ventana_serie)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_serie, text="URL IMDb (ID)").pack(pady=5)
        entry_url_imdb = tk.Entry(ventana_serie)
        entry_url_imdb.pack(pady=5)

        tk.Label(ventana_serie, text="Género").pack(pady=5)
        entry_genero = tk.Entry(ventana_serie)
        entry_genero.pack(pady=5)

        tk.Label(ventana_serie, text="Año de Estreno").pack(pady=5)
        entry_anio = tk.Entry(ventana_serie)
        entry_anio.pack(pady=5)

        tk.Label(ventana_serie, text="Número de Temporadas").pack(pady=5)
        entry_temporadas = tk.Entry(ventana_serie)
        entry_temporadas.pack(pady=5)

        def agregar_serie_datos():
            try:
                codigo = int(entry_codigo.get())
                nombre = entry_nombre.get()
                url_imdb = entry_url_imdb.get()
                genero = entry_genero.get()
                anio = int(entry_anio.get())
                temporadas = int(entry_temporadas.get())

                if self.p.serie_adiciona(codigo, nombre, url_imdb, genero, anio, temporadas):
                    self.cargar_series()
                    ventana_serie.destroy()
                else:
                    messagebox.showerror("Error", "El código de serie ya existe")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese datos válidos.")

        tk.Button(ventana_serie, text="Agregar", command=agregar_serie_datos).pack(pady=10)

    def editar_serie(self):
        seleccion = self.tree_series.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una serie para editar")
            return

        codigo_serie = int(seleccion[0])
        serie = self.p.get_serie(codigo_serie)
        if not serie:
            messagebox.showerror("Error", "Serie no encontrada")
            return

        ventana_serie = tk.Toplevel(self.root)
        ventana_serie.title("Editar Serie")

        tk.Label(ventana_serie, text="Código").pack(pady=5)
        entry_codigo = tk.Entry(ventana_serie)
        entry_codigo.insert(0, str(serie.codigo))
        entry_codigo.config(state='disabled')
        entry_codigo.pack(pady=5)

        tk.Label(ventana_serie, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(ventana_serie)
        entry_nombre.insert(0, serie.nombre)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_serie, text="URL IMDb (ID)").pack(pady=5)
        entry_url_imdb = tk.Entry(ventana_serie)
        entry_url_imdb.insert(0, serie.url_imdb.split('/')[-1].strip('{}'))  # Extraer solo el ID
        entry_url_imdb.pack(pady=5)

        tk.Label(ventana_serie, text="Género").pack(pady=5)
        entry_genero = tk.Entry(ventana_serie)
        entry_genero.insert(0, serie.genero)
        entry_genero.pack(pady=5)

        tk.Label(ventana_serie, text="Año de Estreno").pack(pady=5)
        entry_anio = tk.Entry(ventana_serie)
        entry_anio.insert(0, str(serie.anio_estreno))
        entry_anio.pack(pady=5)

        tk.Label(ventana_serie, text="Número de Temporadas").pack(pady=5)
        entry_temporadas = tk.Entry(ventana_serie)
        entry_temporadas.insert(0, str(serie.num_temporadas))
        entry_temporadas.pack(pady=5)

        def editar_serie_datos():
            try:
                nombre = entry_nombre.get()
                url_imdb = entry_url_imdb.get()
                genero = entry_genero.get()
                anio = int(entry_anio.get())
                temporadas = int(entry_temporadas.get())

                if self.p.serie_edita(codigo_serie, nombre, url_imdb, genero, anio, temporadas):
                    self.cargar_series()
                    ventana_serie.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo editar la serie")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese datos válidos.")

        tk.Button(ventana_serie, text="Guardar", command=editar_serie_datos).pack(pady=10)

    def borrar_serie(self):
        seleccion = self.tree_series.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una serie para borrar")
            return

        codigo_serie = int(seleccion[0])
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea borrar esta serie?"):
            if self.p.serie_borra(codigo_serie):
                self.cargar_series()
                messagebox.showinfo("Éxito", "Serie borrada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo borrar la serie")

    def agregar_actor(self):
        ventana_actor = tk.Toplevel(self.root)
        ventana_actor.title("Agregar Nuevo Actor")

        tk.Label(ventana_actor, text="Código").pack(pady=5)
        entry_codigo = tk.Entry(ventana_actor)
        entry_codigo.pack(pady=5)

        tk.Label(ventana_actor, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(ventana_actor)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_actor, text="URL IMDb (ID)").pack(pady=5)
        entry_url_imdb = tk.Entry(ventana_actor)
        entry_url_imdb.pack(pady=5)

        tk.Label(ventana_actor, text="Nacionalidad").pack(pady=5)
        entry_nacionalidad = tk.Entry(ventana_actor)
        entry_nacionalidad.pack(pady=5)

        tk.Label(ventana_actor, text="Fecha de Nacimiento").pack(pady=5)
        entry_fecha = tk.Entry(ventana_actor)
        entry_fecha.pack(pady=5)

        tk.Label(ventana_actor, text="Premios (separados por coma)").pack(pady=5)
        entry_premios = tk.Entry(ventana_actor)
        entry_premios.pack(pady=5)

        def agregar_actor_datos():
            try:
                codigo = int(entry_codigo.get())
                nombre = entry_nombre.get()
                url_imdb = entry_url_imdb.get()
                nacionalidad = entry_nacionalidad.get()
                fecha_nacimiento = entry_fecha.get()
                premios = [p.strip() for p in entry_premios.get().split(",")] if entry_premios.get() else []

                if self.p.actor_adiciona(codigo, nombre, url_imdb, nacionalidad, fecha_nacimiento, premios):
                    self.cargar_actores()
                    ventana_actor.destroy()
                else:
                    messagebox.showerror("Error", "El código de actor ya existe")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese datos válidos.")

        tk.Button(ventana_actor, text="Agregar", command=agregar_actor_datos).pack(pady=10)

    def editar_actor(self):
        seleccion = self.tree_actores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un actor para editar")
            return

        codigo_actor = int(seleccion[0])
        actor = next((a for a in self.p.actores if a.codigo == codigo_actor), None)
        if not actor:
            messagebox.showerror("Error", "Actor no encontrado")
            return

        ventana_actor = tk.Toplevel(self.root)
        ventana_actor.title("Editar Actor")

        tk.Label(ventana_actor, text="Código").pack(pady=5)
        entry_codigo = tk.Entry(ventana_actor)
        entry_codigo.insert(0, str(actor.codigo))
        entry_codigo.config(state='disabled')
        entry_codigo.pack(pady=5)

        tk.Label(ventana_actor, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(ventana_actor)
        entry_nombre.insert(0, actor.nombre)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_actor, text="URL IMDb (ID)").pack(pady=5)
        entry_url_imdb = tk.Entry(ventana_actor)
        entry_url_imdb.insert(0, actor.url_imdb.split('/')[-1].strip('{}'))  # Extraer solo el ID
        entry_url_imdb.pack(pady=5)

        tk.Label(ventana_actor, text="Nacionalidad").pack(pady=5)
        entry_nacionalidad = tk.Entry(ventana_actor)
        entry_nacionalidad.insert(0, actor.nacionalidad)
        entry_nacionalidad.pack(pady=5)

        tk.Label(ventana_actor, text="Fecha de Nacimiento").pack(pady=5)
        entry_fecha = tk.Entry(ventana_actor)
        entry_fecha.insert(0, actor.fecha_nacimiento)
        entry_fecha.pack(pady=5)

        tk.Label(ventana_actor, text="Premios (separados por coma)").pack(pady=5)
        entry_premios = tk.Entry(ventana_actor)
        entry_premios.insert(0, ", ".join(actor.premios) if actor.premios else "")
        entry_premios.pack(pady=5)

        def editar_actor_datos():
            try:
                nombre = entry_nombre.get()
                url_imdb = entry_url_imdb.get()
                nacionalidad = entry_nacionalidad.get()
                fecha_nacimiento = entry_fecha.get()
                premios = [p.strip() for p in entry_premios.get().split(",")] if entry_premios.get() else []

                if self.p.actor_edita(codigo_actor, nombre, url_imdb, nacionalidad, fecha_nacimiento, premios):
                    self.cargar_actores()
                    ventana_actor.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo editar el actor")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese datos válidos.")

        tk.Button(ventana_actor, text="Guardar", command=editar_actor_datos).pack(pady=10)

    def borrar_actor(self):
        seleccion = self.tree_actores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un actor para borrar")
            return
        
        codigo_actor = int(seleccion[0])
        
        # Verificar si el actor está en alguna serie
        series_con_actor = [s.nombre for s in self.p.series if codigo_actor in s.actores]
        
        if series_con_actor:
            mensaje = ("No se puede borrar el actor porque está asociado a las siguientes series:\n\n" +
                     "\n".join(f"- {serie}" for serie in series_con_actor) +
                     "\n\nPor favor, disocie al actor de estas series primero.")
            messagebox.showerror("Error", mensaje)
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea borrar este actor?"):
            if self.p.actor_borra(codigo_actor):
                self.cargar_actores()
                messagebox.showinfo("Éxito", "Actor borrado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo borrar el actor") 

    def gestionar_actores_serie(self):
        seleccion = self.tree_series.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una serie para gestionar sus actores")
            return
        
        codigo_serie = int(seleccion[0])
        serie = self.p.get_serie(codigo_serie)
        if not serie:
            messagebox.showerror("Error", "Serie no encontrada")
            return
        
        # Crear ventana de gestión de actores
        gestion_window = tk.Toplevel(self.root)
        gestion_window.title(f"Actores en {serie.nombre}")
        gestion_window.geometry("500x400")
        
        # Frame principal
        main_frame = ttk.Frame(gestion_window)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Lista de todos los actores disponibles
        ttk.Label(main_frame, text="Actores disponibles:").pack(anchor='w')
        
        # Crear un Treeview con checkboxes para selección múltiple
        self.tree_actores_modal = ttk.Treeview(main_frame, columns=("Nombre",), show='headings')
        self.tree_actores_modal.heading("Nombre", text="Nombre")
        self.tree_actores_modal.pack(fill='both', expand=True, pady=5)
        
        # Llenar el Treeview con todos los actores
        for actor in self.p.actores:
            esta_asociado = actor.codigo in serie.actores
            self.tree_actores_modal.insert('', 'end', iid=str(actor.codigo), 
                                         values=(actor.nombre,), 
                                         tags=('asociado' if esta_asociado else 'no_asociado'))
        
        # Configurar colores para visualización
        self.tree_actores_modal.tag_configure('asociado', background='lightgreen')
        self.tree_actores_modal.tag_configure('no_asociado', background='white')
        
        # Frame para botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(pady=10)
        
        def actualizar_asociaciones():
            seleccionados = self.tree_actores_modal.selection()
            for actor in self.p.actores:
                codigo_actor = actor.codigo
                esta_seleccionado = str(codigo_actor) in seleccionados
                actualmente_asociado = codigo_actor in serie.actores
                
                if esta_seleccionado and not actualmente_asociado:
                    self.p.serie_asocia(codigo_serie, codigo_actor)
                elif not esta_seleccionado and actualmente_asociado:
                    self.p.serie_disocia(codigo_serie, codigo_actor)
            
            # Actualizar colores
            for actor in self.p.actores:
                esta_asociado = actor.codigo in serie.actores
                self.tree_actores_modal.item(str(actor.codigo), 
                                           tags=('asociado' if esta_asociado else 'no_asociado'))
            
            messagebox.showinfo("Éxito", "Asociaciones actualizadas correctamente")
        
        ttk.Button(frame_botones, text="Guardar Cambios", command=actualizar_asociaciones).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=gestion_window.destroy).pack(side='left', padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()