import logging
from flask import request, jsonify
from treelib import Node, Tree
from codeitsuisse import app
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
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
    print("data sent for evaluation {}".format(data))

    bossHp = data.get("boss").get("offense")
    skillList = data.get("skills")
    skillIndex = {}
    parent = len(skillList)*[-1]

    cnt = 0;
    for skill in skillList:
        skillIndex[skill["name"]] = cnt
        cnt += 1;

    for skill in skillList:
        if skill["require"] is not None:
            parent[skillIndex[skill["require"]]] = skillIndex[skill["name"]]

    starters = []
    for i in range(len(skillList)):
        if skillList[i]["require"] is None: starters.append(i)

    skillArray = len(starters)*[0]
    skillIdxArray = len(starters)*[0]
    for i in range(len(starters)):
        skillArray[i] = []
        skillIdxArray[i] = [];
        tmp = starters[i]
        while tmp is not -1:
            skillArray[i].append(0);
            skillIdxArray[i].append(tmp)
            tmp = parent[tmp]

    totalDmg = 0;
    for i in range(len(skillIdxArray)):
        for j in range(len(skillIdxArray[i])):
            skillArray[i][j] = (skillList[skillIdxArray[i][j]]["offense"], skillList[skillIdxArray[i][j]]["points"])
            totalDmg += skillArray[i][j][0]
        for j in range(1, len(skillArray[i])):
            skillArray[i][j] = (skillArray[i][j][0] + skillArray[i][j-1][0], skillArray[i][j][1] + skillArray[i][j-1][1])

    d = len(skillArray)*[0]
    trace = len(skillArray)*[0]

    d[0] = totalDmg*[float('inf')]
    trace[0] = totalDmg*[0]

    trace[0][0] = -1
    for j in range(len(skillArray[0])):
        d[0][skillArray[0][j][0]] = skillArray[0][j][1]
        trace[0][skillArray[0][j][0]] = j

    for i in range(1, len(d)):
        d[i] = totalDmg*[float('inf')]
        trace[i] = totalDmg*[-1]

        skills = skillArray[i]
        for j in range(len(d[i])):
            d[i][j] = d[i-1][j]
            trace[i][j] = -1
            for k in range(len(skills)):
                skill = skills[k]
                if j-skill[0] >= 0:
                    newCost = d[i-1][j-skill[0]] + skill[1]
                    if(d[i][j] > newCost):
                        d[i][j] = newCost
                        trace[i][j] = k

    minSkillPt = float('inf')
    dmgDealt = 0
    for i in range(bossHp, totalDmg):
        if minSkillPt > d[-1][i]:
            minSkillPt = d[-1][i]
            dmgDealt = i

    traces = []
    for i in range(len(skillArray)-1, -1, -1):
        traces.append(trace[i][dmgDealt])
        if trace[i][dmgDealt] >= 0:
            dmgDealt -= skillArray[i][trace[i][dmgDealt]][0]

    traces.reverse();

    ans = [];
    for i in range(len(traces)):
        if traces[i] >= 0:
            for j in range(traces[i]+1):
                ans.append(skillList[skillIdxArray[i][j]]['name'])

    print("My result :{}".format(ans))
    return jsonify(ans)
