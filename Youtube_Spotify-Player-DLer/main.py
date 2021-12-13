from tkinter import *
from PIL import ImageTk, Image     # need install Pillow
from tkinter import scrolledtext
from tkinter import messagebox
from youtubesearchpython import VideosSearch  # need install youtube-search-python
import youtube_dl             # need install youtube-dl
from pytube import Playlist   # need install pytube
import requests
import re
import spotipy                  # need install spotipy
from spotipy.oauth2 import SpotifyOAuth
from playsound import playsound
import os   # directory/ location
import random
import pygame
from tkinter.filedialog import askdirectory

class Music_Downloader_Player():
    def __init__(self):
        self.yt_api_key = "AIzaSyA0248NWqX0bHMXN0MecaukU-eZi38lElc"  # Youtube
        self.client = "181f8a45131a45df994a1761c4c07b28"
        self.client_secret = "2cc198a735974b288a8cf4e8346000a4"
        self.redirect_uri = "http://localhost:443"
        self.win = Tk()
        self.win.resizable(0, 0)
        self.win.geometry("1200x672")
        self.win.iconbitmap("image/icon.ico")
        self.canvas1 = Canvas(self.win, width=1200, height=672)
        self.canvas1.pack(fill="both", expand=True)
        self.menu()
        self.win.mainloop()

    """ Page 1 """
    def menu(self):
        self.canvas1.delete("all")  # remove all widgets
        self.win.title("Music Player and Downloader")
        bg = PhotoImage(file="image/bg.png")
        self.canvas1.create_image(0, 0, image=bg, anchor="nw")

        """ Add image as image """
        title_img = ImageTk.PhotoImage(Image.open("image/title.png"))
        self.canvas1.create_image(800, 50, image=title_img, anchor="nw")

        """ Add images as button"""
        down_but = PhotoImage(file="image/down_but.png")
        list_but = PhotoImage(file="image/list_but.png")
        exit_but = PhotoImage(file="image/exit_but.png")

        """ Add Label """
        self.canvas1.create_text(890, 250, text="Music Downloader & Player", font=("Debby", 55), fill="Black")
        self.canvas1.create_text(860, 530, text="For entertainment purpose only", font=("Debby", 25), fill="red")

        """ Add Image """
        down_but = PhotoImage(file="image/down_but.png")
        list_but = PhotoImage(file="image/list_but.png")
        exit_but = PhotoImage(file="image/exit_but.png")

        """ Add Button """
        exit = Button(self.win, image=exit_but, command=quit, highlightthickness=0, bd=0)
        down_button = Button(self.win, image=down_but, command=self.download_page, highlightthickness=0, bd=0)
        listen_button = Button(self.win, image=list_but, command=self.listen_music, highlightthickness=0, bd=0)

        """ Display Buttons """
        exit_canvas = self.canvas1.create_window(810, 570, anchor="nw", window=exit)
        down_img_button_canvas = self.canvas1.create_window(810, 330, anchor="nw", window=down_button)
        listen_img_button_canvas = self.canvas1.create_window(810, 420, anchor="nw", window=listen_button)

        self.win.mainloop()


    """ Page 2 """
    def download_page(self):
        """ Basic settings """
        self.win.title("Music Downloader")
        self.canvas1.delete("all")  # remove all widgets
        bg1 = PhotoImage(file="image/bg1.png")
        self.canvas1.create_image(0, 0, image=bg1, anchor="nw")

        """ Add Entry """
        self.enter_url = Entry(self.canvas1, width=70)
        self.canvas1.create_window(350, 60, window=self.enter_url)
        self.enter_url.insert(0, "Enter your link here")

        """ Add Label """
        self.canvas1.create_text(350, 90, text="Choose the source of your music: ", font=("HanWangZonYi", 15))

        """ Add scrollbar """
        self.scr = scrolledtext.ScrolledText(self.win, width=80, height=32, wrap=WORD)
        self.canvas1.create_window(350, 420, window=self.scr)

        """ Add text """
        self.text = Text(self.scr, font="Calibri 11")
        self.text.pack(fill="both", expand=True)
        self.text.insert("end", "In the first time to use, you are required to login the spotify to finish authentication if you choose spotify url,\n\n"
                                "You can use the following username and passwords:\n"
                                "username:   useforspotifytesting@gmail.com\n"
                                "password:   Spotify4test")

        """ Add Image as Button """
        spotify_but = PhotoImage(file="image/spot_but.png")
        yt_but = PhotoImage(file="image/yt_but.png")
        exit2_but = PhotoImage(file="image/exit2_but.png")
        list2_but = PhotoImage(file="image/list2_but.png")

        """ Add Button """
        exit2 = Button(image=exit2_but, command=self.exit_, highlightthickness=0, bd=0)
        youtube_button = Button(self.win, image=yt_but, command=self.youtube_info, highlightthickness=0, bd=0)
        spotify_button = Button(self.win, image=spotify_but, command=self.spotify_info, highlightthickness=0, bd=0)
        listen2_button = Button(self.win, image=list2_but, command=self.listen_music, highlightthickness=0, bd=0)

        """" Display """
        youtube_convas = self.canvas1.create_window(221, 142, window=youtube_button)
        spotify_convas = self.canvas1.create_window(480, 140, window=spotify_button)
        exit_canvas = self.canvas1.create_window(940, 600, anchor="nw", window=exit2)
        listen_img_button_canvas = self.canvas1.create_window(690, 600, anchor="nw", window=listen2_button)

        """ Execute """
        self.win.mainloop()

    def youtube_info(self):
        self.text.delete(1.0, END)
        self.scr.delete(1.0, END)  # clear the text box in scrollbar

        self.url = self.enter_url.get()
        if "youtube" and "www." not in self.url:
            self.wrong = self.canvas1.create_text(350, 180, text="Incorrect youtube link!", font=("Chizz", 15), fill='red')
            self.win.after(1500, self.canvas1.delete, self.wrong)  # delete message after 1.5 sec

        else:
            if ("&list=") in self.url:
                self.status = "list"
                id = self.url.split("&list=")[-1]
                self.yt_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId={id}&key={self.yt_api_key}&maxResults=50"

            elif ("watch?v=") in self.url:
                self.status = "single"
                id = self.url.split("watch?v=")[-1]
                self.yt_url = f"https://www.googleapis.com/youtube/v3/videos?id={id}&fields=items(snippet(title))&part=snippet&key={self.yt_api_key}"

            self.run_url = self.url
            res = requests.get(self.yt_url)
            self.json = res.json()
            self.youtube_downloader()

    def youtube_downloader(self):
        self.working = self.canvas1.create_text(350, 180, text="Downloading ... Just let this app along", font=("Chizz", 15), fill='red')
        self.location = "download/"
        self.ydl_opts = {'outtmpl': f'{self.location}%(title)s.%(ext)s',
                    'format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    }

        if "&list=" in self.run_url:
            playlist = Playlist(self.run_url)
            playlist._video_regex=re.compile(r'\"url\":\"(/watch\?v=[\w-]*)')
            for i, playlist_url in enumerate(playlist.video_urls):
                try:
                    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                        ydl.download([playlist_url])
                        info_dict = ydl.extract_info(playlist_url, download=False) # Only want to extract the info
                        video_title = info_dict.get('title', None) # extract the tilt of music
                        self.text.insert("end", f'{i}: {video_title}' + "\t\n")
                except:
                    self.text.insert("end", f'Error in downloading following song  {i}: {video_title}' + "\n")

            self.text.insert("end", "\n\nFinish Download\n\n")


        elif "watch?v=" in self.run_url:
            try:
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    info_dict = ydl.extract_info(self.run_url)
                    ydl.download([self.run_url])
                    for i in self.json["items"]:
                        self.text.insert("end", f'{i["snippet"]["title"]}' + "\n")  # Showing the test inside the Textbox
            except:
                self.text.insert("end", f'Error in downloading following song: {i["snippet"]["title"]}' + "\n")

            self.text.insert("end", "\n\nFinish Download")


        # When finish downloading
        self.win.after(0, self.canvas1.delete, self.working)
        self.finish = self.canvas1.create_text(350, 180, text="Finish Download !!!!", font=("Chizz", 15), fill='green')
        self.win.after(3000, self.canvas1.delete, self.finish)

        messagebox.showinfo("Download info", "Your download is complete !")   # title; content

    def spotify_info(self):
        self.url = self.enter_url.get()
        if "open.spotify" not in self.url:
            self.wrong = self.canvas1.create_text(350, 180, text="Incorrect Spotify link!", font=("Chizz", 15), fill='red')
            self.win.after(1500, self.canvas1.delete, self.wrong)  # delete message after 1.5 sec

        else:
            self.play_list_downloader()

    def play_list_downloader(self):
        self.working = self.canvas1.create_text(350, 180, text="Downloading ... Just let this app along", font=("Chizz", 15), fill='red')
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client, client_secret=self.client_secret, redirect_uri=self.redirect_uri))
        result = sp.playlist(self.url)
        for item in result["tracks"]["items"]:
            for k1, v1 in item.items():
                if k1 == "track":
                    for k2, v2 in v1.items():
                        # Song name
                        if k2 == "album":
                            for k3, v3 in v2.items():
                                if k3 == "images":
                                    img_url = v3[0]["url"]
                        elif k2 == "name":
                            videosSearch = VideosSearch(v2, limit=1)
                            for i, item in enumerate(videosSearch.result()["result"]):
                                item["title"] = item["title"].replace("/", "_")
                                self.location = "download/"
                                self.ydl_opts = {'outtmpl': f'{self.location}%(title)s.%(ext)s',
                                                 'format': 'bestaudio',
                                                 'postprocessors': [{
                                                     'key': 'FFmpegExtractAudio',
                                                     'preferredcodec': 'mp3',
                                                     'preferredquality': '192',
                                                 }],
                                                 }
                                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                                    ydl.download([item["link"]])
                                    self.text.insert("end", f'{i}: {item["title"]}' + "\n")

        self.win.after(0, self.canvas1.delete, self.working)
        self.finish = self.canvas1.create_text(350, 180, text="Finish Download !!!!", font=("Chizz", 15), fill='green')
        self.win.after(3000, self.canvas1.delete, self.finish)

        self.text.insert("end", "\n\nFinish Download")
        messagebox.showinfo("Download info", "Your download is complete !")  # title; content

    def exit_(self):
        self.win.destroy()

    """ Page 3 """
    def listen_music(self):
        self.pygame = pygame
        self.pygame.init()
        """ Background """
        self.win.title("Music Player")
        self.canvas1.delete("all")  # remove all widgets
        bg2 = PhotoImage(file="image/bg2.png")
        self.canvas1.create_image(0, 0, image=bg2, anchor="nw")

        def play():
            playsound("download/")

        # making a button which trigger the function so sound can be playeed

        """ Add image """
        play_but = PhotoImage(file="image/play_but.png")
        bar = PhotoImage(file="image/bar.png")
        next_but = PhotoImage(file="image/next_but.png")
        prev_but = PhotoImage(file="image/prev_but.png")
        p_but = PhotoImage(file="image/p_but.png")
        lib_but = PhotoImage(file="image/lib_but.png")
        fav_but = PhotoImage(file="image/fav_but.png")
        add_playlst_but = PhotoImage(file="image/add_playlst_but.png")
        del_but = PhotoImage(file="image/del_but.png")
        album_but = PhotoImage(file="image/album_but.png")
        queue_but = PhotoImage(file="image/queue_but.png")
        repeat_one_but = PhotoImage(file="image/repeat_one_but.png")
        search_but = PhotoImage(file="image/search_but.png")
        repeat_but = PhotoImage(file="image/repeat_but.png")
        shuffle_but = PhotoImage(file="image/shuffle_but.png")
        player_icon = ImageTk.PhotoImage(Image.open("image/player_icon.png"))
        self.canvas1.create_image(600, 630, image=bar)
        self.canvas1.create_image(400, 90, image=player_icon, anchor="nw")

        """ Add Button """
        self.play_button = Button(self.win, image=play_but, relief=GROOVE, highlightthickness=0, bd=0,
                                  command=self.playing)
        self.play_button_forget = Button(self.win, image=play_but, relief=GROOVE, highlightthickness=0, bd=0,
                                         command=lambda: self.play_button.pack_forget())
        next_button = Button(self.win, image=next_but, relief=GROOVE, highlightthickness=0, bd=0, command=self.next_song)
        prev_button = Button(self.win, image=prev_but, relief=GROOVE, highlightthickness=0, bd=0, command=self.prev_song)
        self.p_button = Button(self.win, image=p_but, relief=GROOVE, highlightthickness=0, bd=0, command=self.pausing)
        self.lib_button = Button(self.win, image=lib_but, relief=GROOVE, highlightthickness=0, bd=0,
                                 command=self.open_file)
        fav_button = Button(self.win, image=fav_but, relief=GROOVE, highlightthickness=0, bd=0, command=self.fav_song)
        del_button = Button(self.win, image=del_but, relief=GROOVE, highlightthickness=0, bd=0)
        add_playlst_button = Button(self.win, image=add_playlst_but, relief=GROOVE, highlightthickness=0, bd=0)
        album_button = Button(self.win, image=album_but, relief=GROOVE, highlightthickness=0, bd=0)
        queue_button = Button(self.win, image=queue_but, relief=GROOVE, highlightthickness=0, bd=0)
        repeat_button = Button(self.win, image=repeat_but, relief=GROOVE, highlightthickness=0, bd=0)
        repeat_one_button = Button(self.win, image=repeat_one_but, relief=GROOVE, highlightthickness=0, bd=0)
        search_button = Button(self.win, image=search_but, relief=GROOVE, highlightthickness=0, bd=0)
        shuffle_button = Button(self.win, image=shuffle_but, relief=GROOVE, highlightthickness=0, bd=0)

        """ Display Button """
        self.play = self.canvas1.create_window(600, 630, window=self.play_button)  # Great
        self.canvas1.create_window(660, 630, window=next_button)
        self.canvas1.create_window(540, 630, window=prev_button)
        self.canvas1.create_window(880, 630, window=self.lib_button)
        self.canvas1.create_window(940, 630, window=fav_button)
        self.canvas1.create_window(1060, 630, window=del_button)
        self.canvas1.create_window(1120, 630, window=add_playlst_button)
        self.canvas1.create_window(50, 630, window=album_button)
        self.canvas1.create_window(110, 630, window=queue_button)
        self.canvas1.create_window(290, 630, window=repeat_one_button)
        self.canvas1.create_window(350, 630, window=repeat_button)
        self.canvas1.create_window(410, 630, window=search_button)
        self.canvas1.create_window(820, 630, window=shuffle_button)

        """ Execute """
        self.win.mainloop()

    def open_file(self):
        self.song_lst = []
        directory = askdirectory()
        for file in os.listdir(directory):
            if file.endswith("mp3"):
                self.song_lst.append(file)  # song list
                self.sit = "finish loading"

        """ Song list """
        check = self.canvas1.create_text(600, 100, text=f"Detected file: {len(self.song_lst)}", font=("Poiret One", 15),
                                         fill="Black")
        self.win.after(1500, self.canvas1.delete, check)

    """ pygame exexute here """

    def playing(self):  # Suppose to play all songs
        """ Set conditions """
        # 1. When finished loading the song list > random song
        if self.song_lst:
            if self.sit == "finish loading":
                random.shuffle(self.song_lst)
                global i, song
                for i, song in enumerate(self.song_lst):
                    self.current_song = i
                    self.pygame.mixer.music.load(f"download/{song}")  # load
                    self.pygame.mixer.music.play()  # play
                    self.sit = "pause"

            # hide the play button and show the pause button
            self.canvas1.create_text(600, 500, text=f"Now Playing: {song.strip('.mp3')}", font=("Poiret One", 20), fill="Black")
            self.canvas1.delete(self.play)
            self.pause = self.canvas1.create_window(600, 630, window=self.p_button)  # pause the
            self.pygame.mixer.music.unpause()

    def pausing(self):
        # hide the pause button and show the play button
        self.canvas1.delete(self.pause)
        self.pygame.mixer.music.pause()
        self.play = self.canvas1.create_window(600, 630, window=self.play_button)

    def next_song(self):
        for i_, song_ in enumerate(self.song_lst):
            if self.current_song != (len(self.song_lst) - 1):
                if i_ != (self.current_song + 1):
                    continue
                self.pygame.mixer.music.load(f"download/{song}")  # load
                self.pygame.mixer.music.play()  # play
                self.sit = "pause"

    def prev_song(self):
        for i_, song_ in enumerate(self.song_lst):
            if self.current_song != 0:
                if i_ != (self.current_song - 1):
                    continue
                self.pygame.mixer.music.load(f"download/{song}")  # load
                self.pygame.mixer.music.play()  # play
                self.sit = "pause"

    def fav_song(self):
        self.finish = self.canvas1.create_text(350, 200, text="G", font=("BonusHearts", 500), fill='red')
        self.win.after(1300, self.canvas1.delete, self.finish)

GUI = Music_Downloader_Player()

