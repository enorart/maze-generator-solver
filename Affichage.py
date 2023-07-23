import tkinter as tk        #fenetre/interface graphique
from tkinter import filedialog      #pour aller chercher les images dans notre répertoire
from PIL import Image, ImageTk      #pour gérer l'import d'image, car tkinter ne support que le GIF de base
from Labyrinthe import Labyrinthe    #import de la classe Labyrinthe pour la génération et résolution du labyrinthe
from Traitement_image import Traitement_image #import de la classe Traitement_image s'occupant de transformer en matrice une image et d'y resoudre la labyrinthe associé

class Fenetre():    #classe représentant la fenetre tkinter
    """Interface (GUI) de notre programme\n
    l'utilisateur peut importer ou générer un labyrinthe\n
    le programme pourra le résoudre\n
    plusieurs modes et options disponibles\n
    animation du chemin trouvé\n"""
    
    def __init__(self):
        """initialisation de notre classe labyrinthe\n
        appel de ses méthodes\n"""
        
        #création de la fenetre principale       
        self.fen_princ = tk.Tk()
        self.fen_princ.title("Menu")        #la première fenetre est le menu du jeu : importer une image => choix de l'image 
                                                #générer aléatoirement : choix de la taille : longueur et largeur avec des scales
        self.fen_princ.geometry("300x150")      #largeur x hauteur
        self.fen_princ.resizable(height=False,width=False)      #fenetre non resizable
        
        self.fen_graph=None     #initialisation des fenetres secondaires
        self.fen_choix = None
       
        self.type_choix=0       #variable pour faire la distintion de cas (labyrinthe importé ou généré) pour la résolution
        
        #appel de la méthode des widgets
        self.creer_widgets(self.fen_princ)    
        
    def creer_widgets(self,root):
        """création des widgets de notre programme : fenetre principale"""
        #-------------------------------------------texte-------------------------------------------------#
        self.texte1 = tk.Label(root, text ="Choisir mode :",font='Helvetica 11 bold')
        self.texte1.pack()    #placement des widgets avec la méthode pack
        
        #-----------------radio button pour le choix du mode : importer ou générer------------------------#
        self.v = tk.IntVar()        #variable du radio button
        self.v.set(1)               #préselection sur importer
        #importer le labyrinthe (choisir une image de labyrinthe)
        self.check1 = tk.Radiobutton(root, text="Importer labyrinthe", padx=20, variable=self.v,value=1)
        self.check1.pack()
        #gérérer le labyrinthe 
        self.check2 = tk.Radiobutton(root,text = "Générer aléatoirement", padx=20, variable=self.v, value=2)
        self.check2.bind('<Button-1>',self.choix_taille)      #ouverture des scales pour le choix de la taille du labyrinthe
        self.check2.pack() 
        
        #------------bouton pour afficher le labyrinthe => va chercher l'image et créer le canvas-----------#
        self.bouton1 = tk.Button(root, text = "Afficher Labyrinthe",bg="lightblue")
        self.bouton1.pack(fill="x")
        self.bouton1.bind("<Button-1>",self.ouvrir)
      
        #-----------------------------bouton pour obtenir de l'aide/tutoriel--------------------------------------#
        self.bouton_aide = tk.Button(root, text = "Aide", bg = "lightgreen")
        self.bouton_aide.pack(fill = "x")
        self.bouton_aide.bind("<Button-1>", self.aide) 
           
        #-----------------------------bouton pour quitter le programme---------------------------------------#
        self.bouton_quitter=tk.Button(root,text="Quitter l'application", bg="lightyellow")
        self.bouton_quitter.pack(fill="x")
        self.bouton_quitter.bind("<Button-1>", self.quitter)
    
    #________________________PRINCIPAUX CALLBACK DES BOUTONS______________________#
    def quitter(self,event):
        """quitter la fenetre principale du programme"""
        self.fen_princ.destroy() 

    def aide(self,event):
        """Ouvre une nouvelle fenêtre informant l'utilisateur du fonctionnement du programme/Tutoriel"""
        self.fen_aide = tk.Tk()
        self.fen_aide.title("Aide")

        self.texte_aide = tk.Label(self.fen_aide, text = "Dans le menu principal, vos options sont : \n - D'importer un labyrinthe enregistré au préalable à l'aide de son image \n - De générer un labyrinthe de manière aléatoire, en renseignant sa hauteur et sa largeur (nombre à choisir entre 5 et 50) \n - De quitter la fenêtre (et donc de fermer l'application) \n \n L'option afficher le labyrinthe vous permettra de visualiser le type de labyrinthe que vous avez choisi au préalable. Une seconde fenêtre s'ouvre. Dans celle-ci, vous avez le choix : \n - D'afficher la résolution du labyrinthe avec le bouton 'resolution' \n - D'afficher le coloriage du labyrinthe, qui sert à identifier la distance de chaque case à l'entrée, avec le bouton 'pathfinding' \n - D'enregistrer l'image du labyrinthe, pour éventuellement l'importer plus tard, avec le bouton 'enregistrer' \n - De retourner au menu principal avec le bouton 'menu'\n \n L'entrée du labyrinthe se trouve dans le coin supérieur gauche et la sortie du labyrinthe se trouve dans le coin inférieur droit \n\n")
        self.texte_aide.pack()

        self.bouton_quitter_aide = tk.Button(self.fen_aide, text = "Retour au menu", bg = "lightyellow")    #retour au menu principal
        self.bouton_quitter_aide.bind("<Button-1>", self.quitter_aide)
        self.bouton_quitter_aide.pack(fill = "x", side = "bottom")
    
    def quitter_aide(self, event):
        """retourner au menu principal"""
        self.fen_aide.destroy()    #destruction de la fenetre 
        self.fen_aide = None
  
    def ouvrir(self,event):
        """création du canvas et mise ne place de l'image\n
        distinction de cas si importer ou générer\n
        ATTENTION ne marche que sur windows (a cause du \ et /)"""
        
        if self.v.get()==1:     #mode importer une image
            #filedialog pour aller cherche l'image dans notre répertoire 
            ouvrir_fichier = filedialog.askopenfilename(title = "ouvrir l'image du labyrinthe",defaultextension = ".png",filetypes = (("png files","*.png"),("all files","*.*")),initialdir = "/")
            self.image_pil = Image.open(ouvrir_fichier)
            self.photo_tk = ImageTk.PhotoImage(self.image_pil)
            self.type_choix=1
        else:       #mode générer un labyrinthe
            self.type_choix=2
            
        if (self.fen_graph==None):
            self.fen_graph=tk.Toplevel(self.fen_princ)
            self.fen_graph.title("Labyrinthe")
            self.fen_graph.resizable(height=False,width=False)
            self.fen_graph.canevas=tk.Canvas(self.fen_graph,bg="white", height=self.photo_tk.height(), width=self.photo_tk.width())
            self.image_on_canvas=self.fen_graph.canevas.create_image(0,0,anchor=tk.NW, image=self.photo_tk)
            self.fen_graph.canevas.pack()

            self.Bouton_resoudre=tk.Button(self.fen_graph,text="Resolution")        #pour lancer la résolution du labyrinthe
            self.Bouton_resoudre.pack(side=tk.LEFT,padx=10, pady=10)
            self.Bouton_resoudre.bind("<Button-1>",self.resoudre_labyrinthe)

            self.Bouton_pathfinding=tk.Button(self.fen_graph,text="Pathfiding")        #pour lancer le pathfinding du labyrinthe
            self.Bouton_pathfinding.pack(side=tk.LEFT,padx=10, pady=10)
            self.Bouton_pathfinding.bind("<Button-1>",self.pathfinding)

            self.Bouton_menu=tk.Button(self.fen_graph,text="Menu")      #pour revenir au menu => choisir une autre image ou générer un labyrinthe
            self.Bouton_menu.pack(side=tk.RIGHT,padx=10,pady=10)
            self.Bouton_menu.bind("<Button-1>",self.retour_menu)
            
            self.Bouton_enregistrer=tk.Button(self.fen_graph,text="Enregistrer")        #pour enregister l'image du labyrinthe => comme une capture d'écran
            self.Bouton_enregistrer.pack(side=tk.RIGHT,padx=10,pady=10)
            self.Bouton_enregistrer.bind('<Button-1>',self.enregistrer_lab)
    
    def pathfinding(self,event):        
        """affichage du pathfinding sur notre image de labyrinthe \n
        appel de la méthode résolution de la classe Labyrinthe \n 
        et de la classe Traitement_image"""  
        if self.type_choix==2:      #cas labyrinthe générer aleatoirement
            self.lab.resolution() 
            self.image_pil=self.lab.im1
            self.lab.img=self.lab.matrice_pathfinding
            self.image_pil=self.image_pil.convert("L")    #conversion de l'image sinon problème d'affichage lors de l'enregistrement 
            self.image_actuelle=ImageTk.PhotoImage(self.lab.im1)
            self.fen_graph.canevas.itemconfig(self.image_on_canvas,image=self.image_actuelle)
           
            
        else:       #cas résolution image importé
            self.matrice=Traitement_image(self.image_pil)
            self.image_pil=self.matrice.im1
            self.matrice.img=self.matrice.matrice_pathfinding
            self.image_pil=self.image_pil.convert("L")
            self.image_actuelle=ImageTk.PhotoImage(self.matrice.im1)
            self.fen_graph.canevas.itemconfig(self.image_on_canvas, image=self.image_actuelle)
        
    
    def enregistrer_lab(self,event):
        """enregistrement de l'image du labyrinthe, a n'importe quel état de résolution \n
        comme une capture d'écran de l'image du labyrinthe \n"""
        
        self.adresse_photo = filedialog.asksaveasfilename(title = "enregistrer l'image du labyrinthe aléatoire",defaultextension = ".png",filetypes = (("png files","*.png"),("all files","*.*")),initialdir = "/")
        self.image_pil=self.image_pil.convert("L")       #il est nécessaire de convertir la photo en mode L sinon on a des problèmes d'affichage (noir et blanc tout ou rien)
        self.image_pil.save(self.adresse_photo)     #enregistrement de l'image à l'endroit souhaité

            
    def retour_menu(self,event):
        """retourner au menu principal pour choisir un autre labyrinthe ou en générer un"""
        self.fen_graph.destroy()
        self.fen_graph=None

    def choix_taille(self,event):
        """fenetre qui s'ouvre pour mettre deux scales pour choisir la taille du labyrinthe générer aléatoirement"""
        
        #enlever la fenetre toplevel existante si elle existe déjà
        if (self.fen_choix != None) :
            self.fen_choix.destroy()
        
        self.fen_choix = tk.Toplevel(self.fen_princ)
        self.fen_choix.geometry("400x300")
        self.taille_x = tk.IntVar()
        self.taille_y = tk.IntVar()
        
        #ccale pour choisir la taille du labyrinthe généré
        self.scale1 = tk.Scale(self.fen_choix, orient='horizontal',
        from_= 5, to = 50, resolution=1,
        tickinterval=5, label='Hauteur du labyrinthe', variable = self.taille_x)
        self.scale1.pack(fill = 'x')
        
        self.scale2 = tk.Scale(self.fen_choix, orient='horizontal',
        from_= 5, to = 50, resolution=1,
        tickinterval=5, label='Largeur du labyrinthe',variable = self.taille_y)
        self.scale2.pack(fill = 'x')
        self.bouton10 = tk.Button(self.fen_choix,text = "Valider",height = 1,width = 15)
        self.bouton10.pack()
        self.bouton10.bind('<Button-1>', self.generation_aleatoire)
        
        #gérer la bonne sélection des radios button
        self.check1.deselect()
        self.check2.select()
       
    #_____________________________________GENERATION ALEATOIRE______________________________________#   
    def generation_aleatoire(self,event):
        """génération aléatoire du labyrinthe \n
        appel de la classe Labyrinthe \n"""
        taille_x = self.taille_x.get()
        taille_y = self.taille_y.get()
        self.lab = Labyrinthe(taille_x,taille_y,15,1)       #création de l'objet Labyrinthe de la taille souhaité
        self.lab.kruskal() #appel de la génération avec la classe Labyrinthe
        self.lab.affichage()      #récupération de l'adresse de la photo avec la classe Labyrinthe      
        self.photo_tk=ImageTk.PhotoImage(self.lab.im)
        self.image_pil=self.lab.im
        self.fen_choix.destroy()
    #________________________________________ANIMATION TIMER_______________________________________#
    def animation_gene_aleatoire(self):         #cas labyrinthe généré aléatoirememnt
        """timer pour gerer l'animation du chemin de l'entrée vers la sortie du labyrinthe \n
        cas labyrinthe générer aléatoirement"""
        if self.compteur<len(self.lab.trace):  
           self.lab.img[self.lab.trace[len(self.lab.trace)-1-self.compteur][0]-(self.lab.largeur_chemin//2):self.lab.trace[len(self.lab.trace)-1-self.compteur][0]+(self.lab.largeur_chemin//2)+1,self.lab.trace[len(self.lab.trace)-1-self.compteur][1]-(self.lab.largeur_chemin//2):self.lab.trace[len(self.lab.trace)-1-self.compteur][1]+(self.lab.largeur_chemin//2)+1]=200   
           self.compteur+=1
           self.image_pil=Image.fromarray(self.lab.img)
           self.image_actuelle=ImageTk.PhotoImage(self.image_pil)
           self.fen_graph.canevas.itemconfig(self.image_on_canvas,image=self.image_actuelle)
           self.fen_graph.canevas.after(15,self.animation_gene_aleatoire)    #15ms entre chaque animation
      
    def animation_import(self):     #cas labyrinthe importé
        """timer pour gerer l'animation du chemin de l'entrée vers la sortie du labyrinthe \n
        cas labyrinthe importé à l'aide d'une image"""
        if self.compteur<len(self.matrice.trace):  
           self.matrice.img[self.matrice.trace[len(self.matrice.trace)-1-self.compteur][0]-(self.matrice.largeur_chemin//2):self.matrice.trace[len(self.matrice.trace)-1-self.compteur][0]+(self.matrice.largeur_chemin//2)+1,self.matrice.trace[len(self.matrice.trace)-1-self.compteur][1]-(self.matrice.largeur_chemin//2):self.matrice.trace[len(self.matrice.trace)-1-self.compteur][1]+(self.matrice.largeur_chemin//2)+1]=200   
           self.compteur+=1
           self.image_pil=Image.fromarray(self.matrice.img)
           self.image_actuelle=ImageTk.PhotoImage(self.image_pil)
           self.fen_graph.canevas.itemconfig(self.image_on_canvas,image=self.image_actuelle)
           self.fen_graph.canevas.after(15,self.animation_import)    #15ms entre chaque animation
         
    #____________________________________________RESOLUTION__________________________________________#
    def resoudre_labyrinthe(self,event):  
        """resolution du labyrinthe\n
        affichage du chemin et lancement des animations\n"""
        if self.type_choix==2:      #cas labyrinthe générer aleatoirement
            self.lab.resolution()       #appel de la fonction resolution du labyrinthe
            self.image_actuelle=ImageTk.PhotoImage(self.lab.im)
            self.image_pil=self.lab.im
            self.image_pil=self.image_pil.convert("L")
            self.fen_graph.canevas.itemconfig(self.image_on_canvas,image=self.image_actuelle)
            self.compteur=0
            self.animation_gene_aleatoire()
            

        else:       #cas résolution image importé
            self.matrice=Traitement_image(self.image_pil)
            self.matrice.resolution_image()     #appel de la fonction resolution lors d'un labyrinthe importé
            self.image_actuelle=ImageTk.PhotoImage(self.matrice.im)
            self.image_pil=self.matrice.im
            self.image_pil=self.image_pil.convert("L")
            self.fen_graph.canevas.itemconfig(self.image_on_canvas, image=self.image_actuelle)
            self.compteur=0
            self.animation_import()
