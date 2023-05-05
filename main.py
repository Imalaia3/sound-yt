#Python Library Hell
try:
    
    from moviepy.editor import concatenate_audioclips, AudioFileClip
    from mutagen.mp3 import MP3
    
except ImportError:
    print("""[FAILED] There are missing libraries!\nSoundYT Requires\n-MoviePy\n-Mutagen
    Use this commands to install them:
    pip install moviepy
    pip install mutagen
    """)
    exit(-1)


try:
    from sys import argv
    from os import path,listdir
    from shutil import which
except:
    print("[FAILED] Python is, somehow, missing the sys, shutil or the os library!\nTry re-installing python")
    
    exit(-1)

argc = len(argv)

ONLY_DESCRIPTION = True


if argc > 1 and argv[1] == "--help":
    print("""
SoundYT
The Steam Soundtrack to Youtube video converter.
Copyright: Imalaia3. This program falls under the GNU GPL v3 (more info at: https://www.gnu.org/licenses/gpl-3.0.en.html)
Built for Python 3.

Commands:
--help - Prints this screen
--no-credit - Disables the "build with SoundYT" footer at the description

    
Note: This program requires FFMPEG. This program must be able to be ran via the "ffmpeg" command. FFMPEG can be found at: https://ffmpeg.org/.
""")
    exit()

#TODO: Optimize
def comm_exists(cmd):
    return which(cmd)


def mutagen_length(path):
    try:
        return MP3(path).info.length
    except:
        pass
   
def ffmpeg_detector():
    if comm_exists("ffmpeg") == None:
        print("""You don't have ffmpeg in your (Windows) PATH
    or it isn't installed. Exit this program and visit
    https://ffmpeg.org/ for installation instructions""")
        exit()
    print("FFMPEG is installed.")


def run():
    ffmpeg_detector()


    ST_PATH = input("Enter Soundtrack Folder PATH > ")

    if not path.isdir(ST_PATH):
        print("This directory doesn't exist!")
        exit(-1)

    
    trackName = ST_PATH.split("/")[-1]


    MPFILES = {}
    hasCover = False
    for file in listdir(ST_PATH):
        if file.split(".")[-1] == "png":
            hasCover = True
            print("Cover Detected.")
            continue
        if len(file.split(".")) == 1:
            continue
        MPFILES[file] = None


    #Load AudioFileClips into MPFILES
    for file in MPFILES:
        #break
        MPFILES[file] = AudioFileClip(ST_PATH+"/"+file)


    #Grab timestamps for every MPFILE
    MPLEN = {}
    totalsize = 0
    for file in MPFILES:
        mins = mutagen_length(ST_PATH+"/"+file)
        MPLEN[file] = mins
        totalsize += mins

    print(f"Found {len(MPLEN)} Music Files.")
    print(f"The Album Name is: {trackName}.\n")
    print(f"The total size of the video will be: {totalsize} seconds.")


    if not hasCover:
        print("No cover.png Detected! Enter a path of your own")
        coverpath = '"'+input(">")+'"'
    else:
        coverpath = '"'+ST_PATH+"/"+"cover.png"+'"'

    print("Building Audio File.")

    if not ONLY_DESCRIPTION:
        AUDIO_DONE = concatenate_audioclips(list(MPFILES.values()))
        AUDIO_DONE.write_audiofile("output.mp3")

    print("Writing video.")

    #Stackexchange ffmpeg Will try to output as mp4
    if not ONLY_DESCRIPTION:
        system(
            "ffmpeg -loop 1 -i {} -i {} -shortest -acodec copy -vcodec libx264 upload.mp4".format(
            coverpath,
            "output.mp3"
            ))

    print("Making Description.")
    
    #Convert Lengths to Timestamps
    OLEN = {}
    for c,file in enumerate(MPLEN):
        if c == 0:
            print(MPLEN[file])
            OLEN[file] = 0
            print(OLEN)
            continue
        
        OLEN[file] = list(OLEN.values())[c-1] +list(MPLEN.values())[c-1]

    
    DESC = f"""
##{"#"*len(trackName)}##
# {trackName} #
##{"#"*len(trackName)}##\n\n\n\n
Tracklist:
"""

    for track in OLEN:
        if totalsize > 3600: #1 h
            if OLEN[track] < 3600:
                #zero padding
                stamp = "00:"+str(int(OLEN[track]/60)).zfill(2) + ':' + str(int(OLEN[track]%60)).zfill(2)
                
                
            else:
                #Convert secs to h mins and secs
                h = OLEN[track]/3600
                minutes = OLEN[track]%3600/60 
                secs = OLEN[track]%60
                stamp = str(int(h))+":"+str(int(minutes)).zfill(2) + ':' + str(int(secs)).zfill(2)



            DESC += f"{track} - {stamp}\n"
            continue
                



        stamp = str(int(OLEN[track]/60)).zfill(2) + ':' + str(int(OLEN[track]%60)).zfill(2)
        
        DESC += f"{track} - {stamp}\n"



    #--no-credit mode
    if argc > 1 and argv[1] == "--no-credit":
        print("Skipping Credits.")
    else:
        DESC+="\nGenerated with SoundYT by Imalaia3."


        


    input("Press enter to get your description")
    print("======================================\n")

    print(DESC)



    print("Bye Bye!") #Bye bye!





if __name__ == "__main__":
    run()



### Thanks for reading!
### Feel free to: edit, use, remaster, improve this program. It uses the Gnu GPL licence!
### -Imalaia3
