# Uploading to Usenet

!!! note
    This page covers the process of manually uploading a file to usenet. You do not need to know this to use the `juicenet-cli`. This is essentially what it does. This is what I initially wrote when I was first figuring this stuff out and seeing how there's no good guide out there, I've decided to keep it for anyone else trying to figure this stuff out. It's not a good guide because it was never meant to be one, but it's better than nothing.

## Prerequisites

### Linux

1. Install [nvm](https://github.com/nvm-sh/nvm)

    ``` bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
    ```

2. Install [`node`](https://nodejs.org/en)

    ``` bash
    nvm install node
    ```

3. Install [`yencode`](https://github.com/animetosho/node-yencode)

    ``` bash
    npm install yencode
    ```

4. Install [`Nyuu`](https://github.com/animetosho/Nyuu)

    ``` bash
    npm install -g git+https://github.com/animetosho/Nyuu.git --production
    ```
    !!! warning
        You must not install the release [v0.4.1](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1) because it lacks alot of important features that are currently only available on git.

5. Install [`ParPar`](https://github.com/animetosho/ParPar)

    ``` bash
    npm install -g @animetosho/parpar
    ```

### Windows

On Windows, you simply need to grab the following two pre-built binaries:

1. [Nyuu](https://github.com/animetosho/Nyuu)

    !!! warning
        You need version [`a4b1712`](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1). Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/releases/latest) or build it yourself.

2. [ParPar](https://github.com/animetosho/ParPar)

## Getting Started

Let's assume I want to upload this file:

```txt
Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv
```

## Parpar

Parpar is a tool to create `PAR2` files. `PAR2` files are very important because they are parity data that can be used to recover missing or damaged files. This can be done easily with the following command:

``` bash
parpar -s700k --slice-size-multiple=700K --max-input-slices=4000 -r1n*1.2 -R \
--filepath-format basename \
-o "path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv"
```
!!! note
    You must generate PAR2 files for every single file you upload. Uploading stuff to usenet without `PAR2` files is as good as not uploading them.

Apart from being parity data, `PAR2` files also store the path of the file. This then allows downloaders like [SABnzbd](https://sabnzbd.org/) to reconstruct folder structures. This is really handy for stuff like `BDMVs` where the folder structure is important.

In this case, I'm uploading a singular episode where paths don't matter so I'll use `--filepath-format basename` which discards all the paths and only keeps the filename.

This means that:

```
path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv
```
will become
```
Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv
```

`--filepath-format` has more options and might change depending on your use case. You can read more about it [here](parpar-filepath-formats.md). You can read what the other options do [here](https://github.com/animetosho/ParPar/blob/master/help.txt) but they'll mostly remain constant.

After this, you will now have `.par2` files like this:

```txt
.
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol00+01.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol01+02.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol03+04.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol07+08.par2
└── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol15+16.par2
```

## Nyuu

Now that we have the our video file with it's corresponding `.par2` files, we have to upload it. The upload command will look something like this:

``` bash
nyuu -C "/path/to/config.json" \
-o "path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.nzb" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.par2" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol00+01.par2" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol01+02.par2" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol03+04.par2" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol07+08.par2" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol15+16.par2"
```

As you can see, you have to explicitly pass each file and it's `.par2` files to Nyuu and tell it to make a single output `nzb` with `-o "path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.nzb"`. Not really ideal, considering doing this for every episode would be tedious.

Alternatively, you can move the files into a folder as such:

```txt
Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group/
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol00+01.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol01+02.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol03+04.par2
├── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol07+08.par2
└── Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.mkv.vol15+16.par2
```

And, then uploading gets much simpler because you can just pass the folder to Nyuu and it'll make a single nzb out of them:

``` bash
nyuu -C "/path/to/config.json" \
-o "path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group.nzb" \
"path/to/Show.S01E01.BluRay.1080p.FLAC2.0.H.265-Group/"
```

Either of the above commands will start uploading our video and `.par2` files and output the `.nzb` file once it's done but neither of them are ideal. Explicitly specifying each file is tedious and moving files into a folder might break other stuff (e.g. if you're seeding the file in a torrent client).

During the above upload process, your files are uploaded in tiny chunks (`~700KiB`) called `raw articles`. Think of it as `pieces` in torrents. Now some of these `raw articles` can fail to upload for various reasons. Nyuu will put all the failed `raw articles` in the folder defined by `--dump-failed-posts`. You should check this folder and repost the failed `raw articles` later which can be done with the command below:

``` bash
nyuu -C "/path/to/config.json" \
--log-time --skip-errors all \
--delete-raw-posts \
--input-raw-posts "/path/to/your/dump/as/defined/in/config"
```