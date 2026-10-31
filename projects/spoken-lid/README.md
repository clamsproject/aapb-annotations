# Spoken Language Identification

Dataset used for the detection of the language used in scenes in a video.


## Data Format and data processing

Data processing requires a `mappings.py` file, which is not in the repository. There is however a file `sample_mappins.py` which can be copied to `mappings.py`. It is then the responsibility of the developer to replace the keys in the `annotators` table with the correct values.

This can be simplified if we decide that the names of the annotators in the database can be exposed to the whole wide world.


### Raw data

The raw data live in a SQLite data base where the table with annotations has the following schema:

```sql
CREATE TABLE annotation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    clip_id TEXT NOT NULL,
    guid TEXT,
    start_sec REAL,
    end_sec REAL,
    duration_sec REAL,
    video_filename TEXT,
    audio_filename TEXT,
    video_codec_used TEXT,
    label TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    view_count INTEGER DEFAULT 0,
    total_time_sec REAL DEFAULT 0,
    last_visit_started_at REAL,
    is_edit INTEGER DEFAULT 0,
    dataset_name TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    mixed_order TEXT DEFAULT '');
```

Data drop files are created with the `export.py` script, which simply exports the data into CSV files, where each guid gets a CSV file.

```bash
python3 export.py <database_file> <data_drop_directory>
```

Here are the first couple of lines from one such file:

```
"id","username","clip_id","guid","start_sec","end_sec","duration_sec","video_filename","audio_filename","video_codec_used","label","updated_at","view_count","total_time_sec","last_visit_started_at","is_edit","dataset_name","notes","mixed_order"
350,"a4","cpb-aacip-0145bf2c149_0001_4.68_66.10","cpb-aacip-0145bf2c149",4.68,66.1,61.42,"cpb-aacip-0145bf2c149_0001_4.68_66.10.mp4","cpb-aacip-0145bf2c149_0001_4.68_66.10.wav","","eng","2026-04-18 13:34:27",1,0.0,1776519251.5544925,0,"clips_cpb-aacip-0145bf2c149_vadish","",""
351,"a4","cpb-aacip-0145bf2c149_0002_66.26_143.56","cpb-aacip-0145bf2c149",66.26,143.56,77.3,"cpb-aacip-0145bf2c149_0002_66.26_143.56.mp4","cpb-aacip-0145bf2c149_0002_66.26_143.56.wav","","eng","2026-04-18 13:35:09",1,0.0,1776519269.3010435,0,"clips_cpb-aacip-0145bf2c149_vadish","",""
```
 
The `process.py` script takes the data drop files, selects fields needed for the evaluation and normalizes them.

```bash
python3 process.py <data_drop_directory>
```

Results are written two the `golds` directory, existing files for the same guid will be overwritten.


### Gold data

These are CSV files that contain time frames labeled with the language spoken in them.

Fields:

* `start` - start of the frame in `hh:mm:ss.mmm` format
* `end` - end of the frame in `hh:mm:ss.mmm` format
* `scene-label` - language label, one of `yupik`, `samoan`, `spanish`, `english`, `mixed` and `other`

Example:

```
start,end,scene-label
...
00:28:14.590,00:28:32.300,yupik
00:28:32.720,00:28:52.960,yupik
00:28:47.030,00:29:31.500,english
00:28:53.210,00:29:03.010,yupik
00:29:12.270,00:29:31.400,english
00:29:32.710,00:30:52.040,english
...
```
