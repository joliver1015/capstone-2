from re import L
from flask import Flask, render_template, redirect, g, session, url_for, flash
from models import db, connect_db, User, Game, Genre, Platform
from forms import *
from helpers import *

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '20930485093202934'


connect_db(app)





#######################################################################################################
# User signup/login/logout
@app.before_request
def add_user_to_g():

    """Adds user to global"""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):

    """ logs in user"""

    session[CURR_USER_KEY] = user.user_id  

def do_logout():

    """Logs out user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

##### Home Page #####

@app.route('/')
def home_page():

    """Shows home page"""

    latest_reviews = []
    new_games = []
    top_games = []
    rankings = []

    ## Grabs latests reviews posted

    reviews = Review.query.order_by(Review.review_id.desc()).limit(5).all()

    for review in reviews:
        temp = {}
        review_game = Game.query.get(review.game_id)
        temp['review'] = review
        temp['game'] = review_game
        latest_reviews.append(temp)
    
    games = Game.query.all()

    ## Gets top 10 games

    for game in games: 
        temp = {}
        temp['game_id'] = game.game_id
        temp['ranking'] = find_ranking(game.game_id)
        rankings.append(temp)
        rankings = sorted(rankings, key= lambda i: i['ranking'])
    
    for r in rankings:
        game = Game.query.get(r['game_id'])
        top_games.append(game)
    
    top_games = top_games[:10]

    ## Gets 10 latest added games

    new_games = Game.query.order_by(Game.game_id.desc()).limit(10).all()
    


    return render_template('home.html', latest_reviews=latest_reviews, top_games=top_games, new_games=new_games  )

##### Registration and Login/Logout #####

@app.route('/signup', methods=["GET","POST"])
def signup():

    """ Shows registration page and form """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    

    form = SignUpForm()

    if form.validate_on_submit():

        username = form.username.data  
        pwd = form.password.data
        email = form.email.data

        user = User.register(username,pwd,email)
        db.session.add(user)
        
        db.session.commit()

        do_login(user)
       
        

        return redirect('/')
    
    return render_template("auth/signup.html", form=form)
        

@app.route('/login',methods=["GET","POST"])
def login():

    """ Shows log-in page """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            do_login(user)
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.user_id
            
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('auth/login.html', form=form)
   

@app.route('/logout')
def logout_user():
    do_logout()
    return redirect('/')

@app.route('/profile/<user_id>')
def show_profile(user_id):

    """Shows user profile"""

    scores = []

    user = User.query.get(user_id)

    num_ratings = len(user.ratings)

    num_reviews = len(user.reviews)

    for rating in user.ratings:
        scores.append(rating.score)
    if len(scores) > 0:
        mean_score = sum(scores) / len(scores)
    else:
        mean_score = 0

    return render_template('/profile/profile.html', user=user, num_ratings=num_ratings,num_reviews=num_reviews, mean_score=mean_score)

@app.route('/vglist/<user_id>')
def show_vglist(user_id):

    """Shows user's video game list"""

    games_list = []

    user = User.query.get(user_id)

    for rating in user.ratings:
        temp = {}
        game = Game.query.get(rating.game_id)
        temp['game'] = game
        temp['score'] = rating.score
        games_list.append(temp)
    
    return render_template('/profile/list.html',user=user, games_list=games_list)

@app.route('/reviewlist/<user_id>')
def review_list(user_id):

    """Shows list of user's reviews"""

    review_list = []

    user = User.query.get(user_id)

    reviews = Review.query.filter(Review.user_id==user_id).all()

    for review in reviews:
        temp = {}
        game = Game.query.get(review.game_id)
        temp['review'] = review
        temp['game'] = game
        review_list.append(temp)
    
    return render_template('/profile/reviewlist.html', review_list=review_list, user=user)

@app.route('/profile/<user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):

    """Page with edit profile form"""

    user = User.query.get(user_id)

    form = ProfileEditForm()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.profile_image = form.profile_image.data
        db.session.commit()
        return redirect(url_for("show_profile", user_id=user_id))
    
    return render_template('/profile/edit.html', user=user, form=form)
    
@app.route('/profile/<user_id>/change-password', methods=["GET","POST"])
def change_password(user_id):

    """Page for changing password"""

    user = User.query.get(user_id)



    form = NewPasswordForm()

    if form.validate_on_submit():
        user.password = form.new_password.data
        db.session.commit()

    return render_template('/profile/changepassword.html', form=form, user=user)



@app.route('/delete-profile', methods=["POST"])
def delete_user(user_id):

    """Deletes user profile"""

    users = User.query.all()

    user = User.query.get(user_id)

    users.remove(user)

    return redirect(url_for("home_page"))

##### Genre Routes #####

@app.route('/genres')
def show_genre_list():

    """Shows list of genres"""

    genres = Genre.query.all()


    return render_template('/genres/all.html', genres=genres)

@app.route('/genres/<genre_id>')
def show_genre_games(genre_id):

    """Shows games within genre"""

    genre = Genre.query.get_or_404(genre_id)

    game_count = len(genre.games)

    return render_template('/genres/detail.html', genre=genre, game_count=game_count)

##### Platform Routes #####

@app.route('/platforms')
def show_all_platforms():

    """Shows all game platforms"""

    platforms = Platform.query.all()

    num_platforms = len(platforms)

    return render_template('/platforms/all.html', platforms=platforms, num_platforms=num_platforms)

@app.route('/platforms/<platform_id>')
def show_platform_games(platform_id):

    """Gets list of games from platform"""

    platform = Platform.query.get(platform_id)

    games_count = len(platform.games)

    return render_template('/platforms/detail.html', platform=platform, games_count=games_count)

##### Game Routes #####

@app.route('/games')
def show_all_games():

    """Shows all games"""

    games = Game.query.all()

    num_games = len(games)

    return render_template('/games/all.html', games=games, num_games=num_games)

@app.route('/games/<game_id>')
def show_game_page(game_id):

    """Shows details and reviews of game"""
   
    user_review = None
    platform_list = []
    genre_list = []

    form = RatingForm()

    game = Game.query.get_or_404(game_id)

    num_users = len(game.ratings)

    avg_score = round(get_avg_score(game_id), 2)

    ranking = find_ranking(game_id)

    platforms = Platform.query.all()
    for platform in platforms:
        for ga in platform.games:
            if ga == game:
                platform_list.append(platform)
    
    genres = Genre.query.all()
    for genre in genres:
        for ga in genre.games:
            if ga == game:
                genre_list.append(genre)

    reviews = Review.query.filter(Review.game_id==game_id).all()

    user_rating = Rating.query.filter(Rating.game_id==game_id, Rating.user_id==g.user.user_id).first()

    for review in reviews:
        if review.user_id == g.user.user_id:
            user_review = review
            reviews.remove(review)
    
    return render_template('/games/detail.html', game=game, form=form, avg_score = avg_score, ranking = ranking, platforms=platform_list, genres=genre_list, reviews=reviews, user_review=user_review, num_users=num_users, user_rating=user_rating)

@app.route('/games/<game_id>', methods=["POST"])
def rate_game_page(game_id):

    """Adds user score to game's ratings"""

    form = RatingForm()

    new_score = form.score.data

    game = Game.query.get(game_id)

    rating = Rating.query.filter((Rating.user_id==g.user.user_id) & (Rating.game_id==game_id)).first()

    if not rating:
        rating = Rating(score=new_score, user_id=g.user.user_id, game_id=game_id)
    else:
        rating.score = new_score
    
    db.session.add(rating)
    db.session.commit()

    return redirect(url_for("show_game_page", game_id=game_id))

@app.route('/games/top')
def show_top_games():

    """Shows list of games sorted by ranking"""

    rankings = []
    top_games = []

    games = Game.query.all()

    for game in games: 
        temp = {}
        temp['game_id'] = game.game_id
        temp['ranking'] = find_ranking(game.game_id)
        rankings.append(temp)
        rankings = sorted(rankings, key= lambda i: i['ranking'])
    
    for r in rankings:
        game = Game.query.get(r['game_id'])
        top_games.append(game)
    
    
    return render_template('/games/top.html', rankings=rankings, top_games=top_games)
    
##### Reviews #####

@app.route('/games/<game_id>/reviews')
def show_all_reviews(game_id):

    
    game = Game.query.get(game_id)

    reviews = game.reviews

    return render_template("/reviews/all", reviews = reviews)

@app.route('/games/<game_id>/reviews/new', methods=["GET","POST"])
def new_review(game_id):

    """Form for creating new game review"""

    form = ReviewForm()

    game = Game.query.get(game_id)

    author = g.user.username

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        review = Review(
                user_id=g.user.user_id,
                game_id=game.game_id,
                author=author,
                title=title,
                body=body
        )

        game.reviews.append(review)
        db.session.commit()
        return redirect(url_for("show_game_page", game_id=game_id))
    
    return render_template("/reviews/new.html", game=game, form=form)

@app.route('/games/<game_id>/reviews/<review_id>/edit',methods=["GET","POST"])
def edit_review(game_id, review_id):

    """Page for editing review"""

    game = Game.query.get(game_id)

    review = Review.query.get(review_id)

    form = ReviewForm()

    if form.validate_on_submit():
        review.title = form.title.data
        review.body = form.body.data
        db.session.commit()
        return redirect(url_for("show_game_page", game_id = game_id))
    
    return render_template("/reviews/edit.html", game=game, review=review, form=form)

@app.route('/games/<game_id>/reviews/<review_id>/delete', methods=["GET","POST"])
def delete_review(game_id, review_id):

    """Deletes review"""

    game = Game.query.get(game_id)

    review = Review.query.get(review_id)

    game.reviews.remove(review)
    db.session.commit()

    return redirect(url_for("show_game_page", game_id=game_id))










    
    


    


    
    




   
    
    
    


















    
    








