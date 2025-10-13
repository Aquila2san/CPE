#####################################################################################################################################################################
# Objectifs : 
# Date :
# Auteurs : 
# ToDo :
#####################################################################################################################################################################


from tkinter import *

# Définition des classes

class classe_brique:
    def __init__(self, indice, x, y, largeur=80, hauteur=25, couleur="red"):
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
    def __init__(self, x, y = 700, largeur = 100, hauteur = 10, couleur = "black"):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.vitesse = 10
        self.vers_gauche = False
        self.vers_droite = False
        self.id = None
    
    def afficher(self,canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur)

    def deplacer_gauche(self, canvas):
        if self.x - self.vitesse >= 0:
            self.x -= self.vitesse
            canvas.move(self.id, -self.vitesse, 0)

    def deplacer_droite(self, canvas):
        if self.x + self.largeur + self.vitesse <= canvas.winfo_width():
            self.x += self.vitesse
            canvas.move(self.id, self.vitesse, 0)

    def appui_gauche(self, event=None):
        self.vers_gauche = True

    def relache_gauche(self, event=None):
        self.vers_gauche = False

    def appui_droite(self, event=None):
        self.vers_droite = True

    def relache_droite(self, event=None):
        self.vers_droite = False

    def mise_a_jour(self, canvas):
        if self.vers_gauche:
            self.deplacer_gauche(canvas)
        if self.vers_droite:
            self.deplacer_droite(canvas)


class classe_balle:
    def __init__(self, x, y, rayon = 8, couleur = "red"):
        self.x = x
        self.y = y 
        self.rayon = rayon
        self.couleur = couleur
        self.vx = 3
        self.vy = -3
        self.id = None

    def afficher(self, canvas):
        self.id = canvas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill = self.couleur)

    def bouger(self, canvas, raquette, liste_brique):
        self.x += self.vx
        self.y += self.vy
        canvas.move(self.id, self.vx, self.vy)
        largeur = canvas.winfo_width()
        hauteur = canvas.winfo_height()
        
        # Collision avec les murs gauche/droite/plafond
        if self.x - self.rayon <= 0:
            self.x = self.rayon
            self.vx = -self.vx
        elif self.x + self.rayon >= largeur:
            self.x = largeur - self.rayon
            self.vx = -self.vx
        elif self.y - self.rayon <= 0:
            self.y = 0 + self.rayon
            self.vy = -self.vy
        
        # Collision avec la bordure inférieure
        if self.y - self.rayon >= hauteur:
            # recentre la raquette
            nouveau_raquette_x = (largeur - raquette.largeur) / 2
            dx = nouveau_raquette_x - raquette.x
            raquette.x = nouveau_raquette_x
            canvas.move(raquette.id, dx, 0)
            # replace la balle juste au-dessus de la raquette
            self.x = raquette.x + raquette.largeur / 2
            self.y = raquette.y - self.rayon - 1
            self.vx = 3
            self.vy = -3
            canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

        # Collision avec la raquette
        if raquette.id is not None:
            rx1, ry1, rx2, ry2 = canvas.coords(raquette.id)
            # si la balle touche la raquette
            if (self.vy > 0 and (self.y + self.rayon) >= ry1 and (self.y - self.rayon) <= ry2 and (self.x >= rx1) and (self.x <= rx2)):
                # on place la balle juste au-dessus et on inverse vy
                self.y = ry1 - self.rayon
                self.vy = -abs(self.vy)

        # Collision avec les briques
        for ligne in liste_brique:
            for brique in ligne:
                if brique.id is not None:
                    bx1, by1, bx2, by2 = canvas.coords(brique.id)
                    # Vérifie si la balle touche la brique
                    if (self.x + self.rayon >= bx1 and self.x - self.rayon <= bx2 and self.y + self.rayon >= by1 and self.y - self.rayon <= by2):
                        canvas.delete(brique.id) # Supprime la brique
                        brique.id = None 
                        self.vy = -self.vy 
                        break  



# === Programme principal ===
fenetre = Tk()
fenetre.title("Casse-briques")

LARGEUR_FENETRE = 1200
HAUTEUR_FENETRE = 800
fond = Canvas(fenetre, width=LARGEUR_FENETRE, height=HAUTEUR_FENETRE, bg="lightblue")
fond.pack()

fenetre.update()

# Création des objets

liste_brique = [] # Création et affichage des briques
for i in range(10): 
    ligne_brique = []
    for j in range(12):
        x = 50 + j * 92.7
        y = 50 + i * 35
        couleur = ["red", "orange", "yellow", "green", "blue", "blue", "green", "yellow", "orange", "red"][i]
        brique = classe_brique((i,j), x, y, couleur=couleur)
        brique.afficher(fond)
        ligne_brique.append(brique)
    liste_brique.append(ligne_brique)

raquette_x = (LARGEUR_FENETRE - 80) / 2
raquette = classe_raquette(raquette_x)
raquette.afficher(fond)

balle_x = raquette.x + raquette.largeur / 2
balle_y = raquette.y - 8 - 1
balle = classe_balle(balle_x, balle_y)
balle.afficher(fond)



# Contrôles de la raquette
fond.focus_set()
fenetre.bind("<KeyPress-Left>", raquette.appui_gauche)
fenetre.bind("<KeyRelease-Left>", raquette.relache_gauche)
fenetre.bind("<KeyPress-Right>", raquette.appui_droite)
fenetre.bind("<KeyRelease-Right>", raquette.relache_droite)

# Boucle d'animation : déplacement de la balle, de la raqutte et vérification collisions
def mise_a_jour():
    balle.bouger(fond, raquette, liste_brique)
    raquette.mise_a_jour(fond)
    fenetre.after(10, mise_a_jour)  


mise_a_jour()
fenetre.mainloop()


