import streamlit as st
 
class MultiPage: 
    """
    Framework that combines multiple Streamlit applications in one single website.
    """
    def __init__(self) -> None:
        """
        Class constructor
        """
        self.pages = {}
    
    def addPage(self, title, func) -> None: 
        """
        Function that adds a new page to the MultiPage (adds new entry to the pages dictionary)
        """
        self.pages.update({title: func})

    def run(self, db):
        """
        Method that runs the MultiPage (executes the selected page).
        """
        #Selector   
        page = st.sidebar.radio(
            "App Navigation", 
            self.pages.keys()
        )

        #Run app of the selected page
        self.pages[page](db)