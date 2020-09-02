import re
vsAI = False
cardsUndo = []

def onCardsMoved(args):
    mute()
    global cardsUndo
    cardsUndo.append(args)
    if len(cardsUndo) > 10:
        cardsUndo.pop(0)

def undo(args):
    mute()
    global cardsUndo
    if len(cardsUndo) == 0:
        whisper("Sorry, we have no saved card movements to undo.")
        return
    lastMove = cardsUndo.pop()
    index = 0
    for card in lastMove.cards:
        oldCoords = (lastMove.xs[index], lastMove.ys[index])
        newCoords = (card.position[0], card.position[1])
        group = lastMove.fromGroups[index]
        if group == table:
            card.moveToTable(oldCoords[0], oldCoords[1])
        else:
            card.moveTo(group)
        index += 1

def onGameStarted(*args):
    mute()
    if len(players) == 1:
        choiceList = ['Yes', 'No']
        colorsList = ['#FF0000', '#FF0000']
        playAI = askChoice("Would you like to play against an AI?", choiceList, colorsList)
        if playAI == 1:
            initSinglePlayer()

def initSinglePlayer(*args):
    mute()
    playAICharacters()
    for card in flipDeck:
        shared.Deck.create(card, 1)
    me.deck.shuffle()

def playAICharacters(*args):
    mute()
    AICharacters = getAICharacters()
    count = len(AICharacters)
    characters = AICharacters
    i = -1
    if count == 1:
        c = table.create(characters[0], -50, 150)
        c.filler = "Neutral"
        c.anchor = True
        return
    for card in characters:
        x = round(600/(count-1))*i + 250
        c = table.create(card, x, -150)
        c.filler = "Neutral"
        c.anchor = True
        i += 1

def onCardsMovedDeprecated(args):
    ##Effectively disables manual card movement unless player turns the AI off.
    ##vsAI is set to False to disable this as it is not in use at the moment.
    mute()
    global vsAI
    if vsAI == False:
        return
    choiceList = ['Yes', 'No']
    colorsList = ['#FF0000', '#FF0000'] 
    choice = askChoice("If you move cards manually, automation will break.  Continue?", choiceList, colorsList)
    if choice == 1:
        vsAI = False
        return
    index = 0
    for card in args.cards:
        oldCoords = (args.xs[index], args.ys[index])
        group = args.fromGroups[index]
        if args.fromGroups[index] != table:
            card.moveTo(group)
        else:
            card.moveToTable(oldCoords[0], oldCoords[1])
        index += 1

    
def declareAttack(atkCard, *args):
    mute()
##    if isinstance(card, list):
##        return
    if len(atkCard) > 1:
        notify("Please only select one card while attacking.")
        return
    atkCard = atkCard[0]

    defCardsInTable = [c for c in table if "Character" in c.type and c.filler == 'Neutral']
    c = 0
    for card in defCardsInTable:
        if card.targetedBy:
            defCard = card
            c += 1
            if c > 1:
                notify("Please only target one enemy at a time when attacking")
                return
    if c == 0:
        notify("Please select an enemy bot when making your attacks!")
        return
    message = "{} is attacking the enemy {}".format(atkCard.name, defCard.name)
    makeAttack(atkCard, defCard, message)
    
def makeAttack(atkCard, defCard, message = ""):
    mute()
    DEF = int(defCard.DEF) + defCard.markers[CounterMarkerDefense]
    notify(format(DEF))
    ATK = int(atkCard.ATK) + atkCard.markers[CounterMarkerAttack]
    atkFlip = askInteger(message + "\n\n" + "How many cards should you flip for your attack?", 2)
    if atkFlip == None:
        notify("Please make sure you select a value next time")
        return
    atkCard.orientation = Rot90
    flippedOrange = flipMany(8, atkFlip)
    ATK += flippedOrange

    flippedBlue = aiFlipDefense()
    DEF = int(defCard.DEF) + defCard.markers[CounterMarkerDefense]
    DEF += flippedBlue
    DEF += tempDEF

    DMG = ATK - DEF
    DMG = max(DMG, 0)

    message = "{} attacks {} with {} total ATK against a DEF of {}, dealing {} damage.".format(atkCard.name, defCard.name, ATK, DEF, DMG)
    notify(message)
    
    if DMG > 0:
        dealDamage(defCard, DMG)
##        defCard.markers[CounterMarker] += DMG
    

def aiDeclareAttack(*args):
    mute()
    abilityMessage = args[0]
    atkCards = atkCardsInTable()
    if len(atkCards) == 0:
        notify("The AI has no available attackers!")
        return
    if len(atkCards) == 1:
        atkCard = atkCards[0]
    else:
        atkCard = atkCards[rnd(0,len(atkCards) - 1)]

    defCards = defCardsInTable()
    if len(defCards) == 0:
        notify("No available defenders!")
        return
    if len(defCards) == 1:
        defCard = defCards[0]
    else:
        defCard = defCards[rnd(0,len(defCards) - 1)]
      
    aiMakeAttack(atkCard, defCard, abilityMessage)

def aiMakeAttack(atkCard, defCard, abilityMessage = ""):
    mute()
    ATK = int(atkCard.ATK)
    flippedOrange, flippedBlack = aiFlipAttack()
    ATK += flippedOrange
    ATK += tempATK
    DEF = int(defCard.DEF) + defCard.markers[CounterMarkerDefense]
    pierce += flippedBlack
    message = abilityMessage + "\n\n" + "{} attacks {} with {} total ATK against a DEF of {} with a Pierce of {}".format(atkCard.name, defCard.name, ATK, DEF, pierce)
##    atkCard.orientation = Rot90

    defFlip = askInteger(message + "\n\n" + "How many cards should you flip for defense?", 2)
    atkCard.orientation = Rot90
    if defFlip == None:
        return
    b = flipMany(9, defFlip)
    DEF += b
    DMG = ATK - DEF
    DMG = max(DMG, 0)
    DMG = max(DMG, max(ATK, pierce))
    notify("{} deals {} damage to {}".format(atkCard, DMG, defCard))
    if DMG > 0:
        aiDealDamage(defCard, DMG)

def aiDealDamage(defCard, DMG):
    mute()
    defCard.markers[CounterMarker] += DMG

def dealDamage(defCard, DMG):
    mute()
    defCard.markers[CounterMarker] += DMG
    if int(defCard.markers[CounterMarker]) >= int(defCard.HP):
        koAICard(defCard)
        return
    defCard.target(False)

def koAICard(defCard):
    mute()
    notify("You KO'd {}!".format(defCard))
    defCard.delete()
    defCardsInTable = [c for c in table if "Character" in c.type and c.filler == 'Neutral']
    if len(defCardsInTable) == 0:
        victory()

def victory(*args):
    message = "You've beaten the AI, congratulations!"
    notifyBar("#FF0000", message)
    aiFlippedCardsRemove()

def aiFlipAttack(count = 2):
    orange = 0
    black = 0
    for i in range(count + bold):
        if len(shared.Deck) == 0:
            reshuffleAI()
        c = shared.Deck.top()
        c.moveToTable(325, i * 10 - 150)
        c.orientation = Rot90
        c.sendToFront()
        c.filler = "Neutral"
        try:
            orange += int(c.properties["Orange Pips"])
        except:
            pass    
        try:
            black += int(c.properties["Black Pips"])
        except:
            pass    
    return(orange, black)

def aiFlipDefense(count = 2):
    blue = 0
    for i in range(count + tough):
        if len(shared.Deck) == 0:
            reshuffleAI()
        c = shared.Deck.top()
        c.moveToTable(325, i * 10 - 150)
        c.orientation = Rot90
        c.sendToFront()
        c.filler = "Neutral"
        try:
            blue += int(c.properties["Blue Pips"])
        except:
            pass    
    return(blue)

def atkCardsInTable(*args):
    mute()
    p = players[0]
    cards = [c for c in table if "Character" in c.type and c.filler == 'Neutral' and c.orientation == Rot0]
    return(cards)

def defCardsInTable(*args):
    mute()
    p = players[0]
    cards = [c for c in table if c.controller == p and "Character" in c.type and c.filler != "Neutral"]
    tappedCards = [c for c in cards if c.orientation == Rot90]
    untappedCards = [c for c in cards if c.orientation == Rot0]
    if len(tappedCards) > 0:
        cards = tappedCards
    else:
        cards = untappedCards
    return(cards)

def overrideTurnPassed(args):
    mute()
##    global vsAI
##    if vsAI == False:
##        nextTurn(args.player)
##        return
    turnCleanUp()
    aiTurn()
##    turnCleanUp()

def turnCleanUp(*args):
    mute()
    global bold, tough, tempATK, tempDEF
    cards = [c for c in table if c.controller == me and "Character" not in c.type and c.orientation == Rot270 and c.filler != "Neutral"]
    for card in cards: card.moveTo(me.scrap)
    bold = 0
    tough = 0
    tempATK = 0
    tempDEF = 0
    
def aiTurn(*args):
    mute()
##    notify("This is where the AI will do stuff!")
    if aiCardsUntap() == False:
        return
    aiFlippedCardsRemove()
    aiPlayCardsMessage = aiPlayCards()
    aiDeclareAttack(aiPlayCardsMessage)
    aiFlippedCardsRemove()
    nextTurn(me)

def passTurn(*args):
    overrideTurnPassed(me)

def aiFlippedCardsRemove(*args):
    mute()
    for card in table:
        if card.filler == "Neutral" and card.orientation == Rot90 and "Character" not in card.type:
            card.moveTo(shared.Scrap)
    shared.Deck.shuffle()

def aiCardsUntap(*args):
    untappedAICards = [card for card in table if card.filler == "Neutral" and card.orientation == Rot0]
    tappedAICards = [card for card in table if card.filler == "Neutral" and card.orientation == Rot90]
    if len(untappedAICards) == 0:
        if confirm("The AI is wanting to untap and start a new turn.  Proceed?"):
            for card in table:
                if card.orientation == Rot90 and card.filler == "Neutral" and "Character" in card.type:
                    card.orientation = Rot0
                    untapAll(table)
        else:
            return(False)
        notify("You and the AI untap your bots!")

def aiPlayCards(*args):
    mute()
##    cardChosen = aiGetCard()
    aiPlayCardsMessage = aiGetCard()
    return(aiPlayCardsMessage)

def aiGetCard(*args):
    ##Creating a few custom actions to simulate "cards" the AI can play.
    ##Should move command execution to aiPlayCards() function.
    ##Should modularize the command selection to allow arbitrary lists to be provided..
    mute()
    actionsAI = ["Scrap", "Discard", "Damage"]
    actionsAI = getAIActions(1)
    actionNumber = rnd(0,len(actionsAI) - 1)
    for action in actionsAI[actionNumber:]:
        if action == "Draw":
            message = aiDraw()
            if message is not None:
                return(message)
        if action == "Scrap":
            message = abilityScrap()
            if message is not None:
                return(message)
        if action == "Discard":
            message = abilityDiscard()
            if message is not None:
                return(message)
        if action == "Damage":
            message = abilityDamage(True)
            return(message)
    return("The AI was unable to perform any special actions this turn.")

def getAIDamage(*args):
    ##Temporarily assigning a static value for all DMG abilities.
    ##Could expand to allow RNG or even modifiers based on difficultly setting.
    return(2)

def reshuffleAI(*args):
    mute()
    for card in shared.Scrap:
        card.moveTo(shared.Deck)
    shuffle(shared.Deck)
    notify("The AI reshuffles their Scrap pile into their Deck!")
