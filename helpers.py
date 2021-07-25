from models import Game


def get_avg_score(game_id):

    """Gets average score for a game"""

    scores = []
    game = Game.query.get(game_id)
    for rating in game.ratings:
        scores.append(rating.score)
    
    avg_score = sum(scores)/len(scores)
        
    
    return avg_score

def find_ranking(game_id):

    """Gathers scores from all games, averages them, then sorts them by highest average score.
    Returns target game's ranking. """

    scores = []

    games = Game.query.all()

    target_score = get_avg_score(game_id)

    for game in games:
        scores.append(get_avg_score(game.game_id))
    
    rankings = sorted(scores, key=None,reverse=True)

    target_ranking = rankings.index(target_score)

    return target_ranking + 1





    


    
    

        



    


    











   
