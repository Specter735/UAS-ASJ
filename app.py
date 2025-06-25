from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mountain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    location = db.Column(db.String(200))

    def __repr__(self):
        return f"Mountain('{self.name}', '{self.location}')"

with app.app_context():
    max_retries = 10
    retry_delay = 5 # detik

    for i in range(max_retries):
        try:
            print(f"Attempting to connect to database... (Attempt {i+1}/{max_retries})")
            db.drop_all()
            db.create_all()
            print("Database tables created/updated successfully.")
            break 
        except Exception as e:
            print(f"Database connection or creation failed: {e}")
            if i < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to database.")
                raise

# contoh data yg ada saat tampil nanti 
@app.before_request
def create_initial_data():
    if Mountain.query.count() == 0:
        initial_mountains = [
            Mountain(name="Gunung Rinjani",
                     description="Gunung berapi tertinggi kedua di Indonesia, terletak di Pulau Lombok, Nusa Tenggara Barat.",
                     image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Savanna_Mt._Rinjani_5.JPG/1280px-Savanna_Mt._Rinjani_5.JPG",
                     location="Lombok, Nusa Tenggara Barat"),
            Mountain(name="Gunung Bromo",
                     description="Bagian dari Pegunungan Tengger, terkenal dengan pemandangan matahari terbit dan kawahnya yang menakjubkan.",
                     image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Mount_Bromo_at_sunrise%2C_showing_its_volcanoes_and_Mount_Semeru_%28background%29.jpg/1280px-Mount_Bromo_at_sunrise%2C_showing_its_volcanoes_and_Mount_Semeru_%28background%29.jpg",
                     location="Probolinggo, Jawa Timur"),
            Mountain(name="Gunung Semeru",
                     description="Puncak tertinggi di Pulau Jawa, dikenal sebagai Mahameru. Gunung berapi aktif dan populer untuk pendakian.",
                     image_url="https://upload.wikimedia.org/wikipedia/commons/1/12/Semeru.jpg",
                     location="Malang, Jawa Timur"),
            Mountain(name="Gunung Merapi",
                     description="Salah satu gunung berapi teraktif di Indonesia, terletak di perbatasan Jawa Tengah dan Yogyakarta.",
                     image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Cahaya_Pertama_Menyinari_Puncak.jpg/960px-Cahaya_Pertama_Menyinari_Puncak.jpg",
                     location="Yogyakarta / Jawa Tengah"),
            Mountain(name="Gunung Merbabu",
                     description="Gunung ini memiliki ketinggian sekitar 3.145 meter di atas permukaan laut dan menawarkan pemandangan alam yang indah serta jalur pendakian yang populer.",
                     image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/MtmerbabuA45d.jpg/330px-MtmerbabuA45d.jpg",
                     location="Boyolali, Magelang / Jawa Tengah")
        ]
        for mountain in initial_mountains:
            db.session.add(mountain)
        db.session.commit()

@app.route('/')
def index():
    mountains = Mountain.query.all()
    return render_template('index.html', mountains=mountains)

@app.route('/add', methods=['GET', 'POST'])
def add_mountain():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        location = request.form['location']
        new_mountain = Mountain(name=name, description=description, image_url=image_url, location=location)
        db.session.add(new_mountain)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_mountain.html')

@app.route('/edit/<int:mountain_id>', methods=['GET', 'POST'])
def edit_mountain(mountain_id):
    mountain = Mountain.query.get_or_404(mountain_id)
    if request.method == 'POST':
        mountain.name = request.form['name']
        mountain.description = request.form['description']
        mountain.image_url = request.form['image_url']
        mountain.location = request.form['location']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_mountain.html', mountain=mountain)

@app.route('/delete/<int:mountain_id>', methods=['POST'])
def delete_mountain(mountain_id):
    mountain = Mountain.query.get_or_404(mountain_id)
    db.session.delete(mountain)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)