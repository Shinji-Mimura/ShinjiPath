from app import app, db

def create_db():
    with app.app_context():
        from app.models import User

        db.create_all()

        # Verifica se os usuários não existem no banco de dados antes de criá-los
        if not User.query.filter_by(email='admin@wicked.com').first():
            admin_user = User(email='admin@wicked.com', password='822407b89121ccef03d7ade8de73dc38c745f7cdc18013babc1fc8d0ec7921f3')
            db.session.add(admin_user)

        if not User.query.filter_by(email='contato@wicked.com').first():
            contato_user = User(email='contato@wicked.com', password='senha_contato')
            db.session.add(contato_user)

        db.session.commit()

def check_db_exists():
    with app.app_context():
        from app.models import User

        try:
            User.query.first()
        except:
            return False

        return True

if __name__ == '__main__':

    if not check_db_exists():
        print("Criando banco de dados...")
        create_db()

    app.run(host="0.0.0.0", port=5000)
