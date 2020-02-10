import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from flask import Flask, render_template, request, send_from_directory, jsonify, send_file, redirect
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hasil', methods=['GET','POST'])
def hasil():
    df = pd.read_csv('Pokemon.csv')
    dflegend = df[['Legendary']].replace(False, 'Not Legend')
    dflegend = dflegend[['Legendary']].replace(True, 'Legend')
    df = df.drop(['Legendary'], axis=1)
    df['Legendary'] = dflegend
    dfre = df[['#','Name','Type 1','Generation', 'Legendary']]
    def mergecol(i):
        return str(i['Type 1'])+'aku'+str(i['Generation'])+'aku'+str(i['Legendary'])
    dfre['feature'] = dfre.apply(mergecol,axis='columns')
    dfre['Name'] = dfre['Name'].apply(lambda x:x.capitalize())
    dfre.to_string()
    model = CountVectorizer(
        tokenizer = lambda i: i.split('aku'),
        analyzer = 'word',
    )
    matrix = model.fit_transform(dfre['feature'])
    dfmx = matrix.toarray()
    score = cosine_similarity(dfmx)
    pokename = request.form['pokemon'].capitalize()
    pokename1 = pokename.lower()
    # nomor = df[df['Name'] == pokename.capitalize()]['#'].tolist()[0]
    url1 = f'https://pokeapi.co/api/v2/pokemon/' + pokename1
    # url1 = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{nomor}.png'
    data1 = requests.get(url1)
    picture1= data1.json()['sprites']['front_default']
    if pokename not in list(dfre['Name']):
        return redirect ('/notfound')
        # get the digimon that what we want
    typepoke = dfre['Type 1'][dfre['Name']==pokename.capitalize()].values[0]
    genpoke = dfre['Generation'][dfre['Name']==pokename.capitalize()].values[0]
    legpoke = dfre['Legendary'][dfre['Name']==pokename.capitalize()].values[0]
    likeIndex = dfre['#'][dfre['Name'] == pokename.capitalize()].values[0]
    allpoke = list(enumerate(score[likeIndex]))
    for i in range(len(allpoke)):
        if int(allpoke[i][0]) != int(likeIndex):
            similarpoke = (sorted(allpoke,key = lambda x: x[1],reverse = True))
    listrecom = []
    for i in range(len(similarpoke)):
        if int(similarpoke[i][0]) != int(likeIndex):
            listrecom.append(similarpoke[i])
    newlist = []
    # imgsrc = []
    typeoth = []
    genoth = []
    legoth = []
    for i in range(len(listrecom[:6])):
        newlist.append(dfre['Name'][dfre['#']==listrecom[i][0]].values[0])
    #     imgsrc.append(dfimg['image'][dfimg['no']==listrecom[i][0]].values[0])
        typeoth.append(dfre['Type 1'][dfre['#']==listrecom[i][0]].values[0])
        genoth.append(dfre['Generation'][dfre['#']==listrecom[i][0]].values[0])
        legoth.append(dfre['Legendary'][dfre['#']==listrecom[i][0]].values[0])
    
    
    return render_template(
        'responsefound.html', 
        imgsrc=picture1,
        # imgre=imgre,
        pokename=pokename,
        newlist=newlist,
        typepoke=typepoke,
        genpoke=genpoke,
        legpoke=legpoke,
        typeoth=typeoth,
        genoth=genoth,
        legoth=legoth
        )

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(debug = True)


# df = pd.read_json('digimon.json')
# df = df[['no','digimon','stage','type','attribute']]
# df['digimon'] = df['digimon'].apply(lambda x:x.capitalize())

# df['x']=df['stage']+'budiman'+df['type']+'budiman'+df['attribute']
# model = CountVectorizer(
#     tokenizer = lambda i: i.split('budiman'),
#     analyzer = 'word',
# )

# matrix = model.fit_transform(df['x'])
# digimon = model.get_feature_names()
# countdigi = len(digimon)
# dfmx = matrix.toarray()

# score = cosine_similarity(matrix)

# like = 'agumon'
# likeIndex = df['no'][df['digimon'] == like.capitalize()].values[0]

# allDigi = list(enumerate(score[likeIndex]))

# for i in range(len(allDigi)):
#     if int(allDigi[i][0]) != int(likeIndex):
#         similardigi = (sorted(allDigi,key = lambda x: x[1],reverse = True))

# listrecom = []
# for i in range(len(similardigi)):
#     if int(similardigi[i][0]) != int(likeIndex):
#         listrecom.append(similardigi[i])

# newlist = []
# for i in range(len(listrecom[:6])):
#     newlist.append(df['digimon'][df['no']==listrecom[i][0]].values[0])

# print(newlist)