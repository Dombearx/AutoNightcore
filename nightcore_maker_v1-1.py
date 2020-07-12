import nightcore as nc
import os 
from os import path

# Nowy przyrowstek do nazwy utworu 
new_name_suffix="_nightcored"
# Format audio 
audio_format=".mp3"
# Speed w procentach 
song_speed = 110 
# Peach 
song_tones = 1
# Semi_tones ? 
song_semitones = 0 
# Octaves ? 
song_octaves = 0


# Na ten moment wykluczone są tylko utwory ktore maja w nazie nightcore, trzeba wykluczyc te utwory i te dla ktorych jest juz zrobiony nightcore 


class music_editor:

    # Przerabianie muzyki, parametry podane na poczatku programu 
    def make_nightcore(self,song_name):
            
        if audio_format in song_name:

            new_song_name = song_name[:-4] + new_name_suffix + audio_format

            # Predkosc, pobierany jest utwor z listy, nazwa podmieniana 
            print ("Nazwa obecnego utworu : " + new_song_name) 
            nc_audio = song_name @ nc.Percent(song_speed)
            # Export gotowego audio 
            nc_audio.export(new_song_name)
            
            # Peach, pobierana jest nazwa utrowu podana wczesniej, utwor jest potem podmieniany 
            nc_audio = new_song_name @ nc.Tones(song_tones) 
            # Export gotowego audio 
            nc_audio.export (new_song_name)
            
            
            nc_audio = new_song_name @ nc.Semitones (song_semitones)
            # Export gotowego audio 
            nc_audio.export (new_song_name)

            nc_audio = new_song_name @ nc.Octaves (song_octaves)
            # Export gotowego audio 
            nc_audio.export(new_song_name)

                
    # Sprawdzanie czy plik nie ma juz swojej wersji nightcoru w obecnym katalogu  
    def check_if_file_not_nightcored(self):

        # Wylistowanie plikow 
        list_of_files=os.listdir()

        self.list_to_make_nightcore=[]
        self.list_of_files_without_suffix=[]

        # Ostateczna lista do zrobienia Nightcoru 
        self.list_single_without_suffix=[]
        
        # Usuniecie suffixu dla kazdego wyrazu w liscie 
        for current_file_with_suffix in list_of_files:
            # Usuniecie suffixu z obecnej nazwy
            current_file_without_suffix=current_file_with_suffix.replace(new_name_suffix, "")
            # Dodanie pliku z nazwa bez suffixu do nowej listy 
            self.list_of_files_without_suffix.append(current_file_without_suffix)
        
        # Oddzielenie podwojnych plikow 
        for current_double_file in self.list_of_files_without_suffix:
            # Jezeli nazwa pliku wystepuje tylko raz i jego rozszerzenie zgadza sie z wyszukiwanym 
            if self.list_of_files_without_suffix.count(current_double_file) == 1 and audio_format in current_double_file:
                # Dodanie do playlisty plikow wystepujacych tylko raz z nazwa wyszukiwanego rozszerzenia 
                self.list_single_without_suffix.append(current_double_file) 
                
        # Wypisanie listy plikow ktore bedziemy przerabiac
        print (self.list_single_without_suffix)

    
    # Calosciowe wykonanie Nightcoru 
    def final_nightcore_make(self):
        # Listowanie plików w katalogu, przypisnaie listy do zmiennej 
        self.check_if_file_not_nightcored()

        # Dla każdego wylistowanego pliku zrob nightcore  
        for current_file_name in me.list_single_without_suffix:
            me.make_nightcore(current_file_name)

if __name__ == "__main__":
    # Klasy 
    me=music_editor()

    # Calosciowe wykonanie Nightcoru 
    me.final_nightcore_make()