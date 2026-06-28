from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def home():
    return render_template('index.html', active='home')

@pages_bp.route('/about')
def about():
    return render_template('about.html', active='about')

@pages_bp.route('/choirs')
def choirs():
    return render_template('choirs.html', active='choirs')

@pages_bp.route('/gallery')
def gallery():
    return render_template('gallery.html', active='gallery')
