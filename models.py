
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy.util.langhelpers import hybridproperty



db = SQLAlchemy()

metadata = MetaData()

bcrypt = Bcrypt()



game_platforms = db.Table('game_platforms', db.Model.metadata,
            db.Column('game_id', db.Integer, db.ForeignKey('games.game_id')),
            db.Column('platform_id', db.Integer, db.ForeignKey('platforms.platform_id'))
)

game_genres = db.Table('game_genres', db.Model.metadata,
            db.Column('game_id', db.Integer, db.ForeignKey('games.game_id')),
            db.Column('platform_id', db.Integer, db.ForeignKey('genres.genre_id'))
)




class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.Text)
    bio = db.Column(db.Text)
    

    @classmethod
    def register(cls, username, pwd, email):

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email)

    @classmethod
    def authenticate(cls, username, password):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Game(db.Model):

    __tablename__ = 'games'

    game_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable = True)
    cover_art = db.Column(db.String, nullable=True)
    official_website = db.Column(db.String, nullable=True)

    steam_link = db.Column(db.String, nullable=True)
    amazon_link = db.Column(db.String, nullable=True)
    gamestop_link = db.Column(db.String, nullable=True)
    bestbuy_link = db.Column(db.String, nullable=True)

    

   
    

class Genre(db.Model):

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)

    games = db.relationship("Game", secondary=game_genres)
    

class Platform(db.Model):

    __tablename__ = 'platforms'

    platform_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    platform_name = db.Column(db.String(20), nullable=False)

    games = db.relationship("Game", secondary=game_platforms)


class Rating(db.Model):

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
    user = db.relationship("User",
                            backref=db.backref("ratings"))
    
    game = db.relationship("Game",
                            backref = db.backref("ratings"))

class Review(db.Model):

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    author = db.Column(db.String(20), nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("reviews"))
    
    game = db.relationship("Game",
                            backref = db.backref("reviews"))


    





def connect_db(app):
    """Connect the database to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/myvideogamelist"
    db.app = app
    db.init_app(app)  


