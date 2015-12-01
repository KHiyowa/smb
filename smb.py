#!/usr/local/bin/python3

import sys
import re
import os
import subprocess

# 引数のチェック
if len(sys.argv) < 2:
    print("Usage:\nsmb Host Directory")
    exit()

# configファイルを開く
try:
    configFile = open(os.path.expanduser("~/.smb/config"), "r")
except FileNotFoundError:
    print("~/.smb/config not found.")
    exit()

config = configFile.readlines()
configFile.close()

# ホスト名を読み込む
host = sys.argv[1]
directory = sys.argv[2].rstrip('\n')

# Hostが見つかったフラグ
hostFound = False

# 入力されたホスト名の項を探す
for i in range(len(config)):
    # Host: と入力されたホスト名が同時に出てきたら
    if config[i].find("Host") >= 0 and config[i].find(host) >= 0:
        hostFound = True
        # HostNameに示されたホスト名を抽出
        hostname = re.sub("( +|\t)HostName( +)|\t", "", config[i+1]).rstrip('\n')
        # Userに示されたユーザ名を抽出
        username = re.sub("( +|\t)User( +|\t)", "", config[i+2]).rstrip('\n')
        # パスを生成
        path = "/".join(["/", hostname, directory])

        # smbclientを叩く
        subprocess.call(['smbclient', path, '-U', username])

if hostFound == False:
    print("Host Unknown")
