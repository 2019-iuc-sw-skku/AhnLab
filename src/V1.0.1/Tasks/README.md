tested on Ubuntu 18.04.2 LTS (4.18.0-25-generic)

How to test:
1. using tasks.py
    - download all files and execute tasks.py with following options:
        - --processes
        - --modules
        - --startup
        - --services
        - --schedule-tasks
2. using separated files
    - download all files and execute each .py

You can check the running time of each functions by importing `logging_time` function from `loggingtime` and using `@logging_time` decorator. modules.py can be the example source.


**MY SUGGESTION: HOW ABOUT JUST PRINTING THE CONTENTS W/ WHITE SPACE DELIMITER W/O ANY OTHER CONTENTS? THAT WILL BE EASISER TO PARSE**
