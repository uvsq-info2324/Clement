import tkinter as tk
import random

def Initialisation():
    joueurDebut = 1

    jetonsDebut = 0

    TAB = [[0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]]

    return(joueurDebut,jetonsDebut,TAB)

def Changement_joueur(player): #MOI
    if player==1:
        player=2
    else:
        player=1
    return player

def click(event):
    global yodel
    global nCol
    x = event.x
    yodel.set((x-10)//100)
    nCol = yodel.get()
    print(nCol)
    print("Position X du clic :", x)
    print("Numéro de Colonne :", nCol)

def dessin_grille():  #MOI
    x=10
    y=10
    for i in range(8):
        trace_ligne_ver(x)
        x=x+100
    for j in range(7):
        trace_ligne_hor(y)
        y=y+100

def trace_ligne_ver(x1):
    y1=10
    y2=610
    grille.create_line((x1,y1),(x1,y2),width=2,fill="black")

def trace_ligne_hor(y1):
    x1=10
    x2=710
    grille.create_line((x1,y1),(x2,y1),width=2,fill="black")

def Recherche_Colonne(x): #MOI
    numero_colonne=(x-10)//100
    return numero_colonne

def check_variable():
    if yodel != 0 and yodel < 711:
        print("Donnée récupérée :", yodel)
        return True
    else:
        root.after(100, check_variable)

def Recherche_ligne(nColonne, TabJeu):
    i = 5 #il s'agit de la ligne le plus en bas dans le tableau
    while i >= 0 and TabJeu[i][nColonne] != 0:
        i -= 1 #On enleve 1 à i pour vérifier la ligne du dessus
    print("ligne recherche", i)
    return i #i correspond au numéro de ligne

def Dessin_jeton(X,Y,Player, set):
    colorange1=["blue2", "lime green","blue4","light sea green"]
    colorange2=["dark orange", "deep pink","yellow","hot pink"]
    colonne_du_cercle=X*100+10+50
    ligne_du_cercle=Y*100+10+50#+50 #fois 100 pour mettre à échelle, puis compter la marge et la diff centre/bout
    couleur_du_cercle=Player
    couleur=0
    if couleur_du_cercle==1:
        couleur=colorange1[set]
    else:
        couleur=colorange2[set]
    y1=ligne_du_cercle
    x1=colonne_du_cercle-21
    y2=ligne_du_cercle+15
    x2=colonne_du_cercle+21
    calmar(x1,y1,x2,y2,couleur)



def calmar(X1, Y1, X2, Y2, clr):
    global d1
    global d2
    global d3
    global d4
    global d5
    global d6
    global d7
    global d8
    global d9
    global d10
    global derjet
    #tête
    d1 = grille.create_rectangle(X1,Y1,X2,Y2,outline=clr,fill=clr)
    d2 = grille.create_polygon(X1-15, Y1, X2+15, Y1, X1+20, Y1-40, fill=clr, outline=clr)
    #tentacules
    d3 = grille.create_rectangle(X1, Y2, X1+6, Y2+20, fill=clr, outline=clr)
    d4 = grille.create_rectangle(X1+12, Y2, X1+18, Y2+20, fill=clr, outline=clr)
    d5 = grille.create_rectangle(X2-12, Y2, X2-18, Y2+20, fill=clr, outline=clr)
    d6 = grille.create_rectangle(X2, Y2, X2-6, Y2+20, fill=clr, outline=clr)

    #yeux
    d7 = grille.create_rectangle(X1+9, Y1+4, X1+18, Y2-1, fill="white")
    d8 = grille.create_rectangle(X2-9, Y1+4, X2-18, Y2-1, fill="white")
    d9 = grille.create_rectangle(X1+12, Y1+7, X1+17, Y2-2, fill="black", outline="white")
    d10 = grille.create_rectangle(X2-12, Y1+7, X2-17, Y2-2, fill="black", outline="white")
    derjet = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10]

def Actualiser_Jeu (ligne,colonne,joueur,jeu): #MOI
    global nbJetons
    nbJetons+=1
    if joueur==1:
        jeu[ligne][colonne]=1
    else:
        jeu[ligne][colonne]=2
    return jeu

def Controle_alignement(TAB, Player):
    #Cette fonction vérifie l'alignement en appellant trois fonctions vérifiant l'alignement vertical, horizontal et diagonal.
    Vict = False
    Gagnant = 0

    alignementVertical = controle_alignement_vertical(TAB, Player, Ligne, nCol)

    alignementHorizontal = Controle_alignement_horizontal(TAB, Player, Ligne, nCol)

    alignementDiagonal = Controle_alignement_diagonal(TAB, Player, Ligne, nCol)

    if alignementHorizontal or alignementVertical or alignementDiagonal:
        Vict = True
        Gagnant = Player

    return (Gagnant, Vict)

#Cette fonction prend en paramètre le tableau représentant le jeu, le joueur actuel et les coordonnées du jeton placé
def controle_alignement_vertical(TAB, Player, x, y):
    nbAlignes = 1  # Initialise le compteur à 1 pour le jeton actuel
    i = x + 1  # Commence à vérifier les jetons en dessous du jeton actuel

    # Vérifie les jetons en dessous du jeton actuel
    while i <= 5 and TAB[i][y] == Player:
        nbAlignes += 1
        i += 1

    # Si au moins 4 jetons sont alignés verticalement, retourne True, sinon False
    return nbAlignes >= 4

def Controle_alignement_horizontal(TAB, Player, x, y):
    #Pour gagner, un joueur doit aligner aumoins 4 jetons de la même couleur.
    #Cette fonction vérifie s'il y a 3 jetons de la même couleur, sur la même ligne de part et d'autre du jeton qui vient d'être placé.
    #Pour cela, la fonction vérifie la présence de jetons de la même couleur dans un rayon de trois cases autour du jeton qui vient d'être placé.
    #La fonction compte le nombre de jetons alignés, et s'il y a aumoins 3 jetons alignés, la fonction retourne qu'il y a bien un alignement horizontal.

    xDebut = x
    yDebut = y
    nbAlignés = 0

    while y <= 6 and TAB[x][y] == Player:
        nbAlignés += 1
        y += 1


    while TAB[xDebut][yDebut-1] == Player and yDebut > 0:
        nbAlignés += 1
        yDebut -= 1

    if nbAlignés >= 4:
        return True
    else:
        return False

def Controle_alignement_diagonal(TAB,Player,X,Y):
    init_X=X
    init_Y=Y
    BackUp_X=X+1
    BackUp_Y=Y-1
    Extend_X=X+1
    Extend_Y=Y+1
    Score=0
    Compteur=0
    while X>=0 and Y<=6 and TAB[X][Y]==Player:
         Score+=1
         X-=1
         Y+=1
    while BackUp_X<=5 and BackUp_Y>=0 and TAB[BackUp_X][BackUp_Y]==Player:
        Score+=1
        BackUp_X+=1
        BackUp_Y-=1
    while init_X>=0 and init_Y>=0 and TAB[init_X][init_Y]==Player:
        Compteur+=1
        init_X-=1
        init_Y-=1
    while Extend_X<=5 and Extend_Y<=6 and TAB[Extend_X][Extend_Y]==Player:
        Compteur+=1
        Extend_X+=1
        Extend_Y+=1
    if Score>=4 or Compteur>=4:
        return True
    else:
        return False
    

def retour(line, column, token, matrix): #MOI
    global Joueur
    matrix[line][column] = 0
    for i in range(len(derjet)):
        grille.delete(derjet[i])
    if Joueur !=1:
        Joueur = 1
    else:
        Joueur = 2


    
def Affichage_Final(Victoire,Vainqueur,compteur):
    B1=tk.Label(root,text="Le joueur 1 a gagné",font=("Impact", 50),bg="black",fg="white")
    B2=tk.Label(root,text="Le joueur 2 a gagné",font=("Impact", 50),bg="black",fg="white")
    B3=tk.Label(root,text="égalité.",font=("Impact", 50),bg="black",fg="white")
    if Victoire==True and Vainqueur==1:
        B1.place(x=0,y=0)
    elif Victoire==True and Vainqueur==2:
        B2.place(x=0,y=0)
    elif compteur>=42: #s'il n'y a plus de place dans la grille
        B3.place(x=0,y=0)





'''########################################################################
###################################################################################
########################################################################'''



# Création de la fenêtre principale
root = tk.Tk()
root.title("Puissance 4 (Spl4t ?)")
root.geometry("1020x720")


# Création d'une zone de dessin (grille) pour représenter la grille          MOI
grille = tk.Canvas(root, width=710, height=610, bg="seashell2")
grille.place(x=0, y=0)
grille.pack()

# Création d'une zone d'interface secondaire
inter = tk.Canvas(root, width = 150, height = 600, bg = "gray")
inter.place(x=870, y=5)
inter.create_line((2,2),(2,598),width=2,fill="black")
inter.create_line((2,2),(148,2),width=2,fill="black")
inter.create_line((148,2),(148,598),width=2,fill="black")
inter.create_line((2,598),(148,598),width=2,fill="black")

undo = tk.Button(inter, text = "Undo", width = 4, height = 1, command = lambda : retour(Ligne, nCol, derjet, JEU),
                 font = ("Arial", 25))
undo.place(x=2, y=400)



nbJoueur, nbJetons, JEU = Initialisation()
victoire = False
Joueur = random.randint(1,2)
couleurs = random.randint(0,3)


# Dessiner une grille simple pour l'exemple
dessin_grille()

# Associer la fonction click à un clic de souris sur la zone de dessin
yodel = tk.IntVar()
nCol = 0
while victoire == False and nbJetons < 42:
    grille.bind("<Button-1>", click)
    root.wait_variable(yodel)
    Ligne = Recherche_ligne(nCol, JEU)
    print(Ligne)
    Dessin_jeton(nCol, Ligne, Joueur, couleurs)
    print(derjet)
    Actualiser_Jeu(Ligne, nCol, Joueur, JEU)
    print(JEU)
    Vainqueur, victoire = Controle_alignement(JEU, Joueur)
    Joueur = Changement_joueur(Joueur)
Affichage_Final(victoire, Vainqueur, nbJetons)


root.mainloop()