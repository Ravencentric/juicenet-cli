!!! note
    This page covers the usage of the `--filepath-format` option in ParPar. You do not need to know this to use `juicenet`. I wrote this after testing all of the filepath formats to better understand them myself.



Filepath format is what allows us to either discard paths for singular files or preserve complex folder structures such as those in BDMVs when uploading to Usenet without the need of RAR. PAR2 files can store the folder structure which can then be used by SABnzbd to reconstruct the folder structure from the PAR2 files completely eliminating the need to RAR them. [What's wrong with RAR?](https://github.com/animetosho/Nyuu/wiki/Stop-RAR-Uploads)

ParPar's help text on `--filepath-format`:

``` shell
  -f,  --filepath-format     How to format input file paths, can be either:
                                 basename: discard paths
                                 keep: retain full paths as specified
                                 common: discard common parts of paths; falls
                                         back to basename if there is no common
                                         path
                                 outrel: path computed relative to output
                                 path: path computed relative to that specified
                                       in `--filepath-base`
                             Default is `common`, or `path` if `--filepath-base`
                             is specified.
  -B,  --filepath-base       The base path to use when computing paths when
                             `--filepath-format=path` is used.
                             Default is `.` (i.e. current working directory)
```

## Filepath Formats

I'll be using `[EAC][170215] Porter Robinson & Madeon - SHELTER` BDMV as an example to better demonstrate what I'm talking about. This is located `D:\topdir\subdir`. These details are important so remember them.

```txt
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00001.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00002.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00003.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\MovieObject.bdmv
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\PLAYLIST\00000.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\PLAYLIST\00001.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\PLAYLIST\00002.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\index.bdmv
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\CLIPINF\00000.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\CLIPINF\00001.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\CLIPINF\00002.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\CLIPINF\00003.clpi
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\MovieObject.bdmv
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\PLAYLIST\00000.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\PLAYLIST\00001.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\PLAYLIST\00002.mpls
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\STREAM\00000.m2ts
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\STREAM\00001.m2ts
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\STREAM\00003.m2ts
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\index.bdmv
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\CERTIFICATE\BACKUP\id.bdmv
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\CERTIFICATE\id.bdmv
```

### `--filepath-format basename`

- Simply keeps the filename and discards all path.
- NOT affected by either `-o` or input path.

Example:

``` shell
parpar [args] --filepath-format basename -o "[EAC][170215] Porter Robinson & Madeon - SHELTER" "[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
00000.1.clpi
00000.1.mpls
00000.clpi
00000.m2ts
00000.mpls
00001.1.clpi
00001.1.mpls
00001.clpi
00001.m2ts
00001.mpls
00002.1.clpi
00002.1.mpls
00002.clpi
00002.mpls
00003.1.clpi
00003.clpi
00003.m2ts
MovieObject.1.bdmv
MovieObject.bdmv
id.1.bdmv
id.bdmv
index.1.bdmv
index.bdmv
```

As you can see it simply discarded all paths and added numbers to duplicate filenames.

### `--filepath-format keep`

- Stores the complete input path as passed to parpar.
- NOT affected by `-o` but affected by the input path as it'll keep whatever you pass.

Example 1:

``` shell
parpar [args] --filepath-format keep -o "anything-goes-here" "[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

Example 2:

``` shell
parpar [args] --filepath-format keep -o "anything-goes-here" "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi"
```

Result:

``` shell
D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

### `--filepath-format common`

- Discards part of the path that's common across ALL the files.
- NOT affected by `-o` but affected by the input path

Example:

``` shell
parpar [args] --filepath-format common -o "anything-goes-here" "[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
BDMV\BACKUP\CLIPINF\00000.clpi
```

Explanation:
Look at the BDMV directory structure provided at the top and see how `[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\` is common across all the files. This common part gets discarded. This is the **DEFAULT** behavior.

### `--filepath-format outrel`

- Stores path relative to the output (`-o`)
- NOT affected by the input path as all path is calculated relative to whatever you pass in `-o`

Example 1:

``` shell
parpar [args] --filepath-format outrel -o "[EAC][170215] Porter Robinson & Madeon - SHELTER" "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

Explanation:
I passed `"[EAC][170215] Porter Robinson & Madeon - SHELTER"` as my output path which means it's in the current working directory and parpar will store the path relative to my output path. This is inclusive, which means the output directory will be included.

Example 2:

``` shell
parpar [args] --filepath-format outrel -o "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER" "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

Explanation:
I passed `"D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER"` as my output path. This is an absolute path and in this case parpar will store the path relative to final directory in the path which is `[EAC][170215] Porter Robinson & Madeon - SHELTER` located in `D:\topdir\subdir`. Again this is inclusive, which means the final directory will be included. The results end up being identical to Example 1.

Example 3:

``` shell
parpar [args] --filepath-format outrel -o "C:\test\[EAC][170215] Porter Robinson & Madeon - SHELTER" "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

Explanation: In this case output directory is in a different drive and so there's no relative path possible to our files, so parpar stores the absolute path when there's no possible relative path.

### `--filepath-format path`

- Stores input path relative to the path passed to `--filepath-base`.
- NOT affected by `-o`

My current working directory: `D:\topdir`

Example:

``` shell
parpar [args] --filepath-base "D:\topdir\subdir" --filepath-format path -o "arbitrary\path\[EAC][170215] Porter Robinson & Madeon - SHELTER" "D:\topdir\subdir\[EAC][170215] Porter Robinson & Madeon - SHELTER"
```

Result:

``` shell
[EAC][170215] Porter Robinson & Madeon - SHELTER\BDROM\PORTER_ROBINSON_MADEON_SHELTER\BDMV\BACKUP\CLIPINF\00000.clpi
```

Explanation:
As you can see the path being stored here starts from `[EAC][170215] Porter Robinson & Madeon - SHELTER` because my `filepath-base` was `D:\topdir\subdir` which was used to calculate the relative path from base to input and my working directory got ignored entirely. Just like `outrel`, when there's no relative path to be found, it'll store the absolute path.