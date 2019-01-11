#!/usr/local/bin/python
####################################### Huffman Coding ################################################
#######################################################################################################

DEBUG = False

## This is the class for making huffman tree
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return "%s_%s" % (self.left, self.right)
#######################################################################################################
## This functions are for the encoding part
    
## Tansverse the NodeTress in every possible way to get codings
def huffmanCodeTree(node, left=True, binString=""):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    #######################################################################################################
    ################################# Exercise 3: Write the code here!#####################################
    #######################################################################################################
    return d
## This function is for computing the compressed string for the input based on the computed huffman codes
def computeCompressedString(iputstr,huffcodes):
    codestr = ''
    for chrs in iputstr:
        
        chrcode = huffcodes.get(chrs)
        print(chrs,chrcode)
        codestr= codestr + chrcode
    return(codestr)
#######################################################################################################
## This functions are for the decoding part

## build  the "reverse" of the  encoding  dictionary """
def  build_decoding_dict(encoding_dict ):
    return {y:x for (x,y) in  encoding_dict.items ()}

## Decompress the input string based on the compressed format of the input
def  decompress(bits , decoding_dict ):
    prefix = ''
    result = []
    for  bit in bits:
        ################################################################################################
        ################################## Exercise 4: Write the code here!#############################
        ################################################################################################
    assert  prefix  == '' # must  finish  last  codeword
    return  ''.join(result)   # converts  list of  chars  to a string

    
#######################################################################################################
## Main part of the code  
## Input String
string = "This is Lab 1!!"

## Compute the frequency of the characters in the input string
freq = {}
#######################################################################################################
################################## Exercise 1: Write the code here!####################################
#######################################################################################################

## Sort the frequency table based on occurrence this will also convert the dict to a list of tuples
#######################################################################################################
################################## Exercise 2: Write the code here!####################################
#######################################################################################################


if DEBUG:
    print(" Char | Freq ")
    for key, c in freq:
        print(" %4r | %d" % (key, c))

nodes = freq

## Encoding: Huffman tree creation
while len(nodes) > 1:
    key1, c1 = nodes[-1]
    key2, c2 = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    # Re-sort the list
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

if DEBUG:
    print("left: %s" % nodes[0][0].nodes()[0])
    print("right: %s" % nodes[0][0].nodes()[1])
## Encoding: Huffman tree binary code creation
huffmanCode = huffmanCodeTree(nodes[0][0])


## Output of Encoding part in the format of a table
print(huffmanCode)
print(" Char | Freq  | Huffman code ")
print("-----------------------------")
for char, frequency in freq:
    print(" %-4r | %5d | %12s" % (char, frequency, huffmanCode[char]))
## Output of the Compressed String 
hufcodestr = computeCompressedString(string,huffmanCode)
print(hufcodestr)

## Decoding
# part 1- "reverse" of the  encoding  dictionary  
decdic = build_decoding_dict(huffmanCode)
print(decdic)
# part 2- Get the decompressed string
print(decompress(hufcodestr,decdic))
