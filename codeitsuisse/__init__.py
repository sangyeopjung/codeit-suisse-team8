from flask import Flask;
app = Flask(__name__)

app.debug = True
import codeitsuisse.routes.square
import codeitsuisse.routes.tally_expense
import codeitsuisse.routes.airtrafficcontroller
import codeitsuisse.routes.images_gps
import codeitsuisse.routes.PrimeSum
import codeitsuisse.routes.tetris
import codeitsuisse.routes.sorting_game
<<<<<<< HEAD
import codeitsuisse.routes.skill_tree
=======
import codeitsuisse.routes.hotel
import codeitsuisse.routes.broadcaster
import codeitsuisse.routes.dinos
>>>>>>> 208f4c317f0a54a600e8c4532375e3e2e5013451
