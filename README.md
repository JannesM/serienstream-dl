# serienstream-dl
A script that downloads videos as mp4 files from s.to without using account creation.

### How to use

0. Install dependencies
```shell
pip install -r requirements.txt
```

1. Open `main.py` and set `BASE_URL` variable to your target series. The url should follow the schema `https://s.to/serie/stream/<YOUR_SERIE>`

2. Execute the script and wait. This might take serveral hours to finish depending on your internet connection

```shell
python main.py
```

### Upcomming features
- [] A clean CLI (maybe a GUI)
- [] More options to specify
  - [] Download single episodes  
  - [] Download single seasons
- [] Proxy chain (although it is working fine without)
- [] Support for animworld.to

### Known Bugs
- [] The script may crash if there is an extra tab next to the seasons (e.g. `Movies`)