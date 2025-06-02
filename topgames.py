import urllib2
import json

def get_top_games(username):
    """Ultra simple version that just gets games"""
    url = "https://lichess.org/api/games/user/{}?max=50&rated=true&analysed=true&accuracy=true".format(username)
    
    print("Fetching games for {}...".format(username))
    
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/x-ndjson')
        response = urllib2.urlopen(req)
        data = response.read()
        
        games = []
        
        for line in data.strip().split('\n'):
            if not line:
                continue
                
            try:
                game = json.loads(line)
                game_id = game.get('id', '')
                
                # Find user's color and accuracy
                user_accuracy = None
                user_color = None
                
                if 'players' in game:
                    players = game['players']
                    
                    # Check white player
                    if 'white' in players and 'user' in players['white']:
                        white_user = players['white']['user']
                        if 'name' in white_user and white_user['name'].lower() == username.lower():
                            user_color = 'white'
                            if 'analysis' in players['white'] and 'accuracy' in players['white']['analysis']:
                                user_accuracy = players['white']['analysis']['accuracy']
                    
                    # Check black player
                    if 'black' in players and 'user' in players['black']:
                        black_user = players['black']['user']
                        if 'name' in black_user and black_user['name'].lower() == username.lower():
                            user_color = 'black'
                            if 'analysis' in players['black'] and 'accuracy' in players['black']['analysis']:
                                user_accuracy = players['black']['analysis']['accuracy']
                
                if user_accuracy is not None:
                    games.append({
                        'id': game_id,
                        'accuracy': user_accuracy,
                        'color': user_color,
                        'url': "https://lichess.org/{}".format(game_id)
                    })
            except:
                continue
        
        # Sort by accuracy
        games.sort(key=lambda g: g['accuracy'], reverse=True)
        
        # Print top 20
        print("\nTop games by accuracy:")
        print("Rank  Accuracy  Color  URL")
        print("-" * 50)
        
        for i, game in enumerate(games[:20], 1):
            print("{}     {}      {}    {}".format(
                i, 
                game['accuracy'], 
                game['color'], 
                game['url']
            ))
            
    except Exception as e:
        print("Error: {}".format(e))

# Run the script
username = raw_input("Enter Lichess username: ")
get_top_games(username)
