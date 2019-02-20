# Auto Sync
> Automatically synchronize folders when external drives are mounted.


I wrote this script to easily synchronize data between multiple usb keys.

I use [Launchd](http://www.launchd.info/) to detect when a new volume is been mounted, thanks to the ```start_on_mount.plist``` file positioned in the ```~/Library/LaunchAgents``` folder.
The .plist file than execute ```autosync.sh``` script which uses rsync and unison synchronize the data.

Since this script uses Launchd, it will works only on MacOs.

## Dependencies
- unison
- terminal-notifier

```sh
$ brew install unison terminal-notifier
```





