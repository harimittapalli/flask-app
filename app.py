from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import time

def chart():
    labels = ["OK", "WARNING", "CRIT", "UNKNOWN", "PENDING"]
    values = [103, 19, 21, 7, 6]
    colors = ["#008000", "#FFFF00", "#800000", "#FFA500", "#808080"]
    return render_template('chart.html', set=zip(values, labels, colors), set2=zip(values, labels, colors))

