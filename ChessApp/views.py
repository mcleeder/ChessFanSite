import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChessGameGroup, ChessGame
from .forms import GetGamesByPlayer, GroupStats, GetGameDetails, CreateGroup
from .helpers import json_to_game, chess_game_stats, render_final_position


# Create your views here.
def index(request):
    return render(request, "ChessApp/index.html")


def group_stats(request):
    if request.method == 'POST':
        form = GroupStats(request.POST)
        if form.is_valid():
            group_db = ChessGameGroup.Groups.get(id=form.cleaned_data['title'])
            group_games1 = group_db.game_list1.filter(
                Q(white_player=group_db.player1) | Q(black_player=group_db.player1))
            group_games2 = group_db.game_list1.filter(
                Q(white_player=group_db.player2) | Q(black_player=group_db.player2))

            # generate some stats
            player_1_stats = chess_game_stats(group_games1, group_db.player1)
            player_2_stats = chess_game_stats(group_games2, group_db.player2)

            # game details button
            game_details_form = GetGameDetails()

            context = {'group_db': group_db,
                       'group_form': form,
                       'group_games1': group_games1,
                       'group_games2': group_games2,
                       'player_1_stats': player_1_stats,
                       'player_2_stats': player_2_stats,
                       'game_details': game_details_form,
                       }
            return render(request, "ChessApp/group_stats.html", context)
    else:
        form = GroupStats()
        context = {'group_form': form}
        return render(request, "ChessApp/group_stats.html", context)


def create_group(request):
    if request.method == 'POST':
        form = CreateGroup(request.POST)
        context = {'new_group': form}
        if form.is_valid():
            new_group = form.save()
            games = ChessGame.Games.all()
            for g in games:
                if g.white_player == new_group.player1 or g.black_player == new_group.player1 or g.white_player == new_group.player2 or g.black_player == new_group.player2:
                    new_group.game_list1.add(g)

            new_group.save()
            context.update({'msg': "Successfully created group."})

        return render(request, "ChessApp/create_group.html", context)
    else:
        form = CreateGroup()
        context = {'new_group': form}
        return render(request, "ChessApp/create_group.html", context)


def group_edit(request, group_id):
    group = ChessGameGroup.Groups.get(id=group_id)
    form = CreateGroup(instance=group)
    context = {
        'group_id': group_id,
        'form': form
    }
    return render(request, "ChessApp/edit_group.html", context)


def group_save(request, group_id):
    group = ChessGameGroup(id=group_id)
    form = CreateGroup(request.POST, instance=group)
    games = group.game_list1.all()
    # if players changed, remove games
    for g in games:
        if g.white_player != group.player1 or g.black_player != group.player1 or g.white_player != group.player2 or g.black_player != group.player2:
            group.game_list1.remove(g)
    form.save()
    games_db = ChessGame.Games.all()
    # if players changed, add games
    for g in games_db:
        if g.white_player == group.player1 or g.black_player == group.player1 or g.white_player == group.player2 or g.black_player == group.player2:
            group.game_list1.add(g)
    save_game = form.save()
    return redirect('group_stats')


def group_delete(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(ChessGameGroup, id=group_id)
        print(group_id)
        group.delete()
    return redirect('group_stats')


def load_data(request):
    # request method is POST
    if request.method == 'POST':
        form = GetGamesByPlayer(request.POST)
        context = {'form': form}
        if form.is_valid():
            username = form['username'].value().strip()
            year = form['year'].value()
            month = form['month'].value()
            lookup_string = "https://api.chess.com/pub/player/{}/games/{}/{}".format(username, year, month)
            json_request = requests.get(lookup_string)
            # if we find a user on chess.com
            if json_request.status_code == requests.codes.ok:
                json_games = json_request.json()
                for game in json_games['games']:
                    json_to_game(game).save()
                load_status = "Loaded {} games.".format(len(json_games['games']))
                context.update({"load_status": load_status})
            # if no user found on chess.com
            else:
                load_status = "Username not found."
                context.update({"load_status": load_status})
        return render(request, "ChessApp/load_data.html", context)
    # request method is GET
    else:
        form = GetGamesByPlayer
        return render(request, "ChessApp/load_data.html", {'form': form})


def game_details(request, game_id):
    game = ChessGame.Games.get(id=game_id)
    game_board = render_final_position(game.fen)
    context = {'game': game, 'game_board': game_board}
    return render(request, "ChessApp/game_details.html", context)


def chess_news(request):
    chess_com = requests.get("https://www.chess.com/news")
    soup = BeautifulSoup(chess_com.text, 'html.parser')
    content = []

    for article in soup.find_all('article'):
        headline = article.find('a', class_='post-preview-title').text.strip()
        link = article.find('a', class_='post-preview-title')['href']
        summary = article.find('p', class_="post-preview-excerpt").text.strip()
        date_time = article.find('span', class_='post-preview-meta-content').span['title']
        date_time = date_time.split(",")
        date = f'{date_time[0]}, {date_time[1]}'
        s_article = {
            'headline': headline,
            'link': link,
            'summary': summary,
            'date': date,
        }
        content.append(s_article)

    paginator = Paginator(content, 6)
    page_number = request.GET.get('page')
    page_list = paginator.get_page(page_number)

    context = {'context': page_list}

    return render(request, "ChessApp/chess_news.html", context)
