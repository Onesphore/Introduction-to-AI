
import ply.lex as lex
import ply.yacc as yacc

from itertools import combinations # this import was introduced
import copy # this import was introduced

tokens = ('TRUE', 'FALSE', 'SYMBOL', 'LPARENTHESIS', 'RPARENTHESIS', 'NEGATION', 'AND', 'OR', 'IMPLICATION', 'BICONDITION');

t_TRUE = 'True';
t_FALSE = 'False';
t_SYMBOL = r'[_a-zA-Z][_a-zA-Z0-9]*';
t_LPARENTHESIS = r'\(';
t_RPARENTHESIS = r'\)';
t_NEGATION = r'!';
t_AND = r'&';
t_OR = r'\|';
t_IMPLICATION = r'=>';
t_BICONDITION = r'<=>';
t_ignore = ' \t\n'

def t_error(t):
    print "error: illegal character '" + t.value[0] + "' in line '%s'" % t.lexer.lexdata;
    raise SyntaxError;

def p_expression_bicondition(p):
    '''expression_bicondition : expression_bicondition BICONDITION expression_implication
                              | expression_implication'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[1].parent = p[3].parent = p[0] = Tree();
        p[0].content = p[2];
        p[0].leftChild = p[1];
        p[0].rightChild = p[3];
        p[0].isBinaryOperator = True;

def p_expression_implication(p):
    '''expression_implication : expression_implication IMPLICATION expression_or
                              | expression_or'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[1].parent = p[3].parent = p[0] = Tree();
        p[0].content = p[2];
        p[0].leftChild = p[1];
        p[0].rightChild = p[3];
        p[0].isBinaryOperator = True;

def p_expression_or(p):
    '''expression_or : expression_or OR expression_and
                     | expression_and'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[1].parent = p[3].parent = p[0] = Tree();
        p[0].content = p[2];
        p[0].leftChild = p[1];
        p[0].rightChild = p[3];
        p[0].isBinaryOperator = True;

def p_expression_and(p):
    '''expression_and : expression_and AND expression_negation
                      | expression_negation'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[1].parent = p[3].parent = p[0] = Tree();
        p[0].content = p[2];
        p[0].leftChild = p[1];
        p[0].rightChild = p[3];
        p[0].isBinaryOperator = True;

def p_expression_negation(p):
    '''expression_negation : NEGATION expression_negation
                           | expression_factor'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[2].parent = p[0] = Tree();
        p[0].content = p[1];
        p[0].rightChild = p[2];
        p[0].isUnaryOperator = True;

def p_expression_factor(p):
    '''expression_factor : SYMBOL
                         | TRUE
                         | FALSE
                         | LPARENTHESIS expression_bicondition RPARENTHESIS'''
    if len(p) == 2:
        p[0] = Tree();
        p[0].isOperand = True;
        p[0].content = p[1];
    else:
        p[0] = p[2];

def p_error(p):
    print "error: illegal grammar in line '%s'" % lexer.lexdata;
    raise SyntaxError;

lexer = lex.lex();
parser = yacc.yacc();

# Clause class
class Clause:
    # Attributes of an instance of the Clause class (look at the constructor)
    # 1. __literals; A set of literals (private).
    #	A literal is represented as a string such as "A", "!B", and so on.
    #	If __literals = {"a", "b", "!c"},
    #		then it means "a | b | !c".

    # Constructor for Clause
    def __init__(self):
        self.__literals = set();

    # Overloading operator "toString"
    # If __literals = {"a", "b", "!c"},
    #	then the return value is "a | b | !c".
    def __str__(self):
        if len(self.__literals) > 0:
            str = '';
            for literal in self.__literals:
                str += literal + '|'
            return (str[0:len(str) - 1]);
        else:
            return ('');

    # Overloading operator "=="
    def __eq__(self, other):
        if len(self.__literals) != len(other.__literals):
            return (False);
        for literal in self.__literals:
            if literal not in other.__literals:
                return (False);
        return (True);

    # Overloading operator "!="
    def __ne__(self, other):
        if len(self.__literals) != len(other.__literals):
            return (True);
        for literal in self.__literals:
            if literal not in other.__literals:
                return (True);
        return (False);

    # Overloading operator "+, +="
    def __add__(self, other):
        clause = Clause();
        for literal in self.__literals:
            clause.addLiteral(literal);
        for literal in other.__literals:
            clause.addLiteral(literal);
        return (clause);

    # Overloading operator "abs()"
    # Return the size of __literals
    def __abs__(self):
        return (len(self.__literals));

    # Check whether a literal is already in __literals
    # If a given literal isn't in __literals,
    #	then return True.
    # Otherwise, return False.
    # input : literal:String
    # output: a boolean value
    def contains(self, literal):
        return (literal in self.__literals);

    # Add a literal
    # If a given literal isn't in __literals,
    #	then add the literal to __literals and return True.
    # Otherwise, return False and do nothing.
    # input : literal:String
    # output: a boolean value
    def addLiteral(self, literal):
        if self.contains(literal):
            return (False);
        else:
            self.__literals.add(literal);
            return (True);

	# Remove a literal
    # If a given literal is in __literals,
    #	then remove the literal from __literals and return True.
    # Otherwise, return False and do nothing.
    # input : literal:String
    # output: a boolean value
    def removeLiteral(self, literal):
        if self.contains(literal):
            self.__literals.remove(literal);
            return (True);
        else:
            return (False);

    # Return __literals
    # input : none
    # output: a set of strings (= a set of literals)
    def getLiterals(self):
        return (self.__literals);

    # input : none
    # output: a boolean value
    def isEmpty(self):
        return (True if abs(self) == 0 else False);

# CNF class
class CNF:
    # Attributes of an instance of the CNF class (look at the constructor)
    # 1. __clauses; A list of clauses (private).
    #	If __clauses = {clause1, clause2, clause3},
    #		then it means "(clause1) & (clause2) & (clause3)".

    # Constructor for CNF
    def __init__(self):
        self.__clauses = list();
        
    # Overloading operator "toString"
    # If __clauses = {clause1, clause2, clause3},
    #	then the return value is "(clause1) & (clause2) & (clause3)".
    def __str__(self):
        if len(self.__clauses) > 0:
            str = '(' + self.__clauses[0].__str__() + ')';
            for i in range(1, len(self.__clauses)):
                str += '&(' + self.__clauses[i].__str__() + ')';
            return (str);
        else:
            return '';

    # Overloading operator "+, +="
    def __add__(self, other):
        cnf = CNF();
        for clause in self.__clauses:
            cnf.addClause(clause);
        for clause in other.__clauses:
            cnf.addClause(clause);
        return (cnf);

    # Overloading operator "abs()"
    def __abs__(self):
        return (len(self.__clauses));
    
    # Check whether a clause is already in __clauses
    # If a given clause isn't __clauses,
    #	then return True.
    # Otherwise return False.
    # input : clause:Clause
    # output: a boolean value
    def contains(self, clause_):
        for clause in self.__clauses:
            if clause == clause_:
                return (True);
        return (False);

    # Add a clause
    # If an given clause isn't in __clauses,
    #	then add the clause into __clauses and return True.
    # Otherwise, return False and do nothing.
    # input : clause:Clause
    # output: a boolean value
    def addClause(self, clause):
        if self.contains(clause):
            return (False);
        else:
            self.__clauses.append(clause);
            return (True);

    # Return __clauses[idx]
    # input : idx:Integer
    # output: an instance of __clauses class
    def getClause(self, idx):
        return (self.__clauses[idx]);

    # Return __clauses
    # input : none
    # output: a list of instances of __clauses class
    def getClauses(self):
        return (self.__clauses);

    # input : none
    # output: a boolean value
    def isEmpty(self):
        return (True if abs(self) == 0 else False);
        
# Class for parse tree
# This data structure results from parsing a logic statement.
# Each instance of this class represents a sub-tree as well as a tree node.
# This data structure also represents a logic statement guaranteeing operator precedences.
class Tree:
    # Attributes of an instance of the Tree class (look at the constructor)
    # 1. content; The content (public).
    # 	If the current node stands for an operator,
    #		then the content is an operator such as "=>".
    #	Otherwise, the content is an operand such as "a".
    # 2. parent; The parent node (public).
    #	If the current node stands for the root of a whole tree,
    #		then parent = None.
    # 3. leftChild; The left child node (public).
    #	If the current node stands for an unary operator or operand,
    #		then leftChild = None.
    # 4. rightChild; The right child node (public).
    #	If the current node stands for an operand,
    #		then rightChild = None.
    # 5. isBinaryOperator; A flag to check whether the current node stands for a binary operator (public).
    # 6. isUnaryOperator; A flag to check whether the current node stands for an unary operator (public).
    # 7. isOperand; A flag to check whether the current node stands for an operand (public).

    # Constructor for Tree
    def __init__(self):
        self.content = '';
        self.parent = self.leftChild = self.rightChild = None;
        self.isBinaryOperator = self.isUnaryOperator = self.isOperand = False;

    # Overloading operator "toString"
    # Returns the sub-graph considering the current node as the root in a string form.
    # The returned string is exactly same to the original logic statement except for some additional parentheses that represent operator precedences explicitly.
    def __str__(self):
        str = '';
        if self.leftChild != None:
            str += '(' + self.leftChild.__str__() + ')';
        str += self.content;
        if self.rightChild != None:
            str += '(' + self.rightChild.__str__() + ')';
        return (str);

    # Replicate itself.
    # input : none
    # output: an instance of the Tree class
    def copy(self):
        newNode = Tree();
        newNode.content = self.content;
        newNode.parent = self.parent;
        if self.isBinaryOperator:
            newNode.isBinaryOperator = True;
            newNode.leftChild = self.leftChild.copy();
            newNode.rightChild = self.rightChild.copy();
        elif self.isUnaryOperator:
            newNode.isUnaryOperator = True;
            newNode.rightChild = self.rightChild.copy();
        else:
            newNode.isOperand = True;
        return (newNode);

# Negate an given tree by creating a new root which represents a negation operator and whose right child is the previous root.
# input : tree:Tree
# output: an instance of the Tree class
def negate(tree):
    tree.parent = root = Tree();
    root.content = "!";
    root.isUnaryOperator = True;
    root.rightChild = tree;
    return (root);

# Check whether an given clause is always True.
#	If so, the clause is not helpful in resolution.
# If the clause is always True,
#	then return True.
# Otherwise, return False.
# input : clause:Clause
# output: an boolean value
def isAlwaysTrue(clause):
    for i in clause.getLiterals():
        for j in clause.getLiterals():
            if (i != j) and ((j[0] == '!' and i == j[1:])or (i[0]=="!" and i[1:] == j)):
                return True

    for i in clause.getLiterals():
        if i == 'True' or i == '!False':
            return True

    return False



def resolveBiconditions(node):

    new = node.copy()
    if node.isUnaryOperator:
        node.rightChild = resolveBiconditions(node.rightChild)

    elif node.isBinaryOperator:
        node.leftChild = resolveBiconditions(node.leftChild)
        node.rightChild = resolveBiconditions(node.rightChild)

        if node.content == "<=>":
            node.content = "=>"


            leftChild = node

            rightChild = node.copy()


            temp = rightChild.leftChild

            rightChild.leftChild = rightChild.rightChild
            rightChild.rightChild = temp


            new.content = "&"
            new.isBinaryOperator = True
            new.leftChild = leftChild
            new.rightChild = rightChild
            new.parent = leftChild.parent

            leftChild.parent = new
            rightChild.parent = new
    else:
        pass


    return new


#I defined 2 other functions to help me define convertIntoCNF. And those are convertIntoCNF1, convertIntoCNF2

def convertIntoCNF(tree):
    cnf1 = convertIntoCNF2(tree)
    cnf = CNF()


    List  = []
    clausesInStrings = cnf1.__str__().split("&")
    for i in clausesInStrings:
        List.append(i.replace("(", "").replace(")", ""))

    for i in List:
        cl = Clause()
        for k in i.split("|"):
            cl.addLiteral(k)
        cnf.addClause(cl)

    return cnf

def convertIntoCNF2(tree):
    cnf1 = CNF()
    tree = convertIntoCNF1(tree)

    if tree.content == "&":
        if tree.rightChild.content != "&":
            c =  tree.rightChild.copy()

            cnf1.addClause(c)
        else:
            for i in (convertIntoCNF2(tree.rightChild)).getClauses():
                cnf1.addClause(i)

        if tree.leftChild.content != "&":
            c =  tree.leftChild.copy()
            cnf1.addClause(c)
        else:
            for i in (convertIntoCNF2(tree.leftChild)).getClauses():
                cnf1.addClause(i)

    elif tree.content == "|":
        cnf1.addClause(tree)

    elif tree.isOperand or (tree.isUnaryOperator and tree.rightChild.isOperand):
        cnf1.addClause(tree)
    return cnf1


def convertIntoCNF1(tree):


    tree = resolveBiconditions(tree)
    if tree.isUnaryOperator:
        if tree.rightChild.isUnaryOperator:
            tree = convertIntoCNF1(tree.rightChild.rightChild)


        elif tree.rightChild.isBinaryOperator:
            left = tree.rightChild.leftChild.copy()
            right = tree.rightChild.rightChild.copy()

            if tree.rightChild.content == "&":
                tree.parent = root = Tree()
                root.content = "|"
                root.isBinaryOperator = True
                root.rightChild = convertIntoCNF1(negate(right))
                root.leftChild = convertIntoCNF1(negate(left))
                tree = root

            elif tree.rightChild.content == "|":
                tree.parent = root = Tree()
                root.content = "&"
                root.isBinaryOperator = True
                root.rightChild = convertIntoCNF1(negate(right))
                root.leftChild = convertIntoCNF1(negate(left))
                tree = root

            elif tree.rightChild.content == "=>":

                tree.parent = root = Tree()
                root.content = "&"
                root.isBinaryOperator = True
                root.rightChild = convertIntoCNF1(negate(right))
                root.leftChild = convertIntoCNF1(left)
                tree = root

    if tree.isBinaryOperator:
        if tree.content == "|" and tree.rightChild.content == "&":
            tree.parent = root = Tree()
            root.content = "&"

            treec1 = tree.rightChild.copy()
            treec2 = tree.rightChild.copy()
            root.rightChild = treec1
            root.leftChild = treec2
            root.rightChild.content = "|"
            root.leftChild.content = "|"

            root.rightChild.leftChild = tree.leftChild
            root.rightChild.rightChild = tree.rightChild.rightChild

            root.leftChild.leftChild = tree.leftChild
            root.leftChild.rightChild = tree.rightChild.leftChild


            root.isBinaryOperator = True

            root.rightChild = convertIntoCNF1(root.rightChild)
            root.leftChild = convertIntoCNF1(root.leftChild)

            tree = root


        elif tree.content == "|" and tree.leftChild.content == "&":
            tree.parent = root = Tree()
            root.content = "&"

            treeCopy1 = tree.leftChild.copy()
            treeCopy2 = tree.leftChild.copy()
            root.rightChild = treeCopy1
            root.leftChild = treeCopy2
            root.rightChild.content = "|"
            root.leftChild.content = "|"

            root.leftChild.leftChild = tree.leftChild.leftChild
            root.leftChild.rightChild = tree.rightChild

            root.rightChild.leftChild = tree.leftChild.rightChild
            root.rightChild.rightChild = tree.rightChild

            root.isBinaryOperator = True

            root.rightChild = convertIntoCNF1(root.rightChild)
            root.leftChild = convertIntoCNF1(root.leftChild)

            tree = root
        elif tree.content == "=>":
            tree.content = "|"
            tree.leftChild = negate(tree.leftChild)


        else:
            tree.leftChild = convertIntoCNF1(tree.leftChild)
            tree.rightChild = convertIntoCNF1(tree.rightChild)

        tree.leftChild = convertIntoCNF1(tree.leftChild)
        tree.rightChild = convertIntoCNF1(tree.rightChild)


    return tree






def proveByResolution(queryTree, kb):

    NegQueryTreeInNCF = convertIntoCNF(negate(queryTree))
    for i in NegQueryTreeInNCF.getClauses():
        if not isAlwaysTrue(i):
            kb.addClause(i)

    #removing tautology in kb
    clauses = CNF()
    for i in kb.getClauses():
        if not isAlwaysTrue(i):
            clauses.addClause(i)

    new = CNF()




    while 1:

        clausesCopy = copy.deepcopy(clauses)

        for i, j in combinations(clausesCopy.getClauses(), 2):



            iCopy = copy.deepcopy(i)
            jCopy = copy.deepcopy(j)

            resolvents = CNF()
            for k in list(iCopy.getLiterals()):

                for l in list (jCopy.getLiterals()):
                    if (k[0] == "!" and k[1:] == l) or (k == l[1:] and l[0] == "!"):
                        iCopyCopy = copy.deepcopy(iCopy)
                        jCopyCopy = copy.deepcopy(jCopy)
                        iCopyCopy.removeLiteral(k)
                        jCopyCopy.removeLiteral(l)
                        c = merge(iCopyCopy, jCopyCopy)


                        if not clausesCopy.contains(c):
                            resolvents.addClause(c)
                    else:
                        pass

            for ch in resolvents.getClauses():
                    if ch.isEmpty():
                        return True


            for cl in resolvents.getClauses():
                new.addClause(cl)

        contains = True
        for i in new.getClauses():
            if clauses.contains(i):
                pass
            elif not clauses.contains(i):
                contains = False
                clauses.addClause(i)
        if contains:
            return False


def merge(ci, cj):
    cjCopy = copy.deepcopy(cj)
    for i in ci.getLiterals():
        cjCopy.addLiteral(i)
    return cjCopy






    #----------------------------------------------------------------------------#

# initialize the KB from an input file
# input : kb:CNF, fileName:String
# output: an instance of the CNF class
def initializeKB(kb, fileName):
    true = Clause();
    true.addLiteral('True');
    kb.addClause(true);
    notFalse = Clause();
    notFalse.addLiteral('!False');
    kb.addClause(notFalse);

    file = open(fileName, 'r');
    for line in file.readlines():
        line = line.strip();
        if len(line) > 0:
            try:
                tree = parser.parse(line);
            except SyntaxError:
                break;
            cnf = convertIntoCNF(tree);
            #----------------------------------------------------------------------------#
            # After solving Question 2.C, uncomment the line below.
            kb += cnf;
            #----------------------------------------------------------------------------#
    file.close();
    return (kb);


#----------------------------------------------------------------------------#
# Question 2.A
#----------------------------------------------------------------------------#
clause = Clause();
clause.addLiteral('True');
clause.addLiteral('!False');
clause.addLiteral('A');
clause.addLiteral('B');
clause.addLiteral('C');
clause.addLiteral('!A');
result = isAlwaysTrue(clause);
print "Question 2.A)";
print '\t', result;


#----------------------------------------------------------------------------#
# Question 2.B
#----------------------------------------------------------------------------#
file = open('input.txt', 'r');
line = file.readline().strip();
file.close();
tree = parser.parse(line);
tree = resolveBiconditions(tree);
print 'Question 2.B)';
print '\t', tree;



#----------------------------------------------------------------------------#
# Qeustion 2.C
#----------------------------------------------------------------------------#
file = open('input.txt', 'r');
line = file.readline().strip();
file.close();
tree = parser.parse(line);
cnf = convertIntoCNF(tree);
print 'Question 2.C)';
print '\t', cnf;



#----------------------------------------------------------------------------#
# Question 2.D
#----------------------------------------------------------------------------#
kb = CNF();
kb = initializeKB(kb, 'input.txt');
print "Question 2.D)";
print '\t', kb;
query = '!P12';
try:
    queryTree = parser.parse(query);
    result = proveByResolution(queryTree, kb);
    print '\t', result;
except SyntaxError:
    pass
