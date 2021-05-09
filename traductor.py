import requests
import json
import pandas as pd
import numpy as np

def load_frame(filename):
    return pd.read_csv(filename)

def map_translate(orig, dic):
    return dic[orig]

def unique_translate(df, category):
    df_un = df[[category]]
    df_un = df_un.drop_duplicates()
    df_un["fr"]= df_un[category].apply(deepl)
    trans_table = df_un.set_index(category).to_dict()["fr"]
    df[category] = df[category].apply((lambda x: map_translate(x, trans_table)))
    

def deepl(text_to_translate):   
    data = {
      'auth_key': '21838e3e-51f7-089c-2aff-a64464f6d5c9:fx',
      'text': text_to_translate,
      'source_lang': 'EN',  
      'target_lang': 'FR'
    }

    response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
    jsonresponse = json.loads(response.text)
    translate = jsonresponse["translations"][0]["text"]
    return translate 

def translate(df, dictionary):
    to_change = ["City", "Sport", "Discipline", "Event", "Medal"]
    for unique_change in to_change:
        unique_translate(df, unique_change)
    unique_translate(dictionary, 'Country')

def replace_country(df, cat):
    trans_table = cat.set_index('Code').to_dict()['Country']
    df['Country'] = df['Country'].apply((lambda x: map_translate(x, trans_table)))
    

def delete_pending(df):
    df.drop(df[df['Athlete'] =="Pending"].index, inplace = True)
    df["Country"].fillna('PNC',inplace=True)
    
def reformat_name(text):
    text = text.split(',')
    if(len(text)==1):
        return text[0].lower().title()
    else:
        return text[1]+ " " + text[0].lower().title()
    
def lowercase_name(df):
    df["Athlete"] = df["Athlete"].apply(reformat_name)
    
def manual_change(df):
    print('1')
    #test
    
def dictionary_correction(dictionary):
    new_row1 = {'Country': 'Equipe mixte aux Jeux Olympiques', 'Code': 'ZZX', 'Population': ' ', 'GDP per Capita': ' '}
    new_row2 = {'Country': 'Bohême', 'Code': 'BOH', 'Population': ' ', 'GDP per Capita': ' '}
    new_row3 = {'Country': 'Australasie', 'Code': 'ANZ', 'Population': ' ', 'GDP per Capita': ' '}
    new_row4 = {'Country': 'Empire russe', 'Code': 'RU1', 'Population': ' ', 'GDP per Capita': ' '}
    new_row5 = {'Country': 'Tchécoslovaquie', 'Code': 'TCH', 'Population': ' ', 'GDP per Capita': ' '}
    new_row6 = {'Country': 'République fédérale de Yougoslavie', 'Code': 'YUG', 'Population': ' ', 'GDP per Capita': ' '}
    new_row7 = {'Country': 'Roumanie', 'Code': 'ROU', 'Population': ' ', 'GDP per Capita': ' '}
    new_row8 = {'Country': 'Union des républiques socialistes soviétiques', 'Code': 'URS', 'Population': ' ', 'GDP per Capita': ' '}
    new_row9 = {'Country': 'Équipe unifiée d\'Allemagne', 'Code': 'EUA', 'Population': ' ', 'GDP per Capita': ' '}
    new_row10 = {'Country': 'Fédération des Indes occidentales', 'Code': 'BWI', 'Population': ' ', 'GDP per Capita': ' '}
    new_row11 = {'Country': 'République démocratique allemande', 'Code': 'GDR', 'Population': ' ', 'GDP per Capita': ' '}
    new_row12 = {'Country': 'République fédérale d\'allemande', 'Code': 'FRG', 'Population': ' ', 'GDP per Capita': ' '}
    new_row13 = {'Country': 'Équipe unifiée de l\'ex-URSS', 'Code': 'EUN', 'Population': ' ', 'GDP per Capita': ' '}
    new_row14 = {'Country': 'participants olympiques/paralympiques indépendants', 'Code': 'IOP', 'Population': ' ', 'GDP per Capita': ' '}
    new_row15 = {'Country': 'Serbie', 'Code': 'SRB', 'Population': ' ', 'GDP per Capita': ' '}
    new_row16 = {'Country': 'Pays non connu', 'Code': 'PNC', 'Population': ' ', 'GDP per Capita': ' '}
    new_row17 = {'Country': 'Trinité-et-Tobago', 'Code': 'TTO', 'Population': ' ', 'GDP per Capita': ' '}
    new_row18 = {'Country': 'Monténégro', 'Code': 'MNE', 'Population': ' ', 'GDP per Capita': ' '}
    new_row19 = {'Country': 'Singapour', 'Code': 'SGP', 'Population': ' ', 'GDP per Capita': ' '}

    dictionary = dictionary.append(new_row1, ignore_index=True)
    dictionary = dictionary.append(new_row2, ignore_index=True)
    dictionary = dictionary.append(new_row3, ignore_index=True)
    dictionary = dictionary.append(new_row4, ignore_index=True)
    dictionary = dictionary.append(new_row5, ignore_index=True)
    dictionary = dictionary.append(new_row6, ignore_index=True)
    dictionary = dictionary.append(new_row7, ignore_index=True)
    dictionary = dictionary.append(new_row8, ignore_index=True)
    dictionary = dictionary.append(new_row9, ignore_index=True)
    dictionary = dictionary.append(new_row10, ignore_index=True)
    dictionary = dictionary.append(new_row11, ignore_index=True)
    dictionary = dictionary.append(new_row12, ignore_index=True)
    dictionary = dictionary.append(new_row13, ignore_index=True)
    dictionary = dictionary.append(new_row14, ignore_index=True)
    dictionary = dictionary.append(new_row15, ignore_index=True)
    dictionary = dictionary.append(new_row16, ignore_index=True)
    dictionary = dictionary.append(new_row17, ignore_index=True)
    dictionary = dictionary.append(new_row18, ignore_index=True)
    dictionary = dictionary.append(new_row19, ignore_index=True)
    
    
    
#####################################
def processing(filename, outputfile, needTranslation):
    df =  load_frame(filename)
    dictionary = load_frame("dictionary_mod.csv")
    dictionary_correction(dictionary)
    if(needTranslation):
        translate(df, dictionary)
    delete_pending(df)
    replace_country(df, dictionary)
    lowercase_name(df)
    df.to_csv(outputfile, index=False)
    dictionary.to_csv("dictionary_mod", index=False)
    

#summer = load_frame("summer_mod.csv")
#winter = load_frame("winter_mod.csv")

#translate(summer, winter, dictionary)
#dictionary_correction(dictionary)
#delete_pending(summer)
#delete_pending(winter)
#replace_country(summer, dictionary)
#replace_country(winter, dictionary)
#lowercase_name(winter)
#lowercase_name(summer)

#winter.to_csv('winter_mod.csv', index=False)