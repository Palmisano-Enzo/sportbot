from pywikiapi import Site, ApiError
import re
site = Site('http://wikipast.epfl.ch/wikipast/api.php') # Définition de l'adresse de l'API
site.no_ssl = True # Désactivation du https, car pas activé sur wikipast
site.login("AStampbach@sportBot", "d9di5hf0kalr5t75ohj1ij398slv5rkg") # Login du bot


def get_wiki_text(page, section=None):
    result = site('parse', page=page, prop=['wikitext'], section=section)
    return result['parse']['wikitext']


def import_data(data):
    
    for page, text in data.items():
        
        fullText = ""
        
        for line in text:
            fullText += line + '\n'

        try:
            site('edit', title = page, text="".join(fullText), token=site.token(), createonly=True)

        except ApiError as err:
            if err.data['code'] == 'articleexists':
                print("The page \"",page,"\" already exist --> modification of the existing page")
                sort_by_year(page, text, fullText)

        except Exception as err:
            print('Error :', err)

        
        
def sort_by_year(page_name,text, fullText):
    old_text = get_wiki_text(page_name)

    # When page is empty, just add content
    if not old_text:
        site('edit', title=page_name, text=fullText, token=site.token())
        return
    
    test_string = old_text.split("\n")

    test_string = [x for x in test_string if x.strip().startswith("*")]
    # Page does not contain any valid datafication entries
    if not test_string:
        site('edit', title=page_name, text=fullText, token=site.token())
        return
    
    for ourLine in text:
        
        year = int(ourLine[4:8])
        temp = [None] * len(test_string)
        res = [None] * len(test_string)
        foo = False

        for i in range(len(test_string)):
            temp[i] = re.findall(r'\d+', test_string[i])
            res[i] = list(map(int, temp[i]))
        current_year = 0

        for i in range(len(res)):
            if year <= res[i][0]:
                current_year = i
                foo = True
                break
            current_year = i

        previous_line = test_string[current_year]

        if (current_year >= len(res) - 1) and (not foo):  # add after, append
            old_text = old_text.replace(previous_line, previous_line + '\n' + ourLine, 1)
        else:
            old_text = old_text.replace(previous_line, ourLine + '\n' + previous_line, 1)
            
    site('edit', title=page_name, text=old_text, token=site.token())
    
    