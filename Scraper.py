# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 02:35:45 2023

@author: krisn
"""

import pandas as pd
import glob
import os
import pickle
pickle_path = "A:\\Projects\\OOTP\\Data\\OOTP_Data_Total.p"
used_tournaments_path = "A:\\Projects\\OOTP\\Data\\Scraped_Tournaments.p"

def get_data(file_path, p_file_path):
    if os.path.isfile(p_file_path):
        old_pickle = pickle.load(open(p_file_path, "rb"))
    else:
        old_pickle = pd.DataFrame()
        
    stats = pd.read_html(open(file_path,"r"))[1]
    
    stats = get_tournament(stats)
        
    if len(old_pickle.columns) == len(stats.columns) and all(old_pickle.columns == stats.columns):    
        new_table = pd.concat([old_pickle, stats]).drop_duplicates()
        
        pickle.dump(new_table, open(p_file_path, "wb"))
        
def get_tournament(data):
    tournament_mapping = {"Iron":"ID","Iron Cap":"RL","Bronze":"Claim","Bronze Cap":"ORG","Silver":"LG",
                          "Silver Cap":"DOB","Gold":"Age","Gold Cap":"City","Low Diamond":"HT",
                          "Low Diamond Cap":"WT","Diamond":"EXP","Diamond Cap":"LEA","Open":"AD",
                          "Open Cap":"LOY","Perfect Draft":"GRE","Low Iron":"WE"}
    tournament = tournament_mapping[data.columns[0]]
    data = data.drop(data.columns[0], index = 1)
    data.insert(loc=0, column = "Tournament", value = [tournament]*len(data.index))
    return data
        
def scrape_tournaments(pickle_path, tournaments_path):
    if os.path.isfile(pickle_path):
        current_data = pickle.load(open(pickle_path, "rb"))
    else:
        current_data = None
        
    if os.path.isfile(tournaments_path):
        current_tournaments = pickle.load(open(tournaments_path, "rb"))
    else:
        current_tournaments = []
        
    file_home = "C:\\Users\\krisn\\OneDrive\\Documents\\Out of the Park Developments\\OOTP Baseball 24\\saved_games\\"
    os.chdir(file_home)
    tournaments = glob.glob("7ea[1-2].*")
    files = []
    
    for t in tournaments:
        t_files = glob.glob(f"{t}\\news\\html\\temp\\*")
        if len(t_files) > 0:
            for file in t_files:
                if file not in current_tournaments:
                    files.append(file)
                    
    for f in files:
        get_data(file, pickle_path)
    
scrape_tournaments(pickle_path, tournaments_path)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    