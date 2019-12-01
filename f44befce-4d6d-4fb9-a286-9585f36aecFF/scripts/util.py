##These functions are copied from other OCTGN packages.  Mostly unused.
##Included for potential development purposes with storing/loading data locally.
from datetime import datetime as dt
import collections
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer as json #since .net 3.5?

def loadTable(group, x=0, y=0):
    mute()
    try:
	if group == "Yes":
            tab = json().DeserializeObject(testDeck)
	deserializeTable(tab['table'])
    finally:
        pass
    if tab['players'] is not None and len(tab['players']) > 0:
        for player in tab['players']:
            deserializePlayer(player)

def deserializeTable(tbl):
    if len(tbl) == 0:
	return
    for cardData in tbl:
	deserizlizeCard(cardData)

def deserizlizeCard(cardData):
    mute()
    card = table.create(cardData['model'], cardData['position'][0], cardData['position'][1], 1, True)
    if 'markers' in cardData and cardData['markers'] is not None and len(cardData['markers']) > 0:
	for key, qty in {(i['name'], i['model']): i['qty'] for i in cardData['markers']}.items():
	    card.markers[key] = qty
    return card


def verifySaveDirectory(group,x=0,y=0): 
        dir = wd("")
        if 'GameDatabase' in dir:
                filename = dir.replace('GameDatabase','Decks').replace('f44befce-4d6d-4fb9-a286-9585f36aecFF','Transformers')
        else:
                filename = "Decks\Transformers".join(dir.rsplit('OCTGN',1))
        try:
                nt.mkdir(filename)
        except:
                pass
        try:
                filename = filename + '\\GameStates'
                nt.mkdir(filename)
        except:
                pass


def saveTable(group, x=0, y=0, auto=False):
	mute()
	verifySaveDirectory('')
	
        if auto == False:
                if 1 != askChoice('You are about to SAVE a game.  This will save everything, including all hand and deck states.  \nIf you are certain you want to do this, please take note of the name of your save file.'
                        , ['I understand and want to save a game!', 'Nevermind...'], ['#dd3737', '#d0d0d0']):
                        return

	try:
		tab = {"table":[], "shared": {}, 'counters': None, "players": None}
		
		# loop and retrieve cards from the table
		for card in table:
			tab['table'].append(serializeCard(card))

##		tab['counters'] = serializeCounters(shared.counters)
		
		# loop each player
		players = sorted(getPlayers(), key=lambda x: x._id, reverse=False)
		tab['players'] = [serializePlayer(pl) for pl in players]

                dir = wd("")
##		dir = wd('table-state-{}.json'.format('{:%Y%m%d%H%M%S}'.format(dt.now())))
		if 'GameDatabase' in dir:
			filename = dir.replace('GameDatabase','Decks').replace('f44befce-4d6d-4fb9-a286-9585f36aecff','Transformers')
		else:
			filename = "Decks\Transformers".join(dir.rsplit('OCTGN',1))

		if auto == True:
                        filename = filename + "\\GameStates\\autosave.json"
                else:
                        filename = filename + '\\GameStates\\' + 'table-state-{}.json'.format('{:%Y%m%d%H%M%S}'.format(dt.now()))
        		filename = askString('Please input the path to save the game state', filename)
		
		if filename == None:
			return
		
		with open(filename, 'w+') as f:
			f.write(json().Serialize(tab))
		
##		notify("Table state saves to {}".format(filename))
	finally:
                mute()


def serializeCard(card):
    cardData = {'model':'', 'markers':{}, 'orientation':0, 'position':[], 'isFaceUp':False}
    cardData['model'] = card.model
    cardData['orientation'] = card.orientation
    cardData['markers'] = serializeCardMarkers(card)
    cardData['position'] = card.position
    cardData['isFaceUp'] = card.isFaceUp
    cardData['alternate'] = card.alternate
    #notify("cardData {}".format(str(cardData)))
    return cardData


def serializeCard2(card):
	cardData = {'model':''}
	cardData['model'] = card.model
	return cardData

def serializeCard3(card):
	cardData = {'name':''}
	cardData['name'] = card.name
	return cardData

def serializePlayer(player):
	plData = {'_id':None, 'name': None, 'counters':None, 'hand':[], 'piles': {}}
	plData['_id'] = player._id
	plData['name'] = player.name
	plData['counters'] = serializeCounters(player.counters)
	
	# serialize player hand
	if len(player.hand) > 0:
		for card in player.hand:
			plData['hand'].append(serializeCard(card))
			
	# serialize player's piles
	for k,v in player.piles.items():
		if len(v) == 0:
			continue
		plData['piles'].update({k: [serializeCard(c) for c in v]})

	return plData
		
def serializeCounters(counters):
	if len(counters) == 0:
		return None	
	return {k: counters[k].value for k in counters}

def serializeCardMarkers(card):
	if len(card.markers) == 0:
		return None
	markers = []
	for id in card.markers:
		markers.append({'name': id[0], 'model': id[1], 'qty': card.markers[id]})
	return markers

def deserializePlayer(plData):
	if plData is None or len(plData) == 0:
		return
		
	players = [x for x in getPlayers() if x._id == plData['_id'] ]
	if players == None or len(players) == 0:
		return
		
	player = players[0]
	
	if player is None:
		return
	
	if plData['hand'] is not None and len(plData['hand']) > 0:
		if player != me:
                        for c in plData['hand']:
                                remoteCall(player, "deserializePile2", [c['model'], player.hand, player])
			remoteCall(player, "deserializePile", [plData['hand'], player.hand, player])
		else:
			deserializePile(plData['hand'], player.hand)
	
	if plData['piles'] is not None and len(plData['piles']) > 0:
		for k in plData['piles'].Keys:
			if k not in player.piles:
				continue
			deserializePile(plData['piles'][k], player.piles[k], player)

def deserializePile(pileData, group, who = me):
	if pileData is None or len(pileData) == 0:
		return
	if group != shared and who != me and group.controller != me:
		remoteCall(who, "deserializePile", [pileData, group, who])
	else:
		for c in pileData:
			card = group.create(c['model'])
