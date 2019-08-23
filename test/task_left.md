##### Processes
- Creation time
    - /proc/uptime : 1st element, **[uptime]**
    - /proc/[pid]/stat : 22nd element, **[starttime]**
    - creation time = uptime + starttime
    - uptime is in seconds, and starttime is in clock ticks(since linux 2.6, before linux 2.6 it was in jiffies)
- CPU
    - %cpu
- CPU time
    - /proc/[pid]/stat : 14th element, **[utime]**
    - /proc/[pid]/stat : 15th element, **[stime]**
    - cpu time = utime + stime
    - utime and stime are in clock ticks, so should convert to seconds
- Platform
    - 32 bit or 64 bit?
- Digital signatures
    - I CANNOT FIND THIS
- Version
- Product
- Company


##### Modules
- Attributes
- Digital signatures
- Version
    - /proc/[PID]/maps : every line, **[address] [permission] [offset?] [dev?] [inode] [pathname]**
    - pathname contains version information, so i can get version by parsing this, and i already did w/ C
- Product
- Company


##### Startup
- Name
- Location
- Platform
- Status
- Date modified
- Command
- Path
- Digital signatures
- MD5
- Sha256


##### Services
- Key
- Type
- Status
- Startup type
- Command
- Additional info
- Parameters
- Path
- Digital signatures
- Version
- MD5
- Sha256
- User
- Date modified


##### Schedule tasks
- Name
- Location
- Command
- Attributes
- Triggers
- Last run time
- User
- Author
- Priority

comments:  
- in windows, `taskschd.msc` serves these data  
- in linux, `crontab` serves these data  
- `crontab` is defined in IEEE Std 1003.1-2017, so it will not be a problem that some linux systems do not contains this command  
- scheduled task is given by shell script not execution file, so several items should be changed
