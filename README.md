# ChessFanSite
 
ChessApp: A Django project.

## Introduction

At The Tech Academy, for the last two weeks in every language program we work in teams on a shared project. In the Python program, that app was an Django site for housing personal collections and hobbies. It being Covid-time, we worked remotely. We used Slack, Google Meet, and daily scrum meetings to maintain group cohesion.

A lot of the coding was just setting up models and views in django. If you want to see the whole show, you can [click here](https://github.com/mcleeder/ChessFanSite/tree/main/ChessApp). Following that link will take you to the code I worked on for the site, but not the entire site itself.

Highlights:

-[Chess.com API Request](https://github.com/mcleeder/CodeSamples/blob/main/django_chessapp.md#chesscom-api-request)

-[Beautiful Soup](https://github.com/mcleeder/CodeSamples/blob/main/django_chessapp.md#Beautiful-Soup-web-scraper)

-[Chess game position render](https://github.com/mcleeder/CodeSamples/blob/main/django_chessapp.md#chess-game-position-render)


### Chess.com API Request
This is where this app gets started. It asks you for a month, year, and a username. It'll pull all the chess games on file at Chess.com for that user and store them locally. This is one of the first things I wrote in Python that really made me aware of just how quickly and easily you can get things running.

```python
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
```

This is a helper function that goes with the API request function above. All it does is translate the response data to the local ChessGame() model.

```python
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
```

### Beautiful Soup web scraper
Blurb...

```python
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
```


### Chess game position render
At Chess.com, the final position in a chess game is notated in something called [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation). It's a string of characters with letters representing the pieces and numbers indicating blank spaces. An example would be: rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R

I had been staring at it for about a week when I finally decided to try to render it on the site. Two months prior, I had written [a Sudoku solver in C#](https://github.com/mcleeder/CodeSamples/blob/main/Sudoku_Solver.md) and had gotten pretty good at reading and writing to 2D arrays.

This came with two main challenges. The first was that the string contains both letters and numbers, and you have to either record the letter, or skip forward a number of squares as indicated by a number. My first thought was of the int.tryparse() in C#, so I searched to see if python had one. It didn't, but I learned that you can make one very easily as it's just a function that returns a tuple. Hurray python.

The second challenge was just some head scratching about how to keep track of where the next piece should go. The solution there simply ended up being the index_c(ursor) variable. 

```python
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
```

This helps out the function above. Just here for clarity. These are the Font-Awesome icon codes that get sent to the template for rendering.

```python
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
```

The very last part was getting django to render the board. Again, just a loop inside a loop. And while reading the django docs looking for the |safe feature (that let me render the HTML as HTML) I found the feature that cycles the background color, which was fortunate. There is some simple CSS doing the rest of the sizing and colors.

```html
    <table class="chess-table">
          {% for row in game_board %}
          <tr>
            {% for cell in row %}
            <td class="chess-cell {% cycle 'chess-w' 'chess-b' as rowcolors %}">{{ cell |safe }}</td>
            {% endfor %}
            <!-- {% cycle rowcolors %} -->
            </tr>
          {% endfor %}
    </table>
```

## The Good:
- Pulls chess game data from the Chess.com API.
- Scrapes Chess.com for news using Beautiful Soup.
- Lets the user create groups of games for comparision, generates statistics for those groups.
- Lets the user perform CRUD operations on their data.
- A cool function for rendering a chess board final position.

## The Bad:
- Minimal UI
- Data model needs a re-think. At the very least, I think I should be tracking the users specificlly used to import games seperately from their opponents. As it is right now, both end up being treated the same so the list of users with games in the DB gets very long very quickly.
- The current data model also makes editing the groups of games a bit slow.
- It would be nice to be able to query by the player being white or black pieces.
