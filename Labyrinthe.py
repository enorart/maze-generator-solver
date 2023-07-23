#-----import des bibliothèques (PIL et Numpy pour le traitement d'image, random pour l'algorinthme de Kruskal)-----#
import random
from PIL import Image
import numpy as np
#------------------------------------------------------------------------------------------------------------------#


#-----Classe représentant le Labyrinthe (génération, résolution)---------------------------------------------------#
#Renvoie des images en PNG du Labyrinthe si on utilise show()---------------------------------------------------------------------------#

class Labyrinthe:
  """classe représentant l'objet Labyrinthe : génération aléatoire et résolution"""
  
  def __init__(self, x, y, largeur_chemin, largeur_mur):
    """initialisation de la classe labyrinthe : principale variable"""
    self.x=x    #taille du labyrinthe
    self.y=y   
    self.largeur_mur=largeur_mur    #largeur mur et chemin
    self.largeur_chemin=largeur_chemin
    self.sommets=[]      #liste de sommets du graphe, cette liste représente les coordonnées (x,y) de chaque sommets (ie chaque case du labyrinthe)
    self.matrice_resolution=[]    #création d'une matrice resolution (copie de la matrice img qui affiche le labyrinthe généré) pour le pathfinding
    #on initialise la liste des sommmets avec tous les sommets du labyrinthe
    for j in range(y):
      for i in range(x):
        self.sommets.append((i,j))
    
    self.labyrinthe_dico={}  #initialisation du dictionnaire représentant le labyrinthe  
    #création du dictionnaire représentant le labyrinthe 
    for poids, s in enumerate(self.sommets):    #pour kruskal, chaque sommets (ie chaque case du labyrinthe doit avoir une id unique)
  #enumerate permet d'obtenir un id unique (ca fait un compteur, mais on aurait pu le faire manuellement en faisant i+=1 a chaque fois)
      self.labyrinthe_dico[s]=[poids,[s]]    #créer un dico qui a pour clé (x,y) coordonnée du sommets, et pour valeur un tuple (poids (id unique), sommets reliées)
      #au debut il y aura que lui-meme, mais au fur et a mesure on va rajouter des sommets reliées
    
    self.labyrinthe=[]    #varaible pour s'assurer qu'on a parcouru tout les sommets (avec le while len(self.labyrinthe < len(self.aretes)-1)) + utile pour l'affichage de l'image avec PIL
    #taille des bords en pixel à partir de la largeur des murs, des chemins et de la taille en case du labyrinthe => utile pour la résolution
    self.x_max=self.largeur_mur+self.x*(self.largeur_mur+self.largeur_chemin)
    self.y_max=self.largeur_mur+self.y*(self.largeur_mur+self.largeur_chemin)
    
    #-------------------------appel des méthodes de la classe si on veut faire fonctionner la classe toute seule pour tester---------------------#
    # self.kruskal()    #génération du labyrinthe avec l'algorinthme de Kruskal
    # self.affichage()    #affichage du labyrithe avec les bibliothèques PIL et Numpy
    # self.resolution()   #resolution du labyrinthe (pathfinding et résolution avec affichage du chemin le plus court entre l'entrée et la sortie)
    #------------------------fin de l'appel des méthodes de la classe-------------#
  
  #---------------------------------création des méthodes de notre objet labyrinthe---------------------------------#
  def voisins(self,s):
    """fonction voisins qui retourne pour chaque sommets les sommets adjacents/voisins (c'est les arêtes du graphe)\n
    on parcours autour du point les faces nord(0,1), est(1,0), ouest(-1,0), sud(0,-1) et on ajoute les sommets adjacents\n
    renvoie la liste des voisins sous forme d'une liste voisin"""
    voisin=[]   #initialisation de la liste voisin
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):    #variation de x, cad de la première coordonnées dans (x,y) (donc -1 ou 1) 
      #variation de y, cad de la deuxième coordonnées dans (x,y) (donc -1 ou 1)
      if s[0]+dx >=0 and s[0]+dx < self.x and s[1]+dy >=0 and s[1]+dy < self.y:    #on ne sort pas des bords du labyrinthe
        voisin.append((s[0]+dx,s[1]+dy))
  
    return voisin  
  
  def trouver_id(self, noeud):
      """renvoie le poids/identification unique de la case => utile pour l'algorinthe de Kruskal\n
      renvoie un int (poids de la case en question)"""
      return self.labyrinthe_dico[noeud][0]    

  def union (self, noeud1, noeud2):   
    """méthode s'occupant de l'union : on met dans le dico le sommet adjacent ajouté, et le meme poids car ils sont désormais reliées ensemble (algo de kruskal)\n
    attention, il faut parcourir tout les sommets adjacent qui sont dans labyrinthe_dico, pour s'assurer de bien changer l'id pour tout le monde"""
    poids1=self.trouver_id(noeud1)    #on appel la méthode trouver_id
    poids2=self.trouver_id(noeud2)
    if poids1 != poids2 :         #on leurs mets le même poids 
      self.labyrinthe_dico[noeud1][1].append(noeud2)
      self.labyrinthe_dico[noeud2][1].append(noeud1)
      self.labyrinthe_dico[noeud2][0]=poids1
    #et on regarde bien pour tout les sommets (et on leurs met le meme poids si c'est pas le cas)
      for sommets in self.labyrinthe_dico.keys():
         if self.labyrinthe_dico[sommets][0]==poids2:
            self.labyrinthe_dico[sommets][0]=poids1           

  def kruskal(self):
    """Algorythme de kruskal pour la génération des graphes \n
    Etape 1 : prendre une arete au hasard parmis une liste d'arete (on appelle pour cela la fonction voisin qui donne les voisins pour chaque case (sommet)\n
    Etape 2 : la supprimer de la liste aretes (pour pas la reprendre 2 fois et eviter les boucles)\n
    Etape 3 : regarder le poids (id) des deux cases de l'arete (point du trait) et si ils ont pas le meme poids procéder à la fusion (ATTENTION il faut bien faire la fusion pour tout les sommets et pas forcément le dernier reliée)\n
    Etape 4 : ajouter cette arete (une fois qu'on a traité la fusion et modifié le labyrinthe_dico en conséquence) a labyrinthe (liste) pour permettre de gérer la condition de fin de l'algo + l'affichage pour après\n"""
    
    aretes=[]
    
    for s in self.sommets:    #on parcours tout les voisins de chaque sommets
      for v in self.voisins(s):   
        aretes.append((s,v))

   
    while len(self.labyrinthe)<len(aretes)-1:   #condition d'arret
    
      arete = aretes.pop(random.randint(0,len(aretes)-1))    #on prend une arete au hasard parmis les aretes
    
      if self.trouver_id(arete[0]) != self.trouver_id(arete[1]):    #on s'occupe de la fusion et on modifie labyrinthe en conséquence
        self.union(arete[0],arete[1])
        self.labyrinthe.append(arete) 
           
  def affichage(self):
    """méthode s'occupant de l'affichage du labyrinthe sous forme de PNG\n
    on utilise numpy pour inialiser une matrice (img) avec des 0 (pixel noir) et on ajoute (avec le slicing) les pixels blancs en fonction de labyrinthe (liste)\n
    renvoie avec formarray (PIL) une image créer avec la matrice img\n
    + initialisation de la matrice_resolution qui va nous être utile pour le pathfinding"""
    
    self.img = np.zeros((self.x * (self.largeur_chemin + self.largeur_mur) + self.largeur_mur, self.y * (self.largeur_chemin + self.largeur_mur) + self.largeur_mur),dtype=np.uint8)   #matrice de notre image
    self.matrice_resolution=np.zeros((self.x * (self.largeur_chemin + self.largeur_mur) + self.largeur_mur, self.y * (self.largeur_chemin + self.largeur_mur) + self.largeur_mur),dtype=np.uint32)    #matrice pour la pathfinding (on le fait a part car ca évite les problèmes pour l'image)
    for arete in self.labyrinthe:   #on parcours les aretes de la liste labyrinthe
      min_x = self.largeur_mur+min(arete[0][0],arete[1][0])*(self.largeur_chemin + self.largeur_mur)
      max_x = self.largeur_mur+max(arete[0][0],arete[1][0])*(self.largeur_chemin + self.largeur_mur)
      min_y = self.largeur_mur+min(arete[0][1],arete[1][1])*(self.largeur_chemin+ self.largeur_mur)
      max_y = self.largeur_mur+max(arete[0][1],arete[1][1])*(self.largeur_chemin + self.largeur_mur)
      self.img[min_x:max_x+self.largeur_chemin,min_y:max_y+self.largeur_chemin] = 255    #slincing => 255 représente un pixel blanc en convention noir et blanc
      
      self.matrice_resolution[min_x:max_x+self.largeur_chemin,min_y:max_y+self.largeur_chemin] = 300000000    #on append les chemins a un nb très grand (pour eviter de faire bug la résolution, qui cherche a faire minimiser ce nb, et donc pourrait se retrouver par erreur dans une partie non explorer par le pathfinding) pour la matrice de résolution du labyrinthe
    
    #transformation en image avec formarray
    self.im = Image.fromarray(self.img)
    
 

  def voisin_res(self,x,y):
     """recherche de voisin\n
     simplification du programme en ne prenant que le centre de chemin pour limiter les calculs (c'est donc pour ca que l'on utilise pas dejà la méthode voisin\n
     renvoie une liste de voisin en ne sortant pas du labyrinthe et en ne prenant pas un mur\n
     ATTENTION cette méthode marche seulement pour largeur_chemin impair et largeur mur=1 => concession a faire pour simplifier grandement les calculs du programme
     """
     voisins = [] #initialisation de la liste
     #on cherche les voisins en sautant (cad en prenant le centre du chemin + en parcourant le centre d'une "case") 
     for dx, dy in ((-(self.largeur_chemin//2)-1,0),((self.largeur_chemin//2)+1,0),(0,-(self.largeur_chemin//2)-1),(0,(self.largeur_chemin//2)+1)):
        if (x+dx >= 0) and (y+dy >= 0) and (x+dx < self.x_max) and (y+dy < self.y_max) and (self.matrice_resolution[x+dx][y+dy] != 0):         
          voisin = (x+dx,y+dy)
          voisins.append(voisin)
     return (voisins)
     

  def resolution(self):
    """pathfinding de resolution du labyrinthe\n
    on met un compteur en partant de l'entree jusqu'a arriver à la sortie => utilisation de la méthode voisin_res\n
    on s'arrete une fois que l'on a trouvé la sortie\n
     + tracer du chemin le plus court à partir de ce pathfinding
    renvoie les images du pathdinding et de la resolution (chemin le plus court tracé)""" 
    self.matrice_affichage=self.matrice_resolution.copy()   #copie de la matrice résolution pour la matrice affichage (car on affichera le pathding avec une régle de 3 pour une meilleure lisibilté)
    
    #---------------------------------------------------------pathfinding----------------------------------------------------#
    entree = (int(self.largeur_mur+(self.largeur_chemin//2)),int(self.largeur_mur+(self.largeur_chemin//2)))    #ne marche que pour des largeurs de chemin impair (si on veut que l'entrée soit centrée)
    self.matrice_resolution[entree[0]-(self.largeur_chemin//2):entree[0]+(self.largeur_chemin//2)+1,entree[1]-(self.largeur_chemin//2):entree[1]+(self.largeur_chemin//2)+1] = 2       #entree
    sortie = (int(self.x_max-(self.largeur_mur+(self.largeur_chemin//2)+1)), int(self.y_max-(self.largeur_mur+(self.largeur_chemin//2)+1)))  #ne marche que pour des largeurs de chemin impair (si on veut que la sortie soit centrée) 
    self.matrice_resolution[sortie[0]-(self.largeur_chemin//2):sortie[0]+(self.largeur_chemin//2)+1,sortie[1]-(self.largeur_chemin//2):sortie[1]+(self.largeur_chemin//2)+1] = 1        #sortie
    
    self.im = Image.fromarray(self.matrice_resolution)
    

    compteur_path = 3    #initialisation du compteur_path pour le pathfindig (3 veut dire chemin non explorer)
    compteur_affichage=40   #initiaatoin du compteur_affichage (40 pour avoir un gris foncé)
    
    a_explorer = [entree]   
    deja_explores = []
      
    #l'algo de pathfinding se fait sur le matrice_resolution mais l'affichage sur la matrice affichage
    temp = []
    while not a_explorer == [] and self.matrice_resolution[sortie[0]][sortie[1]] == 1:   #pour eviter de tout parcourir une fois que l'on a trouvé la sortie 
        
        case = a_explorer.pop(0)       
        deja_explores.append(case)
        for voisin in self.voisin_res(case[0],case[1]):
            if voisin not in deja_explores:
                
                self.matrice_resolution[voisin[0]-(self.largeur_chemin//2):voisin[0]+(self.largeur_chemin//2)+1,voisin[1]-(self.largeur_chemin//2):voisin[1]+(self.largeur_chemin//2)+1] = compteur_path
                self.matrice_affichage[voisin[0]-(self.largeur_chemin//2):voisin[0]+(self.largeur_chemin//2)+1,voisin[1]-(self.largeur_chemin//2):voisin[1]+(self.largeur_chemin//2)+1] = compteur_affichage
                temp.append(voisin)      
        
        compteur_path += 1    
        compteur_affichage += 1*(255/7000) #regle de 3 pour l'affichage (a adapter en fonction de la taille de la grid) => le produit en croix se fait en fonction de la taille du labyrinthe 
        a_explorer=temp
    
      #affichage avec la matrice affichage
    self.matrice_affichage[entree[0]-(self.largeur_chemin//2):entree[0]+(self.largeur_chemin//2)+1,entree[1]-(self.largeur_chemin//2):entree[1]+(self.largeur_chemin//2)+1] = 2       #entree    
    self.matrice_affichage[sortie[0]-(self.largeur_chemin//2):sortie[0]+(self.largeur_chemin//2)+1,sortie[1]-(self.largeur_chemin//2):sortie[1]+(self.largeur_chemin//2)+1] = 1        #sortie
    self.matrice_pathfinding=self.matrice_affichage.copy()     #copie pour sauvgarder la matrice pour pouvoir faire l'affichage du path uniquement
    self.im1 = Image.fromarray(self.matrice_affichage)    #image pathfinding sans chemin
    

    
    #----------------------------------------------resolution---------------------------------------------------------#
     
    chemin=[(sortie[0],sortie[1])]
    self.trace=[(sortie[0],sortie[1])]
    explorer=[(sortie[0],sortie[1])]  
   
    while (entree[0],entree[1]) not in chemin:
      
      minimum=self.matrice_resolution[sortie[0]][sortie[1]]+2
      case_chemin=chemin.pop(0)   #on enlève le premier terme de chemin (case a regarder en cours)

      for voisin in self.voisin_res(case_chemin[0], case_chemin[1]):    #on regarde les voisin de la case chemin et on prend son voisin min => on cherche a faire diminuer le compteur
          
          if self.matrice_resolution[voisin[0]][voisin[1]]<=minimum and voisin not in explorer:
            minimum=self.matrice_resolution[voisin[0]][voisin[1]]
            case_minimum=(voisin[0],voisin[1])
            explorer.append((voisin[0],voisin[1]))
         
          else:
            explorer.append((voisin[0],voisin[1]))

      chemin.append((case_minimum[0],case_minimum[1]))
      self.trace.append((case_minimum[0],case_minimum[1]))     
      self.matrice_affichage[case_minimum[0]-(self.largeur_chemin//2):case_minimum[0]+(self.largeur_chemin//2)+1, case_minimum[1]-(self.largeur_chemin//2):case_minimum[1]+(self.largeur_chemin//2)+1]=220  
      
   
      #affichage du chemin le plus court 
    self.im2 = Image.fromarray(self.matrice_affichage)  #image pathfinding avec chemin par dessus
  
  
    

