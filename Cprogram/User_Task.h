#ifndef __USER_TASK_H
#define __USER_TASK_H

#include "SysConfig.h"

typedef struct
{
	u8 _todo;
	u8 sit[6];
}  dt_task;


void LA_CMD(u8 tel);

void Beep_CMD(u8 tel);

void UserTask_OneKeyCmd(void);

void Patrol_Task(void);

void Gothrough(u16 dir_angel);


#endif
