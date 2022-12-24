#include "User_Task.h"
#include "Drv_RcIn.h"
#include "LX_FC_Fun.h"




dt_task task ;

extern u8 mod ;
extern u8 mod_change;

extern u16 distance , speed , angel ;

void UserTask_OneKeyCmd(void)
{
	
	//task.sit=0x00;
    //////////////////////////////////////////////////////////////////////
    //一键起飞/降落例程
    //////////////////////////////////////////////////////////////////////
    //用静态变量记录一键起飞/降落指令已经执行。
    static u8 one_key_takeoff_f = 1, one_key_land_f = 1, one_key_mission_f = 0;
    static u8 mission_step;
	static u8 emergency_stop_f = 1;
    //判断有遥控信号才执行
    if (rc_in.fail_safe == 0)
    {
        //判断第6通道拨杆位置 1300<CH_6<1700
        if (rc_in.rc_ch.st_data.ch_[ch_6_aux2] > 1300 && rc_in.rc_ch.st_data.ch_[ch_6_aux2] < 1700)
        {
            //还没有执行
            if (one_key_takeoff_f == 0)
            {
                //标记已经执行
                one_key_takeoff_f =
                    //执行一键起飞
                    OneKey_Takeoff(60); //参数单位：厘米； 0：默认上位机设置的高度。
							  task._todo = 0x00;
							  task.sit[0] = 0x01;//变更一键起飞任务的标志符号
            }
        }
        else
        {
            //复位标记，以便再次执行
            one_key_takeoff_f = 0;
					  
        }
        //
        //判断第6通道拨杆位置 800<CH_6<1200
        if (rc_in.rc_ch.st_data.ch_[ch_6_aux2] > 800 && rc_in.rc_ch.st_data.ch_[ch_6_aux2] < 1200)
        {
            //还没有执行
            if (one_key_land_f == 0)
            {
                //标记已经执行
                one_key_land_f =
                    //执行一键降落
                    OneKey_Land();
            }
        }
        else
        {
            //复位标记，以便再次执行
            one_key_land_f = 0;
        }
        //判断第6通道拨杆位置 1700<CH_6<2000
        if (rc_in.rc_ch.st_data.ch_[ch_6_aux2] > 1700 && rc_in.rc_ch.st_data.ch_[ch_6_aux2] < 2200)
        {
            //还没有执行
            if (one_key_mission_f == 0)
            {
                //标记已经执行
                one_key_mission_f = 1;
                //开始流程
                mission_step = 1;
            }
        }
        else
        {
            //复位标记，以便再次执行
            one_key_mission_f = 0;
        }
        //
        if (one_key_mission_f == 1)
        {
        }
        else
        {
            mission_step = 0;
        }
				//第七通道
  if (rc_in.rc_ch.st_data.ch_[ch_7_aux3] > 1700 &&
      rc_in.rc_ch.st_data.ch_[ch_7_aux3] < 2200) {
    if (emergency_stop_f == 0) {
      emergency_stop_f = 1;
      //执行一键锁桨
      FC_Lock();
      pwm_to_esc.pwm_m1 = 0;
      pwm_to_esc.pwm_m2 = 0;
      pwm_to_esc.pwm_m3 = 0;
      pwm_to_esc.pwm_m4 = 0;
    }
  } else {
    emergency_stop_f = 0;
  }
    }
    ////////////////////////////////////////////////////////////////////////
}

void Patrol_Task(void)
{
	switch(task._todo)
	{
		case(0x01):
		{//飞行模式切换到模式3：流程控制
			task.sit[1] = 0x00;
			if ((mod)&&(task.sit[0] == 0x01)&&(mod_change > 1))
					task.sit[1] = 0x01 ;
			break;	
		}
		case(0x02):
		case(0x04):
		{//开始巡线（两个方向）
			task.sit[2]=0x00;
			task.sit[4]=0x00;
			
			u8 situa_2=0;
			u8 situa_4=0;
			
			if (angel == 90)
			situa_2=Horizontal_Move( distance , speed , angel);
			
			if (angel == 270)
			situa_4=Horizontal_Move( distance , speed , angel);
			
			if ( situa_2 == 1 )
				task.sit[2]=0x01;
			
			if ( situa_4 == 1 )
				task.sit[4]=0x01;
			
			break;
		}
		case (0x03):
		{
			//蜂鸣器和悬停控制
			task.sit[3] = 0x00;
			task.sit[3] = 0x01;
			break;
		}
		case(0x05):
		{//一键降落
			task.sit[5] = 0x00;
			OneKey_Land();
			task.sit[5] = 0x01;
			break;
		}
		default :
		{
		}
	}
}

//void LA_CMD(u8 tel)
//{
//	
//}

//void Beep_CMD(u8 tel)
//{
//	
//}

//void Gothrough(u16 dir_angel)
//{
//    while(task.sit==0x00)
//		{
//			Horizontal_Move(5,10,dir_angel);
//		}
//}

//void Streering(u16 dir_angel)
//{
//}
	

