#####################################################################################################################################################################
# Objectifs : 
# Date :
# Auteurs : 
# ToDo :
#####################################################################################################################################################################


from tkinter import *

class classe_brique:
    def __init__(self, indice, x, y, largeur=60, hauteur=20, couleur="red"):
        self.indice = indice
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.id = None

    def afficher(self, canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur, outline="black")

class classe_raquette:
    def __init__(self, x, y = 360, largeur = 80, hauteur = 10, couleur = "black"):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.id = None
    
    def afficher(self,canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur)


# === Programme principal ===
fenetre = Tk()
fenetre.title("Casse-briques")
fond = Canvas(fenetre, width=600, height=400, bg="lightblue")
fond.pack()
classe_raquette(260).afficher(fond)

# Création et affichage des briques
liste_brique = []
for i in range(5):
    ligne_brique = []
    for j in range(8):
        x = 50 + j * 65
        y = 50 + i * 25
        couleur = ["red", "orange", "yellow", "green", "blue"][i]
        brique = classe_brique((i,j), x, y, couleur=couleur)
        brique.afficher(fond)
        ligne_brique.append(brique)
    liste_brique.append(ligne_brique)

fenetre.mainloop()


