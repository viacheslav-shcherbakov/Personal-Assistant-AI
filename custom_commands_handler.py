import json

class command:
    def __init__(self, name, details, creation_date, keywords, responses):
        self.name = name
        self.details = details
        self.creation_date = creation_date
        self.keywords = keywords
        self.responses = responses

COMMANDS=[]

def boot():
    #Read through all commands in commands.json
    json_reader=json.loads(open('commands/commands.json', 'r').read())

    for c in json_reader['commands']:
        #Create new objects for each
        COMMANDS.append(
            command(
                c['info']['name'],          #name
                c['info']['details'],       #details
                c['info']['creation_date'], #creation_date
                c['keywords'],              #keywords
                c['responses']              #responses
            )
        )


