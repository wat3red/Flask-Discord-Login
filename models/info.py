from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Info(db.Model):
    __tablename__ = "info"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    is_verified = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def ban_user(self):
        self.status = 5
        db.session.commit()
