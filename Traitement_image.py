#import des bibliothèques
from PIL import Image
import numpy as np

class Traitement_image:
    """classe qui s'occupe du traitement d'image\n 
    transforme un fichier_image (png) => matrice_resolution 30000000 sur les cases libres pour le bon fonctionnement du pathfinding (résolution)\n
    on utilise ensuite cette matrice pour faire la résolution d'un labyrinthe importé\n
    resolution de cette matrice pour trouver le chemin le plus court pour résoudre le labyrinthe\n"""
    
    def __init__(self,fichier): 
        """initialisation de la classe Rraitement_image : principales variables et lancement des méthodes de la classe"""
        self.largeur_mur=1
        self.largeur_chemin=15                                    
        self.fichier=fichier
        self.fichier_image_vers_matrice_resolution()    #convertion image => matrice
        self.resolution_image()    #résolution comme dans la classe Labyrinthe (on devait avoir cette méthode dans la meme classe)

    def fichier_image_vers_matrice_resolution(self):
        """fonction d'import\n
        transforme une image (png) en une matrice\n
        sera utile pour la résolution qui sera faite après\n"""
        #on met l'image dans une matrice avec la fonction np array
        self.img=np.array(self.fichier, dtype=np.uint8)        #pour les animations
        self.matrice_resolution=np.array(self.fichier, dtype=np.uint32)
        
        lignes, colonnes = np.shape(self.matrice_resolution)
        self.x_max=lignes
        self.y_max=colonnes
        for i in range(0,lignes):
            for j in range(0,colonnes):
                if (self.matrice_resolution[i,j] == 255):
                    self.matrice_resolution[i,j] = 300000000        
    
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
    
    def resolution_image(self):
        """nous avons repris la méthode de la classe Labyrinthe (méthode résolution) et nous l'avons adapté pour le faire pour une image importé\n
        en effet, il n'etait pas possible de tout regrouper dans une meme classe si on voulais utiliser seulement la fonction résolution de la classe labyrinthe sans créer d'objet labyrinthe"""
        
        self.matrice_affichage=self.matrice_resolution.copy()   #copie de la matrice résolution pour la matrice affichage (car on affichera le pathding avec une régle de 3 pour une meilleure lisibilté)
    
        #---------------------------------------------------------pathfinding----------------------------------------------------#
        entree = (int(self.largeur_mur+(self.largeur_chemin//2)),int(self.largeur_mur+(self.largeur_chemin//2)))    #ne marche que pour des largeurs de chemin impair (si on veut que l'entrée soit centrée)
        self.matrice_resolution[entree[0]-(self.largeur_chemin//2):entree[0]+(self.largeur_chemin//2)+1,entree[1]-(self.largeur_chemin//2):entree[1]+(self.largeur_chemin//2)+1] = 2       #entree
        sortie = (int(self.x_max-(self.largeur_mur+(self.largeur_chemin//2)+1)), int(self.y_max-(self.largeur_mur+(self.largeur_chemin//2)+1)))  #ne marche que pour des largeurs de chemin impair (si on veut que la sortie soit centrée) 
        self.matrice_resolution[sortie[0]-(self.largeur_chemin//2):sortie[0]+(self.largeur_chemin//2)+1,sortie[1]-(self.largeur_chemin//2):sortie[1]+(self.largeur_chemin//2)+1] = 1        #sortie
        
        self.im=Image.fromarray(self.matrice_resolution)


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
            compteur_affichage += 1*(255/6000)  #regle de 3 pour l'affichage (a adapter en fonction de la taille de la grid) => le produit en croix se fait en fonction de la taille du labyrinthe 
            a_explorer=temp
        
        #affichage avec la matrice affichage
        self.matrice_affichage[entree[0]-(self.largeur_chemin//2):entree[0]+(self.largeur_chemin//2)+1,entree[1]-(self.largeur_chemin//2):entree[1]+(self.largeur_chemin//2)+1] = 2       #entree    
        self.matrice_affichage[sortie[0]-(self.largeur_chemin//2):sortie[0]+(self.largeur_chemin//2)+1,sortie[1]-(self.largeur_chemin//2):sortie[1]+(self.largeur_chemin//2)+1] = 1        #sortie
        self.matrice_pathfinding=self.matrice_affichage.copy()
        self.im1 = Image.fromarray(self.matrice_affichage)      #image juste du pathfinding

        
        #----------------------------------------------resolution---------------------------------------------------------#
        
        chemin=[(sortie[0],sortie[1])]
        explorer=[(sortie[0],sortie[1])]  
        self.trace=[(sortie[0],sortie[1])]

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
        self.im2 = Image.fromarray(self.matrice_affichage)      #image du pathdinding + chemin par dessus
     


    



    




