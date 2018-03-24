#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, Response, request
from gzt.parser import *
from gzt.config import Settings
import webview, ast
import sys, json, socket, os
import threading

app = Flask(__name__)

def listNewspapers():
    filename = os.path.dirname(os.path.realpath(__file__)) + "/parser.py"
    with open(filename) as file:
        node = ast.parse(file.read())
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    names = []
    for i in classes:
        names.append(i.name)
    return names

def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

@app.route('/')
def root():
    if is_connected("www.google.com.tr"):
        thelist = str(Settings().readSetting('newspapers','list')).split(',')
        newspaperlist = []
        for i in thelist:
            newspaperlist.append([i,eval(i+'()').name])
        return render_template("index.html", update_interval = str(Settings().readSetting('main','update_interval')), default_view = str(Settings().readSetting('main','default_view')), newspaper_list = newspaperlist, all_papers = listNewspapers())
    else:
        return render_template("error.html", caption = "Hata!!!", content="Lütfen internet bağlantınızı kontrol edin. Her 60sn de bir bu sayfa kendiliğinden yenilenecektir.")

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/detail', methods=['GET'])
def detail():
    gazete = request.args.get('gazete', type=str)
    link = request.args.get('link', type=str)
    classname = ""
    try:
        classname = eval(gazete+'()')
        header1, header2, content = classname.parseNewsContent(link)
        return Response(json.dumps({'h1': header1, 'h2': header2, 'content': content},),mimetype='application/json')
    except:
        return Response(json.dumps({'h1': "", 'h2': "", 'content': ""},),mimetype='application/json')

@app.route("/toggle")
def toggle():
    webview.toggle_fullscreen()
    return jsonify({})

@app.route("/reload")
def reload():
    webview.load_url('http://localhost:5000')
    return jsonify({})

@app.route("/saveSettings", methods=['GET'])
def saveSettings():
    section = request.args.get('section', type=str)
    key = request.args.get('key', type=str)
    value = request.args.get('value', type=str)
    try:
        Settings().writeSetting(section,key, value)
        return jsonify({'result':'true'})
    except KeyError as e:
        pass
    except:
        return jsonify({'result':'false'})

@app.route('/content', methods=['GET'])
def content():
    gazete = request.args.get('gazete', type=str)
    type = request.args.get('type', type=str)
    try:
        name = ""
        thelist = ""
        thelist = eval(gazete+'()').parseNewsList()
        name = eval(gazete+'()').name
        if type == "grid":
            return render_template("gallery.html", list = thelist, name = name, gazete = gazete)
        else:
            return render_template("content.html", list = thelist, name = name, gazete = gazete)
    except:
        return render_template("error.html", caption = "Hata!!!", content="Bu gazete için hata bulundu.", extraStyle = "style=margin-top:50px;")

@app.route('/refresh')
def refresh():
    result = {}
    try:
        thelist = str(Settings().readSetting('newspapers','list')).split(',')
    except KeyError as e:
        pass
    for y in thelist:
        try:
            newslist = eval(y+'()').parseNewsList()
            counter = 0
            for i in newslist:
                if int(i[3]) == int(Settings().readSetting(y,'lastId')):
                    break
                counter = counter + 1
            newlistnumber = len(newslist) -  (len(newslist) - counter)
            if newlistnumber > 0:
                Settings().writeSetting(y,'lastId', str(newslist[0][3]))
            result[y] = newlistnumber
        except:
            pass
    return Response(json.dumps(result,),mimetype='application/json')

def start_server():
    app.run()

t = threading.Thread(target=start_server)
t.daemon = True
t.start()

webview.create_window("Gazete", "http://127.0.0.1:5000/", min_size=(1280, 768))

sys.exit()
