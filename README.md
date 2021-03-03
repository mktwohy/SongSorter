# SongSorter
# Purpose
My dad's local music was stored in a folder of 8,000 unsorted songs. Surprisingly, I couldn't find any programs for sorting music. However, 
I knew Python was good at file organization, so I spent a few days writing this program. In the end, it was able to sorted 8,000 songs in under a minute, 
which would otherwise be infeasible to sort manually.

# Explanation
Firstly, I needed a way to read the metadata of each song. This turned out to be far more complicated than I hoped, so I tried a few different libraries and settled on Mutagen.
Unfortunately, the documentation is pretty confusing, so my implimentation isn't as elegant as I had hoped. Regardless, it works. 

For each song in the directory, the program uses this getMetaData() function to figure out the song's album and artist. 
If an artist\album path doesn't already exist, it creates one. Finally, it moves the file to that location.

During testing, I wanted a way to undo my work. 7Zip has a way of "flattening" a directory, but that takes a few minutes and a lot of mouse clicks, so I wrote flattenDirectory(). 
This function moves every song back to the parent directory and deletes every empty folder. In hindsight, this could have been more readable if done recursively.

To use it, you simply call either sortSongs(cwd) or flattenDirectory(cwd), where cwd is the address of your music folder. 
