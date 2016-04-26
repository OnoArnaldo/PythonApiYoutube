# PythonApiYoutube
Get channel and playlist info

## Usage

###### Basic usage
```
python api_youtube.py [-channel] [-playlist]
```

###### Parameters
-channel:  Creates file `channels.json` with channel id. It is based on the list in the variable `CHANNELS` (line 16).<br>
-playlist: Creates file `playlist.txt` with last video information. It is based on the file `channels.json`.

######  Variable `API_KEY` and  `CHANNELS`
Change the following variables:
```
API_KEY = 'YOUR KEY'

CHANNELS = [
    'videosimprovaveis',
    'nerdologia',
    'Kurzgesagt',
    '1veritasium',
    'minutephysics',
    'xadrezverbal',
    'estevaoslow',
    'Vsauce',
    'braincraftvideo',
    'CienciaTodoDia',
]
```