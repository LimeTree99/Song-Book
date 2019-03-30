import tkinter as tk
import time
import os
from functools import partial



#constants
bg_colour = 'white'
text_colour = (0,0,0)
menu_colour = 'gray75'
chord_colour = 'blue2'
text_size = 14
line_lim = 34


class Alarm:
    '''
    returns true every time the 'timer' function is called after the given interval
    or after the "alarm" goes off
    '''
    def __init__(self):
        self.old_time = 1
        self.time_ongoing = 0

    def timer(self, interval):
        now = time.time()
        if now - self.old_time >= interval:
            self.old_time = now
            return True
        return False


class Song:
    CHORDS = ['A','B','C','D','E','F','G']
    MODS = ['#','m',' ']
    def __init__(self, path):
        
        with open(path, 'r') as file:
            self.words = file.read()
            
        self.title = os.path.split(path)[-1][:-4]
        self.longest_line = self._longest_line()
        self.height = line_lim
        self.chord_lines = self._find_chords()
        self.alarm = Alarm()
        self.top_line = 0

        self.scroll_speed = 1000
        self.key = None
        self.artist = None
        self.sheet_music = None

    def get_height(self):
        return len(self.words.split('\n'))

    def _longest_line(self):
        lines = self.words.split('\n')
        length = 0
        for i in lines:
            if len(i) > length:
                length = len(i)
        return length

    def _find_chords(self):
        '''
        returns: list of indexes of lines that have chords
        '''
        lis = []
        for i, line in enumerate(self.words.split('\n')):
            line = line.strip()
            line += '  '
            if len(line) > 2:
                if line[0] in Song.CHORDS:
                    if line[1] in Song.MODS:
                        if line[2] == ' ':
                            lis.append(i)

        return lis

    def colour_chords(self, text_box):
        for i in self.chord_lines:
            text_box.tag_add('hold',str(i+1) + '.0', str(i+1)+'.100')
            text_box.tag_config('hold',foreground=chord_colour)

    def scroll(self, root, text_box):
        self.top_line += 1
        text_box.yview(self.top_line)
        root.after(self.scroll_speed, lambda: self.scroll(root, text_box))
        
    def __call__(self):
        return self.words
    
    def __str__(self):
        return self.words

    def __eq__(self, other):
        return self.title == other.title

    def __lt__(self, other):
        return self.title < other.title


class Songlis:
    def __init__(self):
        self.songs = []

    def _insert_any(self, item):
        n = 0
        found = False
        while not found and n < len(self.songs):
            if item < self.songs[n]:
                found = True
            else:
                n += 1
        print(n, item.title)
        self.songs.insert(n, item)

    def insert(self, path):
        song = Song(path)
        self._insert_any(song)

    def populate(self, folder):
        files = []
        for r, d, f in os.walk(folder):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))

        for file in files:
            self.insert(file)        
        
    def __iter__(self):
        for i in self.songs:
            yield i

    def __getitem__(self,i):
        return self.songs[i]
        
    def __str__(self):
        string = ''
        for i in self.songs:
            string += str(i.title) + ', '
        
        return '[' + string[:-2] +']'


# tkinter things
class window(tk.Tk):
    def __init__(self):
        self.current_song = 2
        
        tk.Tk.__init__(self)
        self.configure(bg=bg_colour)

        
        

        # songs
        self.songlist = Songlis()
        self.songlist.populate(os.path.join('songs'))

        # the menus
        self.display_menu()
        
        
        self.display_text()



        #root.after(50, lambda: cc.scroll(root, text))
        
        self.mainloop()
        

    def display_text(self):
        text_left = tk.Text(self, height=self.songlist[self.current_song].height, bd=10, font=("Courier", text_size),relief=tk.FLAT)
        text_left.insert(tk.INSERT, self.songlist[self.current_song])
        self.songlist[self.current_song].colour_chords(text_left)
        
        text_left.yview()

        text_right = tk.Text(self, height=self.songlist[self.current_song].height, bd=10, font=("Courier", text_size),relief=tk.FLAT)
        text_right.insert(tk.INSERT, self.songlist[self.current_song])
        self.songlist[self.current_song].colour_chords(text_right)
        
        text_right.yview(self.songlist[self.current_song].height) 
        
        text_left.grid(row=1, column=0, columnspan=2)
        text_right.grid(row=1, column=2, columnspan=5)
        
    def display_menu(self):
        menubar = tk.Menu(self)
        
        file_menu = tk.Menu(self, tearoff=False)

        choose_song = tk.Menu(self, tearoff=False)
        for i, song in enumerate(self.songlist.songs):            
            choose_song.add_command(label=song.title, command=partial(self.change_song, i))
        
        
        
        file_menu.add_cascade(label='Choose Song', menu=choose_song)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def change_song(self, n):
        self.current_song = n
        self.display_text()

    def change_song_direction(self, up):
        if up:
            self.current_song +=1
        else:
            self.current_song -= 1
        self.display_text()



if __name__ == '__main__':
    pass
    window()
    
