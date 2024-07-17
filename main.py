import pygame as pg
from pygame.locals import *

import random as rnd
import numpy as np

ecran = None  # pour l'affichage, initialisé après

class Ecran:
    ''' classe qui permet de simuler un terminal caractère couleur avec placement
    possible du curseur pour écrire où on veut (voir exemple dans dessiner_cellule) '''
    def __init__(self, dim_x, dim_y, titre):
        self.cursor = (0, 0)  # la position d'écriture (écraser avec la position voulue)
        self.taille_fonte_y = 15  # petite taille permet l'affichage sous replit.com
        pg.init()
        if not pg.font.get_init():
            print("Désolé, les fontes de caractères sont absentes, je ne peux démarrer")
            quit()
        self.font = pg.font.SysFont("Courrier, Monospace",
                                    self.taille_fonte_y)
        self.taille_fonte_x = self.font.size('A')[0]
        self.ecran = pg.display.set_mode((dim_x * self.taille_fonte_x ,
                                          dim_y * self.taille_fonte_y))
        pg.display.set_caption(titre)
    def write(self, texte, fgcolor=(255,255,255), bgcolor=(0,0,0)):
        texte = self.font.render(texte,
                            True,
                            pg.Color(fgcolor),
                            pg.Color(bgcolor))
        self.ecran.blit(texte,
                        (self.cursor[0]*self.taille_fonte_x,
                         self.cursor[1]*self.taille_fonte_y))
        pg.display.flip()

class Oriente:
    ''' conventions pour donner l'orientation d'un domino.
    Utilisation: if sens == Oriente.GD: '''
    GD = 0   # domino orienté Gauche à Droite
    HB = 1   # domino orienté Haut vers Bas
    DG = 2   # domino orienté Droite à Gauche
    BH = 3   # domino orienté Bas vers Haut

class Cellule:
    ''' cellule du plateau de jeu et aussi élément de domino (voir ci-dessous) '''
    def __init__(self, terrain='a', bonus=0) :
        ''' défaut vide et autorisée en écriture, sans bonus de comptage de point '''
        self._terrain = terrain
        self._couleur = Params.couleur[terrain]
        self._bonus = bonus
        self._decompte = False  # utile pour calculer le score des zones
    # fonctions accesseurs pour lire les attributs
    # (qui ne doivent pas être modifiables après création de la cellule)
    def terrain(self):
        return self._terrain
    def couleur(self):
        return self._couleur
    def bonus(self):
        return self._bonus
    def decompte(self):
        return self._decompte
    def set_decompte(self):
        self._decompte = True

class Domino:
    ''' un domino pour le jeu (ne pas confondre avec la liste des "dominos" dans la
    classe Params ci-dessous qui est juste une représentation en chaînes de texte)
    - on pourra indicer par [0] et [1] les 2 cellules du domino et demander son
    numéro de domino par la méthode numero()    
    '''
    def __init__(self, numero = -1, cell1 = None, cell2 = None):
        self._numero = numero
        self._cellule = [cell1, cell2]
    def __getitem__(self, indice):   # implante l'indiçage: objet[indice]
        if isinstance(indice, int):   # implante l'indiçage par entier (pas par tranches)
            return self._cellule[indice]
    def numero(self):
        return self._numero
        
class Params:
    ''' paramètres du jeu : seulement des variables de classe, pas de méthodes
        ni de variables d'instances/objets
        exemple d'utilisation: pile_dominos = Params.dominos'''
    # couleurs utiles définies en RGB sur [0,255]
    couleurs_utiles = {
        'champ'   : (198, 175, 15),
        'bois'    : (52, 122, 48),
        'pature'  : (135, 220, 69),
        'marais'  : (154, 182, 135),
        'filon'   : (170, 110, 90),
        'eau'     : (80, 115, 224),
        'chateau' : (255, 255, 255),
        'interdit': (0, 0, 0),
        'autorisé': (100, 100, 100),
        'rouge'   : (213, 11, 11),
        'bleu'    : (11, 11, 240),
        'blanc'   : (255, 255, 255),
        'noir'    : (0, 0, 0)
    }
    # couleur associées aux types de terrain des cellules
    couleur = {
        'i': couleurs_utiles['interdit'],
        'a': couleurs_utiles['autorisé'],
        '#': couleurs_utiles['chateau'],
        'C': couleurs_utiles['champ'],
        'E': couleurs_utiles['eau'],
        'P': couleurs_utiles['pature'],
        'M': couleurs_utiles['marais'],
        'F': couleurs_utiles['filon'],
        'B': couleurs_utiles['bois'],
    }
    # liste des dominos du jeu comme nuplets d'abbréviations de terrains avec
    # chaque bonus marqué comme "+": ces nuplets devront être traduits en objets Domino
    liste_dominos = [
        ("C", "C"), ("C", "C"), ("B", "B"), ("B", "B"), ("B", "B"), ("B", "B"),
        ("E", "E"), ("E", "E"), ("E", "E"), ("P", "P"), ("P", "P"), ("M", "M"),
        ("B", "C"), ("C", "E"), ("C", "P"), ("C", "M"), ("B", "E"), ("B", "P"),
        ("B", "C+"), ("C+", "E"), ("C+", "P"), ("C+", "M"), ("C+", "F"), ("B+", "C"),
        ("B+", "C"), ("B+", "C"), ("B+", "C"), ("B+", "E"), ("B+", "P"), ("C", "E+"),
        ("C", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("C", "P+"),
        ("P+", "E"), ("C", "M+"), ("P", "M+"), ("C", "F+"), ("C", "P++"), ("E", "P++"),
        ("C", "M++"), ("P", "M++"), ("C", "F++"), ("M", "F++"), ("M", "F++"), ("C", "F+++")
        ]
    # nombre et répartitions des rois # 4 rois, 2 pour joueur 0, 2 pour joueur 1
    nombre_rois = (4, (2, 2))  
    # dimensions pour tracer les terrains des joueurs
    taille_terrain = 11  # taille du côté de la zone de jeu en nombre de cellules
    taille_cellule = (2, 1)  # taille (x,y) cellule de zone de jeu en caracteres
    dim_ecran_x = taille_cellule[0] * taille_terrain * 2 + 3
    dim_ecran_y = taille_cellule[1] * (taille_terrain + 8) + 6
    # ligne où afficher les infos sans pause
    lig_info = (taille_terrain - 2) * taille_cellule[1] + 2
    # ligne où afficher les messages avec pause
    lig_message = (taille_terrain + 8) * taille_cellule[1] + 4
    
##########
##### fonctions graphiques
##########

def init_graphiques():
    ''' déclare l'écran utilisant la classe Ecran qui simule un terminal caractères
    couleurs avec la librairie pygame '''
    global ecran
    ecran = Ecran(Params.dim_ecran_x,
                  Params.dim_ecran_y,
                  'Projet Kingdomino')
    
def attendre():
    ''' attendre une pression de touche ENTRÉE '''
    global ecran
    pg.event.clear()
    while True:
        event = pg.event.wait()
        if event.type == QUIT:  # toujours traiter action fermer la fenêtre de jeu
            exit()
        if (event.type == pg.KEYUP and
            event.key == pg.K_RETURN):  # attendre relachement de touche ENTRÉE
            break
    
def lire_touche():
    ''' retourne une touche soit lettre maj ou min, soit espace, soit touches
    directions, sous forme de chaîne '''
    pg.event.clear()
    while True:
        event = pg.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                return "HAUT"
            if event.key == pg.K_DOWN:
                return "BAS"
            if event.key == pg.K_LEFT:
                return "GAUCHE"
            if event.key == pg.K_RIGHT:
                return "DROITE"
            if event.key >=  pg.K_a and event.key <=  pg.K_z:
                lettre = chr(ord('a') + (event.key - pg.K_a))
                if event.mod and pg.KMOD_SHIFT:
                    return lettre.upper()
                else:
                    return lettre
            if event.key == pg.K_SPACE:
                return " "
        
def message(texte):
    """ affiche un message en bas de l'écran et attends une pression de touche """
    global ecran
    ecran.cursor = (0, Params.lig_message)
    ecran.write(" " * 80)  # efface ligne des messages
    ecran.cursor = (0, Params.lig_message)
    ecran.write(texte)
    attendre()
    ecran.cursor = (0, Params.lig_message)
    ecran.write(" " * 80)  # efface ligne des messages
    
def info(texte):
    """ affiche une info au dessus de la zone de choix de l'écran sans attendre """
    global ecran
    ecran.cursor = (0, Params.lig_info)
    ecran.write(" " * 80)  # efface ligne des messages
    ecran.cursor = (0, Params.lig_info)
    ecran.write(texte)
            
def dessiner_cellule(ligne, colonne, cellule, mode="normal"):
    ''' dessine une cellule de terrain dans la couleur de son contenu '''
    global ecran
    if mode == "possible":  # placement possible du domino, signaler avec "<>"
        motif = "<>"
    elif mode == "impossible":  # place impossible, signaler avec "@ @" 
        motif = "@@"
    else:  # mode normal de dessin : espace coloré selon type de terrain
        motif = "  "

    lig = ligne
    col = colonne
    # boucle utile en cas de changement de taille_cellule 
    for i in range(Params.taille_cellule[1]):
        ecran.cursor = (col, lig)
        ecran.write(motif, bgcolor = cellule.couleur())
        lig += 1
    # affiche bonus
    if cellule.bonus():
        ecran.cursor = (colonne + 1, ligne)
        ecran.write(str(cellule.bonus()),
                    fgcolor = Params.couleurs_utiles["blanc"],
                    bgcolor = cellule.couleur())
                    

def dessiner_domino(haut, gauche, orient, domino, mode="normal"):
    ''' suggestion: 
    dessine le domino en faisant appel à dessiner_cellule(...)
    orient désigne l'orientation (voir classe plus haut)
    haut, gauche désignent les coordonnées du domino
    mode désigne la façon d'afficher selon terrain ou domino en cours de placement
    '''
    global ecran
    
    if orient==0:
        dessiner_cellule(haut,gauche,domino[0],mode)
        dessiner_cellule(haut,gauche+2,domino[1],mode)
    elif orient==1:
        dessiner_cellule(haut,gauche,domino[0],mode)
        dessiner_cellule(haut+1,gauche,domino[1],mode)
    elif orient==2:
        dessiner_cellule(haut,gauche,domino[0],mode)
        dessiner_cellule(haut,gauche-2,domino[1],mode)
    elif orient==3:
        dessiner_cellule(haut,gauche,domino[0],mode)
        dessiner_cellule(haut-1,gauche,domino[1],mode)


def dessiner_terrains(terrains):
    ''' dessine les terrains des 2 joueurs '''
    global ecran
    for i in range(Params.taille_terrain):
        for j in range(Params.taille_terrain):
            dessiner_cellule(i, 1+j*Params.taille_cellule[0], terrains[0][i][j])

    for i in range(Params.taille_terrain):
        for j in range(Params.taille_terrain):
            dessiner_cellule(i, (j+1+Params.taille_terrain)*Params.taille_cellule[0], terrains[1][i][j])


def dessiner_tirage(tirage, choix, cote):
    ''' 
    dessine la pile des 4 dominos du tirage, avec indications des choix éventuels déjà
    faits par les joueurs, suggestion: cote == 'gauche' ou cote == 'droit' pour dessiner
    une des deux piles de dominos 'tirage ancien tour' ou 'tirage tour courant' 
    '''
    global ecran

    """
    ecran.cursor = (col, lig)
    ecran.write(motif, bgcolor = cellule.couleur())
    """
    
    if cote=="droit":
        if tirage:
            for i in range(len(tirage)):
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+i*2)
                ecran.write("   ", bgcolor = Params.couleurs_utiles["noir"])
                dessiner_domino(Params.taille_terrain+3+i*2,(1+Params.taille_terrain)*Params.taille_cellule[0], 0,tirage[i])
        else:
            nul_domino = Domino(-1,Cellule("i"),Cellule("i"))
            for i in range(len(choix)):
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+i*2)
                ecran.write("-"+str(choix[i])+"-", bgcolor = Params.couleurs_utiles["noir"])
                dessiner_domino(Params.taille_terrain+3+i*2,(1+Params.taille_terrain)*Params.taille_cellule[0], 0,nul_domino)
    if cote=="gauche":
        for i in range(len(tirage)):
            ecran.cursor = (2*(Params.taille_cellule[0]-1), Params.taille_terrain+3+i*2)
            ecran.write("-"+str(choix[i])+"-", bgcolor = Params.couleurs_utiles["noir"])
            dessiner_domino(Params.taille_terrain+3+i*2,2+2*Params.taille_cellule[0], 0,tirage[i])

def choisir_domino(choix, position, joueur):
    ''' 
    choisi UN domino pour le joueur sur la pile du côté "droit" (tirage tour courant)
    choix: liste des choix des joueurs déjà fait (pour afficher qu'ils sont
    non disponibles)
    '''
    global ecran
    info("Joueur n "+str(joueur)+" place son roi: touch haut/bas")
    ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+choix.index(-1)*2)
    ecran.write(">>", bgcolor = Params.couleurs_utiles["noir"])
    while True:
        touche = lire_touche()
        if touche == "HAUT":
            if -1 in choix[:position]:
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+position*2)
                ecran.write("  ", bgcolor = Params.couleurs_utiles["noir"])
                pos = position-1
                while pos>-1 and choix[pos]!=-1:pos-=1
                nouveau_position=pos
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+nouveau_position*2)
                ecran.write(">>", bgcolor = Params.couleurs_utiles["noir"])
                position = nouveau_position
        elif touche == "BAS":
            if -1 in choix[position+1:]:
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+position*2)
                ecran.write("  ", bgcolor = Params.couleurs_utiles["noir"])
                nouveau_position=choix.index(-1,position+1)
                ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+nouveau_position*2)
                ecran.write(">>", bgcolor = Params.couleurs_utiles["noir"])
                position = nouveau_position
        elif touche == " ":
            ecran.cursor = ((Params.taille_terrain-1)*Params.taille_cellule[0], Params.taille_terrain+3+position*2)
            ecran.write("-"+str(joueur)+"-", bgcolor = Params.couleurs_utiles["noir"])
            return position

def coordonnes_deuxieme_cellule(x,y,orient):
    '''
    cette fonction determine les coordonnées de la deuxieme cellule du domino 
    sachant que la premiere cellule a les coordonnées (x,y) et l'orientation orient    
    '''
    if orient==0:x2,y2 = x,y+1
    elif orient==1:x2,y2 = x+1,y
    elif orient==2:x2,y2 = x,y-1
    elif orient==3:x2,y2 = x-1,y
    return x2,y2

def domino_posable(domino, x, y, orient, joueur, terrains):
    '''
    cette fonction determine si les cellules qui sont adjoints aux cellules du domino 
    ont un terrain commun, si oui dont le domino a un mode possible sinon le domino est 
    impossible de le placer dans le terrain
    '''
    if orient==0:
        entourage_cellule1 = list(map(lambda x:x.terrain(),[terrains[joueur][x-1][y],terrains[joueur][x+1][y],terrains[joueur][x][y-1]]))
        entourage_cellule2 = list(map(lambda x:x.terrain(),[terrains[joueur][x][y+2],terrains[joueur][x+1][y+1],terrains[joueur][x-1][y+1]]))

    elif orient==1:
        entourage_cellule1 = list(map(lambda x:x.terrain(),[terrains[joueur][x][y+1],terrains[joueur][x][y-1],terrains[joueur][x-1][y]]))
        entourage_cellule2 = list(map(lambda x:x.terrain(),[terrains[joueur][x+1][y-1],terrains[joueur][x+1][y+1],terrains[joueur][x+2][y]]))
      
    elif orient==2:
        entourage_cellule1 = list(map(lambda x:x.terrain(),[terrains[joueur][x-1][y],terrains[joueur][x+1][y],terrains[joueur][x][y+1]]))
        entourage_cellule2 = list(map(lambda x:x.terrain(),[terrains[joueur][x-1][y-1],terrains[joueur][x+1][y-1],terrains[joueur][x][y-2]]))
       
    elif orient==3:
        entourage_cellule1 = list(map(lambda x:x.terrain(),[terrains[joueur][x][y+1],terrains[joueur][x][y-1],terrains[joueur][x+1][y]]))
        entourage_cellule2 = list(map(lambda x:x.terrain(),[terrains[joueur][x-1][y-1],terrains[joueur][x-1][y+1],terrains[joueur][x-2][y]]))
       
    if domino[0].terrain() in entourage_cellule1 or domino[1].terrain() in entourage_cellule2 or "#" in entourage_cellule1+entourage_cellule2:
        return True
    return False

def placer_domino(domino, joueur, terrains):
    '''
    suggestion : affiche le domino du joueur en "surimpression" au
    centre de son terrain, et permet de le déplacer et de le pivoter
    jusqu'à une position valide : le joueur peut alors valider son
    placement et le domino est posé sur son terrain.  On peut aussi
    abandonner le placement si pas possible ou pas souhaitable.
    '''
    global ecran

    info("Joueur "+str(joueur)+" placer: haut/bas/gauche/droite, espace, x")
    x,y,orient = 5,5,0
    x2,y2 = 5,6
    if joueur==0:
        dessiner_domino(x, 1+y*Params.taille_cellule[0], 0, domino, mode="impossible")
    else:
        dessiner_domino(x, (y+1+Params.taille_terrain)*Params.taille_cellule[0],0, domino, mode="impossible")
    mode = "impossible"
    while True:
        touche = lire_touche()
        if touche == "HAUT":
            if terrains[joueur][x-1][y].terrain()!="i" and terrains[joueur][x2-1][y2].terrain()!="i":
                x-=1
                x2-=1
            if terrains[joueur][x][y].terrain()=="a" and terrains[joueur][x2][y2].terrain()=="a" and domino_posable(domino, x, y, orient, joueur, terrains):
                mode = "possible"
            else:
                mode = "impossible"
            
        elif touche == "BAS":
            if terrains[joueur][x+1][y].terrain()!="i" and terrains[joueur][x2+1][y2].terrain()!="i":
                x+=1
                x2+=1
            if terrains[joueur][x][y].terrain()=="a" and terrains[joueur][x2][y2].terrain()=="a" and domino_posable(domino, x, y, orient, joueur, terrains):
                mode = "possible"
            else:
                mode = "impossible"
            
        elif touche == "GAUCHE":
            if terrains[joueur][x][y-1].terrain()!="i" and terrains[joueur][x2][y2-1].terrain()!="i":
                y-=1
                y2-=1
            if terrains[joueur][x][y].terrain()=="a" and terrains[joueur][x2][y2].terrain()=="a" and domino_posable(domino, x, y, orient, joueur, terrains):
                mode = "possible"
            else:
                mode = "impossible"

        elif touche == "DROITE":
            if terrains[joueur][x][y+1].terrain()!="i" and terrains[joueur][x2][y2+1].terrain()!="i":
                y+=1
                y2+=1
            if terrains[joueur][x][y].terrain()=="a" and terrains[joueur][x2][y2].terrain()=="a" and domino_posable(domino, x, y, orient, joueur, terrains):
                mode = "possible"
            else:
                mode = "impossible"

        elif touche == " ":
            x3,y3 = coordonnes_deuxieme_cellule(x,y,(orient+1)%4)
            if terrains[joueur][x3][y3].terrain()!="i":
                x2,y2 = x3,y3
                orient = (orient+1)%4
            if terrains[joueur][x2][y2].terrain()=="a" and domino_posable(domino, x, y, orient, joueur, terrains):
                mode = "possible"
            else:
                mode = "impossible"

        elif touche == "X":
            dessiner_terrains(terrains)
            return x,y,orient,mode

        dessiner_terrains(terrains)
        if joueur==0:
            dessiner_domino(x, 1+y*Params.taille_cellule[0], orient, domino, mode)
        else:
            dessiner_domino(x, (y+1+Params.taille_terrain)*Params.taille_cellule[0],orient, domino, mode)
        

            
    
##########
##### fonctions de gestion du jeu
##########
    
def choisir_nombre_joueurs():
    ''' pourrait être complétée si on améliore l'appli pour plus de 2 joueurs '''
    return 2

def texte_en_cellule(texte):
    ''' transforme le texte de description d'une cellule en objet Cellule '''
    return Cellule(texte[0],texte.count("+"))

def preparer_dominos(nombre_joueurs):
    ''' lit les descriptions de dominos dans Params.liste_dominos, les convertit
    en liste d'objets de classe Domino, les mélange aléatoirement et ajuste leur
    nombre selon le nombre de joueurs (à 2 écarter la moitié des dominos aléatoirement),
    retourne la pile d'objets Domino'''
    domi_desc = Params.liste_dominos
    list_domi = []
    for i in range(len(domi_desc)):
        cel1 = texte_en_cellule(domi_desc[i][0])
        cel2 = texte_en_cellule(domi_desc[i][1])
        somme_bonus = cel1.bonus()+cel2.bonus()
        domino = Domino(somme_bonus,cel1,cel2) 
        list_domi.append(domino)
    #rnd.shuffle(list_domi)
    if nombre_joueurs==2:
        pile = rnd.sample(list_domi,24)
    return pile

def preparer_terrains(nombre_joueurs):
    ''' prépare la zone de jeu de chaque joueur: un tableau numpy de cellules
    vides et autorisées à poser des dominos, sauf la cellule au centre qui
    est le château du joueur (point de départ des dominos), et le cadre des cellules
    interdites autour de la zone 9x9
    '''
    terrains = [np.array([[Cellule() for _ in range(Params.taille_terrain)] for _ in range(Params.taille_terrain)],dtype=Cellule) for _ in range(nombre_joueurs)]
    
    for _ in range(nombre_joueurs):
        terrains[_][5][5]=Cellule("#",0)
        for i in range(Params.taille_terrain):
            terrains[_][0][i]=Cellule("i",0)
            terrains[_][-1][i]=Cellule("i",0)
        for i in range(1,Params.taille_terrain-1):
            terrains[_][i][0]=Cellule("i",0)
            terrains[_][i][-1]=Cellule("i",0)
    

    return terrains

def piocher_dominos(pile, nombre_rois, compte_tours):
    ''' récupérer le bon nombre de dominos pour ce tour, les trier par ordre de
    leur numéro'''
    tirage = pile[compte_tours*nombre_rois:(compte_tours+1)*nombre_rois]
    tirage.sort(key=lambda x:x.numero())
    return tirage

def ordre_jeu_initial(nombre_joueurs):
    ''' rend une liste donnant l'ordre du tour avec les numéros des joueurs (à 2 joueurs
    chacun joue 2 fois)
    '''
    exemple = [0,1,0,1]
    rnd.shuffle(exemple)
    return exemple

def placer_rois_initiaux(ordre_jeu):
    ''' 
    procède au choix de la 1ère série de dominos : rend une liste de numéros de joueurs,
    à l'indice i de la liste on a le numéro de joueur qui choisit le domino i du tirage
    courant
    '''
    choix = [-1 for _ in range(len(ordre_jeu))]
    
    position = 0
    choix_numero = 1
    while choix_numero<5:
        joueur = ordre_jeu[choix_numero-1]
        position = choisir_domino(choix,choix.index(-1),joueur)
        choix[position] = joueur
        choix_numero += 1
        
    return choix

def poser_domino(joueur, ligne, colonne, domino, rotation, terrains):
    ''' suggestion:
    les coordonnées ligne colonne ont été validés avant, on écrit les cellules du
    domino dans le terrain du joueur et on réduits les cases autorisées si nécessaire
    pour imposer la dimension maximum 5x5 du territoire final
    '''
    x,y = ligne,colonne
    terrains[joueur][ligne][colonne]=domino[0]
    if rotation==0:
        terrains[joueur][ligne][colonne+1]=domino[1]
        x_translate = x-5
        y_translate = y+1-5 if y>=5 else y-5
    elif rotation==1:
        terrains[joueur][ligne+1][colonne]=domino[1]
        x_translate = x-5 if x<5 else x+1-5
        y_translate = y-5
    elif rotation==2:
        terrains[joueur][ligne][colonne-1]=domino[1]
        x_translate = x-5
        y_translate = y-5 if y>5 else y-1-5
    elif rotation==3:
        terrains[joueur][ligne-1][colonne]=domino[1]
        x_translate = x-5 if x>5 else x-1-5
        y_translate = y-5

    if x_translate>0:
        for i in range(1,x_translate+1):
            for j in range(Params.taille_terrain):
                terrains[joueur][i][j]=Cellule("i")
    elif x_translate<0:
        for i in range(Params.taille_terrain-2,Params.taille_terrain-2+x_translate,-1):
            for j in range(Params.taille_terrain):
                terrains[joueur][i][j]=Cellule("i")

    if y_translate>0:
        for j in range(1,y_translate+1):
            for i in range(Params.taille_terrain):
                terrains[joueur][i][j]=Cellule("i")
    if y_translate<0:
        for j in range(Params.taille_terrain-2,Params.taille_terrain-2+y_translate,-1):
            for i in range(Params.taille_terrain):
                terrains[joueur][i][j]=Cellule("i")

    dessiner_terrains(terrains)
    return terrains

def jouer_tour(pile, ancien_tirage, ancien_choix, terrains, compte_tours):
    ''' 
    joue un tour de jeu:
    - on pioche le nouveau tirage
    - on affiche l'ancien et le nouveau tirage
    - pour chaque joueur dans l'ordre des joueurs de l'ancien choix on va:
       - choisir le nouveau domino
       - placer le domino de l'ancien tirage, 
    - on retournera le nouveau tirage et les nouveaux choix pour le prochain tour
      (sauf si c'est le dernier tour auquel cas pas de nouveau tirage à faire) '''
    tirage = piocher_dominos(pile, len(ancien_choix), compte_tours+1)
    choix = [-1 for _ in range(len(ancien_choix))]
    dessiner_tirage(ancien_tirage, ancien_choix, cote="gauche")

    if tirage:
        dessiner_tirage(tirage, choix, cote="droit")
        position = 0
        choix_numero = 1
        while choix_numero<5:
            joueur = ancien_choix[choix_numero-1]

            for i in range(choix_numero):
                ecran.cursor = (2*(Params.taille_cellule[0]-1), Params.taille_terrain+3+i*2)
                ecran.write("XXX", bgcolor = Params.couleurs_utiles["noir"])

            position = choisir_domino(choix,choix.index(-1),joueur)
            choix[position] = joueur
            ligne,colonne,orient,mode = placer_domino(ancien_tirage[choix_numero-1], joueur, terrains)
            if mode=="possible":
                terrains = poser_domino(joueur, ligne, colonne, ancien_tirage[choix_numero-1], orient, terrains)
            choix_numero += 1
    else:
        dessiner_tirage(tirage, ancien_choix, cote="droit")
        position = 0
        choix_numero = 1
        while choix_numero<5:
            joueur = ancien_choix[choix_numero-1]

            for i in range(choix_numero):
                ecran.cursor = (2*(Params.taille_cellule[0]-1), Params.taille_terrain+3+i*2)
                ecran.write("XXX", bgcolor = Params.couleurs_utiles["noir"])

            ligne,colonne,orient,mode = placer_domino(ancien_tirage[choix_numero-1], joueur, terrains)
            if mode=="possible":
                terrains = poser_domino(joueur, ligne, colonne, ancien_tirage[choix_numero-1], orient, terrains)
            choix_numero += 1
        

    return tirage, choix, terrains

def compter_bonus(terrain, x, y):
    '''
    fonction récursive qui aide à traverser les cellules de meme couleur et retourne la somme
    des bonus et la somme des cellules dans la meme nature de terrain
    '''
    terrain_cellule = terrain[x][y].terrain()
    terrain[x][y].set_decompte()
    somme = terrain[x][y].bonus()

    if x>0 and terrain[x-1][y].terrain()==terrain_cellule and not terrain[x-1][y].decompte():
        somme1, surface1 = compter_bonus(terrain, x-1, y)
    else: somme1, surface1 = 0,0

    if y>0 and terrain[x][y-1].terrain()==terrain_cellule and not terrain[x][y-1].decompte():
        somme2, surface2 = compter_bonus(terrain, x, y-1)
    else: somme2, surface2 = 0,0

    if x<Params.taille_terrain-1 and terrain[x+1][y].terrain()==terrain_cellule and not terrain[x+1][y].decompte():
        somme3, surface3 = compter_bonus(terrain, x+1, y)
    else: somme3, surface3 = 0,0

    if y<Params.taille_terrain-1 and terrain[x][y+1].terrain()==terrain_cellule and not terrain[x][y+1].decompte():
        somme4, surface4 = compter_bonus(terrain, x, y+1)
    else: somme4, surface4 = 0,0

    return somme+somme1+somme2+somme3+somme4,1+surface1+surface2+surface3+surface4
        
def compter_points(terrains, nombre_joueurs):
    '''
    retourne une liste de paire [joueur, score] en comptant les points
    de chaque joueur. Suggestion: passer sur chaque cellule du terrain
    du joueur, utiliser une autre fonction pour compter récursivement
    les voisines de même couleur d'une cellule et leur bonus, et
    utiliser la variable d'instance 'decompte' de chaque cellule pour
    mémoriser si elle a déjà été comptée (on doit donc l'ignorer et ne
    pas rappeler la récursivité) ou pas encore comptée
    '''
    scores = []
    for joueur in range(nombre_joueurs):
        score = 0
        for i in range(Params.taille_terrain):
            for j in range(Params.taille_terrain):
                if terrains[joueur][i][j].decompte():continue
                somme, surface = compter_bonus(terrains[joueur],i,j)
                score += somme*surface
        scores.append([joueur,score])

    return scores
                
##########
##### fonction principale
##########

def kingdom():
    ''' joue une partie '''    
    # mémoriser l'écran pygcurse de manière globale
    global ecran

    # initialisations
    init_graphiques()
    nombre_joueurs = choisir_nombre_joueurs()
    pile = preparer_dominos(nombre_joueurs)
    terrains = preparer_terrains(nombre_joueurs)
    dessiner_terrains(terrains)
    compte_tours = 1

    # "tour" préparatoire pour placer les premiers rois
    ordre_jeu = ordre_jeu_initial(nombre_joueurs)
    nombre_rois = len(ordre_jeu)  # ne pas confondre nombre de rois et de joueurs
    tirage = piocher_dominos(pile, nombre_rois, compte_tours)
    choix = [-1] * len(ordre_jeu)   # indices choisis par joueurs (-1 = pas encore choisi)
    dessiner_tirage(tirage, choix, cote="droit")
    choix = placer_rois_initiaux(ordre_jeu)

    # boucle des tours de jeu
    # compte_tours = 1
    while tirage:  # tant que tirage non vide, il reste des dominos à placer
        message("tour " + str(compte_tours) + " pressez ENTRÉE svp")        
        tirage, choix, terrains = jouer_tour(pile, tirage, choix, terrains, compte_tours)
        compte_tours += 1

    #afficher les résultats
    scores = compter_points(terrains, nombre_joueurs)
    message("Fin du jeu")
    message("joueur 0: " + str(scores[0][1]) +
            " pts; joueur 1: " + str(scores[1][1]) + " pts")
    
if __name__ == "__main__":   # vrai si fichier exécuté et pas inclus comme module
    kingdom()