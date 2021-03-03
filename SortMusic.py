# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 11:48:05 2021

@author: Twohy
"""

import mutagen as m
import os 

def getMetaData(f):
    title,fext = os.path.splitext(f)
    mf = m.File(f)
    artist = ''
    album = ''
    
    if fext == '.mp3':
        tags = m.mp3.EasyMP3(f)
        album = tags['album'][0]
        artist = tags['artist'][0]

    elif fext == '.m4a' or fext == '.m4p':
        data = mf.pprint().split('1>)')
        metadata = data[len(data)-1].split("\n")
        for i in metadata:
            if "©ART" in i:
                artist = i.split('=')[1]

            if '©alb' in i:
                album = i.split('=')[1]
             
    else:
        raise Exception("Unrecognized file format: ",fext)
        
    return title,fext,artist,album

def printAllSongs():
    counter = 0
    failed = []
    for f in os.listdir():
        try:
            title,fext,artist,album = getMetaData(f) 
                
            if(len(artist)==0 or len(album)==0):
                raise Exception("Failed to find all metadata")
            else:
                counter+=1
                    
            print("Title:",title)
            print("\tAlbum:",album)
            print("\tArtist:",artist)
            print()
        except:
            failed.append(title)
            pass
    
    print(counter)
    print(failed)
 
def replaceIllegal(word):
    illegals = {"<": '(',
                ">": ')',
                ":": ' -',
                "/": ' - ',
                "\\": ' - ',
                "|": ' - ',
                "?": '_',
                "*": '_',
                '"': "'"}
    
    ret = ""
    for char in word:
        if char in illegals:
            ret = ret + illegals[char]
        else:
            ret = ret+char
    return ret   

def sortSongs(cwd):
    os.chdir(cwd)
    files = os.listdir()
    counter = 0
    failed = []
    for f in files:
        try:
            title,fext,artist,album = getMetaData(f)
            album = replaceIllegal(album)
            artist = replaceIllegal(artist)
            albumPath = os.path.join(artist,album)
            if not os.path.exists(albumPath): #If album path doesnt exist
                if not os.path.exists(artist): #and if artist folder doesnt exist
                    os.makedirs(artist)         #make artist and album folder in cwd
                    os.makedirs(albumPath)
                else:
                    os.makedirs(albumPath)      #Otherwise, just make album folder in artist folder
            elif not os.path.exists(artist):  #If artist folder doesn't exist
                os.makedirs(artist)             #Make artist folder in cwd
            os.rename(f,albumPath+'/'+f) #Move file to album folder      
        except:
            pass
            if not os.path.isdir(f):
                failed.append(f)
                
        percent = 100*(counter/len(files))
        print('Progress: '+('#'*int(percent)),int(percent),'%')
        counter +=1
    print("\n\nFailed to sort",len(failed),"songs:")
    for song in failed:
        print("\t"+song)
        
def getFoldersInDir(directory):
    folders = []
    for root, dirs, files in os.walk(directory):
        for f in dirs:
            folders.append(os.path.join(root,f))    
    return folders

def delEmptyFolders(cwd):
    num_folders_deleted = 0
    folders = getFoldersInDir(cwd)
    for f in folders:
        if len(os.listdir(f))==0: #If there are 0 files in this directory
            os.rmdir(f) #Remove directory
            num_folders_deleted +=1
    
    return num_folders_deleted             
                    
def flattenDirectory(cwd,clean_up = True):
    os.chdir(cwd) #Change cwd

    for root, dirs, files in os.walk(os.getcwd()):
        for name in files: 
            old_name = os.path.join(root,name)
            new_name = os.path.join(cwd,name) 
            os.rename(old_name,new_name)
    if clean_up:
        last_del = 0
        cur_del = delEmptyFolders(cwd)
        while cur_del != last_del:
            last_del = cur_del
            cur_del = delEmptyFolders(cwd)
                    
        
cwd = 'C:\\Users\Twohy\Music\Music From Fiio'
# cwd = 'C:\\Users\Twohy\Music\TestSortMusic'
# sortSongs(cwd)
flattenDirectory(cwd,clean_up = False)

