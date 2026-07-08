from datetime import datetime
from extensions import db


class Actualite(db.Model):
    __tablename__ = "actualites"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255)) # Ça reste l'image principale
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    
    # NOUVEAU : Lien vers les photos supplémentaires
    photos = db.relationship('ImageActualite', backref='actualite', lazy=True, cascade="all, delete-orphan")

# NOUVELLE TABLE pour les photos multiples
class ImageActualite(db.Model):
    __tablename__ = "images_actualites"

    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(255), nullable=False)
    actualite_id = db.Column(db.Integer, db.ForeignKey('actualites.id'), nullable=False)


class Activite(db.Model):
    __tablename__ = "activites"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    date_activite = db.Column(db.DateTime, default=datetime.utcnow)


class Formation(db.Model):
    __tablename__ = "formations"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    programme = db.Column(db.Text)


class Galerie(db.Model):
    __tablename__ = "galeries"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)


class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    sujet = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)


class Administrateur(db.Model):
    __tablename__ = "administrateurs"

    id = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)

class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(150), nullable=False)

    grade = db.Column(db.String(100), nullable=False)

    departement = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), nullable=False)

    domaine = db.Column(db.Text, nullable=False)

    photo = db.Column(db.String(255))
    
    biographie = db.Column(db.Text)

   