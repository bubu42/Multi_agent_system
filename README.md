---
# Multi_agent_system

Ce readme permet de faire tourner le projet. Ce projet à été testé sous MacOs. 

Conseil: 
Sous Windows et LinuX, veuillez à verifier les paths.

---
##Comment faire tourner ce projet
- Tout d'abord vérifier bien que vous avez frodo2, java 13, et graphivz ( si vous voulez essayer avec la version GUI de frodo2)
- Ce projet à été créer sous l'environment Python3.7 avec l'IDE PyCharm.
- Veuillez avoir un pc avec minimum 8gb de ram, sinon vous pouvez faire tourner ce projet sous Google Colab.
Mais, pour cela vous devez importer ce projet dans votre drive et à partir de google colab faire ces quelques lignes :

        from google.colab import drive\
        drive.mount('/gdrive')\
        %cd /gdrive
    
    Puis suivre les instructions données.\
    
    Conseil bis : pour lancer frodo avec google colab faudra changer les os.system("..") par :
                  
      !java -cp frodo2/frodo2.17.1.jar frodo2.algorithms.AgentFactory ../xml/scen07.xml agents/MPC/MPC-DisWCSP4_JaCoP.xml -timeout 360000000 >  ../output/MPC-DisWCSP4_JaCoP _scen07.txt
    
    Ne mettez rien sous quote ("",'').

- Une fois cette partie bien assimiler, vous pouvez télécharger le fichier zip du projet nommé : Projet_MAS_BRAHIMI_CITAK.zip
- A l'intérieur vous trouverez les dossiers suivants, s'il en manque un c'est peut-être pas la bonne version :
    - [rep] fichier comprenant tout les fichiers et dossiers FullRLFAP
    - [rep] output comprenant les fichiers de sortie.
    _ [rep] plot comprenant tout les plots par catégorie.
    - [rep] pre repertoire où s'enregistre les fichiers {var.txt,dom.txt,ctr.tx,cst.txt} créer aléatoirement.
    - [rep] src comprend le fichier main.py toutes nos fonctions s'y trouve dedans.
    - [rep] venv lié à Pycharm
    - [rep] xml comprenant tout les fichiers xml créé.
    - [file] README.md fichier d'explication
    - [file] Projet_MAS_BRAHIMI_CITAK.pdf rapport du proejt
- Une fois avoir vérifié que vous possédez bien tout (logiciel + projet). Vous pouvez lancer le projet avec l'IDE ou via ligne de commande en faisant :
            
      python3.7 [PATH/main.py]
    Vous pourrez tester notre créateur de fichier Random.
    Ou bien lancer le test avec une scen donné dans CELAR.
    Respectez bien les paths. Donc pour ne pas avoir de problème. 
    Je vous conseille d'utiliser PyCharm CE gratuite et qui permet 
    de visualiser le code en même-temps.
    


##Exemple de lancement de code 

    CreateRandomAndPlotOrDisplay('./pre/', nbVar=20, nbDom=7)
    
    CreateCelarAndPlotOrDisplay('fichier/FullRLFAP/CELAR/scen01','scen01')
    
Voici les valeurs par défaut:
            
    plot=True #Si False alors pas de plot
    algo=['MGM', 'DSA', 'AFB', 'DPOP', 'ADOPT', 'MaxSum'] # Pour les grosses scen il est conseillez de mettre juste MGM et DSA
    pathResult='./output/' # ni touchez pas, sauf si vous voule zun chemin spécifique sur votre machine
    pathXml='./xml/' # l'endroit où on va stocker et lire les xml

---
###Copyright © BRAHIMI-CITAK M2-DSC UJM 2019/20 

---