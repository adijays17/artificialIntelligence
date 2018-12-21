from expand import expand
from collections import deque

def a_star_search (dis_map, time_map, start, end):
    path = [] 
    expandedNode = []
    if end not in dis_map or start not in dis_map:
        return path
    elif start == end:
        path.append(end)
    else:
        finalPaths = []
        q = deque(sorted(searching(time_map, start, dis_map, end, finalPaths, expandedNode), key=lambda k: (k['Cost'], k['Path'][-1])))
        queue_iteration(q, time_map, dis_map, end, finalPaths, expandedNode)
        if finalPaths:
            path = sorted(finalPaths, key=lambda k: (k['Cost'], k['Path'][-1]))[0]["Path"]
    for each in expandedNode:
        expand(each, dis_map)
    return path
        
def queue_iteration(q, time_map, dis_map, end, finalPaths, expandedNode):
    localQueue = deque([])
    while q:
        temp = q.popleft()        
        if finalPaths and finalPaths[0]["Cost"] <= temp["Cost"]:
            continue 
        newItem = temp["Path"][len(temp["Path"]) - 1]
        if newItem == end:
            continue
        returnedQ = searching(time_map, newItem, dis_map, end, finalPaths, expandedNode, temp["Path"])
        localQueue = mergeQueues(localQueue, returnedQ)
        localQueue = mergeQueues(q, localQueue)
        localQueue = deque(sorted(list(localQueue), key=lambda k: (k['Cost'], k['Path'][-1])))
    q = localQueue
    if q:
        q = deque(sorted(list(q), key=lambda k: (k['Cost'], k['Path'][-1])))
        queue_iteration(q, time_map, dis_map, end, finalPaths, expandedNode)

def searching(time_map, start, dis_map, end, finalPaths, expandedNode, otherItems=None):
    if start not in expandedNode:
        expandedNode.append(start)
    q = deque([])
    for each in time_map[start]:
        if otherItems is not None and each in otherItems:
            continue
        if time_map[start][each] is not None:
            localPath = None
            if otherItems is not None:
                localList = []
                for eachOtherItems in otherItems:
                    localList.append(eachOtherItems)
                localList.append(each)
                localPath = localList
            else:
                localPath = [start, each]
            temp = {}
            timeToTraverse = 0
            if otherItems is None:
                timeToTraverse = time_map[start][each]
            else:
                timeToTraverse = compute_time_to_traverse(otherItems, each, timeToTraverse, time_map)            
            if finalPaths and finalPaths[0]["Cost"] < timeToTraverse + dis_map[each][end]:
                continue    
            temp["Path"] = localPath
            temp["Cost"] = timeToTraverse + dis_map[each][end]
            q.append(temp)
            if each == end:
                finalPaths.append(temp)
    return q

def compute_time_to_traverse(otherItems, lastItem, timeToTraverse, time_map):
    oldItems = None
    for eachItems in otherItems:
        if oldItems is None:
            oldItems = eachItems
            continue
        timeToTraverse = timeToTraverse + time_map[oldItems][eachItems]
        oldItems = eachItems
    timeToTraverse = timeToTraverse + time_map[oldItems][lastItem]
    return timeToTraverse
    
def mergeQueues(a, b):
    newQ = deque([])
    while a:
        if a:
            newQ.append(a.popleft())
    while b:
        if b:
            newQ.append(b.popleft())
    return newQ