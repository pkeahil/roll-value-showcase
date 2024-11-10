import json

from commands import showcase
from profiles import profiles

my_uid = "625733723"

result = showcase.get_character_showcase(my_uid)
result2 = profiles.get_player_info(my_uid)

print(result)

with open("./result.json", "w") as file:
    json.dump(result, file)

with open("./result2.json", "w") as file:
    json.dump(result2, file)
