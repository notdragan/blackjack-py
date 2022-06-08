from copy import deepcopy
import pyxel, random

wnd = {"largeur":128, "hauteur":128, "titre":"Blackjack"}

pyxel.init(wnd["largeur"], wnd["hauteur"], wnd["titre"])

symboles = ["♥", "♦", "♣", "♠"]

valeurs = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def generer_paquets(x:int)->list:
    global symboles, valeurs
    tab = []
    for h in range(x):
        temp_paquets = []
        for i in range(len(symboles)):
            for j in range(len(valeurs)):
                temp_paquets.append({symboles[i]:valeurs[j]})
        tab.append(temp_paquets)
    return tab

def tirer_carte_hasard(paquets:list)->tuple:
    # prend un paquet au hasard
    indice_paquets_rdm = random.randint(0,len(paquets)-1)
    paquet_random = paquets[indice_paquets_rdm]

    # prend une carte random parmis le paquet choisit au hasard précedemment
    indice_carte_rdm = random.randint(0,len(paquet_random)-1)
    carte_random = paquet_random[indice_carte_rdm]

    symbole = list(carte_random)[0]
    valeur = list(dict(carte_random).values())[0]

    return (carte_random,paquet_random,indice_carte_rdm,indice_paquets_rdm,(symbole,valeur)) # carte:tuple, paquet_random:list, indice_paquets_rdm:int, (symbole,valeur):tuple(str,str)

temp_paquets = generer_paquets(10)
paquets = deepcopy(temp_paquets)

statut = 0 # distribution: 0 = joueur, 1 = ordi, 2 = choix, 3 = fin / resultat

joueurs = {"joueur_total":0, "joueur_symbole_courant":"", "joueur_carte_courant":"", "joueur_nb_cartes":0, "joueur_cartes":[], "ordi_total":0, "ordi_symbole_courant":"", "ordi_carte_courant":"", "ordi_nb_cartes":0, "ordi_cartes":[]}

points = {"joueur":0, "ordi":0}

def player_play(carte_hasard_joueur):
    # check valeurs, remplacement si besoin
    if (carte_hasard_joueur[4][1]) == "A" and joueurs["joueur_total"] > 10:
        joueurs["joueur_total"] = joueurs["joueur_total"]  + 1 # A -> 1
    elif (carte_hasard_joueur[4][1]) == "A":
        joueurs["joueur_total"] = joueurs["joueur_total"]  + 11 # A -> 1
    elif (carte_hasard_joueur[4][1]) == "J":
        joueurs["joueur_total"] = joueurs["joueur_total"] + 10 # J -> 10
    elif (carte_hasard_joueur[4][1]) == "Q":
        joueurs["joueur_total"] = joueurs["joueur_total"] + 10 # Q -> 10
    elif (carte_hasard_joueur[4][1]) == "K":
        joueurs["joueur_total"] = joueurs["joueur_total"] + 10 # K -> 10
    else:
        joueurs["joueur_total"] = joueurs["joueur_total"] + int(carte_hasard_joueur[4][1])
        
    joueurs["joueur_nb_cartes"] = joueurs["joueur_nb_cartes"] + 1

    # symbole affichage
    joueurs["joueur_carte_courant"] = carte_hasard_joueur[4][1]
    joueurs["joueur_symbole_courant"] = carte_hasard_joueur[4][0]
    joueurs["joueur_cartes"] = joueurs["joueur_cartes"] + [[carte_hasard_joueur[4][0], carte_hasard_joueur[4][1]]]

    #retire carte du paquet
    carte_hasard_joueur[1].pop(carte_hasard_joueur[2])
    
def bot_play(carte_hasard_ordi):
    # ordi, jeu
    if (carte_hasard_ordi[4][1]) == "A" and joueurs["ordi_total"] >= 11:
        joueurs["ordi_total"] = joueurs["ordi_total"]  + 1 # A -> 1
    elif (carte_hasard_ordi[4][1]) == "A" and joueurs["ordi_total"] < 11:
        joueurs["ordi_total"] = joueurs["ordi_total"] + 11 # A -> 11
    elif (carte_hasard_ordi[4][1]) == "J":
        joueurs["ordi_total"] = joueurs["ordi_total"] + 10 # J -> 10
    elif (carte_hasard_ordi[4][1]) == "Q":
        joueurs["ordi_total"] = joueurs["ordi_total"] + 10 # Q -> 10
    elif (carte_hasard_ordi[4][1]) == "K":
        joueurs["ordi_total"] = joueurs["ordi_total"] + 10 # K -> 10
    else:
        joueurs["ordi_total"] = joueurs["ordi_total"] + int(carte_hasard_ordi[4][1])
        
    joueurs["ordi_nb_cartes"] = joueurs["ordi_nb_cartes"] + 1

    # symbole affichage
    joueurs["ordi_carte_courant"] = carte_hasard_ordi[4][1]
    joueurs["ordi_symbole_courant"] = carte_hasard_ordi[4][0]
    joueurs["ordi_cartes"] = joueurs["ordi_cartes"] + [[carte_hasard_ordi[4][0], carte_hasard_ordi[4][1]]]
 
    #retire carte du paquet
    list(carte_hasard_ordi[1]).pop(carte_hasard_ordi[2])
    
def resultat(joueur_total, ordi_total)->int:
    # 1 = joueur, 2 = ordi, 3 = égalité
    if statut == 3:
        if joueur_total > ordi_total:
            if joueur_total <= 21:
                return "joueur"
            else:
                return "ordi"
        elif ordi_total > joueur_total:
            if ordi_total <= 21:
                return "ordi"
            else:
                return "joueur"
        else:
            return "egalite"
    else:
        return 0

finish_with_bot = False

simple_hit = False

recommencer = False

def reset_values_and_restart():
    global joueurs, recommencer, statut, finish_with_bot, simple_hit
    
    joueurs["joueur_total"] = 0
    joueurs["ordi_total"] = 0
    
    joueurs["joueur_carte_courant"] = ""
    joueurs["ordi_carte_courant"] = ""
    
    joueurs["joueur_symbole_courant"] = ""
    joueurs["ordi_symbole_courant"] = ""
    
    joueurs["joueur_nb_cartes"] = 0
    joueurs["ordi_nb_cartes"] = 0
    
    joueurs["joueur_cartes"] = []
    joueurs["ordi_cartes"] = []
    
    statut = 0
    finish_with_bot = False
    simple_hit = False
    
    recommencer = False
    
def update():
    global paquets, statut, points, finish_with_bot, simple_hit, recommencer

    if not(recommencer):
        if statut == 0:
            if not(finish_with_bot):
                # tire carte hasard joueur
                carte_hasard_joueur = tirer_carte_hasard(paquets)
                player_play(carte_hasard_joueur) # met a jour le score du joueur
                if joueurs["joueur_total"] > 21 or (joueurs["joueur_nb_cartes"] == 2 and joueurs["joueur_total"] == 21) or joueurs["joueur_total"] == 21:
                    finish_with_bot = True
                    simple_hit = False
            
            if joueurs["ordi_nb_cartes"] == 1 and simple_hit:
                statut = 2
                
            # tire carte hasard ordi
            if statut != 2:
                if finish_with_bot: # le joueur a fini de tirer ses cartes, le croupier tire les siennes (jusqu'a 17).
                    if joueurs["ordi_total"] < 17 and joueurs["joueur_total"] <= 21: 
                        carte_hasard_ordi = tirer_carte_hasard(paquets)
                        bot_play(carte_hasard_ordi) # met a jour le score de l'ordi
                    else:
                        statut = 3
                else: # le bot tire sa première carte
                    carte_hasard_ordi = tirer_carte_hasard(paquets)
                    bot_play(carte_hasard_ordi) # met a jour le score de l'ordi
                
                result = resultat(joueurs["joueur_total"], joueurs["ordi_total"]) # obtient le resultat du round si le joueur a fini de jouer

                if result == "joueur":
                    points["joueur"] = points["joueur"] + 1
                    
                elif result == "ordi":
                    points["ordi"] = points["ordi"] + 1
                else:
                    pass #egalite, rien a faire, peu importe si egalite ou round pas termine
            
            simple_hit = True
                    
                

        if statut == 2:
            if pyxel.btnr(pyxel.KEY_KP_PLUS):
                statut = 0 # relance le tirage
                simple_hit = True # mais avec comme consigne une simple carte pour le joueur (passe l'étape du croupier)
            elif pyxel.btnr(pyxel.KEY_KP_MINUS):
                simple_hit = False # ne fait pas qu'un simple tirage
                finish_with_bot = True # mais un tirage avec uniquement le bot
                statut = 0 # et le relance ici
        
        if statut == 3:
            recommencer = True
            
    else:
        if pyxel.frame_count % 240 == 0:
            reset_values_and_restart()

def draw():
    global joueurs, finish_with_bot
    
    pyxel.cls(0)
    
    pyxel.text(0,0, "points : Player = " + str(points["joueur"]) + ", Banker = " + str(points["ordi"]), 7)
    
    pos_x_j = 15
    pos_y_j = 15
    for i in range(len(joueurs["joueur_cartes"])):
        pyxel.rectb(pos_x_j-1, pos_y_j+1, 15, 15*2, 1)
        pyxel.rect(pos_x_j, pos_y_j, 15, 15*2, 7)
        pyxel.text(pos_x_j + 2, pos_y_j + 2, joueurs["joueur_cartes"][i][1], 8)
        pyxel.text(pos_x_j + 10, pos_y_j + 23, joueurs["joueur_cartes"][i][1], 8)
        pos_x_j += 20
    
    
    
    pos_x_o = 15
    pos_y_o = pos_y_j + 55
    for i in range(len(joueurs["ordi_cartes"])):
        pyxel.rectb(pos_x_o-1, pos_y_o+1, 15, 15*2, 1)
        pyxel.rect(pos_x_o, pos_y_o, 15, 15*2, 7)
        pyxel.text(pos_x_o + 2, pos_y_o + 2, joueurs["ordi_cartes"][i][1], 8)
        pos_x_o += 20
    
    if not(finish_with_bot):
        pyxel.text(20, pos_y_j + 35, "Votre total : " + str(joueurs["joueur_total"]), 4)
        pyxel.text(20, pos_y_o + 35, "Total de la banque : " + str(joueurs["ordi_total"]), 7)
    else:
        pyxel.text(20, pos_y_j + 35, "Votre total : " + str(joueurs["joueur_total"]), 7)
        pyxel.text(20, pos_y_o + 35, "Total de la banque : " + str(joueurs["ordi_total"]), 4)

pyxel.run(update, draw)
