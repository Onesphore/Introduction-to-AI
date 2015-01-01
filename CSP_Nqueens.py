#----------------------------------------------------------------------------#
#
# [CS470] Introduction to Artificial Intelligence
# 2014 Fall
# Assignment 2-2: Solving the N-Queens Problem as a CSP
#
#----------------------------------------------------------------------------#

import sys
import datetime
from copy import deepcopy

# CSP class
class CSP(object):
	# Constructor for CSP
	def __init__(self, filename):
		self.parseCSP(filename)
	
	def parseCSP(self, filename):
		f = open(filename, 'r')
		variableList = []
		constraintList = []
		
		for line in f:
			line = line.replace('(', '')
			line = line.replace(')', '')
			chars = line.split()

			if not chars:
				continue
			
			if chars[0] == 'variable':
				name = str(chars[1])
				values = [] 
				for i in range(2, len(chars)):
					values.append(int(chars[i]))
				variableList.append(Variable(name, values))
			elif chars[0] == 'constraint':
				constraint = str(chars[1])
				val1 = str(chars[2])
				val2 = str(chars[3])
				val3 = str(chars[4])
				constraintList.append(Constraint(constraint, val1, val2, val3))
		
		self.variableList = variableList
		self.constraintList = constraintList

	def getVariableList(self):
		return self.variableList
	def setVariableList(self, _variableList):
		self.variableList = _variableList     
	def getConstraintList(self):
		return self.constraintList
	def setConstraintList(self, _constraintList):
		self.constraintList = _constraintList

	def printVariableList(self):
		for variable in self.variableList:
			name = variable.getName()
			values = variable.getValues()
			sys.stdout.write('variable %s ' % (name))
			for value in values:
				sys.stdout.write('%d ' % (value))
			sys.stdout.write('\n')

	def printConstraintList(self):
		for constraint in self.constraintList:
			ct = constraint.getConstraint()
			val1 = constraint.getVal1()
			val2 = constraint.getVal2()
			val3 = constraint.getVal3()
			sys.stdout.write('constraint %s %s %s %s' % (ct, val1, val2, val3))
			sys.stdout.write('\n')

# Variable class for storing variable line
class Variable(object):
	def __init__(self, _name, _values):
		self.name = _name
		self.values = _values

	# properties
	def setName(self, _name):
		self.name = _name
	def setValues(self, _values):
		self.values = _values
	def getValues(self):
		return self.values
	def getName(self):
		return self.name

	def __str__(self):
		return self.name + ': ' + str(self.values)

# Constraint class for storing constraint line
class Constraint(object):
	def __init__(self, _constraint, _val1, _val2, _val3):
		self.constraint = _constraint
		self.val1 = _val1
		self.val2 = _val2
		self.val3 = _val3
	
	# properties
	def setConstraint(self, _constraint):
		self.constraint = _constraint
	def setVal1(self, _val1):
		self.val1 = _val1
	def setVal2(self, _val2):
		self.val2 = _val2
	def setVal3(self, _val3):
		self.val3 = _val3
	def getConstraint(self):
		return self.constraint
	def getVal1(self):
		return self.val1
	def getVal2(self):
		return self.val2
	def getVal3(self):
		return self.val3

	def __str__(self):
		return self.constraint + ': ' + self.val1 + ', ' + self.val2 + ', ' + self.val3

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Complete these funtions.
# You may also modify the other parts of the given program, if necessary,
# but please report to your changes in this case.
#----------------------------------------------------------------------------#

# Make .txt file of N-Queens Problem.
# Input:	{n: 'int'}
# Output:	void
def makeNQueensCSPFile(n):

    cspFile = open('CSP_Nqueens.txt', 'w')

    vLis = list(range(1,n+1))
    variables = str(vLis).strip('[]').replace(',','')
    for i in range(1, n+1):
        cspFile.write ("(variable r%s (%s)\n" % (str(i), variables))



    # writing constraints
    for i in range(1,n+1):
        for k in range (i, n+1):
            if k == i:
                continue
            cspFile.write("(constraint diffneq r%s r%s 0)\n" % (str(i), str(k)))

    for i in range(1,n+1):
        for k in range (i, n+1):
            if k == i:
                continue
            cspFile.write("(constraint diffneq r%s r%s %s)\n" % (str(i), str(k), str(abs(i-k))))

    cspFile.close()






# CSP solver 1 which using Backtracking
# Input:	{csp: 'CSP', assignment: 'list'}
# Output:	'list' or 'bool'
def CSPSolver1(csp, assignment):

    if isComplete(csp, assignment):
        return assignment

    var = selectUnassignedVar(csp, assignment)


    number = csp.getVariableList().index(var)
    for i in var.getValues():

        if isConsistent(csp, assignment, var, i):

            assignment[number] = i
            #print i
            result = CSPSolver1(csp, assignment)
            if not (result == False):
                return result


        assignment[number] = 0
    return False




# CSP solver 2 which using MRV heuristic and Forward checking
# Input:	{csp: 'CSP', assignment: 'list'}
# Output:	'list' or 'bool'
def CSPSolver2(csp, assignment):

	### Implement MRV heuristic and Forward checking algorithm.
	### You can refer textbook.

	### Begin your code.
    if isComplete(csp, assignment):
        return assignment

    var = MRV(csp,assignment)
    varDomain = var.getValues()
    varIndex = csp.getVariableList().index(var)


    for i in varDomain:
        copy = deepcopy(varDomain)

        copy.remove(i)

        #varDomainCopy = deepcopy(copy)
        if isConsistent(csp, assignment, var, i):

            assignment[varIndex] = i



            cspCopy = deepcopy(csp)


            for variable in range(len(cspCopy.getVariableList())):
                k = cspCopy.getVariableList()[variable]
                variableCopy = deepcopy(k)

                for val in range(len(k.getValues())):
                    if not isConsistent(cspCopy, assignment, k, k.getValues()[val]):
                        variableCopy.getValues().remove(k.getValues()[val])

                cspCopy.getVariableList()[variable]= deepcopy(variableCopy)

            success = True
            for variable in cspCopy.getVariableList():
                if not len(variable.getValues()):
                    success = False

                    break





            if success:

                result = CSPSolver2(cspCopy, assignment)
                if not (result == False):
                    return result

            assignment[varIndex] = 0


    return False





#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Use these funtions, if you want.
# It is not mandatory to use these.
#----------------------------------------------------------------------------#

# Check whether given assignment is complete.
# Input:	{csp: 'CSP', assignment: 'list'}
# Output:	'bool'
def isComplete(csp, assignment):	
    for i in assignment:
        if i == 0:
            return False
    return True

# Select unassigned variable in assignment.
# Input:	{csp: 'CSP', assignment: 'list'}
# Output:	'Variable'
def selectUnassignedVar(csp, assignment):
    for i in range(len(assignment)):
        if assignment[i] == 0:
            return csp.getVariableList()[i]

    return None

# Check whether given assigning is consistent with consistants.
# Input:	{csp: 'CSP', assignment: 'list', var: 'Variable', val: 'int'}
# Output:	'bool'
def isConsistent(csp, assignment, var, val):
    for i in range(len(assignment)):
        if assignment[i]!=0:
            x = csp.getVariableList()[i].getName()
            y = var.getName()

            for j in csp.getConstraintList():
                if (j.getVal1() == x and j.getVal2() == y):
                    if int (j.getVal3()) == abs(val-assignment[i]):
                        return False
                if (j.getVal2() == x and j.getVal1() == y):
                    if int (j.getVal3()) == abs(val-assignment[i]):
                        return False

    return True

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# You can make your own functions here.
#----------------------------------------------------------------------------#

### Begin your code.

def MRV(csp, assignment):


    for i in range(len(assignment)):
        if assignment[i] == 0:
            mrv = csp.getVariableList()[i]
            for variable in csp.getVariableList():
                if assignment[csp.getVariableList().index(variable)] == 0:
                    if len(variable.getValues())< len(mrv.getValues()):
                        mrv = variable

            break






    return mrv



#----------------------------------------------------------------------------#

# Display the figure of N-Queens Problem
# Input:	{assignment: 'list', n: 'int'}
# Output:	void
def displayNQueens(assignment, n):
	for i in range(n):
		for j in range(n):
			if j == assignment[i] - 1:
				print '1 ',
			else:
				print '0 ',
		print '\n'

# Verify given assignment is the correct answer for N-Queens Problem.
# Input:	{assignment: 'list', n: 'int'}
# Output:	'bool'
def verifyNQueens(assignment, n):
	for i in range(n):
		for j in range(i + 1, n):
			if assignment[i] == assignment[j]:
				return False
			if abs(assignment[i] - assignment[j]) == j - i:
				return False
	return True

#----------------------------------------------------------------------------#

def main():
	# Choose the size of n.
	if len(sys.argv) == 1:
		n =8
	else:
		n = int(sys.argv[1])

	# Make '.txt' file of N-Queens Problem.
	makeNQueensCSPFile(n)

	# Create N-Queens CSP object
	nQueensCSP = CSP('CSP_Nqueens.txt')

	#------------------------------------------------------------------------#
	# CSP solver 1 - Backtracking
	#------------------------------------------------------------------------#
	print 'CSP solver 1 - Backtracking\n'

	assignment = [0 for i in range(n)]

	tStart = datetime.datetime.now()
	
	CSPSolver1(nQueensCSP, assignment)

	timeElapsed = datetime.datetime.now() - tStart

	displayNQueens(assignment, n)

	if verifyNQueens(assignment, n):
		print 'Correct answer!'
	else:
		print 'Wrong asnwer!'

	print('Running time: %d secs.\n' % timeElapsed.seconds)

	#------------------------------------------------------------------------#
	# CSP solver 2 - MRV heuristic and Forward checking
	#------------------------------------------------------------------------#
	print 'CSP solver 2 - MRV heuristic and Forward checking\n'

	assignment = [0 for i in range(n)]

	tStart = datetime.datetime.now()
	
	CSPSolver2(nQueensCSP, assignment)

	timeElapsed = datetime.datetime.now() - tStart

	displayNQueens(assignment, n)
	
	if verifyNQueens(assignment, n):
		print 'Correct answer!'
	else:
		print 'Wrong asnwer!'

	print('Running time: %d secs.\n' % timeElapsed.seconds)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
	main()
