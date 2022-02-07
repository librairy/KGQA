import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """
    Clase que gestiona multiples paginas en una misma aplicacion de streamlit.
    """
    def __init__(self) -> None:
        """
        Constructor de la clase MultiPage
        """
        #Atributo pages, lista de diccionarios con las subpaginas de nuestra interfaz
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """
        Metodo que agrega una pagina a nuestro proyecto. Argumentos:
        - title: Titulo de la pagina, sera el que aparezca en el selector
        - func: Funcion de Python que ejecutara nuestra interfaz para correr la pagina en cuestion
        """
        self.pages.append(
            {
                "title": title, 
                "function": func
            }
        )

    def run(self):
        """
        Funcion que ejecuta el codigo de la aplicacion
        """
        #Selector   
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function']()