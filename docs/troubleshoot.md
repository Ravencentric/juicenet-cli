This page contains some of the errors that the script might throw at you and how to solve them.

### No such file: `{filename}`

`juicenet` was unable to find your `juicenet.yaml` config file. You can read about how to specify your config [here](configuration.md#loading-the-config-file)

### `{key}` is missing in `{conf_path}`

You are missing a required value in `juicenet.yaml`. Read about the config [here](configuration.md)

### Please check your Nyuu config and ensure it is valid
This just means your nyuu config isn't a valid JSON and most likely the cause is how you've entered the paths. Look at the examples below

On Linux:
```json
  "dump-failed-posts":  "/path/to/folder",
```
On Windows:
```json
  "dump-failed-posts":  "C:\\Users\\raven\\path\\to\\folder",
```
Note how I used `\\` instead of `\`. This is very important on Windows. Won't work if you used a single `\`.

### No matching glob pattern or files with the given extension found in the path

Script couldn't find any files with the defined extensions or glob pattern. This could be simply because the folder you gave doesn't have those files, the folder itself doesn't exist, or you've entered the wrong extensions/glob pattern.

### dump-failed-posts is not defined in your Nyuu config

When you upload stuff to usenet, it gets split into several small chunks called `articles` (equivalent of pieces in bittorrent). Sometimes these `articles` will fail to post. You have the define path to a folder in your [nyuu config](nyuu-config-files.md) with `dump-failed-posts`. This is where those failed articles will get dumped and the script will try to repost them next run.

### Failed to repost {raw_final_count} articles. Either retry or delete these manually

As stated above, the script tries to repost the failed articles on each run. Sometimes they might fail again and again and again... You get the idea. In this case consider those articles dead and empty your `dump-failed-posts` folder.