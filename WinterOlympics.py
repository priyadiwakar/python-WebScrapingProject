# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 03:33:51 2018

@author: priya
"""

import urllib
import sys
import re
import os
import requests
from bs4 import BeautifulSoup
import numpy as np
import projectfunctions as pf


def main():
    
    years,sports=pf.getlist()
    args = sys.argv[1:]
    if not args:
        
        pf.doc_help()
    
        sys.exit(1)
    else:
        if len(args)==1:
            print("Please enter atleast year or country or sport\n")
            pf.doc_help()
            sys.exit(1)
        
        else:
            year=""
            sport=""
            country=""
            
            
            
            for i in range(len(args)):
                if args[i]=="-year" :
                    try:
                        year=args[i+1]
                    except:
                        print("Invalid Number of inputs")
                        pf.doc_help()
                        sys.exit(1)
                if args[i]=="-country" :
                    try:
                        country=args[i+1]
                    except:
                        print("Invalid Number of inputs")
                        pf.doc_help()
                        sys.exit(1)
                        
                if args[i]=="-sport" :
                    try:
                        sport=args[i+1]
                    except:
                        print("Invalid Number of inputs")
                        pf.doc_help()
                        sys.exit(1)
            
            
                
            if year!="" and country!="" and sport!="":
#                x=re.compile(year)
#                sub_list = list(filter(x.match, years))
#                x1=re.compile(sport)
#                sub_list1 = list(filter(x1.match, sports))
                sub_list = [a for a in years if year==a]
                sub_list1 = [b for b in sports if sport==b]
                if sub_list==[] and sub_list1==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                elif sub_list==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    sys.exit(1)
               
                elif sub_list1==[]:
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                else:
                    if len(args[1:])%2!=0:
                        ind=args.index("-country")
                        country=country+" "+args[ind+2]
                    s=""
                    r=country.split(' ')
                    for i in range(len(r)):
                        s=s+r[i]+'_'
                    p,gold1,silver1,bronze1=pf.datafor1(sport,country,year)
                    
                    gold1=int(float(gold1))
                    silver1=int(float(silver1))
                    bronze1=int(float(bronze1))
                    total1=gold1+silver1+bronze1
                    
                    medals=pf.nationlistfor1(year,s)
                    gold,silver,bronze,total=pf.yearpage(year,1,country)
                    years,sports=pf.getlist()
                    
                    gold=int(float(gold))
                    silver=int(float(silver))
                    bronze=int(float(bronze))
                    total=int(float(total))
                    names=[]
                    events=[]
                    if medals!=[]:
                        for i in medals[0:gold]:
                            
                            try:
                                ind=i.index(sport)
                   
                                names.append(i[1])
                                events.append(i[3])
                                
                            except:
                                continue
                                
                        for i in medals[gold:gold+silver]:
                            
                            try:
                                ind=i.index(sport)
                   
                                names.append(i[1])
                                events.append(i[3])
                            except:
                                continue
                                
                        for i in medals[gold+silver:total]:
                            
                            try:
                                ind=i.index(sport)
                    
                                names.append(i[1])
                                events.append(i[3])
                            except:
                                continue
                    
                    if args[0]=="--summary":
                        pf.summaryfor1(year,sport,country,total1,gold1,silver1,bronze1,p,names,events)
                    if args[0]=="--summaryfile":
                        pf.printfilefor1(year,sport,country,total1,gold1,silver1,bronze1,p,names,events)
                    
                    if args[0]=="--graph":
                        print("Too many arguments for graph")
                        sys.exit("Error")
                        
            elif year!=""   and country=="" and sport=="":
#                x=re.compile(year)
#                sub_list = list(filter(x.match, years))
                sub_list=[a for a in years if year==a]
                if sub_list==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    sys.exit(1)
                else:
                    
                    participants,nations=pf.yearsummary(year,years,sports)
                    
                    medallist,host=pf.yearpage(year,0)
                    nationwise=pf.nationlist(year,0)
                    medallist=medallist[0:len(nationwise)]
                    if args[0]=="--summary":
                        pf.printfinal(year,participants,nations,medallist,host,nationwise,years,sports)
                    elif args[0]=="--summaryfile":
                        pf.printtofile(year,participants,nations,medallist,host,nationwise,years,sports)
                    elif args[0]=="--graph":
                        pf.graphforyear(participants,nations,sports,year)
                        
            elif year==""   and country!="" and sport=="":
                    if len(args[1:])%2!=0:
                        ind=args.index("-country")
                        country=country+" "+args[ind+2]
                    goldl=[]
                    silverl=[]
                    bronzel=[]
                    totall=[]
                    nationwisel=[]
                    s=""
                    r=country.split(' ')
                    for i in range(len(r)):
                        s=s+r[i]+'_'
                    for year in years:
                        gold,silver,bronze,total=pf.yearpage(year,1,country)
                        goldl.append(gold)
                        silverl.append(silver)
                        bronzel.append(bronze)
                        totall.append(total)
                        nationwise=pf.nationlist(year,1,s)
                        nationwisel.append(nationwise)
                
                    if args[0]=="--summary":
                        pf.printfinal7(years,country,goldl,silverl,bronzel,totall,nationwisel)
                    elif args[0]=="--summaryfile":
                         pf.printtofile7(years,country,goldl,silverl,bronzel,totall,nationwisel)
                    elif args[0]=="--graph":
                        pf.graphforcountry(goldl,silverl,bronzel,nationwisel,years,country)
            
            elif year==""   and country=="" and sport!="":
                if len(args[1:])%2!=0:
                    ind=args.index("-sport")
                    sport=sport+" "+args[ind+2]
#                x1=re.compile(sport)
#                sub_list1 = list(filter(x1.match, sports))
                
                sub_list1 = [b for b in sports if sport==b]
                if sub_list1==[]:
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                else:
                
                    participants,nations,links,highestc,finalyears=pf.yearsummary5(years,sport)
                    
                    participants1=[item for item in participants if item!=0]
                    nations1=[item for item in nations if item!=0]
                    host=pf.yearpage5(years)
                    
                    
                    if sport==sports[4]:
                        
                        highestc=highestc[1:]
                    if sport==sports[9] or sport==sports[10] :
                        participants1=participants[-len(finalyears):]
                        nations1=nations[-len(finalyears):]
                    
             
                    if args[0]=="--summary":
                        pf.printfinal5(participants1,nations1,highestc,host,finalyears,sport)
                    elif args[0]=="--summaryfile":
                        pf.printtofile5(participants1,nations1,highestc,host,finalyears,sport)
                    elif args[0]=="--graph":
                        pf.graphforsport(participants1,nations1,sport,finalyears,highestc,host,sport)
                
            elif year!=""   and country=="" and sport!="":
                if len(args[1:])%2!=0:
                    ind=args.index("-sport")
                    sport=sport+" "+args[ind+2]
#                x=re.compile(year)
#                sub_list = list(filter(x.match, years))
#                x1=re.compile(sport)
#                sub_list1 = list(filter(x1.match, sports))
                sub_list = [a for a in years if year==a]
                sub_list1 = [b for b in sports if sport==b]
                if sub_list==[] and sub_list1==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                elif sub_list==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    sys.exit(1)
               
                elif sub_list1==[]:
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                else:
                    
                    participants,nations,countries,medallist,finallist,flag=pf.yearsport4(year,sport)
                    
                    if args[0]=="--summary":
                        pf.printsummary4(participants,nations,countries,medallist,finallist,flag,year,sport)
                    elif args[0]=="--summaryfile":
                        pf.printtofile4(participants,nations,countries,medallist,finallist,flag,year,sport) 
                    elif args[0]=="--graph"  :
                        pf.graph4(participants,nations,countries,medallist,finallist,flag,year,sport)
            elif year!=""   and country!="" and sport=="":
                if len(args[1:])%2!=0:
                    ind=args.index("-country")
                    country=country+" "+args[ind+2]
#                x=re.compile(year)
#                sub_list = list(filter(x.match, years))
                sub_list = [a for a in years if year==a]
                
                if sub_list==[]:
                    print("Invalid Year")
                    pf.doc_help_year()
                    sys.exit(1)
                else:    
                    gl=np.zeros(len(sports))
                    sl=np.zeros(len(sports))
                    bl=np.zeros(len(sports))
                    participants=[]
                    countries=[]
                    s=""
                    r=country.split(' ')
                    for i in range(len(r)):
                        s=s+r[i]+'_'
                    
                    gold,silver,bronze,total=pf.yearpage(year,1,country)
                    gold=int(float(gold))
                    silver=int(float(silver))
                    bronze=int(float(bronze))
                    total=int(float(total))
                    medals=pf.nationlist3(year,s)
                    
                    
                    for sport in sports:
                        a,b=pf.yearsport3(year,sport,country)
                        participants.append(int(a))
                        countries.append(b)
                        
                    if medals!=[]:
                        for i in medals[0:gold]:
                            for sport in sports:
                                try:
                                    ind=i.index(sport)
                                    s=i[ind]
                                    ind1=sports.index(s)
                                    gl[ind1]=gl[ind1]+1
                                except:
                                    continue
                                
                        for i in medals[gold:gold+silver]:
                            for sport in sports:
                                try:
                                    ind=i.index(sport)
                                    s=i[ind]
                                    ind1=sports.index(s)
                                    sl[ind1]=sl[ind1]+1
                                except:
                                    continue
                                
                        for i in medals[gold+silver:total]:
                            for sport in sports:
                                try:
                                    ind=i.index(sport)
                                    s=i[ind]
                                    ind1=sports.index(s)
                                    bl[ind1]=bl[ind1]+1
                                except:
                                    continue
                        
                            
                        totalmedals=gl+sl+bl
                        data = np.zeros(len(sports), dtype={'names':('Sport', 'Gold', 'Silver','Bronze','Total','Participants'),
                                      'formats':('<U50', 'i4', 'i4','i4','i4','i4')})
                    
                        data['Sport'] = sports
                        data['Gold'] = gl
                        data['Silver'] = sl
                        data['Bronze'] = bl
                        data['Total'] = totalmedals
                        
                        data['Participants'] = participants
                       
                        sort=np.sort(data,order=["Total","Gold","Silver","Bronze","Participants"])[::-1]
                        
                        nationwise=sum(participants)
                        if args[0]=="--summary":
                            pf.summary3(year,country,gold,silver,bronze,nationwise,sort)
                        if args[0]=="--summaryfile":
                            pf.summarytofile3(year,country,gold,silver,bronze,nationwise,sort)
                        if args[0]=="--graph":
                            pf.graphfor3(year,country,gold,silver,bronze,nationwise,sort)
                    else:
                        print("Medal Table not Found")
                            
            elif year==""   and country!="" and sport!="":
                if len(args[1:])%2!=0:
                    ind=args.index("-country")
                    country=country+" "+args[ind+2]
#                x=re.compile(year)
#                sub_list = list(filter(x.match, years))
                
                sub_list = [b for b in sports if sport==b]
                if sub_list==[]:
                    print("Invalid Sport")
                    pf.doc_help_sport()
                    sys.exit(1)
                else:    
                    p,gold,silver,bronze,finalyears=pf.datafor2(sport,country)
                    if args[0]=="--summary":
                        pf.printsummary2(sport,country,p,gold,silver,bronze,finalyears)
                    if args[0]=="--summaryfile":
                        pf.printfile2(sport,country,p,gold,silver,bronze,finalyears)
                    if args[0]=="--graph":
                        pf.graphfor2(sport,country,p,gold,silver,bronze,finalyears)

if __name__ == "__main__":
    main()
