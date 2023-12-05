# Configuration files for Nyuu

You can read what all the options do [here](https://github.com/animetosho/Nyuu/blob/master/help-full.txt). 
You don't need to know what each option does. Most likely you'll be good to go by just replacing the dummy values.
You should also consider using a paid BLOCK account for uploading.

## Dummy values

All three of the provided configs below have 3 dummy values that you need to replace before using:

- `"host":               "your.provider.com",`

- `"user":               "coolusername",`

- `"password":           "123password",`

- `"dump-failed-posts":  "/path/to/folder",`

!!! note
    Windows paths must use double backslashes `\\`, e.g, `D:\\path\\to\\folder`.

## Example config files

=== "Private"

    This config obfuscates everything so public indexers can't index it.
    This will be the config you pass to `NYUU_CONFIG_PRIVATE`.

    ```json
    {
        " *** Server Options *** ":0,
        "host":               "your.provider.com",
        "port":               563,
        "ssl":                true,
        "ignore-cert":        false,
        "user":               "coolusername",
        "password":           "123password",
        "connections":        20,
        
        " *** Article Options *** ":0,
        "article-size":       "700K",
        "subject":            "${rand(20)}",
        "comment":            "",
        "from":               "${rand(10)}@${rand(5)}.${rand(3)}",
        "groups":             "alt.binaries.boneless",
        "yenc-name":          "${rand(15)}",
        
        " *** Check Options *** ":0,
        "check-connections":  5,
        "check-tries":        2,
        "check-delay":        "5s",
        "check-retry-delay":  "30s",
        "check-post-tries":   2,
        
        " *** NZB Options *** ":0,
        "out":                "{filename}.nzb",
        "overwrite":          true,
        "nzb-subject":        "[{filenum}/{files}] - \"{filename}\" yEnc ({part}/{parts}) {filesize}",
        
        " *** Other Options *** ":0,
        "skip-errors":        "all",
        "dump-failed-posts":  "/path/to/folder",
        "quiet":              false,
        "token-eval":         false,
        
        " *** UI Options *** ":0,
        "log-time":           true,
        
        " *** Input Files *** ":0,
        "subdirs":            "keep"
        }
    ```

=== "Public"

    This config does not obfuscate anything except `from` and public indexers will index it.
    This will be the config you pass to `NYUU_CONFIG_PUBLIC`.

    ```json
    {
        " *** Server Options *** ":0,
        "host":               "your.provider.com",
        "port":               563,
        "ssl":                true,
        "ignore-cert":        false,
        "user":               "coolusername",
        "password":           "123password",
        "connections":        20,
        
        " *** Article Options *** ":0,
        "article-size":       "700K",
        "comment":            "",
        "from":               "${rand(10)}@${rand(5)}.${rand(3)}",
        "groups":             "alt.binaries.boneless",
        
        " *** Check Options *** ":0,
        "check-connections":  5,
        "check-tries":        2,
        "check-delay":        "5s",
        "check-retry-delay":  "30s",
        "check-post-tries":   2,
        
        " *** NZB Options *** ":0,
        "out":                "{filename}.nzb",
        "overwrite":          true,
        "nzb-subject":        "[{filenum}/{files}] - \"{filename}\" yEnc ({part}/{parts}) {filesize}",
        
        " *** Other Options *** ":0,
        "skip-errors":        "all",
        "dump-failed-posts":  "/path/to/folder",
        "quiet":              false,
        "token-eval":         false,
        
        " *** UI Options *** ":0,
        "log-time":           true,
        
        " *** Input Files *** ":0,
        "subdirs":            "keep"
        }
    ```

=== "Schizo"

    This is an alternative private config that randomizes the length of the randomizer for the schizophrenic.

    !!! note
        Nyuu can accept arbitrary `js` code as input, which we can use to further randomize the built in `${rand(N)}`

        ```js
        ${rand(Math.floor(Math.random()*(30-10)+10))}
        /*
        Format: Math.floor(Math.random()*(MAX-MIN)+MIN)
        Replace the Max and Min values with whatever you feel like it.

        In this example, this creates a random integer between 10 and 30,
        which is then used as an argument for the rand() function to generate
        a random string of that length
        */
        ```

    ```json
    {
    " *** Server Options *** ":0,
    "host":               "your.provider.com",
    "port":               563,
    "ssl":                true,
    "ignore-cert":        false,
    "user":               "coolusername",
    "password":           "123password",
    "connections":        20,

    " *** Article Options *** ":0,
    "article-size":       "700K",
    "subject":            "${rand(Math.floor(Math.random()*(30-10)+10))}",
    "comment":            "",
    "from":               "${rand(Math.floor(Math.random()*(20-10)+10))}@${rand(Math.floor(Math.random()*(10-5)+5))}.${rand(Math.floor(Math.random()*(5-2)+2))}",
    "groups":             "alt.binaries.boneless",
    "yenc-name":          "${rand(Math.floor(Math.random()*(20-10)+10))}",

    " *** Check Options *** ":0,
    "check-connections":  5,
    "check-tries":        2,
    "check-delay":        "5s",
    "check-retry-delay":  "30s",
    "check-post-tries":   2,

    " *** NZB Options *** ":0,
    "out":                "${filename}.nzb",
    "overwrite":          true,
    "nzb-subject":        "[${filenum}/${files}] - \"${filename}\" yEnc (${part}/${parts}) ${filesize}",

    " *** Other Options *** ":0,
    "skip-errors":        "all",
    "dump-failed-posts":  "/path/to/folder",
    "quiet":              false,
    "token-eval":         true,

    " *** UI Options *** ":0,
    "log-time":           true,

    " *** Input Files *** ":0,
    "subdirs":            "keep"
    }
    ```

## Explanation

You can understand what most of the options do [here](https://github.com/animetosho/Nyuu/blob/master/help-full.txt) but I'll explain some of them here:

1. `${rand(N)}`
    - This is a [token](https://github.com/animetosho/Nyuu/blob/master/help-full.txt#L87-L110) accepted by various different options, resulting in a random string `N` characters long
    - You use this to obfuscate uploaded nzbs to prevent them from being taken down by DMCAs and getting indexed by public indexers
    - For private uploads, you should randomize `--subject`, `--from`, and `--yenc-name`
    - For public uploads, it's mostly upto you. If you randomize `--subject` and `--yenc-name`, then it won't get picked up by public indexers like NZBKing but it'll work just as expected if you share the NZB file

2. `--token-eval`
    - This option expands on the tokens like `${rand(N)}`
    - It allows us to input JavaScript
    - For example, you can use it to generate a random number between `max` and `min` using `Math.floor(Math.random() * (max - min) + min)` and then feed that random number to `${rand(N)}`
    - Adjust the `min` and `max` values as you like
    !!! note
          You'll have to change your tokens based on whether `token-eval` is true or false. `{filename}` will work without `token-eval`, but you'll have to change it to `${filename}` to make it work with `--token-eval`

3. `--nzb-subject`
    - This is what will be written inside the `.nzb` file created
    - You do not want to obfuscate this for either private or public since this will only ever be accessible to someone who already has the `.nzb` file
    - You can again use more of the built-in tokens to format this in a way we like
    - I'll be using `[${filenum}/${files}] - "${filename}" yEnc (${part}/${parts}) ${filesize}` format, following the [yenc standard](http://www.yenc.org/yenc-draft.1.3.txt)
    - This results in `[1/7] - &quot;Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv&quot; yEnc (1/483) 346,054,287`

4. `--dump-failed-posts`
    - This option writes any failed posts to a user-defined directory
    - You can then repost these failed posts as needed