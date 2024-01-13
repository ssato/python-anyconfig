"""A nested dict."""
import datetime

DATA = {
    'title': 'Table examples',
    'name': {'first': 'Tom', 'last': 'Preston-Werner'},
    'point': {'x': 1, 'y': 2},
    'animal': {'type': {'name': 'pug'}},
    'owner': {
        'name': 'Regina Dogman', 'member_since': datetime.date(1999, 8, 4)
    },
    'fruit': {
        'apple': {
            'color': 'red', 'taste': {'sweet': True},
            'texture': {'smooth': True}
        }
    }
}
