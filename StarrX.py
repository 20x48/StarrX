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
        exit('Invalid syntax at position {}: Too much SPACE that unknown opcode.'.format(index))
    elif code==3:
        exit('Invalid operate at position {}: Nothing could be INDEXED or POPUP.'.format(index))
    elif code==4:
        exit('Invalid operate at position {}: LABEL not found.'.format(index))
    elif code==5:
        exit('Invalid operate at position {}: Divide by ZERO.'.format(index))
    elif code==6:
        exit('Invalid operate at position {}: Unsupported OPERAND.'.format(index))
    elif code==7:
        exit('Invalid INPUT by user at position {}.'.format(index))
    elif code==8:
        exit('Invalid CODE at position {}.'.format(index))



allowSign=list("*+-,.'^`")

findInt=re.compile(r'[\-\d]+')
findFloat=re.compile(r'[\-\d]+\.\d+')
findString=re.compile(r'([ ]+)".*?\1"',re.S)

pointer=0
pointed=0
labels={}
elements=[]

index=-1
counter=0
counted=0



try:
    while index<len(code):
        index+=1
        sign=code[index]

        if sign==' ':
            counter+=1

        elif sign in allowSign:
            # Checking the space.
            if counter==0:
                xExit(index,1)

            # Operating about elements.
            if sign=='*':
                if counter<=2:
                    if counted==0:
                        counted=counter
                        counter=0
                        continue
                    elif counted<=2:
                        pointed=pointer
                        if counted==1 and counter==1:
                            pointer=len(elements)-1
                        elif counted==2 and counter==1:
                            pointer=min(pointer+1,len(elements)-1)
                        elif counted==1 and counter==2:
                            pointer=max(pointer-1,0)
                        elif counted==2 and counter==2:
                            pointer=0
                        counted=0
                        counter=0
                    else:
                        xExit(index,2)
                elif counter<=6:
                    if counter==3:
                        f=findInt.match(code,index+1)
                        if f is None:
                            f=findFloat.match(code,index+1)
                            if f is None:
                                f=findString.match(code,index+1)
                                if f is None:
                                    xExit(index,8)
                                else:
                                    spaces=f.find('"')
                                    elements.insert(pointer,f.group()[spaces+1:-spaces-1])
                            else:
                                elements.insert(pointer,float(f.group()))
                        else:
                            elements.insert(pointer,int(f.group()))
                        pointed+=(0 if pointed<pointer else 1)
                        pointer+=1
                        index=f.end()-1
                    elif counter==4:
                        pointed=pointer
                        elements[pointer],elements[-1]=elements[-1],elements[pointer]
                    elif counter==5:
                        elements.append(elements[pointer])
                    elif counter==6:
                        elements.pop(pointer)
                        pointed-=(0 if pointed<pointer else 1)
                        pointer-=1
                    counter=0
                else:
                    xExit(index,2)

            # Operating about calculation and rounding.
            elif sign=='+':
                if counter<=1:
                    if counted==0:
                        counted=counter
                        counter=0
                        continue
                    elif counted<=3:
                        if counted==1:
                            elements[pointer]=floor(elements[pointer])
                        elif counted==2:
                            elements[pointer]=round(elements[pointer])
                        elif counted==3:
                            elements[pointer]=ceil(elements[pointer])
                        counted=0
                        counter=0
                    else:
                        xExit(index,2)
                elif counter<=7:
                    if counter==2:
                        elements[pointer]+=elements[-1]
                    elif counter==3:
                        elements[pointer]-=elements[-1]
                    elif counter==4:
                        elements[pointer]*=elements[-1]
                    elif counter==5:
                        elements[pointer]/=elements[-1]
                    elif counter==6:
                        elements[pointer]%=elements[-1]
                    elif counter==7:
                        elements[pointer]**=elements[-1]
                    counter=0
                else:
                    xExit(index,2)
            
            # Operating about relationship.
            elif sign=='-':
                if counter<=3:
                    if counted==0:
                        counted=counter
                        counter=0
                        continue
                    elif counted<=3:
                        if counted==1 and counter==1:
                            elements.append(int(elements[pointer]==elements[-1]))
                        elif counted==2 and counter==2:
                            elements.append(int(elements[pointer]!=elements[-1]))
                        elif counted==1 and counter==2:
                            elements.append(int(elements[pointer]<elements[-1]))
                        elif counted==1 and counter==3:
                            elements.append(int(elements[pointer]<=elements[-1]))
                        elif counted==2 and counter==1:
                            elements.append(int(elements[pointer]>elements[-1]))
                        elif counted==3 and counter==1:
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
                    if counter==1:
                        elements.insert(pointer,int(input('Input an integer: ')))
                    elif counter==2:
                        elements.insert(pointer,float(input('Input a float: ')))
                    elif counter==3:
                        elements.insert(pointer,input('Input a string: '))
                    pointer+=1
                    counter=0
                else:
                    xExit(index,2)

            # Output
            elif sign=='.':
                if counter<=2:
                    print(elements[pointer],end=('\n' if counter==1 else ''))
                    counter=0
                else:
                    xExit(index,2)

            # Make one label.
            elif sign=="'":
                labels[counter]=index+1
                counter=0

            # Goto label.
            elif sign=='^':
                if elements[pointer].pop():
                    index=labels[counter]
                counter=0
            
            # Un-move the pointer.
            elif sign=='`':
                pointer,pointed=pointed,pointer
                counter=0
except IndexError:
    xExit(index,3)
except KeyError:
    xExit(index,4)
except ZeroDivisionError:
    xExit(index,5)
except TypeError:
    xExit(index,6)
except ValueError:
    xExit(index,7)
except KeyboardInterrupt:
    xExit(index,0)