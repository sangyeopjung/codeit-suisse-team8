import logging
from flask import request, jsonify
from treelib import Node, Tree
from codeitsuisse import app
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

"""
class node(object):
    def __init__(self, points, offense, children = None):
        self.offense = offense
        self.points = points
        self.children = children or []
        self.parent = None
        for child in self.children:
            child.parent = self
"""

@app.route('/skill-tree', methods=['POST'])
def skill_tree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    value = data.get("boss").get("offense")
    skills = data.get("skills")
    num_skills = len(skills)
    """
    tree = Tree()
    tree.create_node("Root", "root")
    for index, skill in enumerate(skills):
        if(!skill.get("require")):
            ("data" + index) = Node(skill.get("name"), skill.get("name"), parent="root", data=skill.get("points"))
            a.offense = 10;
            print(a.offense);
        else
            tree.create_node(skill.get("name"), skill.get("name"), parent=skill.get("require"), data=skill.get("points"))
    """
    min = -1
    points = 0
    minList = []


    end = datetime.now() + timedelta(seconds=10)
    cur = datetime.now()
    count = 0
    while (end - cur).seconds > 0:
        count+=1
        cur = datetime.now()
        temporaryList = []
        temporaryPoints = 0
        offense = value
        while(offense>0):
            num = random.randrange(0, num_skills)
            if(skills[num].get("name") in temporaryList):
                continue
            if(skills[num].get("require") is not None and skills[num].get("require") not in temporaryList):
                continue
            offense -= skills[num].get("offense")
            temporaryPoints += skills[num].get("points")
            temporaryList.append(skills[num].get("name"))

        if (minList is not None or temporaryPoints < min):
            minList = temporaryList
            min = temporaryPoints
    print(count)
    logging.info("My result :{}".format(minList))
    return jsonify(minList)
