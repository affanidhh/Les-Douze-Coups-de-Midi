import random
import time
import json
import os
import sys

class Presentateur:
    def __init__(self, nom):
        self.nom = nom
        self.repliques = {
            'debut': [
                "Accrochez vos ceintures, on commence l'aventure !",
                "Attention les amis, le stylo est chaud et le jeu aussi !"
            ],
            'correct': [
                "Bonne réponse ! Même mon neveu de 5 ans aurait trouvé ça... enfin presque !",
                "Exact ! Vous êtes chaud comme un soleil d'août aujourd'hui ! 🔥"
            ],
            'incorrect': [
                "Oh la la... C'était {reponse} ! On va dire que c'était un piège !",
                "Non non non ! La réponse était {reponse}. Mais chut, je ne dirai rien à personne ! 🤫"
            ],
            'temps': [
                "Temps écoulé ! Plus lent qu'un escargot enrhumé ! 🐌",
                "Allez, on se réveille ! Le temps, c'est de l'argent ! 💰"
            ],
            'phase': [
                "Phase suivante ! Préparez les glaçons, ça va chauffer ! ❄️",
                "Attention aux oreilles, on passe à la vitesse supérieure ! 🚀"
            ],
            'etoile': [
                "L'Étoile Mystérieuse ! Le moment que tout le monde attend... surtout mon dentiste ! 😬",
                "C'est l'heure de vérité... Et de transpiration ! 💦"
            ],
            'elimination': [
                "C'est la fin du chemin pour {joueur}. On se revoit à la prochaine !",
                "{joueur}, vous êtes éliminé. Mais gardez le sourire ! 😊"
            ],
            'duel': [
                "C'est l'heure du duel final ! Qui sera le Maître de Midi ?",
                "Attention, ça va chauffer entre {joueur1} et {joueur2} ! 🔥"
            ]
        }

    def _random_replique(self, categorie, **kwargs):
        replique = random.choice(self.repliques[categorie])
        return replique.format(**kwargs) if kwargs else replique

    def annoncer_phase(self, nom_phase):
        print(f"\n{self.nom} : --- {nom_phase} ---")
        print(f"{self.nom} : {self._random_replique('phase')}")

    def annoncer_tour(self, nom_joueur):
        print(f"\n{self.nom} : {nom_joueur}, à vous de jouer !")

    def annoncer_resultat(self, resultat, question=None):
        if resultat:
            print(f"{self.nom} : {self._random_replique('correct')}")
        else:
            if question:
                reponse = question.options[question.reponse_correcte - 1]
                print(f"{self.nom} : {self._random_replique('incorrect', reponse=reponse)}")
            else:
                print(f"{self.nom} : {self._random_replique('temps')}")

    def annoncer_elimination(self, joueur):
        print(f"\n{self.nom} : {self._random_replique('elimination', joueur=joueur.nom)}")

    def annoncer_duel(self, joueur1, joueur2):
        print(f"\n{self.nom} : {self._random_replique('duel', joueur1=joueur1.nom, joueur2=joueur2.nom)}")

    def annoncer_etoile_mysterieuse(self, nom_joueur):
        print(f"\n{self.nom} : {nom_joueur}, vous allez maintenant tenter de découvrir l'Étoile Mystérieuse !")
        print(f"{self.nom} : Répondez correctement à au moins 3 questions sur 5 pour remporter l'étoile.")

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0

    def __str__(self):
        return f"{self.nom} : {self.score} points"

class Question:
    def __init__(self, enonce, options, reponse_correcte, difficulte, theme, explication):
        self.enonce = enonce
        self.options = options
        self.reponse_correcte = reponse_correcte
        self.difficulte = difficulte  # 1-3
        self.theme = theme
        self.explication = explication

    def poser(self, presentateur, joueur):
        presentateur.annoncer_tour(joueur.nom)
        print(f"\n[{self.theme}] {self.enonce}")
        for i, opt in enumerate(self.options, 1):
            print(f"{i}. {opt}")

        debut = time.time()
        try:
            reponse = int(input("\nVotre réponse (numéro) : "))
            temps = time.time() - debut
        except ValueError:
            presentateur.annoncer_resultat(False)
            return False

        temps_limite = 5 if self.difficulte == 1 else 7 if self.difficulte == 2 else 10
        if temps > temps_limite:
            print(f"\nTemps écoulé : {temps:.1f}s")
            presentateur.annoncer_resultat(False)
            return False

        if reponse == self.reponse_correcte:
            joueur.score += self.difficulte
            presentateur.annoncer_resultat(True)
            return True
        else:
            presentateur.annoncer_resultat(False, self)
            return False

class Jeu:
    def __init__(self):
        self.presentateur = Presentateur("Jean-Luc Reichmann")
        self.questions = self._charger_questions()
        self.scores = self._charger_scores()

    def _charger_questions(self):
        questions = [
            {"question": "Quelle est la capitale de la France?", "options": ["Paris", "Londres", "Berlin", "Madrid"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "Paris est la capitale de la France depuis le Moyen Âge."},
            {"question": "Quel est le plus grand océan?", "options": ["Atlantique", "Pacifique", "Indien", "Arctique"], "correct_option": 2, "difficulty": "facile", "theme": "Géographie", "explication": "Le Pacifique couvre plus de 165 millions de km²."},
            {"question": "Quel est le plus long fleuve du monde?", "options": ["Nil", "Amazone", "Yangtsé", "Mississippi"], "correct_option": 2, "difficulty": "moyen", "theme": "Géographie", "explication": "L'Amazone est le plus long fleuve avec environ 6 992 km."},
            {"question": "Qui a écrit 'Les Misérables'?", "options": ["Victor Hugo", "Émile Zola", "Gustave Flaubert", "Marcel Proust"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "Victor Hugo a publié 'Les Misérables' en 1862."},
            {"question": "Quelle est la planète la plus proche du soleil?", "options": ["Mercure", "Vénus", "Terre", "Mars"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "Mercure est la planète la plus proche du soleil."},
            {"question": "En quelle année a eu lieu la Révolution française?", "options": ["1789", "1776", "1804", "1815"], "correct_option": 1, "difficulty": "moyen", "theme": "Histoire", "explication": "La Révolution française a commencé en 1789."},
            {"question": "Quel est le symbole chimique de l'or?", "options": ["Au", "Ag", "Fe", "O"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "L'or a pour symbole Au (du latin 'Aurum')."},
            {"question": "Qui a peint la Joconde?", "options": ["Léonard de Vinci", "Michel-Ange", "Raphaël", "Donatello"], "correct_option": 1, "difficulty": "facile", "theme": "Art", "explication": "Léonard de Vinci a peint la Joconde au XVIe siècle."},
            {"question": "Quel est le plus grand désert du monde?", "options": ["Sahara", "Gobi", "Antarctique", "Kalahari"], "correct_option": 3, "difficulty": "difficile", "theme": "Géographie", "explication": "L'Antarctique est le plus grand désert froid."},
            {"question": "Quel est le plus haut sommet du monde?", "options": ["Everest", "K2", "Kangchenjunga", "Lhotse"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "L'Everest culmine à 8 848 mètres."},
            {"question": "Qui a découvert la pénicilline?", "options": ["Alexander Fleming", "Marie Curie", "Louis Pasteur", "Isaac Newton"], "correct_option": 1, "difficulty": "moyen", "theme": "Science", "explication": "Alexander Fleming a découvert la pénicilline en 1928."},
            {"question": "Quel est le plus grand mammifère marin?", "options": ["Baleine bleue", "Orque", "Dauphin", "Requin blanc"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "La baleine bleue peut mesurer jusqu'à 30 mètres."},
            {"question": "Quel est le plus petit pays du monde?", "options": ["Vatican", "Monaco", "Nauru", "San Marin"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "Le Vatican a une superficie de seulement 0,44 km²."},
            {"question": "Qui a écrit 'Le Petit Prince'?", "options": ["Antoine de Saint-Exupéry", "Jules Verne", "Albert Camus", "Jean-Paul Sartre"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "Antoine de Saint-Exupéry a publié 'Le Petit Prince' en 1943."},
            {"question": "Quelle est la capitale de l'Australie?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "correct_option": 3, "difficulty": "moyen", "theme": "Géographie", "explication": "Canberra est la capitale de l'Australie depuis 1908."},
            {"question": "Quel est le plus grand continent?", "options": ["Asie", "Afrique", "Amérique du Nord", "Europe"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "L'Asie couvre environ 44,58 millions de km²."},
            {"question": "Qui a inventé l'ampoule électrique?", "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Benjamin Franklin"], "correct_option": 1, "difficulty": "moyen", "theme": "Science", "explication": "Thomas Edison a breveté l'ampoule électrique en 1879."},
            {"question": "Quel est le plus grand pays du monde par superficie?", "options": ["Russie", "Canada", "Chine", "États-Unis"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "La Russie couvre plus de 17 millions de km²."},
            {"question": "Quel est le plus grand lac d'eau douce du monde?", "options": ["Lac Supérieur", "Lac Victoria", "Lac Baïkal", "Lac Tanganyika"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "Le Lac Supérieur a une superficie de 82 100 km²."},
            {"question": "Qui a écrit 'Roméo et Juliette'?", "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "Shakespeare a écrit 'Roméo et Juliette' vers 1595."},
            {"question": "Quel est le plus grand désert chaud du monde?", "options": ["Sahara", "Gobi", "Antarctique", "Kalahari"], "correct_option": 1, "difficulty": "difficile", "theme": "Géographie", "explication": "Le Sahara couvre environ 9,2 millions de km²."},
            {"question": "Quel est le plus grand pays d'Afrique?", "options": ["Algérie", "Nigeria", "Égypte", "Afrique du Sud"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "L'Algérie a une superficie de 2,38 millions de km²."},
            {"question": "Qui a découvert l'Amérique?", "options": ["Christophe Colomb", "Vasco de Gama", "Marco Polo", "Ferdinand Magellan"], "correct_option": 1, "difficulty": "facile", "theme": "Histoire", "explication": "Christophe Colomb a atteint l'Amérique en 1492."},
            {"question": "Quel est le plus grand volcan actif du monde?", "options": ["Mauna Loa", "Krakatoa", "Etna", "Vésuve"], "correct_option": 1, "difficulty": "difficile", "theme": "Géographie", "explication": "Le Mauna Loa, à Hawaï, est le plus grand volcan actif."},
            {"question": "Qui a écrit 'La Divine Comédie'?", "options": ["Dante Alighieri", "Geoffrey Chaucer", "John Milton", "Homer"], "correct_option": 1, "difficulty": "difficile", "theme": "Littérature", "explication": "Dante Alighieri a écrit 'La Divine Comédie' au XIVe siècle."}
        ]
        return [Question(q["question"], q["options"], q["correct_option"], self._convertir_difficulte(q["difficulty"]), q["theme"], q["explication"]) for q in questions]

    def _convertir_difficulte(self, difficulte):
        if difficulte == "facile":
            return 1
        elif difficulte == "moyen":
            return 2
        elif difficulte == "difficile":
            return 3
        return 1  # Par défaut

    def _charger_scores(self):
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                return json.load(f)
        return {}

    def _sauvegarder_scores(self):
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)

    def _afficher_scores(self, joueurs):
        print("\n--- Scores ---")
        for joueur in joueurs:
            print(joueur)

    def _eliminer_joueurs(self, joueurs):
        scores = [j.score for j in joueurs]
        if len(set(scores)) == 1:
            print("\nÉgalité ! Personne n'est éliminé.")
            return joueurs
        score_min = min(scores)
        return [j for j in joueurs if j.score > score_min]

    def duel_final(self, joueur1, joueur2):
        self.presentateur.annoncer_duel(joueur1, joueur2)
        questions_duel = [q for q in self.questions if q.difficulte == 3]
        random.shuffle(questions_duel)

        for question in questions_duel:
            self.presentateur.annoncer_tour(joueur1.nom)
            if question.poser(self.presentateur, joueur1):
                print(f"{joueur1.nom} marque {question.difficulte} point(s) !")
            else:
                print(f"{joueur1.nom} ne marque pas de point.")

            self.presentateur.annoncer_tour(joueur2.nom)
            if question.poser(self.presentateur, joueur2):
                print(f"{joueur2.nom} marque {question.difficulte} point(s) !")
            else:
                print(f"{joueur2.nom} ne marque pas de point.")

            self._afficher_scores([joueur1, joueur2])

            if joueur1.score > joueur2.score:
                return joueur1
            elif joueur2.score > joueur1.score:
                return joueur2

        # Si égalité après toutes les questions
        print("\nÉgalité parfaite ! Le gagnant est choisi aléatoirement.")
        return random.choice([joueur1, joueur2])

    def etoile_mysterieuse(self, gagnant):
        self.presentateur.annoncer_etoile_mysterieuse(gagnant.nom)
        print("Répondez correctement à au moins 3 questions sur 5 pour remporter l'étoile.")

        questions_etoile = [q for q in self.questions if q.difficulte == 3]
        random.shuffle(questions_etoile)
        questions_etoile = questions_etoile[:5]

        succes = 0
        for i, question in enumerate(questions_etoile, 1):
            print(f"\nQuestion {i}:")
            if question.poser(self.presentateur, gagnant):
                succes += 1

        if succes >= 3:
            print(f"\n⭐ {gagnant.nom} remporte l'Étoile Mystérieuse ! ⭐")
            return True
        else:
            print(f"\nDommage, {gagnant.nom}, vous n'avez pas réussi à découvrir l'Étoile Mystérieuse.")
            return False

    def initialiser_joueurs(self):
        # Le Maître de Midi (avec un avantage initial)
        maitre = Joueur("Dylan")  # Nom du Maître de Midi
        maitre.score = 2  # Par exemple, 2 victoires précédentes

        # 4 nouveaux candidats
        candidats = [Joueur("Amélie"), Joueur("Eve"), Joueur("Hannah"), Joueur("David")]

        # Liste complète des joueurs
        return [maitre] + candidats

    def jouer(self):
        # Initialisation des joueurs
        joueurs = self.initialiser_joueurs()
        print(f"\n{self.presentateur.nom} : {random.choice(self.presentateur.repliques['debut'])}")
        print(f"Aujourd'hui, nous retrouvons notre Maître de Midi en titre : {joueurs[0].nom}, qui cumule déjà {joueurs[0].score} victoires !")

        # Phases de jeu
        phases = [
            ("Coup d'Envoi", 1),
            ("Coup par Coup", 2),
            ("Coup Fatal", 3)
        ]

        for nom_phase, difficulte in phases:
            self.presentateur.annoncer_phase(nom_phase)
            questions_phase = [q for q in self.questions if q.difficulte == difficulte]
            
            for joueur in joueurs:
                question = random.choice(questions_phase)
                question.poser(self.presentateur, joueur)

            self._afficher_scores(joueurs)
            joueurs = self._eliminer_joueurs(joueurs)
            if len(joueurs) == 1:
                break

        # Finale
        if len(joueurs) > 1:
            gagnant = self.duel_final(joueurs[0], joueurs[1])
        else:
            gagnant = joueurs[0]

        print(f"\n{self.presentateur.nom} : Félicitations {gagnant.nom}, vous êtes le nouveau Maître de Midi ! 👑")
        
        if self.etoile_mysterieuse(gagnant):
            print(f"\n⭐ {gagnant.nom} remporte l'Étoile Mystérieuse ! ⭐")
        else:
            print("\nDommage... L'étoile reste mystérieuse ! 🌌")

if __name__ == "__main__":
    try:
        jeu = Jeu()
        
        if input("Mode entraînement ? (o/n) : ").lower() == 'o':
            jeu.mode_entrainement()
        else:
            jeu.jouer()
    except KeyboardInterrupt:
        print("\n\nLe jeu a été interrompu. À bientôt !")
        sys.exit(0)
