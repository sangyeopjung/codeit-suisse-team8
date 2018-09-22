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
import codeitsuisse.routes.hotel
