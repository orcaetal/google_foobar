import copy
def solution(entrances,exits,path):
	
	class node():
		def __init__(self,nodeN,dats):
			self.node = nodeN
			self.path = dats
			self.level = -1
			self.capacity = dats
			self.flow = 0
			
	#add supersource/supersink, init node objects
	def formatData(entrances,exits,path):
		
		#edge to supersource
		for each in path:
			each.insert(0,0)
		
		#supersource
		sourcePath = []
		for count in range(len(path[0])):
			if count - 1 in entrances:
				sourcePath.append(100000000)
			else:
				sourcePath.append(0)
		path.insert(0,sourcePath)
		
		#supersink
		sinkPath=[]
		for count in range(len(path[0])):
			sinkPath.append(0)
			if count - 1 in exits:
				path[count].append(100000000)
			else:
				path[count].append(0)
		sinkPath.append(0)
		path.append(sinkPath)
		
		#init nodeDict from paths
		nodeDict={}
		roomCounter=0
		for vert in path:
			newNode = node(roomCounter,vert)
			nodeDict[roomCounter] = newNode
			roomCounter +=1
		
		nodeDict[0].level = 0
		
		return(nodeDict)
	
	#construct level graph from source
	def levelGraph(nodeDict):
		level = 0
		finished = False
		while finished == False:
			if level > len(nodeDict):
				return('exit')
			for nodes in nodeDict:
				#start at current level
				if nodeDict[nodes].level == level:
					#check capacities of links
					for linkedRoom in range(len(nodeDict[nodes].path)):
						if nodeDict[nodes].path[linkedRoom] > 0 and nodeDict[nodes].capacity[linkedRoom] > 0 and nodeDict[linkedRoom].level == -1:
							nodeDict[linkedRoom].level = level + 1
			#supersink assigned valid level
			if nodeDict[len(nodeDict)-1].level != -1:
				finished = True
			level += 1
	
	#[recursive] -- find a path from source to sink and adjust capacity to blocking flow
	def findSink(node,nodeDict,trace,block,visited,pathBlocks):
		newTrace = copy.copy(trace)
		if node.node not in newTrace:
			newTrace.append(node.node)
		
		#exit cond 1: reached sink -- adjust blocking flow and find new path
		if node.node == len(nodeDict)-1:
			finBlock = copy.copy(block)
			newNodeDict = copy.copy(nodeDict)
			for i in range(len(newTrace)-1):
				newNodeDict[newTrace[i]].capacity[newTrace[i+1]] -= finBlock
			pathBlocks.append(finBlock)
			return(findSink(newNodeDict[0],newNodeDict,[],10000000,visited,pathBlocks))
		
		#check all forward edges
		deadEnd = True
		for roomNo in range(len(node.path)):
			if node.capacity[roomNo] > 0 and nodeDict[roomNo].level == node.level+1 and [node.node,roomNo] not in visited:
				deadEnd = False
				if node.capacity[roomNo] < block:
					newBlock = node.capacity[roomNo]
				else:
					newBlock = copy.copy(block)
				return(findSink(nodeDict[roomNo],nodeDict,newTrace,newBlock,visited,pathBlocks))
					
		#exit cond 2 -- dead end -- add attempt to visited, try new route
		if deadEnd:
			if newTrace == [0]:
				return(pathBlocks)
			newVisited = copy.copy(visited)
			newTrace.pop()
			lastVisited = newTrace[-1]
			newVisited.append([lastVisited,node.node])
			
			return(findSink(nodeDict[lastVisited],nodeDict,newTrace,100000000,newVisited,pathBlocks))
	
	#construct level graph, find blocking flows, sum result, repeat until dead end
	def main():
		result = 0
		sumOfAllPaths = 0
		nodeDict = formatData(entrances,exits,path)
		while result != 'exit':
			result = levelGraph(nodeDict)
			allPaths = findSink(nodeDict[0],nodeDict,[],10000000,[],[])
			sumOfAllPaths += sum(allPaths)
			
			#reset levels
			for ppNodes in nodeDict:
				if ppNodes == 0:
					nodeDict[ppNodes].level = 0
				else:
					nodeDict[ppNodes].level = -1
		return(sumOfAllPaths)
	
	return(main())


	
entrances = [0]
exits = [1]
path = [
  [0,0,2,0,0,20],
  [0,0,0,0,0,0],
  [0,0,0,0,20,0],
  [0,0,20,0,0,0],
  [0,20,0,0,0,0],
  [0,0,0,20,0,0]
]

print(solution(entrances,exits,path))
