from sarabande import db


posts_tags = db.Table(
    'posts_tags', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False,
              index=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False,
              index=True))
