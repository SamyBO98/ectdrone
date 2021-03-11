# Installer plusieurs drones

## Téléchargements

Récupérer les fichiers nécessaires et placez-les la ou il faut:

- **Fichier `launch`**: Il faudra placer `ardupilot_2_drones.launch` dans un fichier spécifique. Taper sur le terminal `roscd gazebo_ros/launch` et placez-le ici. Si `roscd` n'est pas reconnu ou s'il y a une erreur dans la commande, alors **l'installation de `ROS` n'est pas complète**.
- **Fichier `worlds`**: Placez `ardupilot_2_drones.world` dans le fichier de gazebo. **Pour rappel**: Vous devez avoir au prérequis avoir installé la version 9 de gazebo. Il se situe donc dans `/usr/share/gazebo-9` (*ou `/usr/share/gazebo` tant que la version de gazebo reste la version 9!*). Placez ce document dans le fichier `worlds`.
- **Fichier `models`**: Il y a plusieurs fichier qu'il faudra tout déplacer, **fichiers compris**. Avant de vous lancer dedans, vérifier dans `/usr/share/gazebo-9/models` que le fichier `iris_with_standoffs` existe bien. Si oui, un autre fichier similaire à celui-ci commençant par `iris_with_...` devra être supprimé (*car jugé inutile au projet*). Enfin, copiez-collez tout les dossiers dans `models`.

## Compilation

Pour lancer plusieurs drones, il faudra:
- Lancer un terminal et tapez `roslaunch gazebo_ros ardupilot_2_drones.launch`: gazebo se lance avec 2 drones côtes à côtes.

- Lancer autant de terminals qu'il y a de drones, rendez-vous au dossier `ardupilot/ArduCopter` et taper `../Tools/autotest/sim_vehicle.py -f gazebo-iris --console -IO` pour chaque drone (*en incrémentant le chiffre dans l'option `console`: `--console -I1`, ... pour que chaque drone ait sa propre console*)

- Lancer autant de terminals qu'il y a de drones, rendez-vous sur le dossier ou se situe le script python de test pour lancer un drone (*sur cette forge*) et tapez: `python test.py --connect 127.0.0.1:14550`. Cette commande va faire démarrer le premier drone. Pour en lancer un autre, incrémenter de 10 le port: `python test.py --connect 127.0.0.1:14560`

## Compréhension

Le fichier `launch` permet d'appeler un monde avec quelques paramètres en plus, nécessaire pour utiliser `ROS`. En regardant le fichier, on a juste à modifier la ligne appelant le monde `ardupilot_2_drones.world` par un monde existant situé dans `/usr/share/gazebo-9` (*ou dans `/usr/share/gazebo`*).

Le fichier `worlds` contient les mondes appelant les modeles de arducopter. Ce sont les models venant du fichier `models`. De plus on peut positionner les models ou on le souhaite.

Le fichier `models` contient des informations sur le port à connecter pour le drone. Il y a 2 ports: un port d'entrée et une de sortie. Par défaut on met 9002 en entrée et 9003 en sortie. La convention nous indique qu'on peut utiliser un autre drône répondant à un autre port à au moins 10 de plus (*d'ou le renommage des dossiers par `...9002`, `...9012` pour identifier le robot*).

Pour connecter le script python au robot, on le connecte par défaut a `127.0.0.1:14550` et on incrémente de 10 pour chaque drone utilisé (*faites bien attention à appeler les drones dans l'ordre: ne mettez pas dans un monde le drone 9002 puis le drone 9022 car en connectant le code python, celui répondant au port 14560 n'existe pas*).

## Aide

Allez sur le dossier `aides` pour comprendre comment tout ça fonctionne à travers un tutoriel bien expliqué.

## Possibilités

- Un seul code python permettant à un drone d'aller à un certain endroit en lui envoyant des options (*devra être appelé autant de fois qu'il y a de drones*)

- Un code python pouvant se connecter à plusieurs drones en lancant une seule fois ce script et répartir les tâches entre les drones