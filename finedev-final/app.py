from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuration directe
app.secret_key = "15Jlt@2001portefolio"  # Clé secrète Flask



@app.route('/converter')
def converter():
    return render_template('converter.html')
@app.route('/portfolio')
def portfolio():
    return render_template('index.html')  # Renvoie le même template que la route /
# Configuration Gmail
EMAIL_CONFIG = {
    'HOST': 'smtp.gmail.com',
    'PORT': 587,
    'USER': 'clovisfinka01@gmail.com',  # Votre email Gmail
    'PASSWORD': 'qswv fxbz sepn dzve'  # Mot de passe d'application
}

def check_email_config():
    """Vérifie que la configuration email est valide."""
    if not EMAIL_CONFIG['USER'] or not EMAIL_CONFIG['PASSWORD']:
        flash("Erreur: Configuration email manquante", 'danger')
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if not check_email_config():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'Configuration email manquante'})
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not all([name, email, message]):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'Tous les champs sont obligatoires'})
        flash('Tous les champs sont obligatoires', 'danger')
        return redirect(url_for('index'))

    try:
        # Création du message email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['USER']
        msg['To'] = EMAIL_CONFIG['USER']
        msg['Reply-To'] = email
        msg['Subject'] = f"Portfolio - Message de {name}"

        body = f"""
        Nouveau message depuis votre portfolio:

        Nom: {name}
        Email: {email}
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connexion et envoi via SMTP
        with smtplib.SMTP(EMAIL_CONFIG['HOST'], EMAIL_CONFIG['PORT'], timeout=10) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['USER'], EMAIL_CONFIG['PASSWORD'])
            server.send_message(msg)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'success', 'message': 'Message envoyé avec succès!'})
        flash('Message envoyé avec succès!', 'success')
    except smtplib.SMTPAuthenticationError:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'Identifiants Gmail incorrects'})
        flash("Erreur: Identifiants Gmail incorrects", 'danger')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': f"Erreur lors de l'envoi: {str(e)}"})
        flash(f"Erreur lors de l'envoi: {str(e)}", 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)