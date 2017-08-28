"""
Basic operations on V-values
(see https://github.com/jsa-aerial/DMM for the original V-value work)

Implemented by 'nekel'.

Done :
- convert a green tree (i.e. a leaf-adorned dictionary)into an instance of V-value
- multiply V-value by a scalar (2 versions: either in-place or a new copy)
- intersection and addition of V-values;  
       has an argument allowing to specify any other binary operation on the intersection
- masks and linear comnbination
- prettyprint V-values in different ways
- verify kashrut, eliminate zero nodes, compute depths of all branches in a V-value, find keys...

Need:
- agree on access-insertion-deletion syntax
- GRAPHICS: Modern GL??

"""
if True:
    import os,sys,time, string
    #import numpy as np
    from importlib import reload
    from copy import deepcopy
    from functools import reduce
    


class V_value():
        def __init__(self, n=0, D={}, name=None):
            if type(float(n)) != float or type(D) != dict:
                print('Gevalt in V_value: expected a number ', n, 'and a dictionary ', D)
            else:
                self.n=n
                self.D=deepcopy(D)
                self.name=name

            
def sum(a,b):
            try: return a+b
            except:
                print ('gevalt in sum: a= ',a,' b= ',b)
def minus(a,b):
            try: return a-b
            except:
                print ('gevalt in sum: a= ',a,' b= ',b)
            
if True:  # some sample green-trees (aka leaf-adorned dictionaries) for testing
            D2={'c':(7,{}), 'd':(9,{})}
            D20={'c':(6,{}), 'd':(11,{})}
            D1 = {'a':(5,{}), 'b':(0,D2)}
            D0 = {'z':(0,{}), 'b':(0,D20),'e':(100,D2)}
            Dt={'xx':(3,{'YY':(5,{}), 'ZZ':(0,D2)})}
            Dtest={'xx':(3,{'YY':(5,{})})}
            Dt2={'xx':(3,{'YY':(5,Dtest), 'ZZ':(0,D2)})}
            
if True:      # prepare a fancy mask to test apply_mask_combine:
            Dmask={'z':(0,{}), 'b':(0,D20),'e':(100,D2)}
            D20plus={'c':(6,{}), 'd':(11,Dt)}
            D2plus={'c':(7,{}), 'd':(9,Dt2)}
            DV={'z':(0,{}), 'b':(0,D20plus),'e':(100,D2plus)}
            V=convert2V(0,DV,verbose=0)
            Vmask =convert2V(0,Dmask,verbose=0) 
            rootP, key, Vsum = 1,'',[]
            
""" converts green-tree to V_value; returns V_value"""
def convert2V(n,D,verbose=0):
        if type(float(n)) != float or type(D) != dict:
                print ( 'Gevalt in convert2V:', n, ' <---> ', D)
                return False
        vv=V_value(n,{})   
        if not (D.items()) and not n:
               print ('Gevalt in convert2V: zero leaf found!')
        for (ke,va) in D.items():
                if verbose: print ('convert2V looping over', ke, D.items())
                vv.D[ke]= convert2V(va[0],va[1],verbose)
        return vv

""" prettyprint V-Value"""            
def pprint (V, info_string,verbose=0):         
            print (info_string)
            if not V:
                print ('V is empty, nothing to print')
                return
            if verbose:
                try:
                    print ('V.n, V.D.keys() = ', V.n,  V.D.keys())
                except:
                    print ('prettyprint failed', V)
                    return
            for kk in list(V.D.keys()):
                #st='inside '+info_string+' key '+kk
                st='*------* %s[%2s, %2.0f] ' % (info_string,kk,V.D[kk].n)
                pprint (V.D[kk],st)



"""
An auxillary routine for graph_print routine
prints 2 lines of the dependency graph as follows:
          |
           ----[ d,  9]
"""
def graph_part(st,xstep=9):
 
        size=len(st)
        if size<2*xstep:
            return st
        tail=st[-xstep:]
        st1=' '*(size-2*xstep) + '    |'
        st2=' '*(size-2*xstep) + '     ----'+tail
        return st1+'\n'+st2
    
"""
- for a V_value, prettyprints its dependency graph 
- returns a dictionary D of form {string:V_value}  that can be later used for fancier prettyprinting
usage:   D=graph_print(V, 'OO',{},'')
info-string can be initialzed to any string; that's how root shall be printed in the printout
inside is another decorative string to experiment with; should be generally set to '')
"""   
def graph_print (V, info_string,Dstr, inside, verbose=0):
            #inside ='*------* '
            Dstr[info_string]=V
            print(graph_part(info_string))
            if not V:
                print ('V is empty, nothing to print')
                return
            if verbose:
                try:
                    print ('V.n, V.D.keys() = ', V.n,  V.D.keys())
                except:
                    print ('prettyprint failed', V)
                    return
            for kk in list(V.D.keys()):
                #st='inside '+info_string+' key '+kk
                st='%s%s[%2s, %2.0f] ' % (inside, info_string,kk,V.D[kk].n)
                Dstr[st]=V.D[kk]
                _=graph_print (V.D[kk],st,Dstr,inside)
            return Dstr

 
        
"""returns intersection and 2 complements of the two lists or tuples"""
def intersect_lists(b1,b2):
        bi = [val for val in b1 if val in b2]
        bc1 = [val for val in b1 if val not in bi]
        bc2 = [val for val in b2 if val not in bi]
        return  bi,  bc1, bc2
    

def intersect_dict_keys(D1,D2):
        return intersect_lists(list(D1.keys()), list(D2.keys()))

            
""" nodes with (n=0, D={}) can be eliminated if so desired"""
def eliminate_zero_nodes(V):
        keys=[]
        for ke in V.D.keys():
            if V.D[ke].n == 0 and not(V.D[ke].D):
                keys.append(ke)
        for kk in keys:  V.D.pop(kk)                   
        for kk in V.D.keys():
            eliminate_zero_nodes(V.D[kk])
            

"""
count occurences of a key in V_value; in fact. lists all keys....
"""
def if_key_in_V_value(V,key,count):
        c=count
        for ke in V.D.keys():
            print(ke)
            if ke == key:
                c +=1
                print('leaf value at key = ', V.n, ke, 'count=', c)
            c=if_key_in_V_value(V.D[ke],key, c)
        return c

    
""" multiplying V-value by a scalar in place
Assumes that all values of leaves are numbers!!"""
def Vmult_inplace(V,scalar):      
        try:
            V.n *= scalar
        except:
                print ( 'Gevalt in Vmult_inplace: V.n, scalar = ', V.n, scalar)
                return False  
        if not (V.D.items()) and not V.n:
               print ('Gevalt in Vmult_inplace: zero leaf found!')
        for (ke,va) in V.D.items():
                Vmult_inplace(va,scalar)
           
                
""" multiplying V-values, making a new copy """        
def Vmult(V,scalar): #V is V-value; multiplying in place       
        vvv=deepcopy(V)
        Vmult_inplace(vvv,scalar)
        return vvv

            
"""
In_place function: the intersection of V0,V1 will be stored in V0.
we always apply func to the two root leaves, regardless of whether V-values have a non-empty interection;
We also recommend to eliminate ZERO NODES of V1 in advance (didn't QA what can happens otherwise)
Leaves of V0 at each common node are combined of the two original values: (n1,n2)
Therefore this is a template for sum, multiplication or any other binary operation.
For now func can be 'max', 'min' or 'sum'; can write others.... 
"""
# lots of debug printout, will eliminate later
# Should call with rootP = 1 (handling default argument in python is counterintuitive!)           
def intersect_v_values(V0,V1, rootP, func):  # func can be 'sum', 'max', etc
        if rootP and not V0:
            V0=deepcopy(V1)
            V1=None
        pprint(V0, '1st argument before eliminating') #NNN check validity
        eliminate_zero_nodes(V0)                      #NNN check validity
        pprint(V0, '1st argument ')
        pprint(V1, '2nd argument ')
        if rootP and V1==None:
            return
        ki,k1,k2=intersect_dict_keys (V0.D, V1.D)
        print (' **** intersecting nodes: ki, k1, k2 = ', ki,k1, k2)
        if rootP:
            V0.n = eval(func)(V0.n, V1.n) #processing the common root node
        for kk in k2:
            V0.D[kk] = V1.D[kk]
        for kk in ki:
            V0.D[kk].n = eval(func)(V0.D[kk].n, V1.D[kk].n)
            print('kk= ',kk,' --- V0.n = ', V0.n)
            intersect_v_values(V0.D[kk],V1.D[kk], 0,func)


"""multiply V_value inplace by leaves of the mask"""
def apply_mask(V0,Vmask, rootP):
        #V0=deepcopy(V)
        if rootP:
            print ('+++++++++++++++  at Root')
            eliminate_zero_nodes(V0)
            eliminate_zero_nodes(Vmask)
            #pprint(V0, 'in apply_mask: V-value ')
            #pprint(Vmask, 'in apply_mask: mask ')
        ki,k1,k2=intersect_dict_keys (V0.D, Vmask.D)
        print (' *** intersecting nodes: ki, k1, k2 = ', ki,k1, k2)
        if Vmask.n and not Vmask.D:
            Vmult_inplace(V0,Vmask.n)
            pprint(V0,' multiplying by scalar')
            print('scalar = ', Vmask.n)
        for kk in ki:
            print('in apply_mask: processing ',kk,' --- V0.n = ', V0.n)
            apply_mask(V0.D[kk],Vmask.D[kk],0)            

"""
collect branches of V0 multiplied by appropriate scalars (supplied by Vmask leaves)
into a list of V-values: Vbranches.
Called as follows: apply_mask_combine(V,Vmask, 1, None, Vbranches)
Vbranches is a list of V-values, initialized (usually to []) in advance
(A separate routine adds all the branches together)
"""
# Called as follows: apply_mask_combine(V,Vmask, 1, None, Vbranches)
def apply_mask_combine(V,Vmask, rootP, key, Vbranches):
        V0=deepcopy(V)
        if rootP:
            print ('+++++++++++++++  apply_mask_combine')
            eliminate_zero_nodes(V0)
            eliminate_zero_nodes(Vmask)
        if Vmask.n and not Vmask.D:
            #print('multiplying by scalar = ', Vmask.n, 'at key ', key)
            if rootP:
                v=Vmult(V0,Vmask.n)
            else:
                v=V_value(0,{key:Vmult(V0,Vmask.n)})
            Vbranches.append(v)
            #pprint(v,' ..... and get the result: ')             
        ki,k1,k2=intersect_dict_keys (V0.D, Vmask.D)
        #print (' *** intersecting nodes: ki, k1, k2 = ', ki,k1, k2)
        for kk in ki:
              #print('in apply_mask_combine: processing ',kk,' --- V0.n = ', V0.n)
              apply_mask_combine(V0.D[kk],Vmask.D[kk],0, kk, Vbranches)

"""
Vbranches is a list of branches, such as filled by apply_mask_combine()
returns V_value obtained by summing up all those branches
"""
def reduce_branches(Vbranches, verbose=0):
        Vsum=Vbranches.pop()
        for v in Vbranches: 
            intersect_v_values(Vsum, v, 1,'sum')
            if verbose:
                print('            *************** ')
                pprint(v,' ')
        return Vsum

"""
Main rountine: Linear combination
"""
def linear_combination(V,Vmask):
        Vbranches = []
        apply_mask_combine(V,Vmask, 1,None, Vbranches)
        return reduce_branches(Vbranches, verbose=0)
                      
""" (My first attempt at recursion, therefore excessive printouts)
      recursively check validity of a green-tree without converting it to V-value
     return list of tree depths
     Assumes that all values of leaves are numbers!!"""
def check_vv(n,D, count=0, depths=None, verbose=1):
        c=count
        if depths == None: depths = []  
        if type(float(n)) != float:
                print ( 'Gevalt1 in check_vv:', n, ' <---> ', D)
                return False
        if type(D) != dict:
                print ( 'Gevalt2 in check_vv:', n, ' <---> ', D)
                return False
        c+=1
        if not (D.items()):
            if not n:
               print ('Gevalt in check_vv! zero leaf found!')
               c -= 1 
            if verbose: print ('check_vv: appending' , c, ' to depths=', depths )
            depths.append(c)
            c=0           
        for (ke,va) in D.items():
                if verbose: print ('check_vv: ke = ', ke, ' looping over', D.items())
                c,depths=check_vv(va[0], va[1], c, depths)
        return c,depths 

""" count occurences of a key in V_value"""
def if_key_in_V_value(V,key):
        c=0
        for ke in V.D.keys():
            print(ke)
            if ke == key:
                c +=1
                print('leaf value at key = ', V.n, ke, 'count=', c)
            c+=if_key_in_V_value(V.D[ke],key)
        return c
            
################################ bits and scraps

"""
A silent routine, currently unused.
Returns a dictionary D with V-Values as keys and strings as values.
Perhaps can be used later for prettyprinting...
D = pprintD (V, 'o', {})
"""
def pprintD (V, info_string,Dstr, verbose=0):         
            Dstr[V]=info_string
            if not V:
                print ('V is empty, nothing to print')
                return
            if verbose:
                try:
                    print ('V.n, V.D.keys() = ', V.n,  V.D.keys())
                except:
                    print ('prettyprint failed', V)
                    return
            for kk in list(V.D.keys()):
                #st='inside '+info_string+' key '+kk
                st='*------* %s[%2s, %2.0f] ' % (info_string,kk,V.D[kk].n)
                Dstr[V.D[kk]]=st
                _=pprintD (V.D[kk],st,Dstr)
            return Dstr

        
"""
Auxiliary routine for pprintD: prints the dictionary selectively & in the right order:
D = pprintD (V, 'a', {})
pprintL (V, D)
"""
def pprintL (V, Dstr, verbose=0):         
            for kk in list(V.D.keys()):
                #if not V.D[kk].D:
                    #print (Dstr[V.D[kk]])
                print (Dstr[V.D[kk]])
                pprintL (V.D[kk], Dstr)
                

"""
auxiliary routine for next_coord:
computes printing position  of keys in V_value.
"""
# plotadot(1,'xx',3,3,10,1)
def plotadot(n,label,x,y,xstep,ystep):
        #prstr='%s [%s]%3.0f' % (tmp, label[:5], n)
        prstr='[%s]%3.0f    ' % (label[:5], n)
        return prstr[:xstep]
"""
an aborted attempt to do somehing like graph_print.
Doesn't work!!
"""
#   next_coord(V,1, '',5,1,'',10)    
def next_coord(V,rootP, key,x,y, prstr, xstep,ystep=0):
        if rootP:
            print ('root')
            eliminate_zero_nodes(V)
            prstr += plotadot(V.n,key,x,y,xstep,ystep)
            #width,depth=compute_plotsize(V)
        #prstr += plotadot(V.n,key,x,y,xstep,ystep)
        for ke in V.D.keys():  # next key is 1 step below (aka '\n' below)
            #y +=1 ???
            prstr += plotadot(V.D[ke].n,ke,x,y,xstep,ystep)
            if not(V.D[ke].D): 
                x -=1      # this was an end-leaf, so we go 1 step left
                print (prstr)
                #prstr= '\n'*y + ' '*(x-1)*xstep
                prstr=prstr[:-xstep]
                print('at key = ', ke, 'leaf value = ', V.D[ke].n, 'x,y = ', x,y)
            else:
                x+=1               
            next_coord(V.D[ke],0, ke,x,y,prstr, xstep,ystep)
            
def Vmult_inplace_wrong(V,scalar):       
        try:
            V.n *= scalar
        except:
                print ( 'Gevalt in Vmult_inplace: V.n, scalar = ', V.n, scalar)
                return False  
        if not (V.D.items()) and not V.n:
               print ('Gevalt in Vmult_inplace: zero leaf found!')
        for (ke,va) in V.D.items():
                V.D[ke]= Vmult_inplace_wrong(va,scalar)


def apply_mask_test(V,Vmask, key, Dtrees,name_for_root='root_of_Vvalue'):
        V0=deepcopy(V)
        if key==name_for_root:
            print ('+++++++++++++++  ', key)
            Dtrees=deepcopy({})
            # pprint(V0, '1st argument before eliminating')
            eliminate_zero_nodes(V0)
            eliminate_zero_nodes(Vmask)
            #pprint(V0, 'in apply_mask: V-value ')
            #pprint(Vmask, 'in apply_mask: mask ')
        ki,k1,k2=intersect_dict_keys (V0.D, Vmask.D)
        print (' *** intersecting nodes: ki, k1, k2 = ', ki,k1, k2)
        if Vmask.n and not Vmask.D:
             Dtrees[key]=Vmult(V0,Vmask.n)          
        for kk in ki:
            print('in apply_mask: processing ',kk,' --- V0.n = ', V0.n)
            apply_mask_test(V0.D[kk],Vmask.D[kk],kk, Dtrees)
        if key==name_for_root:
            return V_value(0,Dtrees)



