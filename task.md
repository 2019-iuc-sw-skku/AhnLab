##### Processes
- Name
    - name of the process?
    - /proc/[pid]/status : 1st line, **Name: [name]**
    - /proc/[pid]/stat : 2nd element, **([name])**
    - there is no 'name' section in top or ps
- Attributes
    - is it suspended or not? idk
    - /proc/[pid]/status : 3rd line, **State: [status] (status\_explanation)**
    - /proc/[pid]/stat : 3rd element, **[status]**
    - in linux, it is about process life cycle, not if it is suspended
- PID
    - process id
    - /proc : read all directories, and get the name only if the directory name is number and /proc/[directory]/status
    - can do with opendir() and readdir() in C/C++
- PPID
    - parent process id
    - /proc/[pid]/status : 7th line, **PPid: [ppid]**
    - /proc/[pid]/stat : 4th element, **[PPid]**
- Threads
    - /proc/[pid]/status : 34th line, **Threads: [threads]**
- Base priority
    - actually, there are two independent priority in linux: priority and nice
    - priority
        - related to real-time scheduling policy
        - /proc/[pid]/stat : 18th element, **[priority]**
    - nice
        - /proc/[pid]/stat : 19th element, **[nice]**
- Creation time
    - /proc/uptime : 1st element, **[uptime]**
    - /proc/[pid]/stat : 22nd element, **[starttime]**
    - creation time = uptime + starttime
    - uptime is in seconds, and starttime is in clock ticks(since linux 2.6, before linux 2.6 it was in jiffies)
- CPU
    - ~~cpu number where the process is working?~~
    - what is this?
- CPU time
    - /proc/[pid]/stat : 14th element, **[utime]**
    - /proc/[pid]/stat : 15th element, **[stime]**
    - cpu time = utime + stime
    - utime and stime are in clock ticks, so should convert to seconds
- Platform
    - 32 bit or 64 bit?
- Memory working set
    - memory size of the process?
    - /proc/[pid]/statm : 1st element, **[memsize]**
- Page faults
    - /proc/[pid]/stat : 10th element, **[minorfault]**
    - /proc/[pid]/stat : 11th element, **[majorfault]**
    - /proc/[pid]/stat : 12th element, **[childrenminorfault]**
    - /proc/[pid]/stat : 13th element, **[chlidrenmajorfault]**
- Paged pool
    - only in Windows?
- Non paged pool
    - only in Windows?
- Peak virtual size
    - /proc/[pid]/status : 17th line, **VmPeak: [VmPeak]**
- Virtual size
    - /proc/[pid]/status : 18th line, **VmSize: [VmSize]**
- Handles
    - only in windows?
- User
    - /proc/[pid]/status : 9th line, **Uid: [uid] [something] [something] [something]**
    - /etc/passwd : every line, **[user]:[pw]:[uid]:[gid]:[comment]:[homedir]:[loginshell]**
    - can find uid from /proc/[pid]/status, parse /etc/passwd/ and can get user
    - `stat /proc/[pid]/exe` : 4th line, **Access: (permission/permission) Uid: ( [uid]/ [user]) Gid: ( [gid]/ [groupname?])**
- Session ID
    - /proc/[pid]/status : 6th element, **[sessionid]**
- Integrity level
    - only in Windows? ( [link](https://en.wikipedia.org/wiki/Mandatory_Integrity_Control) )
- Command
    - /proc/[pid]/cmdline : just one line, and it is the command
- Digital signatures
    - I CANNOT FIND THIS
- ~~Date created~~
    - this is information about the time when the execution file of the process is created, NOT the time when the process is started, i think...
    - if i am right, linux does not save this information, so it should be discarded
- Date accessed
    - `stat /proc/[pid]/exe` : 5th line, **Access: [yyyy-MM-dd] [HH-mm-ss.~] [timezone]**
    - should parse and remove .~ part
- Date modified
    - `stat /proc/[pid]/exe` : 6th line, **Modified: [yyyy-MM-dd] [HH-mm-ss.~] [timezone]**
    - should parse and remove .~ part
- Version
- Product
- Company
- Path
    - `readlink /proc/[pid]/exe` : just one line, and it is the path
- MD5
    - `md5sum /proc/[pid]/exe` : just one line, **[MD5] [path]** 
- Sha256
    - `sha256sum /proc/[pid]/exe` : just one line, **[Sha256] [path]**

comments:  
    - `stat`, `readlink`, `md5sum` and `sha256sum` commands are included in GNU core utils, so it will not be a problem that some linux system does not have these commands  
    - procfs is common linux file system, so it will not be a problem, maybe?  
    - man page of procfs says that some elements and lines appeared and disappeared with version changes, so we must consider this  


##### Modules
- Name
    - /proc/[PID]/maps : every line, **[address] [permission] [offset?] [dev?] [inode] [pathname]**
    - pathname contains what is in certain memory, so i can get .so file names by parsing this (and i already did this w/ C)
- Attributes
- PIDs
    - PIDs of processes using this module
    - should make hashmap which have path has key, and manage all PIDs by path
- Digital signatures
- ~~Date created~~
    - linux does not have this data, so this should be discarded
- Date accessed
    - `stat [path]` : 5th line, **Access: [yyyy-MM-dd] [HH-mm-ss.~] [timezone]**
    - should parse and remove .~ part
- Date modified
    - `stat [path]` : 6th line, **Modified: [yyyy-MM-dd] [HH-mm-ss.~] [timezone]**
    - should parse and remove .~ part
- Version
    - /proc/[PID]/maps : every line, **[address] [permission] [offset?] [dev?] [inode] [pathname]**
    - pathname contains version information, so i can get version by parsing this, and i already did w/ C
- Product
- Company
- Path
    - /proc/[PID]/maps : every line, **[address] [permission] [offset?] [dev?] [inode] [pathname]**
    - can get pathname by parsing this, and i already did w/ C
- MD5
    - `md5sum [path]` : just one line, **[MD5] [path]**
- Sha256
    - `sha256sum [path]` : just one line, **[Sha256] [path]**

comments:  
    - in windows, this section is about dll files
    - in linux, dll is shared library


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
- Name
- Key
- Type
- Status
- PID
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

comments:  
- service in windows = daemon in linux?  
- if this is right, this information can be optained while analyzing process  
- if ppid of certain process is 1 or 2 and it has no tty, then it is daemon


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
