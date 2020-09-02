##File for storing decks.  testDeck uses JSON format which may be deprecated.
bold = 0
tough = 0
pierce = 0
tempATK = 0
tempDEF = 0

testDeck = '{"shared":{},"players":[{"piles":{"Deck":[{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"1835c230-bb8b-4353-8e6b-f09c53be551c","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"1835c230-bb8b-4353-8e6b-f09c53be551c","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"443c37fc-8284-49cf-9d60-df10175192dd","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"443c37fc-8284-49cf-9d60-df10175192dd","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"830a2e99-52d5-46da-b580-5c0500facd88","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"830a2e99-52d5-46da-b580-5c0500facd88","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"931d7733-055d-4257-8f4d-69df02f4a262","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"931d7733-055d-4257-8f4d-69df02f4a262","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"44e0f1f2-964f-47ff-87a2-ba370308b377","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"44e0f1f2-964f-47ff-87a2-ba370308b377","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"b02a8fc4-b5f1-46e5-a78b-e1e9a72ca7be","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"b02a8fc4-b5f1-46e5-a78b-e1e9a72ca7be","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"181b3347-cc34-437c-9f3f-997187e13631","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"181b3347-cc34-437c-9f3f-997187e13631","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"bae64761-368c-4880-bd0b-03db2e577421","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"bae64761-368c-4880-bd0b-03db2e577421","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"0b19d986-c196-4cdb-9a94-eaa120026db8","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"0b19d986-c196-4cdb-9a94-eaa120026db8","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"c7a9f8da-5974-4d27-9e25-28fc8a6fdf8b","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"c7a9f8da-5974-4d27-9e25-28fc8a6fdf8b","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"5ae71a99-8129-4ead-9890-53f3976055e7","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"5ae71a99-8129-4ead-9890-53f3976055e7","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"5e05e6cf-ccea-4929-a4e3-2bb994e601cc","alternate":"","markers":null},{"orientation":0,"position":[0,0],"isFaceUp":false,"model":"5e05e6cf-ccea-4929-a4e3-2bb994e601cc","alternate":"","markers":null}]},"name":"zz1000zz","hand":[],"_id":1,"counters":{"Tower":0}}],"table":[{"orientation":0,"position":[-189,-2],"isFaceUp":true,"model":"a881606a-5e32-4406-a61c-811a9122cf58","alternate":"","markers":null},{"orientation":0,"position":[31,-4],"isFaceUp":true,"model":"946d4673-b135-43c3-bdb9-6280a40346ef","alternate":"","markers":null}],"counters":null}'

flipDeck = ['c3200832-3e7c-42db-92a7-5ddc02597c33',
            'c3200832-3e7c-42db-92a7-5ddc02597c33',
            'c3200832-3e7c-42db-92a7-5ddc02597c33',
            'c3200832-3e7c-42db-92a7-5ddc02597c33',
            '905abf7f-09bd-47d4-bc1f-d93180860138',
            '4f298a3e-b05e-4c82-8aa5-06e78aea5e22']

AICharacters = [
    ['a881606a-5e32-4406-a61c-811a9122cf58',
    '14c1fd8e-8fc7-464e-b9b1-468e4931b0da'],
    ['a881606a-5e32-4406-a61c-811a9122cf58',
    '14c1fd8e-8fc7-464e-b9b1-468e4931b0da']
                ]

AIActions = [
    ['Scrap', 'Discard', 'Damage'],
    ['Draw', 'Scrap', 'Discard', 'Damage']
    ]

def getAICharacters(*args):
    return AICharacters[0]

def getAIActions(*args):
    return AIActions[0]
