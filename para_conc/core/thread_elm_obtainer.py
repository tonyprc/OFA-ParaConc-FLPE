#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Thread for auto identifying political element from corpus
# Copyright (c) 2024 Tony Chang (42716403@qq.com)

import os, sys, time, json, pickle, re
from PySide6.QtCore import Signal, Slot, QThread
from openai import OpenAI

class ElmObtainerThread(QThread):
    msg_m_signal = Signal(str)       
    output_signal = Signal([str, str])
    refresh_signal = Signal(list)
    pbar_signal = Signal([int, int])
    
    def __init__(self, user_text, api_key):   
        super(ElmObtainerThread, self).__init__()
        self._currentDir = os.getcwd()
        self._dataDir = os.path.join(self._currentDir, "app_data")
        self._moon_key = api_key
        self._prompt = "你是 Kimi，由 Moonshot AI提供的人工智能助手，你更擅长中文和英文的对话。\你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
        self.question = user_text
        self.answer = ""
        self.error = ""
        self.msg = ""

    def __del__(self):
        pass

    def update_prompt(self, new_prompt):
        if new_prompt:
            self._prompt = new_prompt
   
    def run (self):
        T1 = time.perf_counter()        
        self.msg_m_signal.emit("语料传输中，请稍候....")
        time.sleep(2)
        self.msg_m_signal.emit("开始提取元素，请稍候....")
        try:
            client = OpenAI(
                api_key = self._moon_key,
                base_url = "https://api.moonshot.cn/v1",
                )
            completion = client.chat.completions.create(
                model = "moonshot-v1-auto",
                messages = [
                    {"role": "system", "content": self._prompt},
                    {"role": "user", "content": self.question}
                    ],
            temperature = 0.3,
                )
            result = completion.choices[0].message.content
        except Exception as e:
            self.error = e.code
            result = ""
        if result:
            self.answer = result
        if self.answer:
            self.msg = f"元素提取成功！"
        if self.error:            
            self.msg = f"元素提取失败！错误代码：{self.error}"
        self.output_signal.emit(self.answer,self.error)
        T2 = time.perf_counter()
        time_used = T2 - T1
        self.msg_m_signal.emit(f"{self.msg}共用时{time_used:.2f}秒")
        time.sleep(1)
