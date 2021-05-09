from pywikiapi import Site

site = Site('http://wikipast.epfl.ch/wikipast/api.php') # Définition de l'adresse de l'API
site.no_ssl = True # Désactivation du https, car pas activé sur wikipast
site.login("User@Name", "Password") # Login du bot


def get_wiki_text(page, section=None):
    result = site('parse', page=page, prop=['wikitext'], section=section)
    return result['parse']['wikitext']


def input_character(data):

    try:
        site('edit', title = data[0], text="".join(data.[1]), token=site.token(), createonly=True)

    except ApiError as err:
        print('I am inside the exception')
        if err.data['code'] == 'articleexists':
            for year, input_text in zip(years, text):
                sort_year(title, year, input_text)
            return

    except Exception as err:
        print('Error :', err)

        
        
def sort_year(page_name, year, text):
    old_text = get_wiki_text(page_name)

    # When page is empty, just add content
    if not old_text:
        site('edit', title=page_name, text=text, token=site.token())
        return
    
    test_string = old_text.split("\n")

    test_string = [x for x in test_string if x.strip().startswith("*")]
    # Page does not contain any valid datafication entries
    if not test_string:
        site('edit', title=page_name, text=text, token=site.token())
        return
    
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
        old_text = old_text.replace(previous_line, previous_line + '\n' + text, 1)
    else:
        old_text = old_text.replace(previous_line, text + '\n' + previous_line, 1)
    site('edit', title=page_name, text=old_text, token=site.token())
