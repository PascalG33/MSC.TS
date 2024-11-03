# utils/gif_handler.py
def get_gif_message(taux_de_sortie):
    if taux_de_sortie < 0.5:
        return ("https://media.giphy.com/media/jWcypagX0tNtiup1pg/giphy.gif", "Direction le carton à Claire !!")
    elif 0.5 <= taux_de_sortie < 0.8:
        return ("https://media.giphy.com/media/IdQc6gB1B9iDu/giphy.gif", "Je suis en pleine forme… enfin, si on considère la forme d’un triangle.")
    elif 0.8 <= taux_de_sortie < 1:
        return ("https://media.giphy.com/media/WpObP6Qx5QXq9TxHyh/giphy.gif", "L’argent ne fait pas le bonheur… mais ça achète des pizzas, et c’est presque pareil.")
    elif 1 <= taux_de_sortie < 1.5:
        return ("https://media.giphy.com/media/1346qghmDoqF6o/giphy.gif", "Pourquoi courir après le bonheur quand tu peux marcher lentement vers la pizza ?")
    elif 1.5 <= taux_de_sortie < 1.8:
        return ("https://media.giphy.com/media/Lk023zZqHJ3Zz4rxtV/giphy.gif", "Il paraît qu'on ne peut pas tout acheter avec de l'argent. Mais essayons avec une carte de crédit.")
    elif 1.8 <= taux_de_sortie < 2:
        return ("https://media.giphy.com/media/rdma0nDFZMR32/giphy.gif", "La réussite, c'est de réussir à faire croire aux autres que tu sais ce que tu fais.")
    elif 2 <= taux_de_sortie < 2.5:
        return ("https://media.giphy.com/media/l4Jzgmad24DGBqQ4U/giphy.gif", "Le secret de la réussite ? Toujours sembler occupé quand ton patron passe.")
    elif 2.5 <= taux_de_sortie < 3:
        return ("https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif", "Mon idée du succès ? Célébrer tellement fort qu’on en oublie ce qu’on fêtait !")
    elif 3 <= taux_de_sortie < 4:
        return ("https://media.giphy.com/media/65d9b041fc0c684a5b10bb931e4f02db/tenor.gif", "Le sommet est à moi !… Bon, maintenant, quelqu’un peut-il m’aider à redescendre ?")
    else:
        return ("https://media.giphy.com/media/376a9c3bb1e43dc1d8d6f21f4f7d3646/tenor.gif", "Pour moi, la gloire, c’est juste d’avoir trouvé les clés de chez moi du premier coup.")
