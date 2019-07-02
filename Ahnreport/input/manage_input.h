//
// Created by raven on 19. 7. 2.
//

#ifndef MANAGE_INPUT_H
#define MANAGE_INPUT_H
enum task_option{FULL, TASK, NETWORK, SYSTEM, HELP};
enum type_OS{NON, DEBIAN, REDHAT, UBUNTU, ARCH};

enum task_option sorting_task(char * option);
enum type_OS check_OS();
char *take_OS();
void Err_help();
void Err_existFile();
#endif //MANAGE_INPUT_H

