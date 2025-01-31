#!/bin/bash

# Nom de la session tmux
SESSION="dashboard"

# Vérifier si la session existe déjà
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
    # Créer une nouvelle session en mode détaché
    tmux new-session -d -s $SESSION

    # Split horizontal
    tmux split-window -h

    # Split vertical dans le panneau gauche
    tmux split-window -v -t 0

    # Split vertical dans le panneau droit
    tmux split-window -v -t 2

    # Sélectionner le premier panneau
    tmux select-pane -t 0
fi

# Attacher la session
tmux attach -t $SESSION