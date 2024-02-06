import json
new_player_data = {}
existing_data = {}

class SavingScore:
    def __init__(self) -> None:
        self._player_name = None
        self._player_score = None
    
    #Call this methode to save the score of the player, it needs a name and the amount of points 
    def give_score(player_name, player_score):
        
        try:
            with open("ScoreBored.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize existing_data as an empty dictionary
            existing_data = {}

        count = 0
        
        if player_name in existing_data:
            count = sum(1 for name in existing_data if name.startswith(player_name))
            player_name = f"{player_name}({count})"

        new_player_data = {
            player_name: {
                "name": player_name,
                "score": player_score 
            }
        }
        existing_data.update(new_player_data)

        with open("ScoreBored.json", "w") as file:
            json.dump(existing_data, file, indent=4)

    def print_score():
       with open("ScoreBored.json", "r") as file:
            existing_data = json.load(file)
            return existing_data
            