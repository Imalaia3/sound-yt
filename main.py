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
    from os import path,listdir,system
except:
    print("[FAILED] Python is, somehow, missing the sys or/and the os library!\nTry re-installing python")

argc = len(argv)




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

#TODO: Currently only works with mm:ss songs


def mutagen_length(path):
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None
   
def ffmpeg_detector():
    print("""If you don't have ffmpeg in your (Windows) PATH
          or it isn't installed (Linux), exit this program and visit
          https://ffmpeg.org/ for installation instructions""")


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
    for file in MPFILES:
        #print(file)
        mins = mutagen_length(ST_PATH+"/"+file)
        MPLEN[file] = mins

    print(f"Found {len(MPLEN)} Music Files.")
    print(f"The Album Name is: {trackName}.")

    print("Building Audio File.")
    AUDIO_DONE = concatenate_audioclips(list(MPFILES.values()))
    AUDIO_DONE.write_audiofile("output.mp3")

    print("Writing video.")
    #Will try to output as mp4

    if not hasCover:
        print("No cover.png Detected! Enter a path of your own")
        coverpath = '"'+input(">")+'"'
    else:
        coverpath = '"'+ST_PATH+"/"+"cover.png"+'"'


    #Stackexchange ffmpeg
    system(
        "ffmpeg -loop 1 -i {} -i {} -shortest -acodec copy -vcodec mjpeg upload.mp4".format(
        coverpath,
        "output.mp3"
        ))

    print("Making Description.....")
    
    #Convert Lengths to Timestamps
    OLEN = {}
    for c,file in enumerate(MPLEN):
        if c == 0:
            OLEN[file] = MPLEN[file]
            continue
        OLEN[file] = list(OLEN.values())[c-1] +list(MPLEN.values())[c-1]

    
    DESC = f"""
#{"#"*len(trackName)}#
#{trackName}#
#{"#"*len(trackName)}#\n\n\n\n
Tracklist:
"""

    for track in OLEN:
        stamp = str(int(OLEN[track]/60)) + ':'
        if  int(OLEN[track]%60) < 10:
            stamp += "0" + str(int(OLEN[track]%60))
        else:
            stamp+= str(int(OLEN[track]%60))
        DESC += f"{track} - {stamp}\n"



    #--no-credit mode
    if argc > 1 and argv[1] == "--no-credit":
        print("Skipping Credits.")
    else:
        DESC+="\nGenerated with SoundYT by Imalaia3."


        


    input("Press enter to get your description")
    print("======================================")

    print(DESC)



    print("Bye Bye!") #Bye bye!





if __name__ == "__main__":
    run()



### Thanks for reading!
### Feel free to: edit, use, remaster, improve this program. It uses the Gnu GPL licence!
### -Imalaia3
