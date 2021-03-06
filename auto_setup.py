﻿import os
import sys
import threading
import re
import webbrowser

import tkinter as tk  
from tkinter import ttk  
from tkinter import Menu  
from tkinter import messagebox as mBox

from window import *
from version import GetVersion


#全局变量
PROCESS_NAME = "自动安装"
ICON_NAME = "ico.ico"
VERSION = 1.1
CHECK_URL = "https://github.com/lingliqianxun/taobao-auto_setup/blob/master/version.txt?raw=true"
DOWN_URL = "https://github.com/lingliqianxun/taobao-auto_setup/blob/master/dist/auto_setup.exe?raw=true"



def PathShow():
    path = os.getcwd()
    if re.search(u"[\u4e00-\u9fa5]+",path):
        toplevel_path = tk.Toplevel(win)
        toplevel_path.title("路径提示")
        toplevel_path.iconbitmap(WindowResourcePath(ICON_NAME))
        WindowSizeCenter(toplevel_path, 500,250)

        ttk.Label(toplevel_path, text="", foreground='red', anchor=tk.W).grid(stick='W',column=0, row=0, padx=50, pady=5)
        ttk.Label(toplevel_path, text="✖错误路径样例：F:\\game\\极品飞车\\game\\", foreground='red', anchor=tk.W).grid(stick='W',column=0, row=1, padx=50, pady=0)
        ttk.Label(toplevel_path, text="✔正确路径样例：F:\\game\\Need For Speed\\game\\", foreground='green', anchor=tk.W).grid(stick='W',column=0, row=2, padx=50, pady=0)
        ttk.Label(toplevel_path, text="", foreground='red', anchor=tk.W).grid(stick='W',column=0, row=3, padx=50, pady=5)


        path_text = "✖当前路径：" + path
        new_text = ""
        count = 1
        for p in range(0,len(path_text)):
            new_text += path_text[p]
            
            if re.search(u"[\u4e00-\u9fa5]+",path_text[p]):
                count += 2
            else:
                count += 1
                
            if count > 62:
                new_text += '\n'
                count = 0
            
        ttk.Label(toplevel_path, text=new_text, foreground='red', anchor=tk.W).grid(stick='W',column=0, row=4, padx=50, pady=0)


        ttk.Label(toplevel_path, text="提示：大多数游戏不支持中文（文件夹）路径，请检查并更改为英文路径！", anchor=tk.W).grid(stick='W',column=0, row=5, padx=50, pady=20)
        
        toplevel_path.grab_set()
        toplevel_path.focus()

    #弹框模式
    #path = os.getcwd()   
    #if re.search(u"[\u4e00-\u9fa5]+",path):
    #    message = "当前目录：\n" + path + "\n\n大多数游戏不支持中文（文件夹）路径，请检查并更改为英文路径！"
    #    mBox.showinfo("路径提示", message)
    
def Check():
    if os.path.exists("文件完整性校验工具.exe") == False:
        return -1,"没有找到【文件完整性校验工具.exe】"
    if os.path.exists("文件.md5") == False:
        return -1,"没有找到【文件.md5】"
    result = os.system("start 文件完整性校验工具.exe 文件.md5")
    if result == 0:
        return result,"检查开始，请耐心等待结束...\n\n如果损坏请重下损坏包即可！"
    else:
        return result,"检查失败，请手动检查！"

def Unrar(action):
    if action == 0:
        return 0,"rar：右键解压任意一个压缩包，会自动解压所有\n\nzip：右键解压zip包即可"
    
    for f in os.listdir():
        if ('rar' in f) | ('zip' in f):
            result = os.system("start winrar x \"%s\"" % f)
            if result == 0:
                return result,"解压开始，请耐心等待结束..."
            else:
                return result,"解压失败，请手动解压！"
    return -1,"没有找到压缩文件，请检查！"

def Read():
    if os.path.exists("游戏说明.txt") == False:
        return -1,"没有找到【游戏说明.txt】"
    result = os.system("start 游戏说明.txt")
    if result == 0:
        return result,"打开成功，请认真阅读！"
    else:
        return result,"打开【游戏说明.txt】失败，请手动打开！"

def Third_auto(path):
    for p in os.listdir(path):
        path_next = path + "\\" + p
        if os.path.isdir(path_next):
            Third_auto(path_next)
        else:
            if ".exe" in p:
                os.system("start \"\" \"%s\"" % path_next)
    
def Third(action):
    has_dir = False
    for f1 in os.listdir():
        if os.path.isdir(f1):
            has_dir = True
            for f2 in os.listdir(f1):
                path = f1 + "\\" + f2
                if os.path.isdir(path):
                    if (f2 == "_CommonRedist") | (f2 == "_Redist") | (f2 == "Redist") | (f2 == "redist") | (f2 == "__Installer"):
                        os.system("start \"\" \"%s\"" % path)
                        if action == 0:
                            return 0,"请自行安装！"
                        else:
                            Third_auto(path)
                            return 0,"已自动打开插件，请依次安装..."
    if has_dir:
        return -1,"该游戏可能无需安装插件！"
    else:
        return -1,"请先解压游戏！"
      
def Open():
    return 0,"进游戏目录打开游戏即可。\n\n不知道请阅读【游戏说明.txt】"

def CheckVersion(is_show):
    threading.Thread(target=GetVersion, args=(win,is_show,PROCESS_NAME,ICON_NAME,VERSION,CHECK_URL,DOWN_URL)).start()

def click_button(num):
    if num == 1:
        title = "自动检查提示"
        result, message = Check() 
    elif num == 2:
        title = "自动解压提示"
        result, message = Unrar(1)
    elif num == 3:
        title = "手动解压提示"
        result, message = Unrar(0) 
    elif num == 4:
        title = "阅读说明提示"
        result, message = Read() 
    elif num == 5:
        title = "自动安装插件提示"
        result, message = Third(1)
    elif num == 6:
        title = "手动安装插件提示"
        result, message = Third(0) 
    elif num == 7:
        title = "打开游戏提示"
        result, message = Open() 

    if result == 0:
        mBox.showinfo(title, message)
    else:
        mBox.showwarning(title, message)

def click_menu(name):
    if name == "shop_qx":
        url = "https://shop119341111.taobao.com/"
        webbrowser.open(url)
    elif name == "shop_jj":
        url = "https://shop548614869.taobao.com/"
        webbrowser.open(url)
    elif name == "game_buyhouse":
        url = "https://github.com/lingliqianxun/game-buyhouse/blob/master/dist/buyhouse.exe?raw=true"
        webbrowser.open(url)
    elif name == "game_home":
        url = "https://lingliqianxun.github.io/"
        webbrowser.open(url)
    elif name == "video_youku":
        url = "http://i.youku.com/lingliqianxun"
        webbrowser.open(url)
    elif name == "video_bili":
        url = "https://space.bilibili.com/73414137/"
        webbrowser.open(url)
    elif name == "version_check":
        CheckVersion(True)
    elif name == "version_about":
        mBox.showinfo("关于本软件", "只用于自助安装\n版本：v%s\n制作：By 绫里千寻"%VERSION)

#界面
def ViewSet(win):
    #菜单 
    menuBar = Menu(win,bg='red',fg='red')
    
    shopMenu = Menu(menuBar, tearoff=0)  
    shopMenu.add_command(label="千寻电玩", command=lambda:click_menu("shop_qx"))  
    shopMenu.add_command(label="姬机电玩", command=lambda:click_menu("shop_jj"))

    gameMenu = Menu(menuBar, tearoff=0)  
    gameMenu.add_command(label="买房记", command=lambda:click_menu("game_buyhouse"))
    gameMenu.add_command(label="主页更多", command=lambda:click_menu("game_home"))
    gameMenu.add_command(label="敬请期待...") 

    videoMenu = Menu(menuBar, tearoff=0)  
    videoMenu.add_command(label="优酷", command=lambda:click_menu("video_youku"))  
    videoMenu.add_command(label="哔哩哔哩", command=lambda:click_menu("video_bili"))

    versionMenu = Menu(menuBar, tearoff=0)  
    versionMenu.add_command(label="检查更新", command=lambda:click_menu("version_check"))
    versionMenu.add_command(label="关于", command=lambda:click_menu("version_about"))  

    menuBar.add_cascade(label="店铺", menu=shopMenu)  
    menuBar.add_cascade(label="更多游戏", menu=gameMenu)
    menuBar.add_cascade(label="游戏视频", menu=videoMenu)
    menuBar.add_cascade(label="版本", menu=versionMenu)  
    win.config(menu=menuBar) 

    #主界面
    ttk.Label(win, text="第一步：", width=15, anchor=tk.E).grid(column=0, row=0, padx=20, pady=20)
    ttk.Button(win,text="自动检查（可跳过）", width=15, command=lambda:click_button(1)).grid(column=1, row=0)
    
    ttk.Label(win, text="第二步：", width=15, anchor=tk.E).grid(column=0, row=1, padx=20, pady=20)
    ttk.Button(win,text="自动解压", width=15, command=lambda:click_button(2)).grid(column=1, row=1)
    ttk.Button(win,text="手动解压", width=15, command=lambda:click_button(3)).grid(column=2, row=1, padx=20)
    
    ttk.Label(win, text="第三步：", width=15, anchor=tk.E).grid(column=0, row=2, padx=20, pady=20)
    ttk.Button(win,text="阅读游戏说明", width=15, command=lambda:click_button(4)).grid(column=1, row=2)
    
    ttk.Label(win, text="第四步：", width=15, anchor=tk.E).grid(column=0, row=3, padx=20, pady=20)
    ttk.Button(win,text="自动安装插件", width=15, command=lambda:click_button(5)).grid(column=1, row=3)
    ttk.Button(win,text="手动安装插件", width=15, command=lambda:click_button(6)).grid(column=2, row=3, padx=20)
    
    ttk.Label(win, text="第五步：", width=15, anchor=tk.E).grid(column=0, row=4, padx=20, pady=20)
    ttk.Button(win,text="打开游戏", width=15, command=lambda:click_button(7)).grid(column=1, row=4)
    
    ttk.Label(win, text="提示：自动操作失败，请手动操作！", foreground='red').grid(stick='W',column=0, row=5, columnspan=3, padx=60, pady=20)
    
    ttk.Label(win, text="其他注意事项：").grid(stick='EN', column=0, row=6, padx=0, pady=0)
    ttk.Label(win, text="1.配置是否达标\n2.放英文路径\n3.更新所有驱动\n4.笔记本切换独立显卡\n5.关闭杀毒\n6.不要在网盘中打开").grid(stick='W', column=1, row=6, columnspan=3, padx=0, pady=0)


if __name__ == "__main__":
    #####面板#####
    win = tk.Tk()       
    win.title("自助安装工具v"+str(VERSION))  
    #win.resizable(0,0)
    WindowSizeCenter(win,460,510)
    win.iconbitmap(WindowResourcePath(ICON_NAME))
    
    ViewSet(win)

    #中文路径提示
    PathShow()

    #查询版本
    CheckVersion(False)

    win.mainloop()
