# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 08:25:33 2023

@author: casseljf
"""

import string
import pandas as pd
import re
import cleanco

# Clean company names

# Define a translator to remove punctuation
translator = str.maketrans('', '', string.punctuation)



# Set up function to clean up company names
undict ={'â€¦': '…',"â€ž":"„" ,'â€“': '–', 'â€™': '’', "â€\x9d":"”",
         "â€š":"‚","â€°":"‰",
         'â€œ': '“', "â€”":'—', "Â\xad":" ",'Ã©':"é",'â‚¬':'€',
         "â€˜":"‘",'Â£':"£","Ã¢":"â","Â©":"©",'Ã£':"ã","Ãº":'ú',
         'Ã¤':'ä',"â€¢":"•",'Ã¡':'á','Ã¼':'ü',"Â¢":'¢',"Ã±":"ñ",
         'Ã‰':'É','Â¥':'¥','Ã§':'ç','Ã´':'ô','Â®':'®',
         'Â¦':'¦',"Ã¯":"ï",'Ã¶':'ö','Â´':"´","Ëœ":"˜",'Â»':'»',
         'Ã«':"ë","Ã‡":"Ç","Ã³":"ó","Ãµ":"õ","Ã®":"î","Â¾":'¾',
         "Â¼":"¼","Â°":"°","Ã–":"Ö","Ã¥":'å',"Ã¨":"è","Â¯":"¯",
         "Â¬":"¬","Ã„":"Ä","Â§":"§","Ãœ":"Ì","Â¤":"¤","Â·":'·',
         "Â±":"±","Ã²":"ò","Ãƒ":"Ã","ÃŸ":"ß","Ã’":"Ò",
         "Â¡":"¡","Ãª":"ê","Â«":"«",
         "Ã\x8d":"Í","Ã\x81":'Á',"Ã\xad":"í","Ã¦":"æ","Â¿":"¿","Ã¸":"ø",
         "Ã½":"ý","Ã»":"û","Ã¹":"ù","Å½":"Ž","Â¨":"¨","Âµ":"µ",
         "Â²":"²","Â³":"³","Â¹":"¹","â„¢":"™","Ã¤":"ä","Ã“":"Ó",
         'Ã¿': 'ÿ', 'Ã¾': 'þ', 'Ã·': '÷', 'Ã°': "ð", "Ã›": "Û",
         "Ãš": "Ú", "Ã˜": "Ø", "Ã™": "Ù", "Ã—": "×", "Ã‘": "Ñ", 'Ã”': "Ô",
         "Ã•": "Õ", "ÃŠ": "Ê", "Ã‹": "Ë", 'ÃŒ': 'Ì', "ÃŽ": "Î", "Ã…": "Å",
         "Ã†": "Æ", "Ãˆ": "È", "Ã€": "À", "Ã‚": "Â", "Âº": "º", "Â½": "½",
         "Â¶": "¶", "Â¸": "¸", "Âª": "ª", "Å¡": "š", "â€º": "›", "Å“": "œ" ,
         "Å’": "Œ", "Å¾": "ž", "Å¸": "Ÿ", "Ë†": "ˆ"
         }

# Set up three auxilliary functions to deal with encoding issues, non-standard
# characters, and missing data.
def preprocess_name(name):
    # Handle None or NaN values
    if pd.isna(name):
        return ""
    # Remove non-alphanumeric characters, convert to lowercase, and strip whitespace
    return ''.join(char for char in name if char.isalnum()).lower().strip()

def remove_control_characters(s):
    return "".join(ch for ch in s if ch in string.printable)

def handle_encoding_issues(s):
    return s.encode('latin1', 'ignore').decode('utf8', 'ignore')


# Define main function to clean up company names
def clean_up_company_names(s):
    
    # Handle None or NaN values
    if pd.isna(s):
        return ""
    
    # Use undict to recover misrepresented character. Apply prior to applying 
    # lowercase as it is based on charaacters such as Ã
    for key, value in undict.items():
        if key in s:
            s = s.replace(key, value)
            
    # Deal with subsets of problematic names that can break fuzzywuzzy below
    s = handle_encoding_issues(s)
    s = remove_control_characters(s)
    
    # Make all characters lowercase
    s = s.lower()
    
    #
    
    # Remove parts within parentheses 
    # This deals with, for example, the following Pitchbook version of 'Maven':
    # "Maven (Information Services (B2C))".
    s = re.sub(r'\(.+?\)', '', s)
    s = re.sub(r'\[.+?\]', '', s)

    # Remove punctuation characters
    s = s.translate(translator)
    
    
    # Standardize & versus and
    s = s.replace('&', 'and')
    
    
    # Standardize whitespace to exactly one space
    s = ' '.join(s.split())
    

    # Apply the cleanco.basename cleaning that takes away things like 'llc', 'co.' 
    # and similarly at the end. I have added a few special cases that appear in
    # our applications when text is misread, such as 'l l c' or 'l t d' in
    # addition to the package's existing 'llc', 'l.l.c.' versions. Similarly,
    # 'limited partnership' and 'limitedpartnership' was added in addition to
    # 'lp' and 'l.p.'
    # As basename removes at most one company-related term at a time, loop
    # through until it makes no further changes
    while s != cleanco.basename(s):
        s = cleanco.basename(s)
    
    
    return s



# Additional cleaning to be specifically applied to PE/VC firms and funds

# Suffixes we might want to remove
suffix = ['lp', 'ltd', 'llc', 'partnership', 'plc', 'inc', 'fund', 'limited', 'l p', 'dst', 'side',
         'sidecar', 'side car', 'gp', 'gps', 'sa']

# Map numbers to roman numbers to standardize fund count
roman_map = {'1': 'i', '2': 'ii', '3': 'iii', '4': 'iv', '5': 'v', '6': 'vi', '7': 'vii', 
             '8': 'viii', '9': 'ix', '10': 'x', '11': 'xi', '12': 'xii', '13': 'xiii', 
             '14': 'xiv', '15': 'xv', '16': 'xvi', '17': 'xvii', '18': 'xviii', 
             '19': 'xix', '20': 'xx', '21': 'xxi'}

common_words = ["capital", "ventures", "venture", "management", "investment",
                "investments", "growth", "opportunity",
               "coinvestment", "equity", "investors", "investor", "holdings", 
               "special", "opportunities", "private", "street", "group"]



# Set up a name cleaning function
def clean_name_pe_version(s):
    '''
    Clean fund name for SEC data.
    
    ''' 
    
    # Handle None or NaN values
    if pd.isna(s):
        return ""
      
    s = s.lower()

    # convert common terms before removing dashes
    s = s.replace('co-investment','coinvestment')
    s = s.replace('co-invest','coinvest')
    s = s.replace('asia-pacific','asiapacific')
    
    # Remove parts within parentheses 
    # This deals with, for example, the following Pitchbook version of 'Maven':
    # "Maven (Information Services (B2C))", and the Form D (non-US) version of
    # "Ag Real Value Fund (Non-US) Feeder, LP"
    s = re.sub(r'\(.+?\)', '', s)
    s = re.sub(r'\[.+?\]', '', s)

    # convert dash to space
    s = s.replace('-', ' ')
    
    # Remove punctuation characters
    s = s.translate(translator)
    

    
    # remove all suffixes (e.g. lp, llc)
    for suf in suffix:
       s = " ".join([word for word in s.split() if not word==suf])
       
    
    """
    # Use this if you think it helps with the fuzzy matching
    # remove common words to prevent false positives
    for common_wrd in common_words:
        s = " ".join([word for word in s.split() if not word==common_wrd])
    """

    # remove extra spaces between words
    s = ' '.join(s.split())
    
    # Return cleaned name
    return s