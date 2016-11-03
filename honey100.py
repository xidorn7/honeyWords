#! /usr/local/bin/python
# honey100.py
#
#
# Course: Privacy and Privacy Concepts in the Wild :
# Assignment #3: Honey word generation based on the top 100 Rock You passwords
# Group:  Suzie-May Ogunseitan, Jillian Sue, Xi Yu, Junbin Sun
#
# 
# Usage: python honey100.py n f1 f2
#        
# where    n = number of passwords desired [optional; default = 19]
#          f1 is the input password files
#          f2 is the name of the desired output file
#       NOTE: The program outputs n passwords per line to match line by line the input password (list)
#
#     Should run OK with python 2.7 (including pypy) and python 3.5
#
# This version of the program does not implement any password-composition restrictions,
# such as a minimum-length on passwords as none were specified in the assignment specifications
#
#   
#
#  
##############################################################################
#### PARAMETERS CONTROLLING PASSWORD GENERATION (aside from password files)

# probabilities p1, p2, p3 add up to 1 (heuristically chosen)
p1 = 0.10            # chance of a "random" char at this position (see code)
p2 = 0.40            # chance of a markov-order-1 char at this position (see code)
p3 = 0.50            # choice of continuing copying from same word


# syntax parameters for a password
nL = 0               # password must have at least nL letters
nD = 0               # password must have at least nD digit
nS = 0               # password must have at least nS special (non-letter non-digit)

#### END OF PARAMETERS CONTROLLING PASSWORD GENERATION


#Reference: password generation program (intended for generating ``honeywords'') by Ronald L. Rivest and Ari Juels
##############################################################################

import random
import sys
import string


# A short list of high-probability passwords that is used to initialize the
# password list in case no password files are provided.

#rock_you=""


rock_you = []


#if file not in the same folder, please enter path to file
PATH_TO_FILE = 'rockyou100.txt'

lines = open(PATH_TO_FILE,"r").readlines()
for line in lines:
    rock_you.extend( line.split() )



def read_password_files(filenames):
    """ 
    Return a list of passwords in all the password file
    """
    pw_list = [ ]
    if len(filenames) > 0:
        lines = open(filenames,"r").readlines()
        for line in lines:
            pw_list.extend( line.split() )
   
    
    return pw_list



def syntax(p):
    """
    Return True if password p contains at least nL letters, nD digits, and nS specials (others)
    """
    global nL, nD, nS
    L = 0
    D = 0
    S = 0
    for c in p:
        if c in string.ascii_letters:
            L += 1
        elif c in string.digits:
            D += 1
        else:
            S += 1
    if L >= nL and D >= nD and S >= nS:
        return True
    return False
    
    
def make_similar(iPwd):
    
    # sPwd = fraction of selected passwords from all possible passwords meeting criteria
    # could also randomize later
    #sPwd = random.randrange(0,1)

    sPwd = 0.5              
    M=[]
    R = []
    closePwd = []
    L = [pw for pw in rock_you if ((len(pw) == len(iPwd)) and (pw != iPwd))]

    if len(L) < 3:
        for i in range(random.randint(0,20)):
            p = ""
            while len(p) < len(iPwd):
                p += random.choice(rock_you)
            R.append(p)
    
    
    if iPwd.isalnum():
        M = [pw for pw in rock_you if ((pw.isalnum()) and (pw != iPwd))]
    elif iPwd.isdigit():
         M = [pw for pw in rock_you if ((pw.isdigit()) and (pw != iPwd))]
        
    L.extend(M)
    nL = len(L)

    
    if nL > 3:
        choosePwd = int(sPwd * nL)
        
        for i in range(choosePwd):
            p = random.choice(L)
            j = 0
            while (p in closePwd):
                j += 1
                p = random.choice(L)
                if j > len(L)+1:   
                    break
            
            closePwd.append(p)
 
    closePwd.extend(R)
    
    return closePwd
    
def make_randSim():
    L = []
    k = len(random.choice(rock_you))
    # create list of all passwords of length k; we'll only use those in model
    L = [ pw for pw in rock_you if len(pw) == k ]
    return L
    
def make_xpassword():
    """ 
    make a random password like those in given password list
    """

    # start by choosing a random password from the list
    # save its length as k; we'll generate a new password of length k
    k = len(random.choice(rock_you))
    # create list of all passwords of length k; we'll only use those in model
    L = [ pw for pw in rock_you if len(pw) == k ]
    
    nL = len(L)
  
    # start answer with the first char of that random password
    # row = index of random password being used 
    row = random.randrange(nL)
    ans = L[row][:1]                  # copy first char of L[row] 
    j = 1                             # j = len(ans) invariant
    while j < k:                      # build up ans char by char
        p = random.random()           # randomly decide what to do next, based on p
        # here p1 = prob of action 1
        #      p2 = prob of action 2
        #      p3 = prob of action 3
        #      p1 + p2 + p3 = 1.00
        if p < p1:
            action = "action_1"
        elif p < p1+p2:
            action = "action_2"
        else:
            action = "action_3"
        if action == "action_1":
            # add same char that some random word of length k has in this position
            row = random.randrange(nL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_2":
            # take char in this position of random word with same previous char
            LL = [ i for i in range(nL) if L[i][j-1]==ans[-1] ]
            row = random.choice(LL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_3":
            # stick with same row, and copy another character
            ans = ans + L[row][j]
            j = j + 1
    if (nL > 0 or nD > 0 or nS > 0) and not syntax(ans): 
        return make_xpassword(rock_you)
    return ans
    
def generate_passwords(n,pwd):
    """ print n passwords and return list of them """
    ans = [ ]
    ansFin = []
    sim_pw = []


    for t in range( n ):
        pw = make_xpassword()
        ans.append(pw)
        pwd1 = make_similar(pwd)
        pwd2 = make_randSim()
        sim_pw.extend(pwd1)
        sim_pw.extend(pwd2[:(random.randint(0, len(pwd2)))])
        sim_pw.extend(ans)

    for i in range(n):
        if len(ans) > 0:
            p = random.choice(sim_pw)
            j = 0
            while (p in ansFin):
                j += 1
                p = random.choice(sim_pw)
                if j > len(sim_pw)+1:   
                    break
            for bm in range(len(p)):
                if random.random() < 0.1:
                    p = p[:bm] + chr(random.randint(32,48)) + p[bm+1:]
                elif p[bm].isalpha():
                    if random.random() < 0.5:
                        p = p[:bm] + p[bm].upper() + p[bm+1:]
            ansFin.append(p)
 
    return ansFin

def main():
    # get number of passwords desired
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 19
    # read password files
    filenames = sys.argv[2:]           # skip "gen.py" and n   
    outfile = filenames[1]
    pw_list = read_password_files(filenames[0])
    
    # generate passwords
    if len(pw_list) > 0:
        for p in pw_list:
            honeyWords = []
            honeyWords = generate_passwords(n,p)
            
            # shuffle their order
            random.shuffle(honeyWords)    
    
            target = open (outfile, 'a')
            for word in honeyWords:
                if word == honeyWords[-1]:
                    target.write(word + "\n")
                else:
                    target.write(word + ", ")
        target.close()
    

main()


