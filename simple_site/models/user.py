from simple_site import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)
