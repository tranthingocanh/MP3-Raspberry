import os
import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from Tkinter import *
import time
import threading
ALL = N+S+W+E

LIST_SONGS = []
REAL_NAMES = []

INDEX = 0
NUM_SONGS = 0

REPLAY = 0
PAUSED = 0
MUTED = 0
VOLUME = 0.9

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=ALL)
        
        self.var_name = StringVar()
        self.var_clock = StringVar()
        self.var_duration = StringVar()
        self.var_replay = StringVar()
        self.var_mute = StringVar()
        self.var_volume = StringVar()
        
        pygame.init()

        self.create_button_panel()
        self.create_display_panel()

        self.directorychooser()

    def create_button_panel(self):
        
        self.rowconfigure(0, weight=1)
        play_bnt = Button(self, text="Play".format(0))
        play_bnt.grid(row=0, column=0, sticky=ALL)

        self.rowconfigure(1, weight=1)
        pause_bnt = Button(self, text="Pause".format(1))
        pause_bnt.grid(row=1, column=0, sticky=ALL)
        self.rowconfigure(2, weight=1)
        stop_bnt = Button(self, text="Stop".format(2))
        stop_bnt.grid(row=2, column=0, sticky=ALL)
        self.rowconfigure(3, weight=1)
        next_bnt = Button(self, text="Next".format(3))
        next_bnt.grid(row=3, column=0, sticky=ALL)
        self.rowconfigure(4, weight=1)
        prev_bnt = Button(self, text="Previous".format(4))
        prev_bnt.grid(row=4, column=0, sticky=ALL)

        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.var_replay.set("Replay")
        replay_bnt = Button(self, textvariable = self.var_replay)
        replay_bnt.grid(row=5, column=0, sticky=ALL)
        self.columnconfigure(1, weight=1)
        self.var_mute.set("Mute")
        mute_bnt = Button(self, textvariable = self.var_mute)
        mute_bnt.grid(row=5, column=1, sticky=ALL)
        self.columnconfigure(2, weight=1)
        decr_bnt = Button(self, text="-".format(2))
        decr_bnt.grid(row=5, column=2, sticky=ALL)
        self.columnconfigure(3, weight=1)
        incr_bnt = Button(self, text="+".format(3))
        incr_bnt.grid(row=5, column=3, sticky=ALL)
        self.columnconfigure(4, weight=1)
        self.var_volume.set("100")
        volume_bnt = Button(self, textvariable = self.var_volume)
        volume_bnt.grid(row=5, column=4, sticky=ALL)
        self.columnconfigure(5, weight=1)
        shutdown_bnt = Button(self, text = "X".format(5))
        shutdown_bnt.grid(row=5, column=5, sticky=ALL)

        play_bnt.bind("<Button-1>", self.play_song)
        pause_bnt.bind("<Button-1>", self.pause_song)
        stop_bnt.bind("<Button-1>", self.stop_song)
        next_bnt.bind("<Button-1>", self.next_song)
        prev_bnt.bind("<Button-1>", self.prev_song)
        replay_bnt.bind("<Button-1>", self.replay_song)
        mute_bnt.bind("<Button-1>", self.mute_volume)
        decr_bnt.bind("<Button-1>", self.decr_volume)
        incr_bnt.bind("<Button-1>", self.incr_volume)
        volume_bnt.bind("<Button-1>")
        shutdown_bnt.bind("<Button-1>", self.shutdown_app)

    def create_display_panel(self):
        f = Frame(self, bg="skyblue")
        f.grid(row=0, column=1, rowspan=3, columnspan=5, sticky=ALL)
        f.rowconfigure(0, weight=1)
        name_song = Label(f, textvariable = self.var_name, bg="skyblue", font="Verdana 13").grid(row=0, sticky=ALL)
        
        f2 = Frame(self)
        f2.grid(row=3, column=1, rowspan=2, columnspan=5, sticky=ALL)
        f2.rowconfigure(0, weight=1)
        f2.columnconfigure(0, weight=1)
        self.var_clock.set("NGOCANH_THIHONG")
        clock_song = Label(f2, textvariable = self.var_clock, bg="pink", font="DS-Digital 10").grid(row=0, column=0, sticky=ALL)
        f2.columnconfigure(1, weight=1)
        duration_song = Label(f2, textvariable = self.var_duration, bg="green", font="arial 13").grid(row=0, column=1, sticky=ALL)
        return
    
    def directorychooser(self):
        global NUM_SONGS
        listdirectories = os.listdir('/media/pi')
        if len(listdirectories) == 1:
            directory = '/media/pi/' + listdirectories[0]
        else:
            print 'Only 1 USB Devices connected'
        os.chdir(directory)
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                realdir = os.path.realpath(files)
                audio = ID3(realdir)
                REAL_NAMES.append(audio['TIT2'].text[0])
                LIST_SONGS.append(files)
        NUM_SONGS = len(LIST_SONGS)
        if NUM_SONGS == 0:
            self.var_name.set("NO SONGS!!!")
        else:
            pygame.mixer.init()
            self.var_name.set(self.song_title_filter())

            audio = MP3(LIST_SONGS[INDEX])
            total_length_audio = audio.info.length
            timeformat = time.strftime("%H:%M:%S", time.gmtime(total_length_audio))
            self.var_duration.set(timeformat)
    
    def song_title_filter(self):
        if len(REAL_NAMES[INDEX])>22:
            name=REAL_NAMES[INDEX][0:20]+'...'
            pass
        else:
            name=REAL_NAMES[INDEX]
            pass
        return name  

    def time_thread(self):
        threading.Thread(target=self.update_time_).start()
        return
    
        
    def update_time_(self):
        while True:
            time_format = time.strftime("%H:%M:%S", time.gmtime(pygame.mixer.music.get_pos()/1000))
            self.var_clock.set(time_format)
            pygame.time.Clock().tick(30)
        
    def play_song(self, *args, **kwargs):
        global INDEX
        global REPLAY
        
        self.var_name.set(self.song_title_filter())
        
        if self.var_replay.get() == "Unreplay":
            self.var_replay.set("Replay")
            REPLAY = 0
        
        audio = MP3(LIST_SONGS[INDEX])
        total_length_audio = audio.info.length
        
        timeformat = time.strftime("%H:%M:%S", time.gmtime(total_length_audio))
        self.var_duration.set(timeformat)

        pygame.mixer.music.load(LIST_SONGS[INDEX])
        pygame.mixer.music.play()
        self.time_thread()

    def next_song(self, *args, **kwargs):
        global INDEX
        INDEX += 1
        if INDEX == NUM_SONGS:
            INDEX = 0
        self.play_song()

    def prev_song(self, *args, **kwargs):
        global INDEX
        INDEX -= 1
        if INDEX == -1:
            INDEX = NUM_SONGS -1
        self.play_song()


    def stop_song(self, *args, **kwargs):
        self.var_name.set("[STOP] " + self.song_title_filter())
        pygame.mixer.music.pause()
        pygame.mixer.music.stop()
        

    def pause_song(self, *args, **kwargs):
        global PAUSED
        if PAUSED:
            self.var_name.set(self.song_title_filter())
            pygame.mixer.music.unpause()
            PAUSED = 0
        elif PAUSED == 0:
            self.var_name.set("[PAUSE] " + self.song_title_filter())
            pygame.mixer.music.pause()
            PAUSED = 1

    
    def replay_song(self, *args, **kwargs):
        global REPLAY
        if REPLAY == 0:
            self.var_replay.set("Unreplay")
            self.var_name.set(self.song_title_filter())
            pygame.mixer.music.load(LIST_SONGS[INDEX]) 
            pygame.mixer.music.play(-1) #Playing a song infinitely
            self.time_thread()
            REPLAY = 1
        else:
            self.var_replay.set("Replay")
            self.play_song()
            REPLAY = 0
    
    def mute_volume(self, *args, **kwargs):
        global MUTED
        if MUTED == 0:
            pygame.mixer.music.set_volume(0)
            self.var_mute.set("Unmute")
            MUTED = 1
        elif MUTED:
            pygame.mixer.music.set_volume(VOLUME)
            self.var_mute.set("Mute")
            MUTED = 0

    # option volume 0 to 1.0
    def decr_volume(self, *args, **kwargs):
        global VOLUME
        global MUTED
        if VOLUME > 0.2:
            VOLUME = VOLUME - 0.1
        if self.var_mute.get() == "Unmute":
            self.var_mute.set("Mute")
            MUTED = 0
        pygame.mixer.music.set_volume(VOLUME)
        self.var_volume.set(int(VOLUME*100))
      
    def incr_volume(self, *args, **kwargs):
        global VOLUME
        global MUTED
        if VOLUME < 1:
            VOLUME = VOLUME + 0.1
        if self.var_mute.get() == "Unmute":
            self.var_mute.set("Mute")
            MUTED = 0
        pygame.mixer.music.set_volume(VOLUME)
        self.var_volume.set(int(VOLUME*100))
    def shutdown_app(self, *args):
        pygame.quit()
        #sys.exit()
        os.system("shutdown -h now")

root = Tk()
root.title("MP3 _ NGOCANH_THIHONG")#You can set the geometry attribute to change the root windows size
#root.geometry("480x320") #You want the size of the app to be 480x320
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.resizable(0, 0) #Don't allow resizing in the x or y direction
app = Application(master=root)                
app.mainloop()
