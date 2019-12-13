

# MyDevoirs :  La prise de devoirs sur ordinateur enfin simple !!!

![agenda](docs/agenda800.png)

![todo](docs/todo800.png)


## Pourquoi MyDevoirs ?

Mon fils a un ordinateur à l'école depuis le CM1. Nous avons essayé beaucoup de solution (rainlendar, onenote, agenda windows...), malheureusement rien de spécialement adapté pour parfaitement coller aux besoins d'un enfant. MyDevoirs a donc été développé spécialement pour lui, en accord avec ses besoins et ses exigences.

## MyDevoirs c'est pour qui ?

A priori les enfants qui ont beson d'un ordiateur à l'école donc les Dys en général.

## Comment l'installer ?

Pour l'instant disponible sous Windows et Linux (Mac possible si quelqu'un le demande).

- Version Windows : [MyDevoirs.exe](https://github.com/jgirardet/mydevoirs/releases/download/0.5.0/MyDevoirs.exe) 
- Vesion Linux : [MyDevoirs](https://github.com/jgirardet/mydevoirs/releases/download/0.5.0/MyDevoirs)

	- puis sous Windows :
		- windows va vous mettre en garde car l'application n'est pas certifiée mais pas d'inquiétude, il suffit de cliquer sur `informations complémentaires` puis  `exécuter quand même`:

			![Avertissement 1](docs/avertissement1.jpeg) ![Avertissement 2](docs/avertissement2.jpeg)

		- Ensuite il suffit d'éxécuter le fichier est c'est parti.

	- puis sous Linux :
		- Il faut rendre le fichier executable sous en monde teminale:
		```bash
		chmod +x MyDevoirs
		```
		ou en mode graphique, par exemple sous Mint :  click droit => propiétés => permissions => Autoriser l'exécution du fichier comme un programme.


## Comment l'utiliser ?

Il y a 2 interfaces possible : Une interface  type `agenda` ![agenda](data/icons/014-calendar.png) qui affiche chaque jour de la semaine avec les devoirs de chaque jour, une autre type `todo list` (liste des tâches) ![todo list](data/icons/010-test.png). Il semble plus simple de noter ses devoirs dans le mode `agenda` mais plus simple de faire ses devoirs en mode `todo list`. La `todolist` n'affiche que les devoirs non encore effectués alors que l'`agenda` affiche l'intégralité des devoirs.

Il est possible de modifier les jours affichés dans `Paramètres` ![parametres](docs/params.png).

En mode `agenda` on change de semaine en cliquant sur ![suivant](data/icons/chevron-right.png) pour semaine suivante ou pour semaine précédante. ![precedant](data/icons/chevron-left.png)

### Pour ajouter un devoir:

On clique sur ![nouveau](data/icons/012-add.png) et on choisit sa matière en cliquant dessus ou avec `entrée`.

La zone de texte est directement sélectionnée, pour entrer le texte correspondant.

### Pour marquer un devoir comme terminé:

On clique sur ![non fait](data/icons/017-cancel.png) qui devient ![fait](data/icons/apply-64.png). En mode `todo list` la ligne disparaît de l'affichage.

### Pour supprimer un devoir:

On clique sur ![non fait](docs/garbage.png), il faut ensuite confirmer.

## C'est un peu long de reprendre la souris à chaque fois, des raccourcis claviers se serait bien...

Les raccourcis claviers sont à utliser quand le curseur est dans une zone de texte.

 - `Ctrl+D` : (D = dupliquer) Pour créer une nouvelle ligne avec la matière en cours. Pratique quand on veut noter plusieurs choses de la même matière (par exemple leçons, exercices...).

 - `Ctrl+M` : (M = Matière) Pour changer la matière en cours. on peut se déplacer avec les `flêches` et valider son choix avec `entrée` ou la `flêche droite`.

 - `Ctrl+N` : (N = Nouveau) Pour créer une nouvel ligne, le choix des matières s'affiche, on choisit avec les `flêches` et on valide par `entrée`.

 - `Ctrl+E`: (E = effacer) Pour effacer une ligne.


## Au secours j'ai un problème/ il manque une fonctionnalité

Il suffit de laisser un message/issue sur [Github issue](https://github.com/jgirardet/mydevoirs/issues). Il faut créer un compte github gratuit pour pouvoir laisser un message.

## MyDevoirs c'est gratuit ?

MyDevoirs est un logiciel libre (la code source est disponible) sous licence GPL3.

## Remeciements

Je remercie tous les gens impliqués dans la réalisation des technologies utlisés et plus particuliérement l'équipe de dévelopeurs de [Kivy](https://www.kivy.org) et [Ponyorm](https://ponyorm.org) pour disponibilité à repondre aux questions.
