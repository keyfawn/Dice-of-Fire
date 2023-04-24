def check(data):
    games = {'⚽': data.football,
             '🎯': data.darts,
             '🎲': data.dice,
             '🏀': data.basketball,
             '🎳': data.bowling,
             '🎰': data.slot}
    maxi = max(games.values())
    teht = ''
    for game in games.keys():
        if games[game] == maxi:
            teht = teht + game
