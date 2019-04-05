# -*- coding: utf-8 -*-
r'''
 __
(_  _|_  _   _  _ \_/
__)  |_ (_| |  |  / \
                                     __    __            __
|  |  _ . _|_ _|_  _  _    |_         _)  /  \    |__|  (__)
|/\| |  |  |_  |_ (- | |   |_) \/    /__  \__/ )(    |  (__)
                               /
'''



from sys import argv
from math import floor,ceil
import re



try:
    with open(argv[1]) as c:
        code=c.read()
except OSError as e:
    print('OS related error: {}'.format(e))
    exit(e)
except IndexError:
    exit('Usage: StarrX.py <file>')
except UnicodeDecodeError as e:
    print('Decode error: {}'.format(e))
    exit('Please check your encoding of code.')
except BaseException as e:
    exit('Unexpected error: {}'.format(e))



def xExit(index,code):
    if code==0:
        exit('Stopped by user when executed at position {}.'.format(index))
    elif code==1:
        exit('Invalid syntax at position {}: Needs at least one SPACE.'.format(index))
    elif code==2:
        exit('Invalid operate at position {}: Too much SPACE that unknown opcode.'.format(index))
    elif code==3:
        exit('Invalid operate at position {}: SIGN not match that unknown opcode.'.format(index))
    elif code==4:
        exit('Invalid operate at position {}: Nothing could be INDEXED or POPUP.'.format(index))
    elif code==5:
        exit('Invalid operate at position {}: LABEL not found.'.format(index))
    elif code==6:
        exit('Invalid operate at position {}: Divide by ZERO.'.format(index))
    elif code==7:
        exit('Invalid operate at position {}: Unsupported OPERAND.'.format(index))
    elif code==8:
        exit('Invalid INPUT by user at position {}.'.format(index))
    elif code==9:
        exit('Invalid CODE at position {}.'.format(index))



def debug(d):
    if debuging:
        print(d)



debuging=False

allowSign=list("*+-,.'^`")

findInt=re.compile(r' +[\-\d]+')
findFloat=re.compile(r' +[\-\d]+\.\d+')
findString=re.compile(r'([ ]+)".*?\1"',re.S)

pointed=None
pointer=None
labels={}
elements=[]

index=-1
counter=0
counted=0

expected=None



try:
    while index<len(code)-1:
        # Basic operate
        index+=1
        sign=code[index]

        # Maintain the pointer.
        if len(elements)==0:
            pointed=None
            pointer=None
        else:
            pointed=min(pointed,len(elements)-1)
            pointed=max(pointed,0)
            pointer=min(pointer,len(elements)-1)
            pointer=max(pointer,0)

        # Debuging.
        if debuging:
            debug('{}  (POINTER: {} ({} Last), Counter: ({},{}), index: {}, sign: {})'.format(elements,pointer,pointed,counted,counter,index,sign))

        # Space counter.
        if sign==' ':
            counter+=1

        # Prefilter.
        elif sign in allowSign:

            # Check the space.
            if counter==0:
                xExit(index,1)

            # Check the expected sign.
            if expected is not None and sign!=expected:
                xExit(index,3)

            # Operating about elements.
            if sign=='*':
                if counter<=2:
                    if counted==0:
                        expected='*'
                        counted=counter
                        counter=0
                        continue
                    elif counted<=2:
                        expected=None
                        if pointer is not None:
                            pointed=pointer
                            # >>
                            if counted==1 and counter==1:
                                debug('* POINTER >>')
                                pointer=len(elements)-1
                            # >
                            elif counted==2 and counter==1:
                                debug('* POINTER >')
                                pointer=min(pointer+1,len(elements)-1)
                            # <
                            elif counted==1 and counter==2:
                                debug('* POINTER <')
                                pointer=max(pointer-1,0)
                            # <<
                            elif counted==2 and counter==2:
                                debug('* POINTER <<')
                                pointer=0
                            counted=0
                            counter=0
                    else:
                        xExit(index,2)
                elif counter<=6:
                    # Insert
                    if counter==3:
                        debug('* INSERT')
                        i=(0 if pointer is None else pointer+1)
                        f=findInt.match(code,index+1)
                        if f is None:
                            f=findFloat.match(code,index+1)
                            if f is None:
                                f=findString.match(code,index+1)
                                if f is None:
                                    xExit(index,9)
                                else:
                                    spaces=f.group().find('"')
                                    elements.insert(i,f.group()[spaces+1:-spaces-1])
                            else:
                                elements.insert(i,float(f.group()))
                        else:
                            elements.insert(i,int(f.group()))
                        # * Maintain the pointer.
                        if pointed is None:pointed=0
                        else:pointed+=(0 if pointed<pointer else 1)
                        if pointer is None:pointer=0
                        else:pointer+=1
                        index=f.end()-1
                    # Swap
                    elif counter==4:
                        debug('* SWAP')
                        pointed=pointer
                        elements[pointer],elements[-1]=elements[-1],elements[pointer]
                    # Copy
                    elif counter==5:
                        debug('* COPY')
                        elements.append(elements[pointer])
                    # Remove
                    elif counter==6:
                        debug('* REMOVE')
                        elements.pop(pointer)
                        # * Maintain the pointer.
                        pointed-=(0 if pointed>pointer else 1)
                        pointer-=1
                    counter=0
                else:
                    xExit(index,2)

            # Operating about calculation and rounding.
            elif sign=='+':
                if counter<=1:
                    if counted==0:
                        expected='+'
                        counted=counter
                        counter=0
                        continue
                    elif counted<=3:
                        expected=None
                        if counted==1:
                            debug('+ Floor')
                            elements[pointer]=floor(elements[pointer])
                        elif counted==2:
                            debug('+ Round')
                            elements[pointer]=round(elements[pointer])
                        elif counted==3:
                            debug('+ Ceil')
                            elements[pointer]=ceil(elements[pointer])
                        counted=0
                        counter=0
                    else:
                        xExit(index,2)
                elif counter<=7:
                    if counter==2:
                        debug('+ Add')
                        elements[pointer]+=elements[-1]
                    elif counter==3:
                        debug('+ Subtract')
                        elements[pointer]-=elements[-1]
                    elif counter==4:
                        debug('+ Multiply')
                        elements[pointer]*=elements[-1]
                    elif counter==5:
                        debug('+ Divide')
                        elements[pointer]/=elements[-1]
                    elif counter==6:
                        debug('+ Modulo')
                        elements[pointer]%=elements[-1]
                    elif counter==7:
                        debug('+ Power')
                        elements[pointer]**=elements[-1]
                    counter=0
                else:
                    xExit(index,2)

            # Operating about relationship.
            elif sign=='-':
                if counter<=3:
                    if counted==0:
                        expected='-'
                        counted=counter
                        counter=0
                        continue
                    elif counted<=3:
                        expected=None
                        if counted==1 and counter==1:
                            debug('- equal')
                            elements.append(int(elements[pointer]==elements[-1]))
                        elif counted==2 and counter==2:
                            debug('- not equal')
                            elements.append(int(elements[pointer]!=elements[-1]))
                        elif counted==1 and counter==2:
                            debug('- greater than')
                            elements.append(int(elements[pointer]<elements[-1]))
                        elif counted==1 and counter==3:
                            debug('- greater than or equal')
                            elements.append(int(elements[pointer]<=elements[-1]))
                        elif counted==2 and counter==1:
                            debug('- less than')
                            elements.append(int(elements[pointer]>elements[-1]))
                        elif counted==3 and counter==1:
                            debug('- less than or equal')
                            elements.append(int(elements[pointer]>=elements[-1]))
                        counted=0
                        counter=0
                    else:
                        xExit(index,2)
                    counter=0
                else:
                    xExit(index,2)

            # Input
            elif sign==',':
                if counter<=3:
                    i=(0 if pointer is None else pointer+1)
                    if counter==1:
                        debug(', input int')
                        elements.insert(i,int(input('Input an integer: ')))
                    elif counter==2:
                        debug(', input float')
                        elements.insert(i,float(input('Input a float: ')))
                    elif counter==3:
                        debug(', input string')
                        elements.insert(i,input('Input a string: '))
                    # * Maintain the pointer.
                    if pointed is None:pointed=0
                    else:pointed+=(0 if pointed<pointer else 1)
                    if pointer is None:pointer=0
                    else:pointer+=1
                    counter=0
                else:
                    xExit(index,2)

            # Output
            elif sign=='.':
                if counter<=2:
                    debug(r". Print {} '\n'".format(('with' if counter==1 else 'without')))
                    print(elements[pointer],end=('\n' if counter==1 else ''))
                    counter=0
                else:
                    xExit(index,2)

            # Create one label.
            elif sign=="'":
                debug("' Create label {}".format(counter))
                labels[counter]=index
                counter=0

            # Goto label.
            elif sign=='^':
                if elements.pop():
                    debug('^ Go to label {}'.format(counter))
                    index=labels[counter]
                else:
                    debug('^ Failed go to label {}'.format(counter))
                counter=0

            # Un-move the pointer.
            elif sign=='`':
                debug('` Un-move POINTER')
                pointer,pointed=pointed,pointer
                counter=0
except IndexError:
    xExit(index,4)
except KeyError:
    xExit(index,5)
except ZeroDivisionError:
    xExit(index,6)
except TypeError:
    xExit(index,7)
except ValueError:
    xExit(index,8)
except KeyboardInterrupt:
    xExit(index,0)



# Debuging.
if debuging:
    debug('LAST STATUS: {}  (POINTER: {} ({} Last), Counter: ({},{}), index: {}, sign: {})'.format(elements,pointer,pointed,counted,counter,index,sign))
