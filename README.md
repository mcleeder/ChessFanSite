# ChessFanSite
 
ChessApp: A Django project.


The Good:
- Pulls chess game data from the Chess.com API
- Scrapes Chess.com for news using Beautiful Soup
- Lets the user create groups of games for comparision, generates statistics for those groups.
- Lets the user perform CRUD operations on their data
- A cool method for rendering a chess board

The Bad:
- Minimal UI
- Data model needs a re-think. At the very least, I think I should be tracking the users specificlly used to import games seperately from their opponents. As it is right now, both end up being treated the same so the list of users with games in the DB gets very long very quickly.
- It would be nice to be able to query by the player being white or black pieces.
