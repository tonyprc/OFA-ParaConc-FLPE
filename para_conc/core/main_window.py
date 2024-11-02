#!/usr/bin/python3
# -*- coding: utf-8 -*-
# core program
# Copyright (c) 2024 Tony Chang (42716403@qq.com)

import os, re, copy, time, pickle

from para_conc.core.para_conc import ParaConc
from para_conc.core.search.search import SearchRequest, SearchMode
from para_conc.core.search.searchResultConverter import SearchResultConverter, VocFreqResultConverter
from para_conc.core.search.thread_searcher import SrcThread
from para_conc.core.pos_dict import POS_DICT
from para_conc.ui.ui_main_window import UIMainWindow
from para_conc.ui.ui_sub_window import SubWindow, VocWindow, SetVocWindow, TermWindow
from para_conc.ui.ui_word_cloud_window import WordCloudWindow, WordCloudShowWindow
from para_conc.ui.ui_culture_window import CulWindow, CulDictWindow
from para_conc.ui.ui_quiz_window import QuizWindow
from para_conc.ui.ui_textbook_window import TextbookWindow
from collections import Counter
from para_conc.core.pos_thread import TagThread
from para_conc.core.thread_dat_saver import DatSaverThread
from para_conc.core.thread_clouder import CloudThread

class MainWindow:
    def __init__(self):
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self.imgDir = os.path.join(dataDir, "images")
        self._outPutDir = os.path.join(currentDir, "saved_files")
        self._stoplist_zh_file = os.path.join(workFileDir, "stopword_zh.txt")
        self._stoplist_en_file = os.path.join(workFileDir, "stopword_en.txt")
        self._bi_term_file = os.path.join(workFileDir, "bi_term_dict.txt")
        self._error_code_file = os.path.join(workFileDir, "error_code.txt")
        self._help_file = os.path.join(workFileDir, "help.dat")
        self._starter_page_img = os.path.join(self.imgDir, 'frontPageDefault.png')
        self._nya_img = os.path.join(self.imgDir, 'frontPageNya.png')
        self._saa_img = os.path.join(self.imgDir, 'frontPageSaa.png')
        self._sha_img = os.path.join(self.imgDir, 'frontPageSha.png')
        self._rwg_img = os.path.join(self.imgDir, 'frontPageRwg.png')
        self._cwp_img = os.path.join(self.imgDir, 'frontPageCwp.png')
        self._goc_img = os.path.join(self.imgDir, 'frontPageGoc.png')
        self._edu_img = os.path.join(self.imgDir, 'frontPageEdu.png')
        self._hrr_img = os.path.join(self.imgDir, 'frontPageHrr.png')
        self._current_cover = 0        

        self._stopchar_en_list = "\,\.\:\"\'\*\^\# \$\@\!~\(\)\_\-\+\=\{\}\[\]\?\/\<\>\&\%\;\\"
        self._stopchar_zh_list = "，。：、；“”’！…—（）《》｛｝【】？"
        #self._regex_char_regex=r"\*|\^|\# |\$|\@|\!|\(|\)|\-|\+|\=|\{|\}|\[|\]|\?|\<|\>|\\|\|"
        self._regex_char_regex=r"\*|\^|\#|\$|\@|\!|\(|\)|\+|\=|\{|\}|\[|\]|\?|\<|\>|\\|\|"
        self._corpus_selected_list = []
        self.current_corpora_selected = []
        self._help_data = {}

        self.quiz_current_id = ""
        self.quiz_current_result = ""
        
        self._ui = UIMainWindow()
        self._ui.save_text.connect(self.saveTxt)
        self._ui.save_html.connect(self.saveHtml)
        self._ui.search.connect(self.startConc)
        self._ui.set_freq.connect(self.setFreq)
        self._ui.freqcount_output.connect(self.setFreq) 
        self._ui.code_output.connect(self.print_code)  
        self._ui.regex_output.connect(self.print_reg)  
        self._ui.cplist_output.connect(self.print_cplist) 
        self._ui.selecting_item.connect(self.select_item)
        self._ui.quote_display.connect(self.quote_display)
        self._ui.quiz_display.connect(self.quiz_display)
        self._ui.qdict_update.connect(self.update_quote_dict)
        self._ui.textbook_window_display.connect(self.display_textbook_window)
        self._ui.update_current_corpus.connect(self.send_corpus_id)

        self._ui.print_result.connect(self.print_result)        
        self._ui.view_chapter.connect(self.view_chapter)
        self._ui.pynlpir_output.connect(self.print_pynlpir)
        self._ui.penn_output.connect(self.print_penn)
        self._ui.wordcloud_output.connect(self.print_wordcloud)
        self._ui.stop_zh_dict_update.connect(self.stop_zh_dict_update)
        self._ui.stop_en_dict_update.connect(self.stop_en_dict_update)
        self._ui.bi_term_dict_update.connect(self.bi_term_dict_update)        
        self._ui.load_tag_corpus.connect(self.tag_data_preload) 
        self.current_corpus = self._ui._current_corpus
        self.current_selected_corpora = ""
        self.current_wordcloud = ""
        self.current_wordcloud_options = {}

        self.tb_window = TextbookWindow()        

        self._paraConc = ParaConc()            
        self.corpora = self._paraConc.corpora  
        self.bi_dict = self._paraConc.bi_dict  
        self.data_preload()                   
        self._ui._pg_bar.setValue(0)          
        self.resetWindow()                   
        
        self._stop_words_zh = self._paraConc._stps_zh   
        self._stop_words_en = self._paraConc._stps_en   
        
        self.current_cloud_carrier = ""     

        self._html_converter = SearchResultConverter()
        self._converter = VocFreqResultConverter()
        self.voc_opt_window = SetVocWindow()
        self.voc_opt_window.clear_current_results.connect(self.reset_outcomes)
        self.voc_opt_window.freq_print_request.connect(self.printing_freq)
        self._search_result = None
        self._show_context = False
        self._show_source = False
        self.sl = 'zh'
        self.tl = 'en'
        self.src_lang = ''
        self.conc_errors = []
        
        self._page_i=0
        self._custom_set=100
        self._list_num=[]
        self._list_lang=[]
        self._list_cont=[]

        self.wc_win = WordCloudWindow() 
        self.wc_win.error_input_warning.connect(self.maintain_message)
        self.wc_win.filter_dict_output.connect(self.wordcloud_processor)  
        self.wc_win.picture_show_request.connect(self.wordcloud_processor)
        
        self.wc_show_win = WordCloudShowWindow()
        self.wc_show_win.picture_save_request.connect(self.wordcloud_save)

        self.quote_win = CulWindow() 
        self.quote_win.update_pbar.connect(self.update_pbar)
        self.qdict_win = CulDictWindow()

        self.quiz_win = QuizWindow() 
        
        self.zh_stop_win = TermWindow(self._stoplist_zh_file)
        self.zh_stop_win.set_title("中文停用词表")
        self.zh_stop_win.set_icon('./app_data/images/text.png')
        self.zh_stop_win.term_saving.connect(self._ui.set_status_text)
        self.en_stop_win = TermWindow(self._stoplist_en_file)
        self.en_stop_win.set_title("英文停用词表")
        self.en_stop_win.set_icon('./app_data/images/text.png')
        self.en_stop_win.term_saving.connect(self._ui.set_status_text)
        self.bi_term_win = TermWindow(self._bi_term_file)
        self.bi_term_win.set_title("双语术语词表")
        self.bi_term_win.set_icon('./app_data/images/text.png')
        self.bi_term_win.term_saving.connect(self._ui.set_status_text)
        
        self._ui.show()      
        
        if self._paraConc._warning:
            leak_list = self._paraConc._warning['list']
            leak_type = self._paraConc._warning['type']
            r =self._ui._quest(len(leak_list),leak_type)
            if r == "Y":
                self.dat_thread = DatSaverThread(leak_list)
                self.dat_thread.finished.connect(self.dat_thread.deleteLater)
                self.dat_thread.pbar_signal.connect(self.update_pbar)
                self.dat_thread.msg_m_signal.connect(self.maintain_message)
                self.dat_thread.output_window_signal.connect(self.show_window)
                self.dat_thread.refresh_signal.connect(self.data_refresh)
                self.dat_thread.start()
                
    def display_textbook_window(self):
        self.tb_window.show()
          
    def send_corpus_id(self, m):
        self.quote_win._corp_title_box.setText(m)
        self.quote_win._quote_window.clear()
        self.quote_win._current_corpus = self.current_corpus
        self.quiz_win._corp_title_box.setText(m)
        self.quiz_win._current_corpus = self.current_corpus
        self.quiz_win._quiz_window.clear()
        
    # for debugging only    
    def check_freq_opts(self, i):
        print(i)

    def printing_freq(self, opts):
        print_scope = opts['scope']
        zh_wdict = []
        en_wdict = []
        if print_scope == 0:
            if self.current_corpus:
                main_corpus = self.current_corpus[0]
                current_corpus = self.current_corpus[1]
                if current_corpus:
                    zh_wdict = [current_corpus.zh_token_output_dict]
                    en_wdict = [current_corpus.en_token_output_dict]
                else:
                    zh_wdict = [main_corpus.zh_token_output_dict]
                    en_wdict = [main_corpus.en_token_output_dict]
        if print_scope == 1:
            if self._corpus_selected_list:
                corpora_selected = (self.corpora,self.check_selected_corpora())
            else:
                corpora_selected = []
            if not corpora_selected:
                pass              
            else:
                new_corpora = corpora_selected[0]
                index_list = corpora_selected[1]
                for family in index_list:
                    if len(family.keys())== 1:
                        corp_root = family['0']
                        for corp in new_corpora:
                            if corp_root in corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                zh_wdict.append(corpus.zh_token_output_dict)
                                en_wdict.append(corpus.en_token_output_dict)
                    if len(family.keys())== 2:
                        corp_root = family['0']
                        corp_child = family['1']
                        if corp_root not in ["UXEP"]:
                            for corp in new_corpora:
                                if corp_child == corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    zh_wdict.append(corpus.zh_token_output_dict)
                                    en_wdict.append(corpus.en_token_output_dict)
                        else:
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_child == "概况":
                                        art = corpus.info
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                    if corp_child == "目录":
                                        art = corpus.contents
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                    if corp_child == "导言":
                                        art = corpus.preface
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                    if corp_child == "章节":
                                        art = corpus.chapters
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                    if corp_child == "附录":
                                        art = corpus.annex
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)                                           
                    if len(family.keys())== 3:
                        corp_root = family['0'] 
                        corp_pa = family['1']  
                        corp_id = family['2']   
                        if corp_root == "UXEP":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    art_num = corp_id.split("-")[0]
                                    if corp_pa == "章节":
                                        for art in corpus.chapters.articles:
                                            if art.num == art_num:
                                                zh_wdict.append(art.zh_token_output_dict)
                                                en_wdict.append(art.en_token_output_dict) 
                                                break
                                    if corp_pa == "附录":
                                        for art in corpus.annex.articles:
                                            if art.num == art_num:
                                                zh_wdict.append(art.zh_token_output_dict)
                                                en_wdict.append(art.en_token_output_dict) 
                                                break
                                    break
                        if corp_root == "GOC":
                            for corp in new_corpora:
                                if corp_pa == corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_id == "概况":
                                        art = corpus.info
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict) 
                                    if corp_id == "目录":
                                        art = corpus.contents
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                    if corp_id == "主题":
                                        for theme in corpus.themes:
                                            zh_wdict.append(theme.zh_token_output_dict)
                                            en_wdict.append(theme.en_token_output_dict)
                                    if corp_id == "附录":
                                        art = corpus.annex
                                        zh_wdict.append(art.zh_token_output_dict)
                                        en_wdict.append(art.en_token_output_dict)
                                break
                    if len(family.keys())== 4:
                        corp_root = family['0']     
                        corp_gpa = family['1']   
                        corp_pa = family['2']       
                        corp_id = family['3']     
                        corp_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_gpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_pa == "主题":
                                    for theme in corpus.themes:
                                        if corp_num == theme.num:
                                            zh_wdict.append(theme.zh_token_output_dict)
                                            en_wdict.append(theme.en_token_output_dict)
                                            break
                                if corp_pa == "附录":
                                    for art in corpus.annex.articles:
                                        if art.num == corp_num:
                                            zh_wdict.append(art.zh_token_output_dict)
                                            en_wdict.append(art.en_token_output_dict)
                                            break
                            break
                    if len(family.keys())== 5:
                        corp_root = family['0'] 
                        corp_ggpa = family['1']      
                        corp_gpa = family['2']  
                        corp_pa = family['3']  
                        corp_id = family['4']    
                        theme_num = corp_pa.split("-")[0]
                        art_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_ggpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_gpa == "主题":
                                    for theme in corpus.themes:
                                        if theme_num == theme.num:
                                            for art in theme.articles:
                                                if art_num  == art.num:
                                                    zh_wdict.append(art.zh_token_output_dict)
                                                    en_wdict.append(art.en_token_output_dict)
                                                    break
                                            break
                                    break
                            break                       
        if print_scope == 2:
            if self.corpora:
                for corp in self.corpora:
                    corpus = self.open_dat_file(corp[0])
                    zh_wdict.append(corpus.zh_token_output_dict)
                    en_wdict.append(corpus.en_token_output_dict)                               
        if zh_wdict and en_wdict:
            if opts['lang']== 0:
                self.tag_voc_preload(opts, self._stop_words_zh, self._stop_words_en, zh_wdict, en_wdict, 'zh')
            if opts['lang']== 1:
                self.tag_voc_preload(opts, self._stop_words_zh, self._stop_words_en, zh_wdict, en_wdict, 'en')
        else:
            start_sign = "off"
            self._ui._statusBar.showMessage(f"指定语料不存在，请先加载语料！") 
        
    def open_dat_file(self, dat_file):
        dat_read = ''
        with open(dat_file, 'rb') as f:
            dat_read = pickle.load(f)
        return dat_read
        
    def stop_zh_dict_update(self):
        self.zh_stop_win.show()
        
    def stop_en_dict_update(self):
        self.en_stop_win.show()

    def bi_term_dict_update(self):
        self.bi_term_win.show()

    def quote_display(self):
        self.quote_win.show()
        self.qdict_win.close()

    def quiz_display(self):
        self.quiz_win.show()
        
    def update_quote_dict(self):
        self.qdict_win.show()
        self.quote_win.close()
        
    def update_cloud_carrier(self, m):
        self.current_cloud_carrier = m.get('word_cloud')
        try:
            cloud_image = self.current_cloud_carrier.to_image()
            self.wc_show_win.update_canvas(cloud_image)
            self.wc_show_win.show()
            self._ui._statusBar.showMessage(f"词云图片展示成功！")
        except:
            self._ui._statusBar.showMessage(f"词云图提取失败！请重试")
                   
    def check_selected_corpora(self):
        tree_selected_list = []
        for item in self._ui._corpusWindow.selectedItems():
            family = self._ui.find_parents(item)
            if family not in tree_selected_list:
                tree_selected_list.append(family) 
        return tree_selected_list           
                    
    def wordcloud_processor(self, info):
        if isinstance(info, dict):            
            self.current_wordcloud_options = info 
            self._ui._statusBar.showMessage(f"开始生成词云，请稍候！")
            opt_dict = info
            opt_scope = opt_dict['scope']
            zh_word_dict = {}
            en_word_dict = {}
            start_sign = "on"
            if opt_scope == "current":
                if self.current_corpus:
                    if self.current_corpus[1]:
                        zh_word_dict = self.current_corpus[1].zh_word_output_dict
                        en_word_dict = self.current_corpus[1].en_word_output_dict
                    else:
                        zh_word_dict = self.current_corpus[0].zh_word_output_dict
                        en_word_dict = self.current_corpus[0].en_word_output_dict
                else:
                    start_sign = "off"
                    self._ui._statusBar.showMessage(f"当前语料为空，请先加载当前语料！")    
            if opt_scope == "selected":
                if not self._corpus_selected_list:
                    corpora_selected = []
                else:
                    corpora_selected = (self.corpora,self.check_selected_corpora())                
                if corpora_selected:
                    new_corpora = corpora_selected[0]
                    index_list = corpora_selected[1]
                    for family in index_list:
                        if len(family.keys())== 1:
                            corp_root = family['0']
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    zh_word_dict.update(corpus.zh_word_output_dict)
                                    en_word_dict.update(corpus.en_word_output_dict)
                        if len(family.keys())== 2:
                            corp_root = family['0']
                            corp_child = family['1']
                            if corp_root not in ["UXEP"]:
                                for corp in new_corpora:
                                    if corp_child == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        zh_word_dict.update(corpus.zh_word_output_dict)
                                        en_word_dict.update(corpus.en_word_output_dict)
                            else:
                                for corp in new_corpora:
                                    if corp_root in corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        if corp_child == "概况":
                                            art = corpus.info
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_child == "目录":
                                            art = corpus.contents
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_child == "导言":
                                            art = corpus.preface
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_child == "章节":
                                            art = corpus.chapters
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_child == "附录":
                                            art = corpus.annex
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)                                            
                        if len(family.keys())== 3:
                            corp_root = family['0']
                            corp_pa = family['1']   
                            corp_id = family['2']  
                            if corp_root == "UXEP":
                                for corp in new_corpora:
                                    if corp_root in corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        art_num = corp_id.split("-")[0]
                                        if corp_pa == "章节":
                                            for art in corpus.chapters.articles:
                                                if art.num == art_num:
                                                    zh_word_dict.update(art.zh_word_output_dict)
                                                    en_word_dict.update(art.en_word_output_dict)
                                                    break
                                        if corp_pa == "附录":
                                            for art in corpus.annex.articles:
                                                if art.num == art_num:
                                                    zh_word_dict.update(art.zh_word_output_dict)
                                                    en_word_dict.update(art.en_word_output_dict)
                                                    break
                                    break
                            if corp_root == "GOC":
                                for corp in new_corpora:
                                    if corp_pa == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        if corp_id == "概况":
                                            art = corpus.info
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_id == "目录":
                                            art = corpus.contents
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                        if corp_id == "主题":
                                            for theme in corpus.themes:
                                                zh_word_dict.update(theme.zh_word_output_dict)
                                                en_word_dict.update(theme.en_word_output_dict)
                                        if corp_id == "附录":
                                            art = corpus.annex
                                            zh_word_dict.update(art.zh_word_output_dict)
                                            en_word_dict.update(art.en_word_output_dict)
                                    break
                        if len(family.keys())== 4:
                            corp_root = family['0']   
                            corp_gpa = family['1'] 
                            corp_pa = family['2']      
                            corp_id = family['3']      
                            corp_num = corp_id.split("-")[0]
                            for corp in new_corpora:
                                if corp_gpa == corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_pa == "主题":
                                        for theme in corpus.themes:
                                            if corp_num == theme.num:
                                                zh_word_dict.update(theme.zh_word_output_dict)
                                                en_word_dict.update(theme.en_word_output_dict)
                                                break
                                    if corp_pa == "附录":
                                        for art in corpus.annex.articles:
                                            if art.num == corp_num:
                                                zh_word_dict.update(art.zh_word_output_dict)
                                                en_word_dict.update(art.en_word_output_dict)
                                                break
                                break
                        if len(family.keys())== 5:
                            corp_root = family['0']  
                            corp_ggpa = family['1']         
                            corp_gpa = family['2']  
                            corp_pa = family['3']    
                            corp_id = family['4']    
                            theme_num = corp_pa.split("-")[0]
                            art_num = corp_id.split("-")[0]
                            for corp in new_corpora:
                                if corp_ggpa == corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_gpa == "主题":
                                        for theme in corpus.themes:
                                            if theme_num == theme.num:
                                                for art in theme.articles:
                                                    if art_num  == art.num:
                                                        zh_word_dict.update(art.zh_word_output_dict)
                                                        en_word_dict.update(art.en_word_output_dict)
                                                        break
                                            break
                                break                                    
                else:
                    start_sign = "off"
                    self._ui._statusBar.showMessage(f"未选择任何语料，请先从语料列表中选择语料！")
            if opt_scope == "all":
                if self.corpora:
                    for corp in self.corpora:
                        corpus = self.open_dat_file(corp[0])
                        zh_word_dict.update(corpus.zh_word_output_dict)
                        en_word_dict.update(corpus.en_word_output_dict)
                else:
                    start_sign = "off"
                    self._ui._statusBar.showMessage(f"不存在任何语料，请先加载语料！")

            if start_sign == "on":
                self.clouder = CloudThread(opt_dict, self._stop_words_zh, self._stop_words_en, zh_word_dict, en_word_dict)
                self.clouder.finished.connect(self.clouder.deleteLater)
                self.clouder.pbar_signal.connect(self.update_pbar)
                self.clouder.msg_m_signal.connect(self.maintain_message)
                self.clouder.obj_signal.connect(self.update_cloud_carrier) # 以dict形式传出PIL object
                self.clouder.start()
                
    def wordcloud_save(self, info):
        if info == "save":
            scope = self.current_wordcloud_options['scope']
            if scope == "current":
                if self.current_corpus:
                    main_corpus = self.current_corpus[0]
                    current_corpus = self.current_corpus[1]
                    if self.current_cloud_carrier:
                        try:
                            if current_corpus:
                                tempt_id = "_".join(["WordCloud",main_corpus.id.upper(), current_corpus.title_en.title().replace(" ",""), \
                                                     self.current_wordcloud_options['lang'].upper(), \
                                                     self.current_wordcloud_options['mask']])
                                tempt_id += ".png"
                            else:
                                tempt_id = "_".join(["WordCloud",main_corpus.id.upper(),\
                                                     self.current_wordcloud_options['lang'].upper(), \
                                                     self.current_wordcloud_options['mask']])
                                tempt_id += ".png"
                        except:
                            tempt_id = "WordCloud.png"
                        save_id = os.path.join(self._outPutDir, tempt_id)
                        self.current_cloud_carrier.to_file(save_id)
                        self._ui._statusBar.showMessage(f"词云图片已成功保存到本地！")
                    else:
                        self._ui._statusBar.showMessage(f"请在生成词云之后，再保存词云图片！")
                else:
                    self._ui._statusBar.showMessage(f"当前语料为空，请先加载当前语料！")
            if scope == "selected":
                if self.current_cloud_carrier:
                    tempt_id = "_".join(["WordCloud_Selected_Corpera", \
                                         self.current_wordcloud_options['lang'].upper(), \
                                         self.current_wordcloud_options['mask']])
                    tempt_id += ".png"
                    save_id = os.path.join(self._outPutDir, tempt_id)
                    self.current_cloud_carrier.to_file(save_id)
                    self._ui._statusBar.showMessage(f"词云图片已成功保存到本地！")
                else:
                    self._ui._statusBar.showMessage(f"请在生成词云之后，再保存词云图片！")
            if scope == "all":
                if self.current_cloud_carrier:
                    tempt_id = "_".join(["WordCloud_All_Corpura", \
                                         self.current_wordcloud_options['lang'].upper(), \
                                         self.current_wordcloud_options['mask']])
                    tempt_id += ".png"
                    save_id = os.path.join(self._outPutDir, tempt_id)
                    self.current_cloud_carrier.to_file(save_id)
                    self._ui._statusBar.showMessage(f"词云图片已成功保存到本地！")
                else:
                    self._ui._statusBar.showMessage(f"请在生成词云之后，再保存词云图片！")                
             
    def print_wordcloud(self):
        self.current_wordcloud = ""
        self.wc_win.show()
 
    def reset_cover_image(self, m):
        if m == "new year address" and not self._current_cover == 1:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageNya.png);}")
            self._current_cover = 1
        elif m == "speech at home and abroad" and not self._current_cover == 2:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageSha.png);}")
            self._current_cover = 2
        elif m == "signed article abroad" and not self._current_cover == 3:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageSaa.png);}")
            self._current_cover = 3
        elif m == "report" and not self._current_cover == 4:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageRwg.png);}")
            self._current_cover == 4
        elif m in ["white paper", "report on us", "single report"] and not self._current_cover == 5:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageCwp.png);}")
            self._current_cover == 5
        elif m == "governance of china" and not self._current_cover == 6:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageGoc.png);}")
            self._current_cover == 6
        elif m == "educational philosophy" and not self._current_cover == 7:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageEdu.png);}")
            self._current_cover == 7
        elif m == "hr record" and not self._current_cover == 8:
            self._ui._result_window.clear()
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageHrr.png);}")
            self._current_cover == 8
        else:
            if self._current_cover == 0:
                self._ui._result_window.clear()
                self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageDefault.png);}")
            else: pass
            
    def output_arranger(self, affix):
        if affix == "txt":            
            rst_list = []
            for (i, lg, st) in zip(self._list_num, self._list_lang, self._list_cont):
                st = re.sub(r"<font.*?>","【", st)
                st = re.sub(r"</font>","】", st)
                st = re.sub(r"<br>"," ", st)
                st = re.sub(r"</*b>","", st)
                item = str(i) + "\t"+lg+ "\t"+ st
                rst_list.append(item)
            rst = ""
            if rst_list:                
                rst = "\n".join(rst_list)
        elif affix == "html":
            result_pd = self._html_converter.lst2pd(self._list_num, self._list_lang, self._list_cont)
            rst =  self._html_converter.pd2html(result_pd)
        else:
            rst = ""
        return rst

    def resetWindow(self):
        self._ui._result_window.clear()
        if self.current_corpus:            
            self.reset_cover_image(self.current_corpus[0].genre_en)
        else:
            self._current_cover == 0
            self._ui._result_window.setStyleSheet("QTextBrowser{border-image: url(./app_data/images/frontPageDefault.png);}")
                        
    def reset_outcomes(self):
        self.voc_opt_window.close()
        
    def data_refresh(self, m):
        self.corpora.extend(m)
        self._paraConc.corpora = self.corpora
        self._paraConc._warning.clear()
        corpus_list = []
        for corpus in self.corpora:
            corpus_list.append(corpus[1])
        self._ui.reload_corpora_list(corpus_list, self.corpora)
        self._ui._statusBar.showMessage(f"语料列表已更新，请开始使用！")

    def data_preload(self):
        corpus_list = []
        for corpus in self.corpora:
            corpus_list.append(corpus[1])
        self._ui.set_corpora_list(corpus_list, self.corpora)
        self._help_data = self.open_dat_file(self._help_file)
        
    def tag_voc_preload(self, opt, zh_stoplist, en_l_stoplist, zh_wlist, en_wlist, lang = "zh"):       
        if zh_wlist or en_wlist:
            self.my_thread = TagThread(opt, zh_stoplist, en_l_stoplist, zh_wlist, en_wlist, lang)
            self.my_thread.finished.connect(self.my_thread.deleteLater)
            self.my_thread.pbar_signal.connect(self.update_pbar)
            self.my_thread.msg_m_signal.connect(self.maintain_message)
            self.my_thread.output_window_signal.connect(self.show_window)
            self.my_thread.start()
        else:
            self._ui._statusBar.showMessage(f"指定语料不存在，请先加载相关语料！")
        
    def tag_data_preload(self): 
        self.current_corpus = self._ui._current_corpus

    def select_item(self):
        self._corpus_selected_list.clear()
        for item in self._ui._corpusWindow.selectedItems():
            if item.text(0) not in self._corpus_selected_list:
                self._corpus_selected_list.append(item.text(0))             
            
    def selected_corpora(self, scope):
        corpora_selected = []
        msg = ""
        if scope.value == 1:
            if self.corpora:
                corpora_selected = self.corpora
            else:
                msg = "抱歉，语料库不能为空，请先加载语料再试！"
        elif scope.value == 2:
            if self._corpus_selected_list:
                corpora_selected = (self.corpora,self.check_selected_corpora())                
            else:
                msg = "请先选择要检索的语料"
        elif scope.value == 3:
            if self.current_corpus:
                corpora_selected = self.current_corpus
            else:
                msg = "抱歉，当前语料为空，请先双击要检索的语料库名称，然后再试！"
        elif scope.value == 4:
            if self.current_corpus:
                for corp in self.corpora:
                    corpus = self.open_dat_file(corp[0])
                    if corpus.genre_en == self.current_corpus[0].genre_en:
                        corpora_selected.append(corp)
            else:
                msg = "抱歉，请先双击打开某个语料文件！"                
        else:
            msg = "抱歉，语料选择出现未知错误，请联系软件维护人员！"
        return msg, corpora_selected
            
    def maintain_message(self, msg):
        self._ui._statusBar.showMessage(msg)

    def update_pbar(self, i,j):
        self._ui._pg_bar.setVisible(True)
        if j:
            self._ui._pg_bar.setFormat("%v/%m")
            self._ui._pg_bar.setRange(0, j)
            if i != -1:
                self._ui._pg_bar.setValue(i) 
                time.sleep(0.1)
            else: 
                self._ui._pg_bar.setValue(0)
        else:
            self._ui._pg_bar.setFormat("%v%")
            k = int(i/j*100)
            self._ui._pg_bar.setRange(0,100)
            if i != -1:
                self._ui._pg_bar.setValue(k)
                time.sleep(0.1)
            else:
                self._ui._pg_bar.setValue(0)
                
    def view_text(self, r_text, title, j):
        if j == 0:
            show_title = "《"+ title +"》"+ "原文全文"
        elif j == 1:
            show_title = "《"+ title +"》"+ "译文全文"
        elif j == 2:
            show_title = "《"+ title +"》"+ "双语段对齐全文"
        elif j == 3:
            show_title = "《"+ title +"》"+ "双语句对齐全文"
        else:
            show_title = ""
        if r_text:
            sub_window = SubWindow(self._ui)
            sub_window.set_title(show_title)
            sub_window.set_text(r_text)
            sub_window.show() 
            
    # canceled    
    def view_chapter(self, chapter_title, i):
        pass 

    def inputCheck(self):
        srcWord = self._ui.search_text()
        search_mode = self._ui.search_mode()
        if srcWord == "":
            self._ui.set_status_text("检索词不能为空，请重新输入！")
            inputWord = ""
        elif SearchMode.REGEX == search_mode:
            inputWord = srcWord
        else:
            m=re.search(self._regex_char_regex,srcWord)
            if m:
                self._ui.set_status_text("您输入了正则检索专用符号，如想进行正则检索，请点选相应选项")
                inputWord=""
            else:
                srcWord=srcWord.strip()                
                if srcWord[0] in self._stopchar_en_list:
                    byte_sample = [char for char in srcWord if char not in self._stopchar_en_list]
                    if not byte_sample:
                        self._ui.set_status_text("您输入了标点符号，如想进行正则检索，请点选相应选项")
                        inputWord = ""
                    else:
                        inutWord = SrcWord
                elif srcWord[0] in self._stopchar_zh_list:
                    byte_sample = [char for char in srcWord if char not in self._stopchar_zh_list]
                    if not byte_sample:
                        self._ui.set_status_text("检索词不能为中文标点符号，请输入有效检索词")
                        inputWord = ""
                    else:
                        inputWord = srcWord
                else:
                    inputWord = srcWord
        return inputWord

    def _build_search_request(self, note, source, context):
        input_word = self.inputCheck()
        if input_word == '':
            return None
        req = SearchRequest()
        req.q = input_word
        req.q_sl = []
        req.q_tl = []
        for key, v_list in self.bi_dict.items():
            lower_vs = [v.lower() for v in v_list]
            if req.q == key:
                req.q_tl.extend(v_list)            
            if req.q.lower() in lower_vs:
                req.q_sl.append(key)   
        req.dsp_nt = note
        req.dsp_sc = source
        req.dsp_ct = context
        req.mode = self._ui.search_mode()
        return req    
       
    # core program
    def startConc(self):
        display_option = self._ui.display_check()        
        if display_option[0] == 1:
            self._show_note = True
        else:
            self._show_note = False
        if display_option[1] == 1:
            self._show_source = True
        else:
            self._show_source = False
        if display_option[2] == 1:
            self._show_context = True
        else:
            self._show_context = False
        req = self._build_search_request(self._show_note, self._show_source, self._show_context)
        if req is None:
            return ""
        src_scope_option = self._ui.search_scope()        
        self.conc_errors.clear()
        error_msg, corpora_selected = self.selected_corpora(src_scope_option)
        if src_scope_option.value == 1:
            self.current_corpora_selected = corpora_selected
        if error_msg:
            self.conc_errors.append(error_msg)
            corpora = []
        else:
            corpora = corpora_selected
        if corpora:
            self.src_thread = SrcThread(corpora, req, src_scope_option)
            self.src_thread.finished.connect(self.src_thread.deleteLater)
            self.src_thread.pbar_signal.connect(self.update_pbar)
            self.src_thread.msg_m_signal.connect(self.maintain_message)
            self.src_thread.output_window_signal.connect(self.show_window)
            self.src_thread.refresh_signal.connect(self.data_refresh)    
            self.src_thread.result_signal.connect(self.get_conc_result)
            self.src_thread.start()
        else:
            self._ui.set_status_text(";".join(self.conc_errors))
    
    def get_conc_result(self, r_dict):
        self._page_i=0       
        self._search_result = r_dict['obj']
        if self._search_result.hit_words != 0:
            self.resetWindow()
            self._list_num = self._search_result.num_list
            self._list_lang = self._search_result.lang_list
            self._list_cont = self._search_result.sent_list
            startNum = self._page_i
            startSetNum = self._list_num[startNum]
            endSetNum = startSetNum + self._custom_set
            list_limit = max(self._list_num)
            if endSetNum <= list_limit:
                endNum = self._list_num.index(endSetNum)
                self._page_i = endNum
            else:
                endNum = -1
                self._page_i = 0
            if endNum == -1:
                result_pd = self._html_converter.lst2pd(self._list_num, self._list_lang, self._list_cont)
                html =  self._html_converter.pd2html(result_pd)
            else:
                result_pd = self._html_converter.lst2pd(self._list_num[startNum:endNum],\
                                                        self._list_lang[startNum:endNum],\
                                                        self._list_cont[startNum:endNum])
                html =  self._html_converter.pd2html(result_pd)
            self._ui.set_result_html(''.join(html))
            if self._page_i != 0:
                self._ui._next_page_button.setDisabled(False)
            else:
                self._ui._next_page_button.setDisabled(True)
            self._ui._words_hit_value.setText(str(self._search_result.hit_words)+"次")
            self._ui._pairs_hit_value.setText(str(self._search_result.hit_pairs)+"对")            
        else:
            self.resetWindow()
            self._ui._words_hit_value.setText('0')
            self._ui._pairs_hit_value.setText('0')

    def result_list_generator(self, final_dict, lang = "zh"):        
        if lang == "zh":
            result_list_zh = []
            nm_list_zh = []
            hw_list_zh = []
            hq_list_zh = []
            tq_list_zh =[]
            for i, (w,q) in enumerate(sorted(final_dict.keys(), key=lambda x:x[1],reverse =True),start=1):
                st_list = [w+ "/"+q + " ("+str(f)+")" for w, q, f in final_dict[(w,q)]]
                st = "; ".join(st_list)             
                nm_list_zh.append(str(i))
                hw_list_zh.append(w)
                hq_list_zh.append(q)
                tq_list_zh.append(st)
            return nm_list_zh, hw_list_zh, hq_list_zh, tq_list_zh
        else:
            result_list_en = []
            nm_list_en = []
            hw_list_en = []
            hq_list_en = []
            tq_list_en =[]
            for i, (w,q) in enumerate(sorted(final_dict.keys(), key=lambda x:x[1],reverse =True),start=1):
                st_list = [w+ "_"+q + " ("+str(f)+")" for w, q, f in final_dict[(w,q)]]
                st = "; ".join(st_list)
                nm_list_en.append(str(i))
                hw_list_en.append(w)
                hq_list_en.append(q)
                tq_list_en.append(st)
            return nm_list_en, hw_list_en, hq_list_en, tq_list_en
        
    def dict_filter(self, my_dict, word_list, freq):
        new_dict ={}
        for (w, q) in my_dict.keys():
            if w.title() not in word_list and w.lower() not in word_list and q >= freq:
                new_dict[(w,q)]= copy.deepcopy(my_dict[(w,q)])
        return new_dict                
    
    def preparing_output_results(self, choices, zl, el):
        T1 = time.perf_counter()
        voc_html_zh = ""
        voc_txt_zh = ""
        voc_html_en = ""
        voc_txt_en = ""
        results = []
        stop_zh = []
        stop_en = []
        if "z_stop" in choices['stop']:
            stop_zh = self._stop_words_zh
        if "e_stop" in choices['stop']:
            stop_en = self._stop_words_en
        zh_fq = choices['freq']["zh"]
        en_fq = choices['freq']["en"]
        zh_main_dict = {}
        en_main_dict = {}        
        for key in zl.keys():
            if key not in choices['off']:
                zh_main_dict.update(zl[key])        
        final_zh_dict = self.dict_filter(zh_main_dict, stop_zh, zh_fq)
        z_0, z_1, z_2, z_3 = self.result_list_generator(final_zh_dict, lang = "zh")
        for key in el.keys():
            if key not in choices['off']:
                en_main_dict.update(el[key])
        final_en_dict = self.dict_filter(en_main_dict, stop_en, en_fq)
        e_0, e_1, e_2, e_3 = self.result_list_generator(final_en_dict, lang = "en")
        result_pd_zh = self._converter.lst2pd(z_0, z_1, z_2, z_3)
        voc_html_zh = self._converter.pd2html(result_pd_zh)
        voc_txt_zh = "\n".join([str(a)+ "\t" +b + "\t" + str(c) + "\t" +d for (a,b,c,d) in zip(z_0, z_1, z_2, z_3)])
        result_pd_en = self._converter.lst2pd(e_0, e_1, e_2, e_3)
        voc_html_en = self._converter.pd2html(result_pd_en)
        voc_txt_en = "\n".join([str(a)+ "\t" +b + "\t" + str(c) + "\t" +d for (a,b,c,d) in zip(e_0, e_1, e_2, e_3)])
        if voc_html_zh:
              results = [voc_html_zh, voc_txt_zh, voc_html_en, voc_txt_en]
        else:
            pass        
        T2 = time.perf_counter()
        time_used = T2 - T1
        self._ui.set_status_text(f"词表输出准备就绪，用时{time_used:.2f}秒")
        return results

    def reset_output_files(self, rlts):
        self._voc_html_zh = rlts[0]
        self._voc_txt_zh = rlts[1]
        self._voc_html_en = rlts[2]
        self._voc_txt_en = rlts[3]
        
    def saveTxt(self):
        T1 = time.perf_counter()
        text_to_save = os.path.join(self._outPutDir, "current_concordance_result.txt")
        rst_text = self.output_arranger('txt')
        if rst_text:
            with open(text_to_save, 'wt', encoding="utf-8-sig") as f:
                f.write(rst_text)
            T2 = time.perf_counter()
            tm = T2 - T1
            msg = f'当前检索结果已输出为文本文件，用时{tm:.2f}秒！'                     
        else:
            msg = '抱歉，没有检索结果可供输出，请先检索！'        
        self._ui.set_status_text(msg)

    def saveHtml(self):
        T1 = time.perf_counter()
        html_to_save = os.path.join(self._outPutDir, "current_concordance_result.html")
        html = self.output_arranger('html')
        if html:
            with open(html_to_save, 'w', encoding="utf-8-sig") as f:
                f.write(html)
            T2 = time.perf_counter()
            tm = T2 - T1
            msg = f'当前检索结果已输出为网页文件，用时{tm:.2f}秒！'                     
        else:
            msg = '抱歉，没有检索结果可供输出，请先检索！'        
        self._ui.set_status_text(msg)
        
    def print_result(self):
        if self._page_i !=0:
            self.resetWindow()
            startNum = self._page_i  
            startSetNum = self._list_num[startNum]
            endSetNum = startSetNum + self._custom_set
            list_limit = max(self._list_num)
            if endSetNum <= list_limit:
                endNum = self._list_num.index(endSetNum)
                self._page_i = endNum
            else:
                endNum = -1
                self._page_i = 0
            if endNum == -1:
                result_pd = self._html_converter.lst2pd(self._list_num[startNum:], self._list_lang[startNum:],
                                                          self._list_cont[startNum:])
                html =  self._html_converter.pd2html(result_pd)
            else:
                result_pd = self._html_converter.lst2pd(self._list_num[startNum:endNum], self._list_lang[startNum:endNum],
                                                          self._list_cont[startNum:endNum])
                html =  self._html_converter.pd2html(result_pd)
            self._ui.set_result_html(''.join(html))
            total_sents = str(len(self._list_num))
            total_set = str(self._list_num[-1])
            if self._page_i != 0:
                self._ui._next_page_button.setDisabled(False)
            else:
                self._ui._next_page_button.setDisabled(True)
            self._ui.set_status_text(f"本次检索已完成")
        else:
            self.resetWindow()
            self._ui.set_result_html('')
            self._ui._words_hit_value.setText('0')
            self._ui._pairs_hit_value.setText('0')
            self._ui.set_status_text('抱歉，未检索到任何数据')

    def setFreq(self):        
        self.voc_opt_window.show()        
 
    def print_cplist(self):
        self.cpl_window = SubWindow()
        self.cpl_window.set_title("内嵌双语语料库列表")
        cpl_text = self._help_data['corpus']
        self.cpl_window.set_html(cpl_text)
        self.cpl_window.setGeometry(100, 100, 700, 420)
        self.cpl_window.show()            
        msg = f'内嵌双语语料库列表已展示！'
        self._ui.set_status_text(msg)

    def print_reg(self):
        self.reg_window = SubWindow()
        self.reg_window.set_title("正则表达式常用符号释义")
        reg_text = self._help_data['regex']
        self.reg_window.set_html(reg_text)
        self.reg_window.setGeometry(100, 100, 700, 420)
        self.reg_window.show()            
        msg = f'正则表达式列表已展示！'
        self._ui.set_status_text(msg)

    def print_code(self):
        self.code_window = SubWindow()
        self.code_window.set_title("信息提取错误代码")
        code_text = self._help_data['error']
        self.code_window.set_html(code_text)
        self.code_window.setGeometry(100, 100, 700, 420)
        self.code_window.show()            
        msg = f'信息提取错误代码已展示！'
        self._ui.set_status_text(msg)
        
    def print_pynlpir(self):           
        self._ui.set_status_text("正在提取词性赋码表，请稍候...")
        html = self._help_data['pynlpir']
        self.tag_window = SubWindow()
        self.tag_window.set_title("NLPIR中文词性赋码表")
        self.tag_window.setGeometry(100, 100, 400, 420)
        self.tag_window.set_html(html)
        self.tag_window.show()            
        msg = f'中文词性赋码表已展示！'
        self._ui.set_status_text(msg)

    def print_penn(self):              
        self._ui.set_status_text("正在提取词性赋码表，请稍候...")
        html = self._help_data['nltk']
        self.tag_window = SubWindow()
        self.tag_window.set_title("PENN英文词性赋码表")
        self.tag_window.setGeometry(100, 100, 400, 420)
        self.tag_window.set_html(html)
        self.tag_window.show()            
        msg = f'英文词性赋码表已展示！'
        self._ui.set_status_text(msg)

    def show_window(self, msg_a, msg_b, lang):
        T1 = time.perf_counter()
        self._voc_window = VocWindow()
        self._voc_window.set_title(msg_a)
        self._voc_window.set_html(msg_b)
        if lang == "zh":
            icon_path = "./app_data/images/cn.png"
        else:
            icon_path = "./app_data/images/en.png"
        self._voc_window.set_icon(icon_path)
        self._voc_window.show()
        T2 = time.perf_counter()
        tm = T2 - T1
        msg=f'{msg_a}已展示，共用时{tm:.2f}秒'
        self._ui.set_status_text(msg)
        
    def print_zh_freq(self):
        corpora_selected = []
        msg = ""
        opts = self.voc_opt_window.get_filter_options()
        src_scope_option = self._ui.search_scope()
        if opts['scope']== 0:
            if self.current_corpus:
                corpora_selected = self.current_corpus
            else:
                msg = "抱歉，当前语料为空，请先双击要检索的语料库名称，然后再试！"
        if opts['scope']== 1:
            if self.current_corpora_selected:
                corpora_selected = self.current_corpora_selected
            elif src_scope_option['scope'].value == 1:
                error_msg, corpora_selected = self.selected_corpora(src_scope_option)
                if not error_msg:
                    self.current_corpora_selected = corpora_selected
                msg = error_msg                
            else:
                msg = "抱歉，当前所选语料为空，请先选择要检索的语料库名称，然后再试！"
        if opts['scope']== 2:
            corpora_selected = self.corpora
        if corpora_selected:        
            self.tag_voc_preload(opts, self._stop_words_zh, self._stop_words_en, corpora_selected, 'zh')
        if msg:
            self._ui.set_status_text(msg)
  
    def print_en_freq(self):
        corpora_selected = []
        msg = ""
        opts = self.voc_opt_window.get_filter_options()
        src_scope_option = self._ui.search_scope()
        if opts['scope']== 0:
            if self.current_corpus:
                corpora_selected = self.current_corpus
            else:
                msg = "抱歉，当前语料为空，请先双击要检索的语料库名称，然后再试！"
        if opts['scope']== 1:
            if self.current_corpora_selected:
                corpora_selected = self.current_corpora_selected
            elif src_scope_option['scope'].value == 1:
                error_msg, corpora_selected = self.selected_corpora(src_scope_option)
                if not error_msg:
                    self.current_corpora_selected = corpora_selected
                msg = error_msg                
            else:
                msg = "抱歉，当前所选语料为空，请先选择要检索的语料库名称，然后再试！"
        if opts['scope']== 2:
            corpora_selected = self.corpora
        if corpora_selected:      
            self.tag_voc_preload(opts, self._stop_words_zh, self._stop_words_en, corpora_selected, 'en')
        if msg:
            self._ui.set_status_text(msg)

    def get_ratio(self, a, b):
        return ((a/b))*100
