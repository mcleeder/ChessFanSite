from datetime import datetime
from .models import ChessGame, ChessGameGroup


# map a json file from chess.com to a ChessGame object
def json_to_game(json_obj):
    game = ChessGame()
    game.id = json_obj['url'].split('/')[-1]
    game.url = json_obj['url']
    game.time_control = json_obj['time_control']
    game.end_time = datetime.fromtimestamp(json_obj['end_time'])
    game.rated = json_obj['rated']
    game.fen = json_obj['fen']
    game.time_class = json_obj['time_class']
    game.rules = json_obj['rules']
    game.white_player = json_obj['white']['username']
    game.white_player_rating = json_obj['white']['rating']
    game.white_player_result = json_obj['white']['result']
    game.black_player = json_obj['black']['username']
    game.black_player_rating = json_obj['black']['rating']
    game.black_player_result = json_obj['black']['result']
    return game


# lookup all players in db, generate list of tuples
# sorted and distinct
def get_users_from_db():
    all_games = ChessGame.Games.all()
    distinct_users = set()
    result = []
    set_count = 0
    for i in all_games:
        distinct_users.add(i.white_player)
        if set_count < len(distinct_users):
            result.append((i.white_player, i.white_player))
            set_count += 1
        distinct_users.add(i.black_player)
        if set_count < len(distinct_users):
            result.append((i.black_player, i.black_player))
            set_count += 1

    def get_key(item):
        return item[1].casefold()

    return sorted(result, key=get_key)


# lookup all groups in db, generate list of tuples
# sorted
def get_groups_from_db():
    all_groups = ChessGameGroup.Groups.all()
    result = []
    for i in all_groups:
        result.append((i.id, i.title))

    def get_key(item):
        return item[1].casefold()

    return sorted(result, key=get_key)


# used to calc average opponent rating without breaking stuff
def chess_stats_avg(opp_total, total_games):
    try:
        return int(round(opp_total / total_games))
    except ZeroDivisionError:
        return 0


# used to calc win ratio without breaking stuff
def chess_stats_ratio(win, draw, loss):
    try:
        return round(win / (draw + loss), 1)
    except ZeroDivisionError:
        if win > 0 and (draw + loss) == 0:
            return win
        return 0


# calculate some basic stats for a group of chess games
# generate dictionary
def chess_game_stats(games, player):
    total_games = len(games)
    total_win = 0
    total_loss = 0
    total_draw = 0
    opp_rating_total = 0
    avg_opp_rating = 0
    win_ratio = 0

    if total_games > 0:
        for game in games:
            # if our player won, give them a win
            if game.white_player == player and game.white_player_result == 'win':
                total_win += 1
            elif game.black_player == player and game.black_player_result == 'win':
                total_win += 1
            # if either player agreed then game is a draw
            elif game.white_player_result == 'agreed':
                total_draw += 1
            # then our player must have lost
            else:
                total_loss += 1

            if game.white_player == player:
                opp_rating_total += int(game.black_player_rating)  # TODO: change this in the model to be an integer
            else:
                opp_rating_total += int(game.white_player_rating)

        avg_opp_rating = chess_stats_avg(opp_rating_total, total_games)
        win_ratio = chess_stats_ratio(total_win, total_draw, total_loss)

    context = {'total_games': total_games,
               'total_win': total_win,
               'total_loss': total_loss,
               'total_draw': total_draw,
               'win_ratio': win_ratio,
               'avg_opp_rating': avg_opp_rating,
               }
    return context


chess_p = {
    'r': """<i class="fas fa-chess-rook text-dark"></i>""",
    'R': """<i class="fas fa-chess-rook text-light"></i>""",
    'n': """<i class="fas fa-chess-knight text-dark"></i>""",
    'N': """<i class="fas fa-chess-knight text-light"></i>""",
    'b': """<i class="fas fa-chess-bishop text-dark"></i>""",
    'B': """<i class="fas fa-chess-bishop text-light"></i>""",
    'k': """<i class="fas fa-chess-king text-dark"></i>""",
    'K': """<i class="fas fa-chess-king text-light"></i>""",
    'q': """<i class="fas fa-chess-queen text-dark"></i>""",
    'Q': """<i class="fas fa-chess-queen text-light"></i>""",
    'p': """<i class="fas fa-chess-pawn text-dark"></i>""",
    'P': """<i class="fas fa-chess-pawn text-light"></i>""",
    '': """&nbsp;"""
}


# map chess final position to list[][]
# for display in template
def render_final_position(fen):
    def try_parse(c):
        try:
            return int(c), True
        except ValueError:
            return c, False

    fens = fen.split(" ")[0].split("/")
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
    ]
    for y in range(0, 8):
        index_c = 0
        for x in fens[y]:
            if not try_parse(x)[1]:
                board[y][index_c] = chess_p[x]
                index_c += 1
            else:
                board[y][index_c] = chess_p[""]
                index_c += try_parse(x)[0]
    return board
