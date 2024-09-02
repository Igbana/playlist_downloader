import threading
from pprint import pprint
from pydub import AudioSegment
from bs4 import BeautifulSoup
from pytubefix import YouTube
from youtubesearchpython import VideosSearch
from pytubefix.cli import on_progress

html = './Desktop/Home/htm1.txt'
# output_folder = './Desktop/songs/'

def download(song, links, output_folder):
    try:
        print(f"Searching song: {song}")
        videosSearch = VideosSearch(song, limit = 1)
        result = videosSearch.result()['result'][0]['link']
        print(f"[SUCCESS] Link gotten: {result}")
        downloadSong(result, output_folder)
        links.append(result)
    except Exception as e:
        print(f"[ERROR] {e}")
    print("\n")

def getSongsFromHTML(html, output_folder):
    with open(html, encoding="utf8") as file:
        soup = BeautifulSoup(file, 'html.parser').find_all('div', role = 'row')

    songs = [f"{item.find_all('div', class_ = 'encore-text')[0].text} - {item.find_all('div', class_ = 'encore-text')[1].text}" for item in soup]

    links = []
    for song in songs:
        threading.Thread(target= download, args=(song, links, output_folder)).start()

    
    song_links = dict(zip(songs, links))
    # pprint(song_links, file=open(output_folder+"/output.txt", 'w+'))
    # print(f"[SUCCESS] Written to file {output_folder+"/output.txt"}\n")
    return song_links

def getSongsFromList(list_file, output_folder):
    with open(list_file, encoding="utf8") as file:
        songs = file.readlines()

    links = []
    for song in songs:
        threading.Thread(target= download, args=(song, links, output_folder)).start()
    
    song_links = dict(zip(songs, links))
    # pprint(song_links, file=open(output_folder+"/output.txt", 'w+'))
    # print(f"[SUCCESS] Written to file {output_folder+"/output.txt"}\n")
    return song_links
        

def downloadSong(url, folder_name):
    try:
        yt = YouTube(url, on_progress_callback = on_progress)
        print(f"[PENDING] Downloading {yt.title}\n")
        ys = yt.streams.get_audio_only()
        a = ys.download(mp3=True, output_path=folder_name)
        print(f"[SUCCESS] Downloaded {yt.title}\n")
        # sound = AudioSegment.from_mp3(a)
        # sound.export(a, format="wav")
        print(f"[SUCCESS] Converted {yt.title}\n")
    except:
        print(f"[ERROR] Failed to download {yt.title}")
        # pprint(yt.title, file=open(folder_name+'errors.txt', 'a'))




if __name__ == "__main__":
    getSongsFromHTML(html, output_folder='./Desktop/WORKERS_DINNER')
    # getSongsFromList("./Desktop/Home/Songlist - FYB.txt", output_folder='./Desktop/FYB_DINNER')