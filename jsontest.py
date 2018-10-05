import json 
test2='{"test": { "user_id": 2131, "name": "John", "gender": 0,  "thumb_url": "sd", "money": 23, "cash": 2, "material": 5}}'
test='{"test": { "explore": "abc", "grid": "abc", "robotPosition": [1,2,3], "arrow": [1,false,false,false]}}'
test3 = '{"test":"abc", "explore": "abc", "grid": "abc", "robotPosition": [1,2,3], "arrow": [1,false,false,false]}'
datastore = json.loads(test3)
arrow = datastore["arrow"]
print (arrow)