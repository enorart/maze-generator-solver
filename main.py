#import de la classe Fenetre 
from Affichage import Fenetre

#boucle lançant le programme
if __name__ == "__main__":
    fen = Fenetre()              #création de l'objet fenetre
    fen.fen_princ.mainloop()     #boucle infinie pour tkinter
    
