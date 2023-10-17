# maze-generator-solver
Python Program to generate maze and solve them. I used Tkinter for the GUI. Generation using Kruskal algorithm's. 
Maze are saved with their image (png files).
Image processing using Pillow and numpy.

<br> 🎓 _**It was a school project, when we need to use Tkinter for the GUI and a complexe function in the code. Lots of options could have been added, but there was a deadline to finish the project**_  🎓 <br>

<br> 😓 _️**Sorry for my bad English, it's not my native language. I might do an English translation if many of you ask for it. The actual version is in French, but it's not very important to understand the code**_ 😓 <br>

This repository contains the following contents.

* The main program (**main.py**)
* Some saved maze (png files) which you can use as an example
* 3 classes (**Affichage.py** for Tkinter, **Labyrinthe.py** to create and solve the maze, **Traitement_image.py** for image processing and solving a saved maze (using his png file)

# Requirements
* Tkinter 8.5 or Later (normally already installed with python)
* Pillow 10.0.0 or Later
* Numpy 1.24.2 or Later

You can do this command : <pre> pip install -r requirements.txt </pre> to install the libraries more easily

# Demo 
You need to run the _**main.py**_ file in your Python environment (for example VScode, Pycharm, Spyder...)

# Directory
<pre>
│  main.py
│  Affichage.py
│  Labyrinthe.py
│  Traitement_image.py  
│
│  puzzle-1.png  
│  puzzle-2.png  
│  puzzle-3.png  
│  puzzle-4.png  
│  puzzle-5.png  
│  puzzle-6.png  
</pre> 

### main.py
This is the main program. Access to a menu with multiple option. See tutorial (below) for more information

### Affichage.py 
This is the program for Tkinter : creation of the window, launch of other class or function.

### Labyrinthe.py 
This is the program to generate a maze with Kruskal algorithm's (up to a size of 50x50) and to solve the maze (randomly) by displaying the shortest path between the entrance (in the upper left corner) and the exit of the maze (in the lower right corner).
It also allows to display the pathfinding (this allows to see the boxes visited during the resolution with a gradient showing the order of discovery).

#### Kruskal algorithm's 
The principle of Kruskal's algorithm for randomly generating a "perfect" maze is simple. Each cell is assigned a unique ID, in a maze filled with walls. 

This step happens in the initialization of the class, with the use of enumerate during of the creation of the dictionary representing the labyrinth. 

The algorithm will then randomly choose a wall to "break" and will merge the cells thus linked by the same identifier. We use the neighbors method to pick an edge at random from a list of edges, removing it from this list to avoid repeating the same edge twice and thus create a loop infinite. In our Maze class, we use the method find_id to get the id of each cell and union to put the same identifier to all the cells connected between them.

The algorithm will seek to break a wall randomly until all the cells have the same identifier. When all the cells have the same identifier, the created maze will be "perfect" and Kruskal's algorithm will finish, by returning to us the dictionary representing the labyrinth having as key the coordinates of the vertex, and for value a tuple including the weight (the Kruskal identifier) ​​and the list of connected cells (where there is no wall between).

The algorithm of kruskal requires a memory space proportional to the size of the labyrinthe

#### Example in the case of a small 5x4 maze

Because a drawing is better than a long speech...

![Yl_maze_ani_algo1](https://github.com/enorart/maze-generator-solver/assets/135878234/42f53a20-5358-4cc2-8e0c-fcec15904996)

### Traitement_image.py
Image processing using numpy and Pillow. Solve the maze (imported using an import mode of the program) by displaying the shortest path between the entrance (in the upper left corner) and the exit of the maze (in the lower right corner).
It also allows to display the pathfinding (this allows to see the boxes visited during the resolution with a gradient showing the order of discovery). 

<img width="464" alt="image" src="https://github.com/enorart/maze-generator-solver/assets/135878234/e1e0d660-f4a1-4a76-8129-1eeed3041a64">

# Tutorial 
Once the program is launched (with the main.py file), a first tkinter interface opens and you can use the RadioButton to choose the mode: generate a random maze or import a maze image

<img width="222" alt="Capture d’écran 2023-07-23 183802" src="https://github.com/enorart/maze-generator-solver/assets/135878234/749dd1c1-b42d-4806-9b09-ba78c0527447">

If you choose to generate a random maze, you can choose his size :

<img width="298" alt="Capture d’écran 2023-07-23 183727" src="https://github.com/enorart/maze-generator-solver/assets/135878234/3025b1a3-2fa9-45a7-9926-793a0c9697e5">

Then just press the blue button "Afficher Labyrinthe" to display the maze in a second tkinter window.
You can press "Quitter l'application" to exit the program cleanly.
You can press "Aide" for a small program tutorial (in French sorry 😓)

<img width="600" alt="Capture d’écran 2023-07-23 183058" src="https://github.com/enorart/maze-generator-solver/assets/135878234/e607c2a1-8dbd-414c-84fd-e662c12cedae">

In this new window (after clicking on "Afficher Labyrinthe") you can:

-click on "Resolution" to display the resolution of the maze (the path)

-click on "Pathfinding" to display the pathfinding of the maze

-click on "Menu" to return to the main menu and therefore close this window

-click on "Enregistrer" to take a screenshot of the maze (to be able to reuse it afterwards for example)

Here are some screenshots : 
* with the pathfinding...
<img width="600" alt="Capture d’écran 2023-07-23 183541" src="https://github.com/enorart/maze-generator-solver/assets/135878234/50da2779-698f-466e-a6dc-166902f396cc">

* with the resolution...
<img width="601" alt="Capture d’écran 2023-07-23 183142" src="https://github.com/enorart/maze-generator-solver/assets/135878234/920f1cb1-b85d-4686-8fc7-1fb288dc86d5">

* with the resolution and the pathfinding...
<img width="601" alt="Capture d’écran 2023-07-23 183641" src="https://github.com/enorart/maze-generator-solver/assets/135878234/9bf3bd81-60dc-45c3-beb1-d40bde316846">

# Discussion
Since the project had a deadline, it is not perfect and there were concessions to be made. 
This program only supports images with 1 pixel wall widths and odd pixel path widths. This has made it possible to greatly reduce the computing power because we "jump" pixels by only passing each time through the middle of each box
The images offered as examples correspond to these criteria.

# Reference
* [Pillow](https://pypi.org/project/Pillow/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)

# Author
Eno [https://github.com/enorart](https://github.com/enorart)

# License
maze-generator-solver is under [Apache v2 license](LICENSE)
  
