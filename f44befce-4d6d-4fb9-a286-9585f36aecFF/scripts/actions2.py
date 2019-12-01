import re

CounterMarker =("Damage", "0f74413d-45d6-4c52-b584-201b99af4125")

####################################################
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        if x != "Silent":
            notify('{} taps {}.'.format(me, card))
    else:
        if x != "Silent":
            notify('{} untaps {}.'.format(me, card))	

def untapAll(group, x = 0, y = 0): #Modified it to account for Energy which will be played upside down
	mute()
	for card in group:
		if not card.owner == me:
			continue
		if card.orientation == Rot90:
			card.orientation = Rot0
		if card.orientation == Rot270:
			card.orientation = Rot180
	notify("{} untaps all their cards.".format(me))			

def awaken(card, x = 0, y = 0): 
	mute()
##	notify(str(card.alternates))
##	notify(card.alternate)
	if card.alternate == card.alternates[0]:
            try:
                card.alternate = 'bot'
                notify("{}'s' {} switches to its Bot Mode.".format(me, card))
                card.Type = "Character"
            except:
                whisper("Sorry, something went wrong.")
	elif card.alternate == card.alternates[1]:
            try:
                notify("yes")
                card.alternate = card.alternates[2]
                card.Type = "Character"
                notify("{}'s' {} switches to its {} Mode.".format(me, card, card.alternates[2]))
            except:
                try:
                    card.alternate = card.alternates[0]
                    notify("{}'s' {} switches to its Alt Mode.".format(me, card))
                except:
                    whisper("Sorry, something went wrong.")
        elif card.alternate == card.alternates[2]:
            try:
                card.alternate = card.alternates[0]
                notify("{}'s' {} switches to its Alt Mode.".format(me, card))
            except:
                whisper("Sorry, something went wrong.")

def wish(group, x = 0, y = 0):
    mute()
    if group == me.characters:
        guid, quantity = askCard({"Type":"Character"}, "or")
    else:
        guid, quantity = askCard({"Type":"Upgrade - Weapon", "Type":"Upgrade - Armor", "Type":"Upgrade - Utility", "Type":"Action"}, "or")
        group = me.hand
    if quantity == 0:
        return
    if quantity < 10:
        card = group.create(guid)
        notify("{} pulled {} from outside the game.".format(me, card))

def combiner(card, x = 0, y = 0):
    mute()
    try:
        card.alternate = "combiner"
        notify("{}'s {} switches to its Combiner Mode.".format(me, card))
    except:
        whisper("I'm sorry, it appears {} has no Combiner Mode.".format(card))

def unawaken(card, x = 0, y = 0): 
	mute()
	altName = card.alternateProperty('bot', 'name')
        card.alternate = ''
	notify("{}'s' {} switches to its Alr Mosw {}.".format(me, altName, card))
	return

def reshuffle(verbose=True):
    mute()
    if verbose == False:
        for card in me.Scrap:
            card.moveTo(me.Deck)
        shuffle(me.Deck)
        notify("{} reshuffles their Scrap pile into their Deck!".format(me))
    elif confirm("Are you sure you want to reshuffle your Scrap pile into your deck?"):
        for card in me.Scrap:
            card.moveTo(me.Deck)
        shuffle(me.Deck)
        notify("{} reshuffles their Scrap pile into their Deck!".format(me))

def botFaceDown(group = me.Deck, card=''):
    mute()
    card = me.Deck.bottom()
    card.moveToTable(0, 0, forceFaceDown = True)
    notify("{} places the bottom card of their deck on the table face down.".format(me))
    
	
def clearAll(group, x = 0, y= 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
		if card.controller == me:
			card.target(False)
			card.highlight = None

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))
		  
def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def discard(card, x = 0, y = 0): #Renamed
	card.moveTo(me.piles['Scrap'])
	notify("{} discards {}".format(me, card))

def addCounter(card, x = 0, y = 0):
	mute()
	notify("{} adds 1 counter to {}.".format(me, card))
	card.markers[CounterMarker] += 1

def removeCounter(card, x = 0 , y = 0):
	mute()
	notify("{} removes 1 counter to {}.".format(me, card))
	card.markers[CounterMarker] -= 1
	  
def setCounter(card, x = 0, y = 0):
	mute()
	quantity = askInteger("How many counters", 0)
	notify("{} sets {} counters on {}.".format(me, quantity, card))
	card.markers[CounterMarker] = quantity	
		
def play(card, x = 0, y = 0): #Extra Cards will go to Drop after being played
	mute()
	src = card.group
	if card.Type=="Extra": card.moveTo(card.owner.piles['Drop Zone'])
	elif me.id == 1:
                global xBattle
		xBattle += 75
		card.moveToTable(xBattle, 0)
	else:
                global XBattle2
                xBattle -= 75
                card.moveToTable(xBattle2, -90)
	notify("{} plays {} from their {}.".format(me, card, src.name))

def flip1(count=1):
    mute()
    flipMany(0,1)

def flipMany(group, count=None, w=0, o=0, b=0, g=0):
    mute()
    x = 0
    try:
        group + 1
        x = 1
    except:
        pass
    if count == None: count = askInteger("Flip how many cards?", 0)
    try:
        count += 1
        count -= 1
    except:
        return
    if len(me.Deck) == 0:
        reshuffle(False)
    while count > 0:
        card = me.Deck[0]
        if len(card.properties["White Pips"]) > 0 and w == 0 and x != 1:
            count += 2
        flipBattle(1, card)
        try:
            w += int(card.properties["White Pips"])
        except:
            pass
        try:
            o += int(card.properties["Orange Pips"])
        except:
            pass
        try:
            u += int(card.properties["Blue Pips"])
        except:
            pass
        try:
            g += int(card.properties["Green Pips"])
        except:
            pass
        try:
            b += int(card.properties["Black Pips"])
        except:
            pass
        if len(me.Deck) == 0:
            reshuffle(False)
        count -= 1
    notify("{} flips {} orange pips, {} blue pips {} white pips and {} green pips!".format(me, o, b, w, g))
    if group == 9:
        return(u)
        
def flipBattle(count=1, card=None):
    mute()
##    card.moveToTable(0,0)
    testing(card)
    card.orientation = Rot270        

def testing(card):
    mute()
    cardsInTable = [c for c in table if c.controller == me and c.orientation != Rot270 and c.orientation != Rot180]
    flippedCardsInTable = [c for c in table if c.controller == me and c.orientation == Rot270]
    if me._id == 1:
            x = -400
            for c in cardsInTable:
                    if c.position[0] >= (x - 150):
                            x = c.position[0] + 150
    else:
            x = 325
            for c in cardsInTable:
                    if c.position[0] < (x+150):
                            x = c.position[0] - 150
    if me._id == 1:
            y = 0
            for c in flippedCardsInTable:
                    if c.position[1] >= y:
                            y = c.position[1] + 10
    else:
            y = -75
            for c in flippedCardsInTable:
                    if c.position[1] <= y:
                            y = c.position[1] - 10
    card.moveToTable(x, y)
    if not me._id == 1:
        card.sendToFront()

def KO(card, x=0, y=0):
    mute()
    cardsInTable = [c for c in table if c.controller == me and c.orientation != Rot270 and c.orientation != Rot180]
    KOCardsInTable = [c for c in table if c.controller == me and c.orientation == Rot180]
    if me._id == 1:
        x = -400
        for c in cardsInTable:
            if c.position[0] >= (x - 150):
                x = c.position[0] + 350
    else:
            x = 325
            for c in cardsInTable:
                    if c.position[0] < (x+150):
                            x = c.position[0] - 350
    if me._id == 1:
            y = 0
            for c in KOCardsInTable:
                    if c.position[1] >= y:
                            y = c.position[1] + 20
    else:
            y = -75
            for c in KOCardsInTable:
                    if c.position[1] <= y:
                            y = c.position[1] - 20
    if KOCardsInTable:
        notify("Yes")
        x = KOCardsInTable[0].position[0]
    else:
        notify("No")
    card.moveToTable(x, y)
    card.orientation = Rot180
    card.sendToBack()

def unKO(card, x=0, y=0):
    mute()
    if me._id == 1:
        x = card.position[0] - 125
        y = 0
    else:
        x = card.position[0] + 125
        y = 75
    card.moveToTable(x, y)
    card.orientation = 0

def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	if group==me.piles["VP"]:
            notify("{} randomly discards {} from VP.".format(me,card.name))
        else:
        	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Scrap'])

def randomDraw(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} takes a random VP.".format(me))
        card.moveTo(card.owner.hand)

def draw(group, conditional = False, count = 1, x = 0, y = 0): #Added draw function to include choice
    mute()
    for i in range(0,count):
        if len(group) == 0:
            if group == me.Deck:
                reshuffle(False)
            else:
                return
        if conditional == True:
            choiceList = ['Yes', 'No']
            colorsList = ['#FF0000', '#FF0000']
            choice = askChoice("Draw a card?", choiceList, colorsList)
            if choice == 0 or choice == 2:
                return 
        card = group[0]
        card.moveTo(card.owner.hand)
        notify("{} draws a card.".format(me))

def drawMany(group, count = None):
	if len(group) == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 0)
	if count == None: count = 0
	for card in group.top(count): card.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, count))

def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()
  
def lookAtTopCards(num, targetZone='hand'): #Added function for looking at top X cards and take a card
    mute()
    notify("{} looks at the top {} cards of their deck".format(me,num))
    cardList = [card for card in me.Deck.top(num)]
    choice = askCard(cardList, 'Choose a card to take')
    toHand(choice, show = True)
    me.Deck.shuffle() 
	
def lookAtDeck(): #For Automation
    mute()
    notify("{} looks at their Deck.".format(me))
    me.Deck.lookAt(-1)

def sideboard(group=me.Deck, x = 0, y = 0):
    mute()
    topCards = []
    for c in me.Deck.top(100):
        topCards.append(c)
        c.peek()
    dlg = cardDlg(topCards)
    botCards = []
    for c in me.sideboard:
        botCards.append(c)
        c.peek()
    dlg = cardDlg(topCards, botCards)
    dlg.title = "Sideboarding"
    dlg.label = "Deck"
    dlg.bottomLabel = "Sideboard"
    dlg.text = "Move cards between your deck and sideboard."
    cards = dlg.show()
    for c in reversed(dlg.list):
        c.moveTo(me.Deck)
    for c in dlg.bottomList:
        c.moveTo(me.sideboard)
    me.Deck.visibility = "none"
    me.Sideboard.visibility = "Me"
