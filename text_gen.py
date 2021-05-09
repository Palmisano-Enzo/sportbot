import pandas as pd

def format_line_country(year, country, host, text):
    return f"* [[{year}]] / [["+host +f"]] Obtention de "+ text+ " par l'équipe nationale [["+country+"]] aux Jeux olympiques."

def text_medal(gold, silver, bronze):
    text =""
    if(gold > 0):
        text+=f"{gold} médaille(s) d'or"
    if(silver> 0):
        if(text!=""):
            text+=", "
        text+=f"{silver} médaille(s) d'argent"
    if(bronze > 0):
        if(text!=""):
            text+=", "
        text+=f"{bronze} médaille(s) de bronze"
    return text

def get_count_for_country(df, country, year):
    df_filt =  df.loc[lambda df: df['Country'] == country, :]
    df_filt =  df_filt.loc[lambda df: df['Year']==year, :]
    
    host = df_filt["City"].values[0]
    
    count_gold = df_filt.loc[lambda df: df['Medal']=="Or"].count()[0]
    count_silver = df_filt.loc[lambda df: df['Medal']=="Argent"].count()[0]
    count_bronze = df_filt.loc[lambda df: df['Medal']=="Bronze"].count()[0]
    
    if count_bronze == 0 and count_gold == 0 and count_silver == 0:
        return (False,"")
    else:
        return (True, format_line_country(year, country ,host, text_medal(count_gold,count_silver,count_bronze)))
    
def get_list_country_year(df):
    df_loc = df[["Country", "Year"]]
    return df_loc.drop_duplicates()

def get_text_by_country(df):
    texts = {}
    country_year = get_list_country_year(df)
    for index, row in country_year.iterrows():
        ret = get_count_for_country(df, row["Country"], row["Year"])
        if ret[0]:
            texts.get(row["Country"],[]).append(ret[1])
            texts.get(str(row["Year"]),[]).append(ret[1])
            
    return texts

def load_frame(filename):
    return pd.read_csv(filename)

def generate_all_lines(filename):
    df = load_frame(filename)
    dic = get_text_by_country(df)
    dic.update(get_text_by_athlete(df))
    return dic

def format_line_player(year,city,sport,discipline,athlete,country,event,medal) :
    return f"* [[{year}]] / [[{city}]]."+ f"[[{athlete}]]" + f"Obtention d'une médaille en "+ medal+ f" dans la discipline "+discipline + " et pour l'épreuve" + event 

def get_text_by_athlete(df):
    result = {}
    for index,row in df.iterrows() :
        temp =format_line_player(row["Year"],row["City"],row["Sport"]
                                 ,row["Discipline"],row["Athlete"],row["Country"],row["Event"],row["Medal"])
        result.get(row["Athlete"],[]).append(temp)
        result.get(srt(row["Year"]),[]).append(temp)
        
    return result