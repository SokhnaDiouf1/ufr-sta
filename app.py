from flask import Flask, render_template, request, session, redirect, url_for, flash
from extensions import db
import os
from models import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "ufrsta_secret_key"

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "instance", "ufr_sta.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuration des images
app.config["UPLOAD_ACTUALITES"] = "static/images/actualites"
app.config["UPLOAD_ACTIVITES"] = "static/images/activites"
app.config["UPLOAD_FOLDER_ENSEIGNANTS"] = "static/images/enseignants"
app.config["UPLOAD_GALERIE"] = "static/images/galerie"


db.init_app(app)

with app.app_context():
    from models import *
    db.create_all()

    if Administrateur.query.first() is None:
        admin = Administrateur(
            nom_utilisateur="admin",
            mot_de_passe="admin123"
        )
        db.session.add(admin)
        db.session.commit()

# ---------------- ADMIN ----------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Administrateur.query.filter_by(
            nom_utilisateur=username,
            mot_de_passe=password
        ).first()

        if admin:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    nb_actualites = Actualite.query.count()
    nb_activites = Activite.query.count()
    nb_formations = Formation.query.count()
    nb_photos = Galerie.query.count()
    nb_enseignants = Enseignant.query.count()

    return render_template(
        'admin/dashboard.html',
        nb_actualites=nb_actualites,
        nb_activites=nb_activites,
        nb_formations=nb_formations,
        nb_photos=nb_photos,
        nb_enseignants=nb_enseignants
        
    )

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


@app.route('/admin/actualites', methods=['GET', 'POST'])
def admin_actualites():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']

        fichier = request.files['image']

        nom_image = None

        if fichier and fichier.filename != "":
            nom_image = secure_filename(fichier.filename)
            fichier.save(
                os.path.join(app.config["UPLOAD_ACTUALITES"], nom_image)
            )

        new = Actualite(titre=titre, contenu=contenu, image=nom_image)
        db.session.add(new)
        db.session.commit()

        flash("Actualité ajoutée avec succès.", "success")

        return redirect(url_for('admin_actualites'))

    actualites = Actualite.query.all()
    return render_template('admin/actualites.html', actualites=actualites)

@app.route('/admin/activites', methods=['GET', 'POST'])
def admin_activites():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']

        fichier = request.files['image']

        nom_image = None

        if fichier and fichier.filename != "":
            nom_image = secure_filename(fichier.filename)
            fichier.save(
                os.path.join(app.config["UPLOAD_ACTIVITES"], nom_image)
            )

        activite = Activite(
            titre=titre,
            description=description,
            image=nom_image
        )

        db.session.add(activite)
        db.session.commit()
        flash("Activité ajoutée avec succès.", "success")

        return redirect(url_for('admin_activites'))

    activites = Activite.query.order_by(
        Activite.date_activite.desc()
    ).all()

    return render_template(
        'admin/activites.html',
        activites=activites
    )


@app.route('/admin/galerie', methods=['GET', 'POST'])
def admin_galerie():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']

        fichier = request.files['image']

        nom_image = None

        if fichier and fichier.filename != "":
            nom_image = secure_filename(fichier.filename)

            fichier.save(
                os.path.join(
                    app.config["UPLOAD_GALERIE"],
                    nom_image
                )
            )

        photo = Galerie(
            titre=titre,
            description=description,
            image=nom_image
        )

        db.session.add(photo)
        db.session.commit()
        flash("Photo ajoutée avec succès.", "success")

        return redirect(url_for('admin_galerie'))

    photos = Galerie.query.all()

    return render_template(
        'admin/galerie.html',
        photos=photos
    )

@app.route('/admin/galerie/supprimer/<int:id>')
def supprimer_photo(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    photo = Galerie.query.get_or_404(id)

    # Supprimer le fichier image du dossier
    chemin = os.path.join(app.config["UPLOAD_GALERIE"], photo.image)

    if os.path.exists(chemin):
        os.remove(chemin)

    # Supprimer l'enregistrement de la base
    db.session.delete(photo)
    db.session.commit()
    flash("Photo supprimée avec succès.", "success")

    return redirect(url_for('admin_galerie'))

@app.route('/admin/formations', methods=['GET', 'POST'])
def admin_formations():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        programme = request.form['programme']

        formation = Formation(
            nom=nom,
            description=description,
            programme=programme
        )

        db.session.add(formation)
        db.session.commit()
        flash("Formation ajoutée avec succès.", "success")

        return redirect(url_for('admin_formations'))

    formations = Formation.query.all()

    return render_template(
        'admin/formations.html',
        formations=formations
    )

@app.route('/admin/formations/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_formation(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    formation = Formation.query.get_or_404(id)

    if request.method == 'POST':
        formation.nom = request.form['nom']
        formation.description = request.form['description']
        formation.programme = request.form['programme']

        db.session.commit()
        flash("Formation modifiée avec succès.", "success")

        return redirect(url_for('admin_formations'))

    return render_template(
        'admin/modifier_formation.html',
        formation=formation
    )

@app.route('/admin/formations/supprimer/<int:id>')
def supprimer_formation(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    formation = Formation.query.get_or_404(id)

    db.session.delete(formation)
    db.session.commit()
    flash("Formation supprimée avec succès.", "success")

    return redirect(url_for('admin_formations'))

@app.route('/admin/actualites/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_actualite(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    actualite = Actualite.query.get_or_404(id)

    if request.method == 'POST':
        actualite.titre = request.form['titre']
        actualite.contenu = request.form['contenu']

        db.session.commit()
        flash("Actualité modifiée avec succès.", "success")

        return redirect(url_for('admin_actualites'))

    return render_template(
        'admin/modifier_actualite.html',
        actualite=actualite
    )

@app.route('/admin/actualites/supprimer/<int:id>')
def supprimer_actualite(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    actualite = Actualite.query.get_or_404(id)

    db.session.delete(actualite)
    db.session.commit()
    flash("Actualité supprimée avec succès.", "success")

    return redirect(url_for('admin_actualites'))

@app.route('/admin/activites/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_activite(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    activite = Activite.query.get_or_404(id)

    if request.method == 'POST':
        activite.titre = request.form['titre']
        activite.description = request.form['description']

        db.session.commit()
        flash("Activité modifiée avec succès.", "success")

        return redirect(url_for('admin_activites'))

    return render_template(
        'admin/modifier_activite.html',
        activite=activite
    )

@app.route('/admin/activites/supprimer/<int:id>')
def supprimer_activite(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    activite = Activite.query.get_or_404(id)

    db.session.delete(activite)
    db.session.commit()
    flash("Activité supprimée avec succès.", "success")

    return redirect(url_for('admin_activites'))

@app.route('/admin/enseignants', methods=['GET', 'POST'])
def admin_enseignants():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        nom = request.form['nom']
        grade = request.form['grade']
        departement = request.form['departement']
        email = request.form['email']
        domaine = request.form['domaine']
        biographie = request.form['biographie']
        

        fichier = request.files['photo']

        nom_photo = None

        if fichier and fichier.filename != "":
            nom_photo = secure_filename(fichier.filename)
            fichier.save(
                os.path.join(
                    "static/images/enseignants",
                    nom_photo
                )
            )

        enseignant = Enseignant(
            nom=nom,
            grade=grade,
            departement=departement,
            email=email,
            domaine=domaine,
            biographie=biographie,
            photo=nom_photo
        )

        db.session.add(enseignant)
        db.session.commit()

        return redirect(url_for('admin_enseignants'))

    enseignants = Enseignant.query.all()

    return render_template(
        'admin/enseignants.html',
        enseignants=enseignants
    )

@app.route('/admin/enseignants/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_enseignant(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    enseignant = Enseignant.query.get_or_404(id)

    if request.method == 'POST':
        enseignant.nom = request.form['nom']
        enseignant.grade = request.form['grade']
        enseignant.departement = request.form['departement']
        enseignant.email = request.form['email']
        enseignant.domaine = request.form['domaine']
        enseignant.biographie = request.form['biographie']
       

        fichier = request.files['photo']

        if fichier and fichier.filename != "":
            nom_photo = secure_filename(fichier.filename)

            fichier.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER_ENSEIGNANTS"],
                    nom_photo
                )
            )

            enseignant.photo = nom_photo

        db.session.commit()

        return redirect(url_for('admin_enseignants'))

    return render_template(
        'admin/modifier_enseignant.html',
        enseignant=enseignant
    )

@app.route('/admin/enseignants/supprimer/<int:id>')
def supprimer_enseignant(id):

    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    enseignant = Enseignant.query.get_or_404(id)

    db.session.delete(enseignant)
    db.session.commit()

    return redirect(url_for('admin_enseignants'))
# ---------------- PAGES PUBLIC ----------------

@app.route('/')
def accueil():
    actualites = Actualite.query.order_by(
        Actualite.date_publication.desc()
    ).limit(5).all()

    return render_template(
        'index.html',
        actualites=actualites
    )

@app.route('/departements')
def departements():
    return render_template('departements.html')

@app.route('/formations')
def formations():
    formations = Formation.query.all()

    return render_template(
        'formations.html',
        formations=formations
    )

@app.route('/actualites')
def actualites():
    actualites = Actualite.query.order_by(
        Actualite.date_publication.desc()
    ).all()

    return render_template(
        'actualites.html',
        actualites=actualites
    )

@app.route('/activites')
def activites():
    activites = Activite.query.order_by(
        Activite.date_activite.desc()
    ).all()

    return render_template(
        'activites.html',
        activites=activites
    )

@app.route('/galerie')
def galerie():
    photos = Galerie.query.all()

    return render_template(
        'galerie.html',
        photos=photos
    )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/recherche")
def recherche():

    mot = request.args.get("q", "").strip()

    actualites = Actualite.query.filter(
        (Actualite.titre.contains(mot)) |
        (Actualite.contenu.contains(mot))
    ).all()

    activites = Activite.query.filter(
        (Activite.titre.contains(mot)) |
        (Activite.description.contains(mot))
    ).all()

    pages = [

        {
            "titre": "Département MIM",
            "description": "Mathématiques, Informatique et Modélisation",
            "url": url_for("departements") + "#mim"
        },

        {
            "titre": "Département SMU",
            "description": "Sciences de la Matière et de l'Univers",
            "url": url_for("departements") + "#smu"
        },

        {
            "titre": "Formation MPI",
            "description": "Mathématiques, Physique et Informatique",
            "url": url_for("formations")
        },

        {
            "titre": "Formation MIASS",
            "description": "Mathématiques et Informatique Appliquées aux Sciences Sociales",
            "url": url_for("formations")
        },

        {
            "titre": "Galerie",
            "description": "Toutes les photos des activités de l'UFR STA",
            "url": url_for("galerie")
        },

        {
            "titre": "Contact",
            "description": "Contacter l'UFR STA",
            "url": url_for("contact")
        }

    ]

    pages_resultats = []

    for page in pages:

        if mot.lower() in page["titre"].lower() or mot.lower() in page["description"].lower():

            pages_resultats.append(page)

    return render_template(
        "recherche.html",
        mot=mot,
        actualites=actualites,
        activites=activites,
        pages=pages_resultats
    )

@app.route('/enseignants')
def enseignants():

    enseignants = Enseignant.query.order_by(Enseignant.nom).all()

    return render_template(
        'enseignants.html',
        enseignants=enseignants
    )
    
@app.route('/enseignant/<int:id>')
def profil_enseignant(id):

    enseignant = Enseignant.query.get_or_404(id)

    return render_template(
        "profil_enseignant.html",
        enseignant=enseignant
    )

if __name__ == "__main__":
    app.run(debug=True)