#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Tony Chang (42716403@qq.com)

import json, os, pickle
from para_conc.core.lemma_map import LEMMA_MAP
from para_conc.core.search.search import SearchRequest
from para_conc.core.search.searcher import Searcher
from collections import defaultdict

class ParaConc:
    def __init__(self):
        self._currentDir = os.getcwd()
        self._dataDir = os.path.join(self._currentDir, "app_data")
        self._corpusRoot = os.path.join(self._dataDir, "corpus")
        self._datFileDir = os.path.join(self._dataDir, "temp_data")
        self._workFileDir = os.path.join(self._dataDir, "workfiles")  
        self._custom_dict = os.path.join(self._workFileDir, "bi_term_dict.txt") 
        self._stopword_zh_path = os.path.join(self._workFileDir, "stopword_zh.txt")
        self._stopword_en_path = os.path.join(self._workFileDir, "stopword_en.txt")
        self.bi_dict = {}          
        self.corpora = []           
        self._warning ={}          
        self._searcher = Searcher()
        self._stps_zh = []         
        self._stps_en = []         
        self.load_dat()             
        
    def compare_list(self, j_list, d_list):
        mj_list = [y.replace('.json',"") for (x,y) in j_list]
        md_list = [y.replace('.dat',"") for (x,y) in d_list]
        single_list = []
        f_list = []
        for x in mj_list:
            if x not in md_list:
                single_list.append(x)
        for y in md_list:
            if y not in mj_list:
                if y not in single_list:
                    single_list.append(y)
        if single_list:
            for z in single_list:
                for (x, y) in j_list:
                    if z in y:
                        f_list.append((x,y))
        return f_list
        
    def load_dat(self, quest=''):
        self._warning.clear()
        self._searcher.en_lemma_dict = LEMMA_MAP
        self.load_custom_dict()
        self.load_stop_list()
        json_list = [(os.path.join(self._corpusRoot, x), x.replace(".json","")) for x in os.listdir(self._corpusRoot) if x.endswith(".json")]
        pickle_list = [(os.path.join(self._datFileDir, y), y.replace(".dat","")) for y in os.listdir(self._datFileDir) if y.endswith(".dat")]
        if pickle_list and json_list:
            self.corpora = pickle_list
            f_list = self.compare_list(json_list, pickle_list)
            if f_list:
                self._warning['list']=f_list
                self._warning['type']="dat missing"
        elif pickle_list:
            self.corpora = pickle_list
        elif json_list:
            self._warning['list']=json_list
            self._warning['type']='dat missing'
        else:
            self._warning['list']=[]
            self._warning['type']='None'
                
    def load_custom_dict(self):    
        with open(self._custom_dict, "rt", encoding= "utf-8-sig") as f: 
            lines = [line.strip() for line in f.readlines() if line]
            for line in lines:
                if "\t" in line:
                    parts = line.split("\t")
                    if parts[0] not in self.bi_dict.keys():
                        self.bi_dict[parts[0]]=parts[1].split("|")
                        
    def load_stop_list(self):      
        if os.path.isfile(self._stopword_zh_path):
            with open (self._stopword_zh_path, "rt", encoding="utf-8-sig") as f:
                self._stps_zh = [x.strip() for x in f.readlines() if x.strip()]
                
        if os.path.isfile(self._stopword_en_path):
            with open (self._stopword_en_path, "rt", encoding="utf-8-sig") as f:
                self._stps_en = [y.strip() for y in f.readlines() if y.strip()]
    
    def search(self, corpus, req): 
        return self._searcher.search(corpus, req)

