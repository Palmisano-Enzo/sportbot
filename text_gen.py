import pandas as pd

source = "[https://www.kaggle.com/the-guardian/olympic-games]"
nat_team = "Equipe Olympique "

def format_line_country(year, country, host, text, jo):
    # Format the line so that it can easily be added to Wikipast
    return f"* [[{year}]] / [["+host +f"]]. Obtention de "+ text+ " par la nation [["+country+"]] aux Jeux olympiques d'"+jo+"."+source

def text_medal(gold, silver, bronze):
    # Generate a specific text for the medals received by the country
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

def get_count_for_country(df, country, year, jo):
    # Filter to have only the medals for a specific country and year
    df_filt =  df.loc[lambda df: df['Country'] == country, :]
    df_filt =  df_filt.loc[lambda df: df['Year']==year, :]
    
    # Get the host city
    host = df_filt["City"].values[0]
    
    # Count the number of medal per country for a specific year
    count_gold = df_filt.loc[lambda df: df['Medal']=="or"].count()[0]
    count_silver = df_filt.loc[lambda df: df['Medal']=="argent"].count()[0]
    count_bronze = df_filt.loc[lambda df: df['Medal']=="bronze"].count()[0]
    
    # Return the line for the country 
    if count_bronze == 0 and count_gold == 0 and count_silver == 0:
        return (False,"")
    else:
        return (True, format_line_country(year, country ,host, text_medal(count_gold,count_silver,count_bronze), jo))
    
def get_list_country_year(df):
    # Get the list of all country by year
    df_loc = df[["Country", "Year"]]
    return df_loc.drop_duplicates()

def get_and_add_to_list(dic, key, value):
    # Get the correct list in the dictionnary and the value to it
    lis = dic.get(key, [])
    lis.append(value)
    dic[key]=lis

def get_text_by_country(df, jo):
    # Generate text by country 
    texts = {}
    country_year = get_list_country_year(df)
    for index, row in country_year.iterrows():
        # Count the number of medal for each country 
        ret = get_count_for_country(df, row["Country"], row["Year"], jo)
        if ret[0]:
            # Add the formatted text to the dictionnary 
            get_and_add_to_list(texts, str(row["Year"]), ret[1])
            get_and_add_to_list(texts, nat_team+row["Country"], ret[1])
            
    return texts

def load_frame(filename):
    # load panda dataframe
    return pd.read_csv(filename)

def merge_dict(dic1, dic2):
    #Merge two dictionnary together 
    dic3 = dic1.copy()
    for k,v in dic2.items():
        if k in dic3:
            lis = dic3[k]
            lis.extend(v)
            dic3[k]=lis
        else:
            dic3[k]=v
    return dic3

def generate_all_lines(filename,jo):
    # Main method that does everything
    df = load_frame(filename)
    dic = get_text_by_country(df, jo)
    dic = merge_dict(dic, get_text_by_athlete(df, jo))
    return dic

def format_line_player(year, city, sport, discipline, athlete, country, event, medal, jo) :
    # Format a line for a player so that it can be easily insert to wikipast
    prefix = "d'" if medal != "Bronze" else "de "
    # If the event is not exactly the same as the discipline, we need to add it
    needEvent = event != discipline
    text = f"* [[{year}]] / [[{city}]]. "+  f"Obtention de la médaille "+ prefix+ medal+ f" par "+f"[[{athlete}]]"+" dans la discipline "+discipline 
    
    if needEvent:
        text+= " pour l'épreuve " + event 
    text+= " aux Jeux Olympiques d'"+jo+"."+source
    return text

def get_text_by_athlete(df,jo):
    # Generate the line for each player
    result = {}
    
    for index,row in df.iterrows() :
        temp =format_line_player(row["Year"],row["City"],row["Sport"]
                                 ,row["Discipline"],row["Athlete"],row["Country"],row["Event"],row["Medal"],jo)
        get_and_add_to_list(result, str(row["Athlete"]),temp)
        get_and_add_to_list(result, str(row["Year"]),temp)
        
    return result