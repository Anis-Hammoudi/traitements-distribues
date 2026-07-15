# Atelier: Salade de fruits distribuee

Ce repertoire contient les scripts de l'atelier sur les systemes distribues.
Ils sont rediges de maniere minimaliste en Python.

## Pre-requis
- Python 3
- rpyc (`pip install rpyc`)

## Les scripts

1. `0_seq.py` : Version sequentielle de base.
2. `1_server.py` : Serveur RPC minimal pour tester la connexion reseau.
3. `2_slave.py` & `3_master.py` : Architecture maitre-esclave simple avec un pool de travail protege par verrou.
4. `4_slave_crash.py` & `5_master_crash.py` : Simulation de pannes franches (les esclaves crashent aleatoirement). Le maitre restera bloque infiniment en attente.
5. `6_slave_timeout.py` & `7_master_timeout.py` : Systeme robuste avec gestion des pannes via un thread de timeout qui realloue les taches expirees.
6. Dossier `P1/` : Exercice sur les graphes de dependances (taches dynamiques). Le maitre ne distribue une tache que si ses prerequis sont satisfaits.
7. Dossier `P2/` : Exercice sur la gestion de l'inactivite totale. Le maitre s'arrete proprement si plus aucun esclave n'est en vie (Watchdog).

## Execution

Pour tester les versions distribuees :
1. Lancez d'abord le script master (par ex: `python 3_master.py`) dans un terminal.
2. Lancez plusieurs instances de scripts esclaves (par ex: `python 2_slave.py`) dans d'autres terminaux.
