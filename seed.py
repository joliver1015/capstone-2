from sqlalchemy import func
from sqlalchemy.sql.functions import user
from wtforms.fields.core import DateField
from models import User,Game,Genre,Platform,Rating,Review, connect_db, db
import datetime
from games import *



from app import app

def load_users():

    """Loads user data from seed_data file"""
    
    User.query.delete()

    with open("seed_data/users.csv") as user_file:
        for row in user_file:
            row = row.rstrip()
            user_id,username, password, email = row.split(',')

            user = User(user_id=user_id,
                        username=username,
                        password=password,
                        email=email)

            db.session.add(user)

    db.session.commit()

def load_genres():

    """Loads genre data from seed file"""

    Genre.query.delete()

    with open("seed_data/genres.csv") as genre_data:
        for row in genre_data:
            row = row.rstrip()
            genre_id, genre_name = row.split(',')
            genre_id = int(genre_id)
            genre = Genre(genre_id=genre_id,
                        genre_name=genre_name)
            db.session.add(genre)
    db.session.commit()

def load_platforms():

    """Loads platform data from seed_file"""

    Platform.query.delete()

    with open("seed_data/platforms.csv") as platform_data:
        for row in platform_data:
            row = row.rstrip()
            platform_id, platform_name = row.split(',')
            platform_id = int(platform_id)
            platform = Platform(platform_id=platform_id,
                        platform_name=platform_name)
            db.session.add(platform)

    db.session.commit()

def load_games():

    """ Loads games from game list"""

    Game.query.delete()

    for g in games_list:
        game_id, title, release_date, description, cover_art, official_website, genres, platforms, steam_link, amazon_link, gamestop_link, bestbuy_link = g[0:]
        game_id = int(game_id)
        game = Game(game_id=game_id,
                    title=title,
                    release_date=release_date,
                    description=description,
                    cover_art=cover_art,
                    official_website=official_website,
                    steam_link=steam_link,
                    amazon_link=amazon_link,
                    gamestop_link=gamestop_link,
                    bestbuy_link=bestbuy_link)
        db.session.add(game)
        for g in genres:
            genre = Genre.query.get(g)
            genre.games.append(game)
        for p in platforms:
            platform = Platform.query.get(p)
            platform.games.append(game)
    db.session.commit()


def load_ratings():

    """Load ratings from seed_data"""

    Rating.query.delete()

    with open("seed_data/ratings.csv") as rating_data:
        
        for row in rating_data:
            row = row.split(',')
            user_id = int(row[0])
            game_id = int(row[1])
            score = int(row[2])

            rating = Rating(user_id=user_id,
                            game_id=game_id,
                            score=score)
            
            db.session.add(rating)
    db.session.commit()

def load_reviews():

    """Load reviews from reviews"""

    Review.query.delete()

    with open("seed_data/reviews.csv") as review_data:

        for row in review_data:
            row = row.rstrip()
            review_id, user_id, game_id, author, title, body = row.split(',') 
            review_id = int(review_id)
            user_id = int(user_id)
            game_id = int(game_id)
            review = Review(review_id=review_id,
                            user_id=user_id,
                            game_id=game_id,
                            author=author,
                            title=title,
                            body=body)
            
            db.session.add(review)
        db.session.commit()




            


def set_user_id_val():

    """Sets new user id to next available id in table  """

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_review_id_val():

    """Sets new review id to next available id in table"""

    result = db.session.query(func.max(Review.review_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('reviews_review_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

connect_db(app)
db.create_all()

load_users()                  
load_genres()
load_platforms()            
load_games()
load_ratings()
load_reviews()
set_user_id_val()
set_review_id_val()
        
