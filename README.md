# ECTDrones

Bienvenue sur le README officiel de **ECTDrones**. Ce projet à pour but d'initialiser et de piloter des drones de manière automatique pour prendre un maximum d'informations dans une zone donnée auquel les drones vont pouvoir communiquer entre eux pour se partager les différentes tâches à acoomplir.

Voici la table des matières:
- [Prérequis](#Prérequis)
- [Installation](#Installation)

## Prérequis

Vous devez au préalable utiliser Linux et avoir installé [gazebo version 9](http://gazebosim.org/tutorials?cat=install&tut=install_ubuntu&ver=9.0) (*Suivez l'installation alternative*) et [ROS](http://wiki.ros.org/Installation/Ubuntu) (*Suivez l'installation de ROS Melodic*).

Pour vérifier l'installation, les commandes suivantes doivent être reconnus par votre terminal (*cela peut marcher mais il n'est pas nécessaire que ces commandes marchent, il faut juste qu'il ne vous mette pas d'erreur d'installation*):
- `gazebo`
- `roscd`
- `roslaunch`

De plus, vous allez devoir installer le projet [ardupilot](https://github.com/ArduPilot/ardupilot) sur GitHub (*clonez le projet*). Il va permettre de définir tout les paramètres et les conditions des drones.

Après avoir récupéré le projet d'Ardupilot, rendez-vous au dossier `ArduCopter` et assurez vous que la commande `../Tools/autotest/sim_vehicles.py` ne vous indique pas qu'il manque une installation spécifique (*dans le cas contraire, installez ce qui est nécessaire d'installer jusqu'à ce qu'il ne vous demande plus d'installer quoi que ce soit*).


Une fois tout ceci fait, on peut passer à la compilation.

**Partie incomplète, à éditer...**

## Compilation

-Test de ROS avec Turtlesim:
Dans un terminal saisisez la commande `roscore`
Dans un autre, saisissez `rosrun turtlesim turtlesim_node`

ROS est bien installé si un fond bleu avec une tortue s'affichent à l'écran.

-Installation de ardupilot
Clonez le github cité précédemment
Saisissez les commandes suivantes : 
`cd ardupilot`
`git submodule update --init --recursive`
`cd /etc/drone/devel `
`source setup.bash`

# Setup de gazebo

Saisissez ensuite les commandes suivantes dans le répertoire de ce projet : 

`source /opt/ros/melodic/setup.bash`
`source /usr/share/gazebo-9/setup.sh`
`source /usr/share/gazebo/setup.sh`
`export GAZEBO_MODEL_PATH=~/ectdrone/src/my_simulations/models`
`export GAZEBO_RESOURCE_PATH=~/ectdrone/src/my_simulations/world:${GAZEBO_RESOURCE_PATH}`
`source ardupilot/Tools/completion/completion.bash`
`source ~/ectdrone/devel/setup.bash`

Pour vérifier que votre installation est fonctionnelle, saisissez la commande suivante : 
`roslaunch my_simulations ardupilot_2_drones.launch`

Cela devrait lancer la simulation avec Gazebo
