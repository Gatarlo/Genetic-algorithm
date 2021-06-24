# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 08:12:00 2021
ps : c'est mon anniversaire aujourd'hui, souyez gentil (~￣▽￣)~  ヽ(*ﾟｰﾟ*)ﾉ  ~(￣▽￣~)
@author: Audenaert Arthur
"""

from random import random
from string import printable
 
# lambda pour choisir aléatoirement un élément, plus efficace que random.choice(x).
choice = lambda x: x[int(random() * len(x))]
 
# Configuration.
phrase_attendue = "Chtholly Nota Seniorius est la meilleure waifu !"
# Pourcentage (entre 0.0 = 0% et 1.0 = 100%) de chance qu'une mutation arrive.
chance_de_mutation = 0.1
# pourçentage de chance qu'un individu "mieux adapté" soit retenu pour la generation suivante.
pourcentage_de_retenue_des_plus_adaptes = 0.2
# pourcentage de chance qu’un individu « moins adapté » soit retenu pour la génération suivante.
pourcentage_de_retenue_des_moins_adaptes = 0.05
# Nombre d'individus dans la population.
compte_de_population = 100
# Nombre max de générations avant de couper le script (ou que je m'impatiente).
nombre_de_generations_max = 100000

#___________________________________________________
 
# Le nombre d’individus « hauts gradés » à retenir.
nombre_d_adaptes_a_retenir = int(compte_de_population * pourcentage_de_retenue_des_plus_adaptes) 
# La taille de la chaîne de caractères à deviner.
taille_de_la_phrase_attendue = len(phrase_attendue)
# La moitié de la taille de la chaîne de caractères à deviner.
moitié_de_taille_de_la_phrase_attendue = taille_de_la_phrase_attendue // 2
caracteres_autorises = printable
# Adaptabilité max atteignable.
adaptabilite_max = taille_de_la_phrase_attendue
 
# Code de l'Algorithme
 
def get_random_char():
    # Retourne un caractère aléatoire depuis la liste de caractères autorisés
    return choice(caracteres_autorises)
     
 
def get_random_individu():
    # Retourne un individu (un tableau de caractères) constitué de caractères aléatoires générés par la fonction ci-dessus.
    return [get_random_char() for _ in range(taille_de_la_phrase_attendue)]
 
 
def get_random_population():
    # Retourne une population faite d’individus aléatoires.
    return [get_random_individu() for _ in range(compte_de_population)]
 
 
def get_individu_adaptabilite(individu):
    # Pour chaque caractère au bon endroit on incrémente le adaptabilite de 1.
    adaptabilite = 0
    for c, c_atendu in zip(individu, phrase_attendue):
        if c == c_atendu:
            adaptabilite += 1
    return adaptabilite
 
 
def average_population_grade(population):
    # Retourne le adaptabilite moyen de la population
    total = 0
    for individu in population:
        total += get_individu_adaptabilite(individu)
    return total / compte_de_population
 
 
def grade_population(population):
    # adaptabilite la population à partire d'un tuple (individu, adaptabilite) trié du plus adapté ou moins adapté en fonction de leurs adaptabilites.
    graded_individu = []
    for individu in population:
        graded_individu.append((individu, get_individu_adaptabilite(individu)))
    return sorted(graded_individu, key=lambda x: x[1], reverse=True)
 

def evolve_population(population):
    # Evolution de la population vers la génération suivante.
 
    # Obtentions des infividus triés par adaptabilite, et génère une liste des individus triés des meilleurs aux pires.
    raw_population_adaptabilitee = grade_population(population)
    adaptabilite_moyenne = 0
    solution = []
    population_adaptabilitee = []
    for individu, adaptabilite in raw_population_adaptabilitee:
        adaptabilite_moyenne += adaptabilite
        population_adaptabilitee.append(individu)
        if adaptabilite == adaptabilite_max:
            solution.append(individu)
    adaptabilite_moyenne /= compte_de_population
 
    # Si un ou des individus de notre population ont atteint le meilleur niveau d’optimisation,
    # on retourne la population telle quelle avec la valeur moyenne d'adaptabilité et la liste des individus mentionnés juste avant.
    if solution:
        return population, adaptabilite_moyenne, solution    
 
    # Si aucun individu n'a atteint le meilleur niveau, on garde les plus adaptés
    parents = population_adaptabilitee[:nombre_d_adaptes_a_retenir]
 
    # Ajoute de nouveaux individus aléatoires pour la génération suivante (et conserver une diversité génétique)
    for individu in population_adaptabilitee[nombre_d_adaptes_a_retenir:]:
        if random() < pourcentage_de_retenue_des_moins_adaptes:
            parents.append(individu)
 
    # Mutations d'individus sélectionnés aléatoirement
    for individu in parents:
        if random() < chance_de_mutation:
            place_to_modify = int(random() * taille_de_la_phrase_attendue)
            individu[place_to_modify] = get_random_char()
 
    # Croisement aléatoire des individus de la liste afin d’obtenir une population de taille fixe.
    parents_len = len(parents)
    desired_len = compte_de_population - parents_len
    enfants = []
    while len(enfants) < desired_len:
        pere = choice(parents)
        mere = choice(parents)
         # Peut générer une boucle infinie. Signe que la population est trop petite ou que le pourcentage d'adaptés conservés entre chaque génération est trop élevé.
         # Il faut trouver le bon pourcentage / nombre d'individus si c'est le cas.
        if pere != mere:
            enfant = pere[:moitié_de_taille_de_la_phrase_attendue] + mere[moitié_de_taille_de_la_phrase_attendue:]
            enfants.append(enfant)
 
    # Retourne la nouvelle génération
    parents.extend(enfants)
    return parents, adaptabilite_moyenne, solution
 
 
# Execution
 
def main():

    # Génération d'une nouvelle population, calcul de son adaptabilité moyenne.
    population = get_random_population()
    adaptabilite_moyenne = average_population_grade(population)
    print('Adaptabilité d\'origine : %.2f' % adaptabilite_moyenne, '/ %d' % adaptabilite_max)
 
    # Evolution de la population tant qu'aucune solution n'a été trouvée, ou que la limite des génération est atteinte.
    i = 0
    solution = None
    log_avg = []
    while not solution and i < nombre_de_generations_max:
        population, adaptabilite_moyenne, solution = evolve_population(population)
        if i & 255 == 255:
            print('Adaptabilité actuelle : %.2f' % adaptabilite_moyenne, '/ %d' % adaptabilite_max, '(%d génération)' % i)
            tempResult = ''.join(str(p) for p in population[-1])
            print(tempResult + '\n')
        if i & 31 == 31:
            log_avg.append(adaptabilite_moyenne)
        i += 1
 
    #Graphique 
    import pygal
    graphique = pygal.Line(show_dots=True, show_legend=True)
    graphique.title = 'Evolution de l\'aptabilite'
    graphique.x_title = 'Generations'
    graphique.y_title = 'Adaptabilité'
    graphique.add('Adaptabilité', log_avg)
    graphique.render_to_file('Graphique.svg')
    graphique.render_to_png('Graphique.png')

    # Statistiques finales
    adaptabilite_moyenne = average_population_grade(population)
    print('Adaptabilité finale : %.2f' % adaptabilite_moyenne, '/ %d' % adaptabilite_max)
    result = ''.join(str(s) for s in solution[-1])
    print(result)
 
    # Affichage Solution
    if solution:
        print('Solution trouvée (%d times) après %d générations.' % (len(solution), i))
    else:
        print('Aucune solution trouvée après %d générations.' % i)
        print('- La dernière population était :')
        for number, individu in enumerate(population):
            print(number, '->',  ''.join(individu))
 
 
if __name__ == '__main__':
    main()