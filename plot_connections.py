# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:00:20 2015

@author: baillard
"""

import time
import datetime
import numpy as np
import sys

###### Fucntions

def datetotimestamp(date_list):
    [year,month,day,hour,min,sec]=date_list
    sec_floor=int(sec)
    dec=(sec-sec_floor)
    dt = datetime.datetime(year,month,day,hour,min,sec_floor)
    timestamp=time.mktime(dt.timetuple())+dec
    return timestamp

def timestamptodate(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    date_list=[value.year,value.month,value.day,value.hour,value.minute,float("%.2f" %(value.second+value.microsecond*1e-6))]
    return date_list

def load_xyz(filename):
    fic=open(filename,'r') 
    # Laod file unto dictionary
    dic_data={'lon':[],'lat':[],'z':[],'mag':[],'time':[],'rms':[],'xerr':[],'yerr':[],'zerr':[],'terr':[]}
    lines=fic.readlines()
    for line in lines:
        line_spl=line.split()
        [lon,lat,z]=map(float,line_spl[0:3])
        mag=float(line_spl[4])
        xerr,yerr,zerr,terr=float(line_spl[5]),float(line_spl[6]),float(line_spl[7]),float(line_spl[8])
        rms=float(line_spl[9])
        nofrag, frag = line_spl[3].split('.')
        nofrag_dt = time.strptime(nofrag, "%Y-%m-%dT%H:%M:%S")
        timestamp=time.mktime(nofrag_dt)+float('0.'+frag)
        dic_data['lon'].append(lon)
        dic_data['lat'].append(lat)
        dic_data['z'].append(z)
        dic_data['mag'].append(mag)
        dic_data['time'].append(timestamp)
        dic_data['xerr'].append(xerr)
        dic_data['yerr'].append(yerr)
        dic_data['zerr'].append(zerr)
        dic_data['terr'].append(terr)
        dic_data['rms'].append(rms)
    for key, value in dic_data.iteritems():
        dic_data[key]=np.array(value)
    fic.close()
    return dic_data
    
def load_neic(filename):
    fic=open(filename,'r') 
    # Laod file unto dictionary
    dic_data={'lon':[],'lat':[],'z':[],'mag':[],'time':[]}
    lines=fic.readlines()[1:] # skip header
    for line in lines:
            line_spl=line.split(',')
            [lon,lat,z]=map(float,[line_spl[2],line_spl[1],line_spl[3]])
            mag=float(line_spl[4])
            nofrag, frag = line_spl[0].split('.')
            nofrag_dt = time.strptime(nofrag, "%Y-%m-%dT%H:%M:%S")
            timestamp=time.mktime(nofrag_dt)+float('0.'+frag[:-1])
            dic_data['lon'].append(lon)
            dic_data['lat'].append(lat)
            dic_data['z'].append(z)
            dic_data['mag'].append(mag)
            dic_data['time'].append(timestamp)
    for key, value in dic_data.iteritems():
        dic_data[key]=np.array(value)
    fic.close()
    return dic_data
    
def select(dicname,mag=[-5,10],lon=[-180,360],lat=[-90,90],z=[0,9999],timed=[-1893456561.0,time.time()]):
    """ Function made to select data depending on parameters such as depth, mag..."""
    new_dic=dict.fromkeys(dicname.keys())
    lat_array=dicname['lat']
    lon_array=dicname['lon']
    z_array=dicname['z']
    mag_array=dicname['mag']
    time_array=dicname['time']
    check=np.where(np.logical_and.reduce((lon_array>=lon[0], lon_array<=lon[1],
                                  lat_array>=lat[0], lat_array<=lat[1],
                                  z_array>=z[0], z_array<=z[1],
                                  mag_array>=mag[0], mag_array<=mag[1],
                                  time_array>=timed[0], time_array<=timed[1])))
    for key, value in dicname.iteritems():
        new_dic[key]=value[check]
    return new_dic
                                  
def write_xyz(dicname,filename):
    """
    dicname is the input dict generated by load_xyz and filename is the output file in xyzformat
    """
   
    timet=np.sort(dicname['time'])
    foc=open(filename,'w')
    for timestamp in timet:  
        indexes=np.where(timet==timestamp)
        for index in indexes:
            date_f=timestamptodate(timestamp)
            date_string='%4d-%02d-%02dT%02d:%02d:%04.1f' % (date_f[0],date_f[1],date_f[2],date_f[3],date_f[4],date_f[5])
            foc.write('%8.3f %7.3f %5s %21s %6s %6s %6s %5s %5s %5s\n' \
            %(dicname['lon'][index][0],dicname['lat'][index][0],dicname['z'][index][0],
              date_string,dicname['mag'][index][0],
              dicname['xerr'][index][0],dicname['yerr'][index][0],dicname['zerr'][index][0],dicname['terr'][index][0],
              dicname['rms'][index][0]))
    foc.close()
    
######### Main Programs
#
##lon_lim=[166, 167.75]
##lat_lim=[-16.5, -15]
#z_lim=[0, 70]
#
#lon_lim=[166.5, 168]
#lat_lim=[-16.5, -15]
#date_lim=[datetotimestamp([2008,5,1,0,0,0]), datetotimestamp([2009,3,1,0,0,0])]
#dt=30
#
#file_local='/Users/baillard/_Moi/SCRATCH/collect_BEST_clean.xyz'
#file_global='/Users/baillard/_Moi/Programmation/Matlab/Seismic_Catalogs/NEIC_Van_after_2006.txt'
#
##dic_loc=load_xyz(file_local)
##dic_loc_sel=select(dic_loc,lon=lon_lim,lat=lat_lim,z=z_lim)
##write_xyz(dic_loc_sel,'t')
#
##
#dic_loc=load_xyz(file_local)
#dic_glo=load_neic(file_global)
##
### Select proper range from dictionaries
##
#dic_loc_sel=dic_loc
##dic_loc_sel=select(dic_loc,lon=lon_lim,lat=lat_lim,z=z_lim)
#dic_glo_sel=select(dic_glo,lon=lon_lim,lat=lat_lim,z=z_lim,timed=date_lim)
##
#i=0
#dict_A={'lon':[],'lat':[],'z':[],'mag':[],'time':[],'key':[]}
#dict_B={'lon':[],'lat':[],'z':[],'mag':[],'time':[],'key':[]}
#for time_f in np.nditer(dic_glo_sel['time']):
#    print timestamptodate(time_f)
#    index=np.where(dic_glo_sel['time']==time_f)
#    #print dic_glo_sel['z'][index]
#    print dic_glo_sel['lon'][index],dic_glo_sel['lat'][index]
#    time_loc=dic_loc_sel['time']
#    check=np.where(np.logical_and(time_loc>=time_f-dt, time_loc<=time_f+dt))
#    if check[0].size:
#        i=i+1
#        for keys in dict_A:
#            if keys != 'key':
#                dict_A[keys].append(list(dic_loc_sel[keys])[check[0]])
#                dict_B[keys].append(list(dic_glo_sel[keys])[index[0]])
#            else:
#                dict_A[keys].append(i)
#                dict_B[keys].append(i)
#    
#filename1='/Users/baillard/_Moi/SCRATCH/test1.txt'
#filename2='/Users/baillard/_Moi/SCRATCH/test2.txt'
#timet=np.sort(dict_A['key'])
#foc=open(filename1,'w')
#fic=open(filename2,'w')
#for keys in timet:  
#    indexes=np.where(timet==keys)
#    for index in indexes:
#        date_fA=timestamptodate(dict_A['time'][index])
#        date_stringA='%4d-%02d-%02dT%02d:%02d:%04.1f' % (date_fA[0],date_fA[1],date_fA[2],date_fA[3],date_fA[4],date_fA[5])
#        date_fB=timestamptodate(dict_B['time'][index])
#        date_stringB='%4d-%02d-%02dT%02d:%02d:%04.1f' % (date_fB[0],date_fB[1],date_fB[2],date_fB[3],date_fB[4],date_fB[5])
#        foc.write('%21s %8.3f %7.3f %5s %i\n' %(date_stringA,dict_A['lon'][index],dict_A['lat'][index],dict_A['z'][index],dict_A['key'][index]))
#        fic.write('%21s %8.3f %7.3f %5s %i\n' %(date_stringB,dict_B['lon'][index],dict_B['lat'][index],dict_B['z'][index],dict_B['key'][index]))
#foc.close()           
#fic.close()     
