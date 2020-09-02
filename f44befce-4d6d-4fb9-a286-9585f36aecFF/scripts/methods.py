##File to store a list of cards with automation for the AI.
##Also includes the underlying functions.  May want to break those out later.

cardList = {
    'Zap': {abilityDamage: (True, 2)},
    'aiZap': {abilityDamage: (True, 2)},
    }


##Looks up a card's name in the cardList dictionary.  If present, executes one
##or more functions associated with that card using the listed parameters.
##Should raise an error instead of whispering an error message in the future.
def activate(card, x=0, y=0, silent = False):
    if card.Name in cardList:
        for f in cardList[card.Name]:
            f(*cardList[card.Name][f])
    else:
        if silent == False:
            whisper("This card doesn't have an automated ability yet.")

def abilityDamage(targted = False, DMG = 2, args*):
    mute()
    p = players[0]
    cards = [c for c in table if c.controller == p and "Character" in c.type and c.filler != "Neutral"]
    DMG = getAIDamage()
    d = 0
    if args[0] == True:
        for c in table:
          if c.markers[CounterMarker] > d:
            card = c
            d = c.markers[CounterMarker]
        if d == 0: card = cards[rnd(0,len(cards) - 1)]
    card = cards[rnd(0,len(cards) - 1)]
    card.markers[CounterMarker] += DMG
    message = "The AI uses its X technique to deal {} damage to {}".format(DMG, card.name)
    return(message)

def abilityDiscard(*args):
    mute()
    p = players[0]
    if len(p.hand) == 0: return(None)
    discardCard = p.hand.random()
    discardCard.moveTo(p.Scrap)
    message = "The AI uses its X technique to make you discard {}!".format(discardCard.name)
    return(message)

def abilityScrap(*args):
    mute()
    p = players[0]
    cards = [c for c in table if c.controller == p and "Upgrade" in c.type and c.filler != "Neutral"]
    if len(cards) == 0: return(None)
    scrapCard = cards[rnd(0,len(cards) - 1)]
    scrapCard.moveTo(p.Scrap)
    message = "The AI used its X technique and scrapped {}!".format(scrapCard.name)
    return(message)

def aiGainBold(count, *args):
    mute()
    global bold
    bold += count

def aiGainTough(count, *args):
    mute()
    global tough
    tough += count

def aiGainATK(count, *args):
    mute()
    global tempATK
    tempATK += count

def aiGainDEF(count, *args):
    mute()
    global tempDEF
    tempDEF += count

