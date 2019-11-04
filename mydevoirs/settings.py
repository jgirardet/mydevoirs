import json

settings_json = json.dumps(
    [
        # {"type": "title", "title": "Réglages", "section":"agenda"},
        # {'type': 'bool',
        #  'title': 'A boolean setting',
        #  'desc': 'Boolean description text',
        #  'section': 'example',
        #  'key': 'boolexample'},
        {
            "type": "numeric",
            "title": "Nombre de jour à afficher",
            "desc": "Nombre de jour à afficher",
            "section": "agenda",
            "key": "nbjour",
        },
        # {
        #     "type": "buttons",
        #     "title": "essai bout",
        #     # "title": "$lvar(565)",
        #     "desc": "la desc",
        #     # "desc": "$lvar(566)",
        #     # "section": "$var(InterfaceConfigSection)",
        #     "section": "agenda",
        #     "key": "configchangebuttons",
        #     "buttons": [
        #         {"title": "Add", "id": "button_add"},
        #         {"title": "Del", "id": "button_delete"},
        #         {"title": "Rename", "id": "button_rename"},
        #     ],
        # },
        {
            "type": "slider",
            "title": "essai bout",
            "desc": "la desc",
            "section": "agenda",
            "key": "slider1",
        }
        # {
        #     "type": "options",
        #     "title": "An options setting",
        #     "desc": "Options description text",
        #     "section": "example",
        #     "key": "optionsexample",
        #     "options": ["option1", "option2", "option3"],
        # },
        # {
        #     "type": "string",
        #     "title": "A string setting",
        #     "desc": "String description text",
        #     "section": "example",
        #     "key": "stringexample",
        # },
        # {
        #     "type": "path",
        #     "title": "A path setting",
        #     "desc": "Path description text",
        #     "section": "example",
        #     "key": "pathexample",
        # },
    ]
)
