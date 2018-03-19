#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, Response, request
from gzt.parser import YeniAkit, Sozcu, Alert
from gzt.config import Settings
import webview
import sys, json
import threading

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html", update_interval = int(Settings().readSetting('main','update_interval')))

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/detail', methods=['GET'])
def detail():
    gazete = request.args.get('gazete', type=str)
    link = request.args.get('link', type=str)
    classname = ""
    try:
        if gazete == "Yeni Akit":
            classname = YeniAkit()
        if gazete == "Sözcü":
            classname = Sozcu()
        header1, header2, content = classname.parseNewsContent(link)
        return Response(json.dumps({'h1': header1, 'h2': header2, 'content': content},),mimetype='application/json')
    except:
        return Response(json.dumps({'h1': "", 'h2': "", 'content': ""},),mimetype='application/json')

@app.route("/toggle")
def toggle():
    webview.toggle_fullscreen()
    return jsonify({})

@app.route('/content', methods=['GET'])
def content():
    gazete = request.args.get('gazete', type=str)
    name = ""
    thelist = ""
    if gazete == "akit":
            thelist = YeniAkit().parseNewsList()
            name = "Yeni Akit"
    if gazete == "Sözcü":
            thelist = Sozcu().parseNewsList()
            name = "Sözcü"
    return render_template("content.html", list = thelist, name = name)

@app.route('/refresh')
def refresh():
    global notify
    thelist = YeniAkit().parseNewsList()
    counter = 0
    for i in thelist:
        if i[3] == int(Settings().readSetting('yeniakit','lastId')):
            break
        counter = counter + 1
    ylastnews = len(thelist) -  (len(thelist) - counter)
    if ylastnews > 0:
        Settings().writeSetting('yeniakit','lastId', str(thelist[0][3]))
    thelist = Sozcu().parseNewsList()
    counter = 0
    for i in thelist:

        if int(i[3]) == int(Settings().readSetting('sozcu','lastId')):
            break
        counter = counter + 1
    slastnews = len(thelist) -  (len(thelist) - counter)
    if slastnews > 0:
        Settings().writeSetting('sozcu','lastId', str(thelist[0][3]))
    return Response(json.dumps({'yeniakit': ylastnews, 'sozcu': slastnews},),mimetype='application/json')

def start_server():
    app.run()



t = threading.Thread(target=start_server)
t.daemon = True
t.start()

webview.create_window("Gazete", "http://127.0.0.1:5000/")

sys.exit()
