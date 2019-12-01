import re
vsAI = False

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
    ##testDeck is the name of a sample deck intended to be loaded from a data file
    ##Coud add other decks and code to choose between them.
##    loadTable("Yes", testDeck)
    ##May not use this approach.  For now, manually create a cards for the AI.
    c = table.create("a881606a-5e32-4406-a61c-811a9122cf58", 0, -150, 1, False)
    c.filler = "Neutral"
    ##card.filler is currently used to track who cards belong to.
    c = table.create("a881606a-5e32-4406-a61c-811a9122cf58", 150, -150, 1, False)
    c.filler = "Neutral"
    c.anchor = True
    me.deck.shuffle()

def onCardsMoved(args):
    ##Effectively disables manual card movement unless player turns the AI off.
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
    
def declareAttack(*args):
    mute()
    atkCardsInTable = [c for c in table if c.controller == me and Character in c.type]
    dlg = cardDlg(atkCardsInTable)
    dlg.max = 1
    cardsSelected = dlg.show()
    if cardsSelected:
        for card in cardsSelected:
            notify("{} was selected to attack!".format(card))

    defCardsInTable = [c for c in table if c.controller != me and "Character" in c.type]
    if len(defCardsInTable) > 1:
        dlg = cardDlg(defCardsInTable)
        dlg.max = 1
        cardsSelected = dlg.show()
        if cardsSelected:
            for card in cardsSelected:
                notify("{} was selected as the target of the attack!".format(card))
    elif len(defCardsInTable) == 1:
        card = defCardsInTable[0]
        notify("{} was selected as the target of the attack!".format(card))

def aiDeclareAttack(*args):
    mute()
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
      
    aiMakeAttack(atkCard, defCard)

def aiMakeAttack(atkCard, defCard):
    mute()
    ATK = int(atkCard.ATK)
    flippedOrange = aiFlipAttack()
    ATK += flippedOrange
    notify("{} attacks {} with {} total ATK.".format(atkCard, defCard, ATK))
    atkCard.orientation = Rot90

    DEF = askInteger("What is {}'s current DEF?".format(defCard.name), 1)
    if DEF == None:
        return
    defFlip = askInteger("How many cards should you flip for defense?", 2)
    if defFlip == None:
        return
    b = flipMany(9, defFlip)
    DEF += b
    notify("{} deals {} damage to {}".format(atkCard, ATK-DEF, defCard))
    if ATK - DEF > 0:
        defCard.markers[CounterMarker] += ATK-DEF

def aiFlipAttack(count = 2):
    orange = 0
    for i in range(count):
        guid = flipDeck[rnd(0,len(flipDeck) - 1)]
        c = table.create(guid, 325, i * 10 - 150)
        c.orientation = Rot90
        c.sendToFront()
        c.filler = "Neutral"
        try:
            orange += int(c.properties["Orange Pips"])
        except:
            pass
    return(orange)

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
    aiTurn()

def aiTurn(*args):
    mute()
##    notify("This is where the AI will do stuff!")
    aiFlippedCardsRemove()
    aiCardsUntap()
    aiPlayCards()
    aiDeclareAttack()
    aiFlippedCardsRemove()
    nextTurn(me)

def aiFlippedCardsRemove(*args):
    mute()
    for card in table:
        if card.filler == "Neutral" and card.orientation == Rot90 and "Character" not in card.type:
            card.delete()

def aiCardsUntap(*args):
    untappedAICards = [card for card in table if card.filler == "Neutral" and card.orientation == Rot0]
    tappedAICards = [card for card in table if card.filler == "Neutral" and card.orientation == Rot90]
    if len(untappedAICards) == 0:
        for card in table:
            if card.orientation == Rot90 and card.filler == "Neutral" and "Character" in card.type:
                card.orientation = Rot0
        if not confirm("The AI is untapping to start a new turn.  Proceed?"):
            for card in tappedAICards:
                card.orientation = Rot90
        notify("The AI untaps its characters to start a new turn!")

def aiPlayCards(*args):
    mute()
    cardChosen = aiGetCard()
    return

def aiGetCard(*args):
    mute()
    return
