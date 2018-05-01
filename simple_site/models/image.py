from simple_site import db


class Image(db.Model):
    __tablename__ = 'images'

    name = db.Column(db.String, nullable=False, index=True)
    image = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('images', lazy=True))

    def __repr__(self):
        return '<Image {name}>'.format(name=self.name)

    @property
    def url(self):
        return '/images/{id}/{name}'.format(id=self.id, name=self.name)
