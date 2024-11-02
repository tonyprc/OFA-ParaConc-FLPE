#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Specific Corpus for the books of Governance of China Volume 1 to 4
# This is a private corpus, used within campus only
# Copyright (c) 2024 Tony Chang (42716403@qq.com)

import re, copy, json
from collections import Counter, defaultdict
from para_conc.core.statistics import Statistics

class Note:
    def __init__(self):
        self.num = 0          
        self.index = ""           
        self.index_tag = ""          
        self.note = ""         
        self.note_tag = ""     
        self.para_count = 0
        self.sent_count = 0    
        self.seg_count = 0    
        self.raw_text = ""
        self.tag_text = ""
       
class Sent:
    def __init__(self):
        self.num = 0     
        self.zh = ""     
        self.en = ""      
        self.zh_tag = ""  
        self.en_tag = "" 
        self.zh_sent_count = 0 
        self.zh_seg_count = 0  
        self.en_sent_count = 0 
        self.en_seg_count = 0  
        self.bi_sent_ratio = "" 
        self.bi_seg_ratio = "" 
         
class Para:
    def __init__(self):
        self.num = 0     
        self.sents = []   
        self.bi_sent_count = 0 
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0    
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""
             
class Article:
    def __init__(self):
        self.num = 0
        self.sect_id = ""      
        self.sect_num = 0
        self.type_zh = ""      
        self.type_en = ""      
        self.genre_zh = ""      
        self.genre_en = ""
        self.title_zh = ""      
        self.title_en = ""      
        self.title_zh_tag = ""  
        self.title_en_tag = ""
        
        self.date_zh = ""       
        self.date_en = ""       
        self.date_zh_tag = ""   
        self.date_en_tag = "" 

        self.notes = ""

        self.paras = []
        
        self.bi_para_count = 0  
        self.bi_sent_count = 0
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()
        
class Info:
    def __init__(self):
        self.num = 0
        self.id_en = "info"  
        self.id_zh = "概况"
        self.type_zh = ""               
        self.type_en = ""   
        self.genre_zh = ""                  
        self.genre_en = ""   
        self.title_zh = ""           
        self.title_zh_tag = ""         
        self.title_en = ""        
        self.title_en_tag = ""
        
        self.paras =[]
        
        self.bi_para_count = 0
        self.bi_sent_count = 0
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()
        
class Contents:
    def __init__(self):
        self.num= 0          
        self.id_en = "contents"  
        self.id_zh = "目录"
        self.type_zh = ""                    
        self.type_en = ""    
        self.genre_zh = ""                   
        self.genre_en = ""   
        self.title_zh = ""      
        self.title_en = ""      
        self.title_zh_tag = ""  
        self.title_en_tag = ""  
        
        self.paras = []      
        
        self.bi_para_count = 0
        self.bi_sent_count = 0
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()
        
class Preface:
    def __init__(self):
        self.num = 0
        self.id_en = "preface"  
        self.id_zh = "前言"
        self.type_zh = ""                  
        self.type_en = ""    
        self.genre_zh = ""                  
        self.genre_en = ""   
        self.title_zh = ""           
        self.title_zh_tag = ""         
        self.title_en = ""        
        self.title_en_tag = ""
        
        self.articles =[]
        
        self.zh_para_count = 0
        self.zh_sent_count = 0
        self.zh_seg_count = 0
        self.en_para_count = 0
        self.en_sent_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()
        
class Theme:
    def __init__(self):
        self.num= 0          
        self.id_en = "theme"  
        self.id_zh = "主题"
        self.type_zh = ""              
        self.type_en = ""    
        self.genre_zh = ""                 
        self.genre_en = ""   
        self.title_zh = ""      
        self.title_en = ""      
        self.title_zh_tag = ""  
        self.title_en_tag = ""  
        
        self.articles = []
        
        self.article_count = 0  
        self.bi_para_count = 0
        self.bi_sent_count = 0
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()
        
class Annex:
    def __init__(self):
        self.num = 0
        self.id_en = "annex"  
        self.id_zh = "附录"
        self.type_zh = ""                
        self.type_en = ""    
        self.genre_zh = ""                     
        self.genre_en = ""   
        self.title_zh = ""           
        self.title_zh_tag = ""         
        self.title_en = ""        
        self.title_en_tag = ""
        
        self.articles =[]
        
        self.article_count = 0  
        self.notes_zh_count = 0 
        self.notes_en_count = 0 
        self.bi_para_count = 0
        self.bi_sent_count = 0
        self.zh_para_count = 0
        self.en_para_count = 0
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""

        #------newly added---------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics() 

class Notes:
    def __init__(self):
        self.num = 0
        self.id_en = "notes"  
        self.id_zh = "注释"
        self.type_zh = ""                   
        self.type_en = ""    
        self.genre_zh = ""               
        self.genre_en = ""   
        self.title_zh = ""           
        self.title_zh_tag = ""         
        self.title_en = ""        
        self.title_en_tag = ""           
        self.notes_zh =[]         
        self.notes_en =[]
        self.zh_para_count = 0
        self.zh_sent_count = 0
        self.zh_seg_count = 0
        self.en_para_count = 0
        self.en_sent_count = 0
        self.en_seg_count = 0
        self.bi_para_ratio = 0
        self.bi_sent_ratio = 0
        self.bi_seg_ratio = 0
        self.raw_text_zh = ""
        self.raw_text_en = ""
        self.tag_text_zh = ""
        self.tag_text_en = ""
        
class GocCorpus:
    def __init__(self):
        self.id = ""
        self.type_zh = ""                   
        self.type_en = ""
        self.genre_zh = ""                  
        self.genre_en = ""                  
        self.title_zh = ""                
        self.title_en = ""                
        self.author_zh = ""                  
        self.author_en = ""
        self.translator_zh = ""   # 本库无此项
        self.translator_en = ""   # 本库无此项     
        self.date_zh = ""                    
        self.date_en = ""
        self.place_zh = ""          
        self.place_en = ""
        self.source_zh = ""                 
        self.source_en = ""
        self.volume_zh = ""              
        self.volume_en = ""              
        self.edition_zh = ""             
        self.edition_en = ""              
         
        self.info = ""
        self.contents = ""           
        self.preface = ""       # 本库无此项           
        self.themes = []
        self.chapters = ""      # 本库无此项
        self.annex = ""                      
        
        self.raw_text_zh = ""          
        self.raw_text_en = ""            
        self.tag_text_zh = ""          
        self.tag_text_en = ""
        
        #---------------------
        self.preface_count = 0           
        self.theme_count = 0
        self.chapter_count = 0
        self.annex_count = 0             
        self.note_zh_count = 0              
        self.note_en_count = 0              
        self.article_count = 0              
        
        self.bi_para_count = 0     
        self.bi_sent_count = 0
        self.bi_para_ratio = 0   
        self.bi_sent_ratio = 0  
        self.bi_seg_ratio = 0 
        self.zh_para_count = 0     
        self.en_para_count = 0     
        self.zh_sent_count = 0
        self.en_sent_count = 0
        self.zh_seg_count = 0
        self.en_seg_count = 0
        
        #---------------------   

        self.zh_token_tag_list = []
        self.en_token_tag_list = []
        self.zh_token_tag_freq = {} 
        self.en_token_tag_freq = {}
        
        self.zh_word_tag_list = []
        self.en_word_tag_list = []        
        self.zh_word_tag_freq = {} 
        self.en_word_tag_freq = {}
        self.en_word_tag_freq_list = []
        
        self.zh_token_output_dict = defaultdict(dict)
        self.en_token_output_dict = defaultdict(dict)
        self.zh_word_output_dict = defaultdict(dict)
        self.en_word_output_dict = defaultdict(dict)
        
        self.zh_byte_count = 0
        self.en_byte_count = 0
        self.zh_token_count = 0
        self.en_token_count = 0
        self.zh_type_count = 0
        self.en_type_count = 0        
        self.zh_word_token_count = 0
        self.en_word_token_count = 0                
        self.zh_word_type_count = 0
        self.en_word_type_count = 0
        
        self.zh_word_ttr = 0
        self.en_word_ttr = 0        
        self.zh_word_sttr = 0
        self.en_word_sttr = 0

        self.warnings = []

        self.dat = Statistics()  
    #----------------------------------------------    
    def seg_finder(self, sent, lang="zh"):
        punc_regex = r"[\[〔。，？！；…“”—\.\,\?\!\;:\-\'\"]"
        en_seg_regex = r"[\,\;\:\-\"\']+\s+"
        zh_seg_regex = "[，—：；、]+" 
        sent_num = 0
        seg_num = 0
        s = re.search(punc_regex, sent)
        if not s:               
            sent_num += 1        
            seg_num += 1         
        elif lang == "zh":      
            para = re.sub(r'\[PS\]', r"\n", sent)
            para = re.sub('([。！？\?][。！？\?])', r"\1\n", para) 
            para = re.sub('([。！？\?][”’）])', r"\1\n", para)
            para = re.sub('([”’）][”’）])', r"\1\n", para)
            para = re.sub('([。！？\?])([^”’）])', r"\1\n\2", para)  
            para = re.sub('(\w)([：；])(\w)', r"\1\2\n\3", para)  
            para = re.sub('(\.{6})([^”’）])', r"\1\n\2", para) 
            para = re.sub('(\…{2})([^”’）])', r"\1\n\2", para)
            para = re.sub('([。！？\?][”’）])([^，。！？\?])', r'\1\n\2', para)
            para = re.sub('([！？\?，。])(\n)([！？\?，。])', r'\1\3', para)
            para = re.sub('\ufeff', r"", para)  
            para = re.sub('\n\n', r"\n", para)
            para = re.sub('\n(〔\d+〕)', r'\1\n', para)
            para = para.rstrip()
            para_sents=para.split("\n")
            sents= [x.strip() for x in para_sents if x.strip() and x.lstrip().rstrip() != '〔无〕' ]
            sent_num += len(sents)       
            for st in sents:
                segs = [z for z in re.split(zh_seg_regex, st) if z.strip()!=""]
                seg_num += len(segs) 
        elif lang == "en":            
            para = re.sub(r'\[PS\]', r"\n", sent)
            para = re.sub('(;’|;|;"|;”) ', r"\1\n", para)
            para = re.sub('(\.) ', r"\1\n", para)
            para = re.sub('(\?|\?\'|\?"|\?”)\s+([A-Z“‘]) ', r"\1\n\2", para)
            para = re.sub('([’”])\s+([‘“])', r"\1\n\2", para)
            para = re.sub('(,”|,"|,\'|,’)\n', r"\1 ", para)
            para = re.sub('(Mr\.|Mrs.)\n', r"\1 ", para)
            para = re.sub('([A-Z]\.)\n([A-Z]\.)\n([A-Z])', r"\1 \2 \3", para)
            para = re.sub('(\.)\n(\.)\n(\.\n)', r"\1\2\3", para)
            para = re.sub('(\s[A-Z]\.|[\n“\"\'][A-Z]\.)\n([A-Z])', r"\1 \2", para)
            para = re.sub('(\.”)\s+([A-Z])', r"\1\n\2", para)            
            sents= [y.strip() for y in para.split("\n") if y.strip()!="" and y.lstrip().rstrip() != '[UnTr]']
            sent_num += len(sents)
            for st in sents:
                segs = [z for z in re.split(en_seg_regex, st) if z.strip()!=""]
                seg_num += len(segs)
        else:
            pass
        return sent_num, seg_num
    
    def get_ratio(self, zh_count, en_count):
        try:
            if en_count == 0 or zh_count == 0: 
                bi_ratio_result = f"{zh_count}:{en_count}"
            else:                            
                bi_ratio = en_count / zh_count
                bi_ratio_result = f"1:{bi_ratio:.2f}"
                if bi_ratio_result.endswith(".00"):
                    bi_ratio_result = bi_ratio_result[:-3] 
                elif "." in bi_ratio_result and bi_ratio_result.endswith('0'):
                    bi_ratio_result = bi_ratio_result[:-1] 
                else:
                    pass                      
        except:
            bi_ratio_result = 0 
            self.warnings.append(f"Warning: Critical zero error occured while getting sent and seg ratio")
        return bi_ratio_result 

    def clear_untr_marker(self,text, mark="r-z"):
        if mark == 'r-z':
            clean_text = re.sub(r"\s*\[PS\]\s*","\n", text)
            clean_text = re.sub(r"\|","", clean_text)
            clean_text = re.sub(r"\n\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*\n","\n", clean_text)
            clean_text = re.sub(r"\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*","", clean_text)
            clean_text = re.sub(r"\n\n+","\n", clean_text) 
        elif mark == 't-z':
            clean_text = re.sub(r"\s*\[PS\]/xm\s*","\n", text)
            clean_text = re.sub(r"\|/xn\s*","", clean_text)
            clean_text = re.sub(r"\n\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]/xw\s*\n","\n", clean_text)
            clean_text = re.sub(r"\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]/xw\s*"," ", clean_text)
            clean_text = re.sub(r"\n\n+","\n", clean_text) 
        elif mark == 'r-e':
            clean_text = re.sub(r"\s*\[PS\]\s*","\n", text)
            clean_text = re.sub(r"\|\s*","", clean_text)
            clean_text = re.sub(r"\n\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*\n","\n", clean_text)
            clean_text = re.sub(r"\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*"," ", clean_text)
            clean_text = re.sub(r"\n\n+","\n", clean_text) 
        elif mark == 't-e':
            clean_text = re.sub(r"\s*\[PS\]_XM\s*","\n", text)
            clean_text = re.sub(r"\|_XN\s*","", clean_text)
            clean_text = re.sub(r"\n[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]_XW\s*\n","\n", clean_text)
            clean_text = re.sub(r"[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]_XW\s*"," ", clean_text)
            clean_text = re.sub(r"\n\n+","\n", clean_text) 
        else:
            clean_text = text
        output_text =  re.sub(r"\n\n+","\n", clean_text)
        return output_text
    #----------------------------------------------
    def get_info(self, data):   
        self.type_zh = data["type"][0]
        self.type_en = data["type"][1]
        self.genre_zh = data['genre'][0]
        self.genre_en = data['genre'][1]
        self.title_zh = data['title'][0]
        self.title_en = data['title'][1]
        self.author_zh = data['author'][0]
        self.author_en = data['author'][1]        
        self.date_zh = data['date'][0]
        self.date_en = data['date'][1]
        self.place_zh = data['place'][0]
        self.place_en = data['place'][1]
        self.source_zh = data['source'][0]
        self.source_en = data['source'][1]
        self.volume_zh = data['volume'][0]
        self.volume_en = data['volume'][1]
        self.edition_zh = data['edition'][0]
        self.edition_en = data['edition'][1]
        infos = data['section']['info']
        self.info = Info()
        self.info.num = 1
        self.info.type_zh = self.type_zh
        self.info.type_en = self.type_en
        self.info.genre_zh = self.genre_zh
        self.info.genre_en = self.genre_en
        self.info.title_zh = infos['title']['raw'][0]
        self.info.title_en = infos['title']['raw'][1]
        self.info.title_zh_tag = infos['title']['tag'][0]
        self.info.title_en_tag = infos['title']['tag'][1]     
        info_pas = self.get_paras(infos['paras'], self.id) 
        self.info.paras.extend(info_pas)
        self.info.bi_para_count += len(self.info.paras)
        for pa in self.info.paras:            
            self.info.bi_sent_count += pa.bi_sent_count
            self.info.zh_para_count += pa.zh_para_count
            self.info.en_para_count += pa.en_para_count
            self.info.zh_sent_count += pa.zh_sent_count
            self.info.en_sent_count += pa.en_sent_count
            self.info.zh_seg_count += pa.zh_seg_count
            self.info.en_seg_count += pa.en_seg_count
        self.info.bi_para_ratio = self.get_ratio(self.info.zh_para_count, self.info.en_para_count)
        self.info.bi_sent_ratio = self.get_ratio(self.info.zh_sent_count, self.info.en_sent_count)
        self.info.bi_seg_ratio = self.get_ratio(self.info.zh_seg_count, self.info.en_seg_count)        
        self.info.raw_text_zh = "\n".join([pa.raw_text_zh for pa in self.info.paras])
        self.info.raw_text_en = "\n".join([pa.raw_text_en for pa in self.info.paras])
        self.info.tag_text_zh = "\n".join([pa.tag_text_zh for pa in self.info.paras])
        self.info.tag_text_en = "\n".join([pa.tag_text_en for pa in self.info.paras])
        self.stat_pipeline(self.info)
        self.bi_para_count += self.info.bi_para_count
        self.bi_sent_count += self.info.bi_sent_count
        self.zh_para_count += self.info.zh_para_count
        self.en_para_count += self.info.en_para_count
        self.zh_sent_count += self.info.zh_sent_count
        self.en_sent_count += self.info.en_sent_count
        self.zh_seg_count += self.info.zh_seg_count
        self.en_seg_count += self.info.en_seg_count
        self.bi_para_ratio = self.get_ratio(self.zh_para_count, self.en_para_count)
        self.bi_sent_ratio = self.get_ratio(self.zh_sent_count, self.en_sent_count)
        self.bi_seg_ratio = self.get_ratio(self.zh_seg_count, self.en_seg_count)
        if self.raw_text_zh:
            self.raw_text_zh = self.raw_text_zh + "\n" + self.info.raw_text_zh
        else:
            self.raw_text_zh = self.info.raw_text_zh
        if self.raw_text_en:
            self.raw_text_en = self.raw_text_en + "\n" + self.info.raw_text_en
        else:
            self.raw_text_en = self.info.raw_text_en
        if self.tag_text_zh:
            self.tag_text_zh = self.tag_text_zh + "\n" + self.info.tag_text_zh
        else:
            self.tag_text_zh = self.info.tag_text_zh
        if self.tag_text_zh:
            self.tag_text_zh = self.tag_text_zh + "\n" + self.info.tag_text_zh
        else:
            self.tag_text_zh = self.info.tag_text_zh
            
    def get_contents(self, data):
        cnts = data['section']['contents']
        self.contents = Contents()
        self.contents.num = 1
        self.contents.type_zh = self.type_zh
        self.contents.type_en = self.type_en
        self.contents.genre_zh = self.genre_zh
        self.contents.genre_en = self.genre_en
        self.contents.title_zh = cnts['title']['raw'][0]
        self.contents.title_en = cnts['title']['raw'][1]
        self.contents.title_zh_tag = cnts['title']['tag'][0]
        self.contents.title_en_tag = cnts['title']['tag'][1]     
        conts_pas = self.get_paras(cnts['paras'], self.id) 
        self.contents.paras.extend(conts_pas)
        self.contents.bi_para_count += len(self.contents.paras) 
        for pa in self.contents.paras:            
            self.contents.bi_sent_count += pa.bi_sent_count
            self.contents.zh_para_count += pa.zh_para_count
            self.contents.en_para_count += pa.en_para_count
            self.contents.zh_sent_count += pa.zh_sent_count
            self.contents.en_sent_count += pa.en_sent_count
            self.contents.zh_seg_count += pa.zh_seg_count
            self.contents.en_seg_count += pa.en_seg_count
        self.contents.bi_para_ratio = self.get_ratio(self.contents.zh_para_count, self.contents.en_para_count)
        self.contents.bi_sent_ratio = self.get_ratio(self.contents.zh_sent_count, self.contents.en_sent_count)
        self.contents.bi_seg_ratio = self.get_ratio(self.contents.zh_seg_count, self.contents.en_seg_count)        
        self.contents.raw_text_zh = "\n".join([pa.raw_text_zh for pa in self.contents.paras])
        self.contents.raw_text_en = "\n".join([pa.raw_text_en for pa in self.contents.paras])
        self.contents.tag_text_zh = "\n".join([pa.tag_text_zh for pa in self.contents.paras])
        self.contents.tag_text_en = "\n".join([pa.tag_text_en for pa in self.contents.paras])

        self.stat_pipeline(self.contents)

        self.bi_para_count += self.contents.bi_para_count
        self.bi_sent_count += self.contents.bi_sent_count
        self.zh_para_count += self.contents.zh_para_count
        self.en_para_count += self.contents.en_para_count
        self.zh_sent_count += self.contents.zh_sent_count
        self.en_sent_count += self.contents.en_sent_count
        self.zh_seg_count += self.contents.zh_seg_count
        self.en_seg_count += self.contents.en_seg_count
        self.bi_para_ratio = self.get_ratio(self.zh_para_count, self.en_para_count)
        self.bi_sent_ratio = self.get_ratio(self.zh_sent_count, self.en_sent_count)
        self.bi_seg_ratio = self.get_ratio(self.zh_seg_count, self.en_seg_count)
        if self.raw_text_zh:
            self.raw_text_zh = self.raw_text_zh + "\n" + self.contents.raw_text_zh
        else:
            self.raw_text_zh = self.contents.raw_text_zh
        if self.raw_text_en:
            self.raw_text_en = self.raw_text_en + "\n" + self.contents.raw_text_en
        else:
            self.raw_text_en = self.contents.raw_text_en
        if self.tag_text_zh:
            self.tag_text_zh = self.tag_text_zh + "\n" + self.contents.tag_text_zh
        else:
            self.tag_text_zh = self.contents.tag_text_zh
        if self.tag_text_zh:
            self.tag_text_zh = self.tag_text_zh + "\n" + self.contents.tag_text_zh
        else:
            self.tag_text_zh = self.contents.tag_text_zh

    def get_paras(self, data, data_id=""):      
        pa_obj_group = []
        for k in data.keys():
            goc_pa = Para()
            goc_pa.num = k
            zh_para_count = 1 + data[k]['raw'][0].count("[PS]") 
            en_para_count = 1 + data[k]['raw'][1].count("[PS]")
            zh_test = re.sub(r"\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*","", data[k]['raw'][0]) 
            if zh_test.lstrip().startswith("|[PS]") or zh_test.lstrip().startswith("| [PS]") or zh_test.lstrip().startswith("[PS]"):
                zh_para_count -= 1                                     
            zh_test = re.sub(r"(\s*\|\s*|\s*\[PS\]\s*)","", zh_test)  
            if not zh_test.lstrip().rstrip():                          
                zh_para_count -= 1
            zh_para_count -= data[k]['raw'][0].count("|[PS][无]|[PS]")   
            zh_para_count -= data[k]['raw'][0].count("|[PS]〔无〕|[PS]")
            en_test = re.sub(r"\s*[\[〔]\s*(无|None|NONE|UnTr)\s*[\]〕]\s*","", data[k]['raw'][1])
            if en_test.lstrip().startswith("|[PS]") or en_test.lstrip().startswith("| [PS]")or en_test.lstrip().startswith("[PS]"):
                en_para_count -= 1
            en_test = re.sub(r"(\s*\|\s*|\s*\[PS\]\s*)","", en_test)
            if not en_test.lstrip().rstrip():
                en_para_count -= 1            
            en_para_count -= data[k]['raw'][1].count("|[PS][UnTr]|[PS]")
            en_para_count -= data[k]['raw'][1].count("| [PS][UnTr] | [PS]")
            goc_pa.zh_para_count = zh_para_count 
            goc_pa.en_para_count = en_para_count
            pa_zh = [x for x in data[k]['raw'][0].split("|") if x]
            pa_zht = [a for a in data[k]['tag'][0].split("|/xn ") if a]
            pa_en = [y for y in data[k]['raw'][1].split("|") if y]
            pa_ent = [b for b in data[k]['tag'][1].split("|_XN ") if b]
            if len(pa_zh) == len(pa_en) == len(pa_zht) == len(pa_ent):
                goc_pa.bi_sent_count += len(pa_zh)             
            else:
                self.warnings.append(f"Critical Error Occurred in file {data_id}: bi sents are not aligned!\nzh_raw: {len(pa_zh)}, en_raw: {len(pa_en)}, zh_tag: {len(pa_zht)}, en_tag: {len(pa_ent)}")
                break
            for j, (zs, es, zt, et) in enumerate(zip(pa_zh, pa_en, pa_zht, pa_ent),start = 1):
                goc_st = Sent()
                goc_st.num = j
                goc_st.zh = zs.lstrip().rstrip()
                goc_st.zh_tag = zt.lstrip().rstrip()
                goc_st.en = es.lstrip().rstrip()
                goc_st.en_tag = et.lstrip().rstrip()                
                goc_st.zh_sent_count, goc_st.zh_seg_count = self.seg_finder(goc_st.zh, lang="zh") 
                goc_st.en_sent_count, goc_st.en_seg_count = self.seg_finder(goc_st.en, lang="en") 
                goc_pa.zh_sent_count += goc_st.zh_sent_count 
                goc_pa.en_sent_count += goc_st.en_sent_count
                goc_pa.zh_seg_count += goc_st.zh_seg_count    
                goc_pa.en_seg_count += goc_st.en_seg_count                
                goc_st.bi_sent_ratio = f"{goc_st.zh_sent_count}:{goc_st.en_sent_count}"  
                goc_st.bi_seg_ratio = f"{goc_st.zh_seg_count}:{goc_st.en_seg_count}"
                goc_pa.sents.append(goc_st)
            goc_pa.raw_text_zh = "".join([st.zh for st in goc_pa.sents if st.zh != "〔无〕" and st.zh != "[无]"])
            goc_pa.raw_text_en = " ".join([st.en for st in goc_pa.sents if st.en not in ["[None]", "[UnTr]", "[NONE]"]])
            goc_pa.tag_text_zh = " ".join([st.zh_tag for st in goc_pa.sents if st.zh_tag != "〔无〕/xw" and st.zh != "[无]/xw"])
            goc_pa.tag_text_en = " ".join([st.en_tag for st in goc_pa.sents if st.en_tag not in ["[None]_XW", "[UnTr]_XW", "[NONE]_XW"]])
            goc_pa.bi_para_ratio = self.get_ratio(goc_pa.zh_para_count, goc_pa.en_para_count)
            goc_pa.bi_sent_ratio = self.get_ratio(goc_pa.zh_sent_count, goc_pa.en_sent_count) 
            goc_pa.bi_seg_ratio = self.get_ratio(goc_pa.zh_seg_count, goc_pa.en_seg_count)             
            pa_obj_group.append(goc_pa)
        return pa_obj_group
    
    def get_theme(self, data):
        tms = data['section']['theme']
        for tm_num in tms.keys():
            tm_sect = Theme()
            tm_sect.num = tm_num
            tm_sect.type_zh = self.type_zh
            tm_sect.type_en = self.type_en
            tm_sect.genre_zh = self.genre_zh
            tm_sect.genre_en = self.genre_en
            tm_sect.title_zh = tms[tm_num]['title']['raw'][0]
            tm_sect.title_en = tms[tm_num]['title']['raw'][1]
            tm_sect.title_zh_tag = tms[tm_num]['title']['tag'][0]
            tm_sect.title_en_tag = tms[tm_num]['title']['tag'][1]
            tm_sect.zh_para_count += 1
            tm_sect.en_para_count += 1
            tm_sect.zh_sent_count += 1
            tm_sect.en_sent_count += 1
            tm_sect.zh_seg_count += 1
            tm_sect.zh_seg_count += 1
            tm_sect.bi_para_count += 1
            tm_sect.bi_sent_count += 1            
            art_dict = tms[tm_num]['article']
            for art_num in art_dict.keys():
                tm_art = Article()
                tm_art.num = art_num
                tm_art.sect_id = 'theme'
                tm_art.sect_num = tm_num
                tm_art.type_zh = self.type_zh
                tm_art.type_en = self.type_en
                tm_art.genre_zh = self.genre_zh
                tm_art.genre_en = self.genre_en
                tm_art.title_zh = art_dict[art_num]['title']['raw'][0]
                tm_art.title_en = art_dict[art_num]['title']['raw'][1]
                tm_art.title_zh_tag = art_dict[art_num]['title']['tag'][0]
                tm_art.title_en_tag = art_dict[art_num]['title']['tag'][1]
                tm_art.date_zh = art_dict[art_num]['date']['raw'][0]
                tm_art.date_en = art_dict[art_num]['date']['raw'][1]
                tm_art.date_zh_tag = art_dict[art_num]['date']['tag'][0]
                tm_art.date_en_tag = art_dict[art_num]['date']['tag'][1]
                para_dict = art_dict[art_num]['paras']                
                pas = self.get_paras(para_dict, tm_art.title_zh)
                tm_art.paras.extend(pas)
                tm_art.bi_para_count = len(tm_art.paras)
                for pa in tm_art.paras: 
                    if not tm_art.raw_text_zh:
                        tm_art.raw_text_zh = pa.raw_text_zh.lstrip().rstrip() 
                    else:
                        tm_art.raw_text_zh += "\n"+pa.raw_text_zh.lstrip().rstrip()
                    if not tm_art.raw_text_en:
                        tm_art.raw_text_en = pa.raw_text_en.lstrip().rstrip()
                    else:
                        tm_art.raw_text_en += "\n"+pa.raw_text_en.lstrip().rstrip()
                    if not tm_art.tag_text_zh:
                        tm_art.tag_text_zh = pa.tag_text_zh.lstrip().rstrip()
                    else:
                        tm_art.tag_text_zh += "\n"+pa.tag_text_zh.lstrip().rstrip()
                    if not tm_art.tag_text_en:
                        tm_art.tag_text_en = pa.tag_text_en.lstrip().rstrip()
                    else:
                        tm_art.tag_text_en += "\n"+pa.tag_text_en.lstrip().rstrip()
                    tm_art.bi_sent_count += pa.bi_sent_count
                    tm_art.zh_para_count += pa.zh_para_count
                    tm_art.en_para_count += pa.en_para_count
                    tm_art.zh_sent_count += pa.zh_sent_count
                    tm_art.en_sent_count += pa.en_sent_count
                    tm_art.zh_seg_count += pa.zh_seg_count
                    tm_art.en_seg_count += pa.en_seg_count
                notes_dict = art_dict[art_num].get('notes',"")
                if notes_dict:
                    tm_art.notes = self.get_notes(art_dict[art_num]['notes'])
                    if tm_art.notes.raw_text_zh: 
                        tm_art.raw_text_zh += "\n"+tm_art.notes.raw_text_zh
                        tm_art.tag_text_zh += "\n"+tm_art.notes.tag_text_zh
                    if tm_art.notes.raw_text_en:
                        tm_art.raw_text_en += "\n"+tm_art.notes.raw_text_en
                        tm_art.tag_text_en += "\n"+tm_art.notes.tag_text_en
                    tm_art.zh_para_count += tm_art.notes.zh_para_count 
                    tm_art.en_para_count += tm_art.notes.en_para_count
                    tm_art.zh_sent_count += tm_art.notes.zh_sent_count
                    tm_art.en_sent_count += tm_art.notes.en_sent_count
                    tm_art.zh_seg_count += tm_art.notes.zh_seg_count
                    tm_art.en_seg_count += tm_art.notes.en_seg_count
                tm_art.bi_para_ratio =  self.get_ratio(tm_art.zh_para_count,tm_art.en_para_count) 
                tm_art.bi_sent_ratio =  self.get_ratio(tm_art.zh_sent_count,tm_art.en_sent_count)
                tm_art.bi_seg_ratio =  self.get_ratio(tm_art.zh_seg_count,tm_art.en_seg_count)
                self.stat_pipeline(tm_art)                
                tm_sect.articles.append(tm_art)            
                if not tm_sect.raw_text_zh:
                    tm_sect.raw_text_zh = tm_sect.title_zh + "\n" + tm_art.raw_text_zh
                else:
                    tm_sect.raw_text_zh += "\n" + tm_art.raw_text_zh
                if not tm_sect.raw_text_en:
                    tm_sect.raw_text_en = tm_sect.title_en + "\n" + tm_art.raw_text_en
                else:
                    tm_sect.raw_text_en += "\n" + tm_art.raw_text_en
                if not tm_sect.tag_text_zh:
                    tm_sect.tag_text_zh = tm_sect.title_zh_tag + "\n" + tm_art.tag_text_zh
                else:
                    tm_sect.tag_text_zh += "\n" + tm_art.tag_text_zh
                if not tm_sect.tag_text_en:
                    tm_sect.tag_text_en = tm_sect.title_en_tag + "\n" + tm_art.tag_text_en
                else:
                    tm_sect.tag_text_en += "\n" + tm_art.tag_text_en
                tm_sect.bi_para_count += tm_art.bi_para_count  
                tm_sect.bi_sent_count += tm_art.bi_sent_count  
                tm_sect.zh_para_count += tm_art.zh_para_count
                tm_sect.en_para_count += tm_art.en_para_count
                tm_sect.zh_sent_count += tm_art.zh_sent_count
                tm_sect.en_sent_count += tm_art.en_sent_count
                tm_sect.zh_seg_count += tm_art.zh_seg_count
                tm_sect.en_seg_count += tm_art.en_seg_count
            tm_sect.bi_para_ratio = self.get_ratio(tm_sect.zh_para_count,tm_sect.en_para_count)
            tm_sect.bi_sent_ratio = self.get_ratio(tm_sect.zh_sent_count,tm_sect.en_sent_count)
            tm_sect.bi_seg_ratio = self.get_ratio(tm_sect.zh_seg_count,tm_sect.en_seg_count)
            self.stat_pipeline(tm_sect)            
            self.themes.append(tm_sect)
        for tm_sect in self.themes:
            self.bi_para_count += tm_sect.bi_para_count
            self.bi_sent_count += tm_sect.bi_sent_count
            self.zh_para_count += tm_sect.zh_para_count
            self.en_para_count += tm_sect.en_para_count
            self.zh_sent_count += tm_sect.zh_sent_count
            self.en_sent_count += tm_sect.en_sent_count
            self.zh_seg_count += tm_sect.zh_seg_count
            self.en_seg_count += tm_sect.en_seg_count
            self.raw_text_zh += "\n"+tm_sect.raw_text_zh
            self.raw_text_en += "\n"+tm_sect.raw_text_en
            self.tag_text_zh += "\n"+tm_sect.tag_text_zh
            self.tag_text_en += "\n"+tm_sect.tag_text_en
        self.bi_para_ratio = self.get_ratio(self.zh_para_count,self.en_para_count)
        self.bi_sent_ratio = self.get_ratio(self.zh_sent_count,self.en_sent_count)
        self.bi_seg_ratio = self.get_ratio(self.zh_seg_count,self.en_seg_count)            

    def get_notes(self, file_dict):
        zh_title = file_dict['zh_title'].get('raw',"")
        en_title = file_dict['en_title'].get('raw',"")
        zh_title_tag = file_dict['zh_title'].get('tag',"")
        en_title_tag = file_dict['en_title'].get('tag',"")
        zh_notes = file_dict['zh'].get('raw',"")
        zh_notes_tag = file_dict['zh'].get('tag',"")
        en_notes = file_dict['en'].get('raw',"")
        en_notes_tag = file_dict['en'].get('tag',"")
        invalid_regex = r"[〔\[](无|None|NONE|UnTr)[\]〕]"
        if zh_notes or en_notes:
            art_notes = Notes()
            art_notes.type_zh = self.type_zh
            art_notes.type_en = self.type_en
            art_notes.genre_zh = self.genre_zh
            art_notes.genre_en = self.genre_en
            if zh_notes and zh_notes_tag:
                if zh_title:
                    art_notes.title_zh = zh_title      
                if zh_title_tag:
                    art_notes.title_zh_tag = zh_title_tag
                for ((k, v),(kg,vg)) in zip(zh_notes,zh_notes_tag):
                    r = re.search(invalid_regex, v)
                    if not r:
                        new_note = Note()
                        new_note.num = k
                        new_note.index = k
                        new_note.index_tag = kg
                        new_note.note = v
                        new_note.note_tag = vg
                        new_note.sent_count, new_note.seg_count= self.seg_finder(v, 'zh')
                        new_note.para_count = 1 + v.count("[PS]")
                        new_note.raw_text = new_note.index + " " + new_note.note
                        new_note.tag_text = new_note.index_tag + " " + new_note.note_tag
                        art_notes.notes_zh.append(new_note)
            if en_notes and en_notes_tag:
                if en_title:
                    art_notes.title_en = en_title                
                if en_title_tag:
                    art_notes.title_en_tag = en_title_tag
                for ((k, v),(kg,vg)) in zip(en_notes,en_notes_tag):
                    r = re.search(invalid_regex, v)
                    if not r:
                        new_note = Note() 
                        new_note.num = k
                        new_note.index = k
                        new_note.index_tag = kg
                        new_note.note = v
                        new_note.note_tag = vg
                        new_note.sent_count, new_note.seg_count = self.seg_finder(v, 'en')
                        new_note.para_count = 1 + v.count("[PS]")
                        new_note.raw_text = new_note.index + " " + new_note.note
                        new_note.tag_text = new_note.index_tag + " " + new_note.note_tag
                        art_notes.notes_en.append(new_note)
            if art_notes.notes_zh:
                if art_notes.title_zh:
                    art_notes.raw_text_zh = art_notes.title_zh
                    art_notes.tag_text_zh = art_notes.title_zh_tag
                    art_notes.zh_para_count += 1
                for note in art_notes.notes_zh:
                    if not art_notes.raw_text_zh:
                        art_notes.raw_text_zh = note.raw_text
                        art_notes.tag_text_zh = note.tag_text
                    else:
                        art_notes.raw_text_zh += "\n"+note.raw_text
                        art_notes.tag_text_zh += "\n"+note.tag_text                        
                    art_notes.zh_para_count += note.para_count
                    art_notes.zh_sent_count += note.sent_count
                    art_notes.zh_seg_count += note.seg_count
            if art_notes.notes_en:
                if art_notes.title_en:
                    art_notes.raw_text_en = art_notes.title_en
                    art_notes.tag_text_en = art_notes.title_en_tag
                    art_notes.en_para_count += 1
                for note in art_notes.notes_en:
                    if not art_notes.raw_text_en:
                        art_notes.raw_text_en = note.raw_text
                        art_notes.tag_text_en = note.tag_text
                    else:
                        art_notes.raw_text_en += "\n"+note.raw_text
                        art_notes.tag_text_en += "\n"+note.tag_text 
                    art_notes.en_para_count += note.para_count
                    art_notes.en_sent_count += note.sent_count
                    art_notes.en_seg_count += note.seg_count
            if art_notes:
                art_notes.bi_para_ratio = self.get_ratio(art_notes.zh_para_count,art_notes.en_para_count)
                art_notes.bi_sent_ratio = self.get_ratio(art_notes.zh_sent_count,art_notes.en_sent_count)
                art_notes.bi_seg_ratio = self.get_ratio(art_notes.zh_seg_count,art_notes.en_seg_count)
        else:
            art_notes = ""
        return art_notes

    def get_preface(self, data):
        pass

    def get_annex(self, data):
        ax = data['section'].get('appendix',"")
        if ax:
            ax_sect = Annex()
            ax_sect.num = 1
            ax_sect.type_zh = self.type_zh
            ax_sect.type_en = self.type_en
            ax_sect.genre_zh = self.genre_zh
            ax_sect.genre_en = self.genre_en
            ax_sect.title_zh = "附录"
            ax_sect.title_en = "Appendix"
            ax_sect.title_zh_tag = "附录/n"
            ax_sect.title_en_tag = "Appendix_NNP"
            ax_sect.zh_para_count += 1
            ax_sect.en_para_count += 1
            ax_sect.zh_sent_count += 1
            ax_sect.en_sent_count += 1
            ax_sect.zh_seg_count += 1
            ax_sect.zh_seg_count += 1
            ax_sect.bi_para_count += 1
            ax_sect.bi_sent_count += 1
            for art_num in ax.keys():
                ax_art = Article()
                ax_art.num = art_num
                ax_art.sect_id = 'appendix'
                ax_art.sect_num = 1
                ax_art.type_zh = self.type_zh
                ax_art.type_en = self.type_en
                ax_art.genre_zh = self.genre_zh
                ax_art.genre_en = self.genre_en
                ax_art.title_zh = ax[art_num]['title']['raw'][0]
                ax_art.title_en = ax[art_num]['title']['raw'][1]
                ax_art.title_zh_tag = ax[art_num]['title']['tag'][0]
                ax_art.title_en_tag = ax[art_num]['title']['tag'][1]
                para_dict = ax[art_num]['paras']                
                pas = self.get_paras(para_dict, ax_art.title_zh) 
                ax_art.paras.extend(pas)
                ax_art.bi_para_count = len(ax_art.paras)
                for pa in ax_art.paras: 
                    if not ax_art.raw_text_zh:
                        ax_art.raw_text_zh = pa.raw_text_zh.lstrip().rstrip()
                    else:
                        ax_art.raw_text_zh += "\n"+pa.raw_text_zh.lstrip().rstrip()
                    if not ax_art.raw_text_en:
                        ax_art.raw_text_en = pa.raw_text_en.lstrip().rstrip()
                    else:
                        ax_art.raw_text_en += "\n"+pa.raw_text_en.lstrip().rstrip()
                    if not ax_art.tag_text_zh:
                        ax_art.tag_text_zh = pa.tag_text_zh.lstrip().rstrip()
                    else:
                        ax_art.tag_text_zh += "\n"+pa.tag_text_zh.lstrip().rstrip()
                    if not ax_art.tag_text_en:
                        ax_art.tag_text_en = pa.tag_text_en.lstrip().rstrip()
                    else:
                        ax_art.tag_text_en += "\n"+pa.tag_text_en.lstrip().rstrip()
                    ax_art.bi_sent_count += pa.bi_sent_count
                    ax_art.zh_para_count += pa.zh_para_count
                    ax_art.en_para_count += pa.en_para_count
                    ax_art.zh_sent_count += pa.zh_sent_count
                    ax_art.en_sent_count += pa.en_sent_count
                    ax_art.zh_seg_count += pa.zh_seg_count
                    ax_art.en_seg_count += pa.en_seg_count
                notes_dict = ax[art_num].get("notes","")
                if notes_dict:
                    ax_art.notes = self.get_notes(ax[art_num]['notes'])
                    if ax_art.notes.raw_text_zh: 
                        ax_art.raw_text_zh += "\n"+ax_art.notes.raw_text_zh
                        ax_art.tag_text_zh += "\n"+ax_art.notes.tag_text_zh
                    if ax_art.notes.raw_text_en:
                        ax_art.raw_text_en += "\n"+ax_art.notes.raw_text_en
                        ax_art.tag_text_en += "\n"+ax_art.notes.tag_text_en
                    ax_art.zh_para_count += ax_art.notes.zh_para_count 
                    ax_art.en_para_count += ax_art.notes.en_para_count
                    ax_art.zh_sent_count += ax_art.notes.zh_sent_count
                    ax_art.en_sent_count += ax_art.notes.en_sent_count
                    ax_art.zh_seg_count += ax_art.notes.zh_seg_count
                    ax_art.en_seg_count += ax_art.notes.en_seg_count
                ax_art.bi_para_ratio =  self.get_ratio(ax_art.zh_para_count,ax_art.en_para_count) 
                ax_art.bi_sent_ratio =  self.get_ratio(ax_art.zh_sent_count,ax_art.en_sent_count)
                ax_art.bi_seg_ratio =  self.get_ratio(ax_art.zh_seg_count,ax_art.en_seg_count)
                self.stat_pipeline(ax_art)
                ax_sect.articles.append(ax_art)            
                if not ax_sect.raw_text_zh:
                    ax_sect.raw_text_zh = ax_sect.title_zh + "\n" + ax_art.raw_text_zh
                else:
                    ax_sect.raw_text_zh += "\n" + ax_art.raw_text_zh
                if not ax_sect.raw_text_en:
                    ax_sect.raw_text_en = ax_sect.title_en + "\n" + ax_art.raw_text_en
                else:
                    ax_sect.raw_text_en += "\n" + ax_art.raw_text_en
                if not ax_sect.tag_text_zh:
                    ax_sect.tag_text_zh = ax_sect.title_zh_tag + "\n" + ax_art.tag_text_zh
                else:
                    ax_sect.tag_text_zh += "\n" + ax_art.tag_text_zh
                if not ax_sect.tag_text_en:
                    ax_sect.tag_text_en = ax_sect.title_en_tag + "\n" + ax_art.tag_text_en
                else:
                    ax_sect.tag_text_en += "\n" + ax_art.tag_text_en
                ax_sect.bi_para_count += ax_art.bi_para_count 
                ax_sect.bi_sent_count += ax_art.bi_sent_count  
                ax_sect.zh_para_count += ax_art.zh_para_count
                ax_sect.en_para_count += ax_art.en_para_count
                ax_sect.zh_sent_count += ax_art.zh_sent_count
                ax_sect.en_sent_count += ax_art.en_sent_count
                ax_sect.zh_seg_count += ax_art.zh_seg_count
                ax_sect.en_seg_count += ax_art.en_seg_count
            ax_sect.bi_para_ratio = self.get_ratio(ax_sect.zh_para_count,ax_sect.en_para_count)
            ax_sect.bi_sent_ratio = self.get_ratio(ax_sect.zh_sent_count,ax_sect.en_sent_count)
            ax_sect.bi_seg_ratio = self.get_ratio(ax_sect.zh_seg_count,ax_sect.en_seg_count)
            self.stat_pipeline(ax_sect)
            self.annex = ax_sect
            self.bi_para_count += ax_sect.bi_para_count
            self.bi_sent_count += ax_sect.bi_sent_count
            self.zh_para_count += ax_sect.zh_para_count
            self.en_para_count += ax_sect.en_para_count
            self.zh_sent_count += ax_sect.zh_sent_count
            self.en_sent_count += ax_sect.en_sent_count
            self.zh_seg_count += ax_sect.zh_seg_count
            self.en_seg_count += ax_sect.en_seg_count
            self.raw_text_zh += "\n"+ax_sect.raw_text_zh
            self.raw_text_en += "\n"+ax_sect.raw_text_en
            self.tag_text_zh += "\n"+ax_sect.tag_text_zh
            self.tag_text_en += "\n"+ax_sect.tag_text_en
        self.bi_para_ratio = self.get_ratio(self.zh_para_count,self.en_para_count)
        self.bi_sent_ratio = self.get_ratio(self.zh_sent_count,self.en_sent_count)
        self.bi_seg_ratio = self.get_ratio(self.zh_seg_count,self.en_seg_count)
        
    def get_text(self):
        for para in self.infos:
            if not self.raw_text_zh:
                self.raw_text_zh = para.raw_text_zh.lstrip().rstrip() 
            else:
                self.raw_text_zh += "\n"+para.raw_text_zh.lstrip().rstrip()
            if not self.raw_text_en:
                self.raw_text_en = para.raw_text_en.lstrip().rstrip()
            else:
                self.raw_text_en += "\n"+para.raw_text_en.lstrip().rstrip()
            if not self.tag_text_zh:
                self.tag_text_zh = para.tag_text_zh.lstrip().rstrip()
            else:
                self.tag_text_zh += "\n"+para.tag_text_zh.lstrip().rstrip()
            if not self.tag_text_en:
                self.tag_text_en = para.tag_text_en.lstrip().rstrip()
            else:
                self.tag_text_en += "\n"+para.tag_text_en.lstrip().rstrip()
            self.zh_para_count += para.zh_para_count 
            self.en_para_count += para.en_para_count
            self.zh_sent_count += para.zh_sent_count
            self.zh_seg_count += para.zh_seg_count
            self.en_sent_count += para.en_sent_count
            self.en_seg_count += para.en_seg_count
        for para in self.contents:
            if not self.raw_text_zh:
                self.raw_text_zh = para.raw_text_zh.lstrip().rstrip() 
            else:
                self.raw_text_zh += "\n"+para.raw_text_zh.lstrip().rstrip()
            if not self.raw_text_en:
                self.raw_text_en = para.raw_text_en.lstrip().rstrip()
            else:
                self.raw_text_en += "\n"+para.raw_text_en.lstrip().rstrip()
            if not self.tag_text_zh:
                self.tag_text_zh = para.tag_text_zh.lstrip().rstrip()
            else:
                self.tag_text_zh += "\n"+para.tag_text_zh.lstrip().rstrip()
            if not self.tag_text_en:
                self.tag_text_en = para.tag_text_en.lstrip().rstrip()
            else:
                self.tag_text_en += "\n"+para.tag_text_en.lstrip().rstrip()
            self.zh_para_count += para.zh_para_count
            self.en_para_count += para.en_para_count
            self.zh_sent_count += para.zh_sent_count
            self.zh_seg_count += para.zh_seg_count
            self.en_sent_count += para.en_sent_count
            self.en_seg_count += para.en_seg_count
        if self.prefaces:
            for art in self.prefaces:
                if not self.raw_text_zh:
                    self.raw_text_zh = art.raw_text_zh.lstrip().rstrip() 
                else:
                    self.raw_text_zh += "\n"+art.raw_text_zh.lstrip().rstrip()
                if not self.raw_text_en:
                    self.raw_text_en = art.raw_text_en.lstrip().rstrip()
                else:
                    self.raw_text_en += "\n"+art.raw_text_en.lstrip().rstrip()
                if not self.tag_text_zh:
                    self.tag_text_zh = art.tag_text_zh.lstrip().rstrip()
                else:
                    self.tag_text_zh += "\n"+art.tag_text_zh.lstrip().rstrip()
                if not self.tag_text_en:
                    self.tag_text_en = art.tag_text_en.lstrip().rstrip()
                else:
                    self.tag_text_en += "\n"+art.tag_text_en.lstrip().rstrip()
                self.zh_para_count += art.zh_para_count 
                self.en_para_count += art.en_para_count
                self.zh_sent_count += art.zh_sent_count
                self.zh_seg_count += art.zh_seg_count
                self.en_sent_count += art.en_sent_count
                self.en_seg_count += art.en_seg_count
        if self.themes:
            for theme in self.themes:               
                if not self.raw_text_zh:
                    self.raw_text_zh = theme.raw_text_zh
                else:
                    self.raw_text_zh += "\n"+theme.raw_text_zh
                if not self.raw_text_en:
                    self.raw_text_en = theme.raw_text_en
                else:
                    self.raw_text_en += "\n"+theme.raw_text_en
                if not self.tag_text_zh:
                    self.tag_text_zh = theme.tag_text_zh
                else:
                    self.tag_text_zh += "\n"+theme.tag_text_zh
                if not self.tag_text_en:
                    self.tag_text_en = theme.tag_text_en
                else:
                    self.tag_text_en += "\n"+theme.tag_text_en
                self.zh_para_count += theme.zh_para_count 
                self.en_para_count += theme.en_para_count
                self.zh_sent_count += theme.zh_sent_count
                self.zh_seg_count += theme.zh_seg_count
                self.en_sent_count += theme.en_sent_count
                self.en_seg_count += theme.en_seg_count
        if self.annex:           
            if not self.raw_text_zh:
                self.raw_text_zh = self.annex.raw_text_zh
            else:
                self.raw_text_zh += "\n" + self.annex.raw_text_zh
            if not self.raw_text_en:
                self.raw_text_en = self.annex.raw_text_en
            else:
                self.raw_text_en += "\n" + self.annex.raw_text_en
            if not self.tag_text_zh:
                self.tag_text_zh = self.annex.tag_text_zh
            else:
                self.tag_text_zh += "\n" + self.annex.tag_text_zh
            if not self.tag_text_en:
                self.tag_text_en = self.annex.tag_text_en
            else:
                self.tag_text_en += "\n" + self.annex.tag_text_en
            self.zh_para_count += self.annex.zh_para_count 
            self.en_para_count += self.annex.en_para_count
            self.zh_sent_count += self.annex.zh_sent_count
            self.zh_seg_count += self.annex.zh_seg_count
            self.en_sent_count += self.annex.en_sent_count
            self.en_seg_count += self.annex.en_seg_count
        #---------------------------------------------     
        self.raw_text_zh = self.clear_untr_marker(self.raw_text_zh, mark="r-z")
        self.raw_text_en = self.clear_untr_marker(self.raw_text_en, mark="r-e")
        self.tag_text_zh = self.clear_untr_marker(self.tag_text_zh, mark="t-z")
        self.tag_text_en = self.clear_untr_marker(self.tag_text_en, mark="t-e")
        actual_para_num_zh =len(self.raw_text_zh.split('\n'))
        actual_para_num_en =len(self.raw_text_en.split('\n'))
        tt = self.raw_text_zh.split('\n')[0]
        if actual_para_num_zh != self.zh_para_count:
            msg = f"warning: stat error found in {self.title_zh} {self.volume_zh}: {tt} zh para count error: calculated:{self.zh_para_count}; actual: {actual_para_num_zh}"
            self.warnings.append(msg)
            self.zh_para_count = actual_para_num_zh
        if actual_para_num_en != self.en_para_count:
            msg = f"warning: stat error found in {self.title_zh} {self.volume_zh}: {tt} en para count error: calculated:{self.en_para_count}; actual: {actual_para_num_en}"
            self.warnings.append(msg)
            self.en_para_count = actual_para_num_en        
        #---------------------------------------------
        self.bi_para_ratio = self.get_ratio(self.zh_para_count,self.en_para_count)
        self.bi_sent_ratio = self.get_ratio(self.zh_sent_count,self.en_sent_count)
        self.bi_seg_ratio = self.get_ratio(self.zh_seg_count,self.en_seg_count)
    
    #--------------------------------------------------   
    def generate_corpus(self, my_dict):
        self.get_info(my_dict)
        self.get_contents(my_dict)
        self.get_theme(my_dict)
        self.get_annex(my_dict)
        
   #-----------------------------------------------------
    def get_word_tag_list(self):
        self.zh_byte_count, self.en_byte_count = self.dat.count_bytes(self.raw_text_zh, self.raw_text_en)
        self.zh_token_tag_list, self.zh_word_tag_list, self.zh_word_token_count, \
                                self.zh_word_type_count, self.zh_word_ttr, \
                                self.zh_word_sttr \
                                = self.dat.generate_word_tag_list(self.tag_text_zh, "zh") 
        self.en_token_tag_list, self.en_word_tag_list, self.en_word_token_count = self.dat.generate_word_tag_list(self.tag_text_en, "en")

    def get_freq_dict(self):
        self.zh_token_tag_freq, self.zh_word_tag_freq, self.zh_token_output_dict, self.zh_word_output_dict \
                                = self.dat.count_freq(self.zh_token_tag_list, self.zh_word_tag_list,"zh")
        self.en_token_tag_freq, self.en_word_tag_freq, self.en_word_tag_freq_list = self.dat.count_freq(self.en_token_tag_list, self.en_word_tag_list, "en")

    def get_output_dict(self):
        self.zh_token_output_dict = self.dat.initial_zlist_generator(self.zh_token_tag_freq, self.title_zh)
        #print("zh_token_output_dict done!")
        self.zh_word_output_dict = self.dat.initial_zlist_generator(self.zh_word_tag_freq, self.title_zh)
        #print("zh_word_output_dict done!")
        self.en_token_output_dict = self.dat.initial_elist_generator(self.en_token_tag_freq, self.title_zh)
        #print("en_token_output_dict done!")
        self.en_word_output_dict = self.dat.initial_elist_generator(self.en_word_tag_freq, self.title_zh)
        #print("en_word_output_dict done!")
  
    def get_en_sttr(self):
        self.en_word_type_count, self.en_word_ttr, self.en_word_sttr = self.dat.count_en_sttr(self.en_word_token_count, self.en_word_output_dict, self.en_word_tag_freq_list)
        self.warnings.extend(self.dat.warning)

    def stat_pipeline(self, obj):
        obj.zh_byte_count, obj.en_byte_count = obj.dat.count_bytes(obj.raw_text_zh, obj.raw_text_en)
        obj.zh_token_tag_list, obj.zh_word_tag_list, obj.zh_word_token_count, \
                                obj.zh_word_type_count, obj.zh_word_ttr, \
                                obj.zh_word_sttr \
                                = obj.dat.generate_word_tag_list(obj.tag_text_zh, "zh") 
        obj.en_token_tag_list, obj.en_word_tag_list, obj.en_word_token_count = obj.dat.generate_word_tag_list(obj.tag_text_en, "en")
        obj.zh_token_tag_freq, obj.zh_word_tag_freq, obj.zh_token_output_dict, obj.zh_word_output_dict \
                                = obj.dat.count_freq(obj.zh_token_tag_list, obj.zh_word_tag_list, "zh")
        obj.en_token_tag_freq, obj.en_word_tag_freq, obj.en_word_tag_freq_list = obj.dat.count_freq(obj.en_token_tag_list, obj.en_word_tag_list, "en")
        obj.zh_token_output_dict = obj.dat.initial_zlist_generator(obj.zh_token_tag_freq, obj.title_zh)
        obj.zh_word_output_dict = obj.dat.initial_zlist_generator(obj.zh_word_tag_freq, obj.title_zh)
        obj.en_token_output_dict = obj.dat.initial_elist_generator(obj.en_token_tag_freq, obj.title_zh)
        obj.en_word_output_dict = obj.dat.initial_elist_generator(obj.en_word_tag_freq, obj.title_zh)
        obj.en_word_type_count, obj.en_word_ttr, obj.en_word_sttr = obj.dat.count_en_sttr(obj.en_word_token_count, obj.en_word_output_dict, obj.en_word_tag_freq_list)
        obj.warnings.extend(obj.dat.warning)    
