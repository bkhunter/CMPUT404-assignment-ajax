#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask

import flask
from flask import Flask, request
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

# When given route path, redirect to index.html - where the canvas is
# Return 301 status code, moved permanently
@app.route("/")
def hello():
    return flask.redirect("/static/index.html"), 301

# Creates or updates JSON at <entity> then returns it
@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    data =  flask_post_json()

    if request.method == 'PUT':
        myWorld.set(entity, data)
    elif request.method == "POST":
        for item in data.keys():
            myWorld.update(entity,item,data[item])

    res = myWorld.get(entity)
    return json.dumps(res)

# Displays the JSON of the world state
@app.route("/world", methods=['POST','GET'])    
def world():
    return flask.jsonify(myWorld.world())

# Gets the <entity> and return a JSON representation of it
@app.route("/entity/<entity>")    # entity is just a variable  
def get_entity(entity):
    ent = myWorld.get(entity)
    return flask.jsonify(ent)

# Clear the world, and return a representation of it
@app.route("/clear", methods=['POST','GET'])
def clear():
    myWorld.clear()
    return flask.jsonify(myWorld.world())
    

if __name__ == "__main__":
    app.run()
