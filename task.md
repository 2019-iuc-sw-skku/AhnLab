##### Processes
- Name
    - name of the process?
    - /proc/[pid]/status : 1st line, **Name: [name]**
    - /proc/[pid]/stat : 2nd element, **(name)**
    - there is no 'name' section in top or ps
- Attributes
    - is it suspended or not? idk
    - /proc/[pid]/status : 3rd line, **State: [status] (status\_explanation)**
    - /proc/[pid]/stat : 3rd element, **status**
    - in linux, it is about process life cycle, not if it is suspended
- PID
    - process id
    - /proc : read all directories, and get the name only if the directory name is number and /proc/[directory]/status
    - can do with opendir() and readdir() in C/C++
- PPID
    - parent process id
    - /proc/[pid]/status : 7th line, **PPid: [ppid]**
    - /proc/[pid]/stat : 4th element, **PPid**
- Threads
    - /proc/[pid]/status : 34th line, **Threads: [threads]**
- Base priority
- Creation time
- CPU
    - cpu number where the process is working?
- CPU time
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
- User
    - /proc/[pid]/status : 9th line, **Uid: [uid] [something] [something] [something]**
    - /etc/passwd : every line, **[user]:[pw]:[uid]:[gid]:[comment]:[homedir]:[loginshell]**
    - can find uid from /proc/[pid]/status, parse /etc/passwd/ and can get user
    - `stat /proc/[pid]/exe` : 4th line, **Access: (permission/permission) Uid: ( [uid]/ [user]) Gid: ( [gid]/ [groupname?])**
- Session ID
    - /proc/[pid]/status : 6th element, **[sessionid]**
- Integrity level
- Command
    - /proc/[pid]/cmdline : just one line, and it is the command
- Digital signatures
    - I CANNOT FIND THIS
- Date created
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
- Sha256

comments:
    - `stat` and `readlink` command is included in GNU core utils, so it will not be a problem that some linux system does not have these commands
    - procfs is common linux file system, so it will not be a problem, maybe?
    - man page of procfs says that some elements and lines appeared and disappeared with version changes, so we must consider this

##### Modules
- Name
- Attributes
- PIDs
- Digital signatures
- Date created
- Date accessed
- Date modified
- Version
- Product
- Company
- Path
- MD5
- Sha256

##### Startup

##### Services

##### Schedule tasks
