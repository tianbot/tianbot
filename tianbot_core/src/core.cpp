#include "core.h"
#include "protocol.h"
#include <vector>
#include <stdint.h>

void TianbotCore::serialDataProc(uint8_t *data, unsigned int data_len)
{
    static uint8_t state = 0;
    uint8_t *p = data;
    static vector<uint8_t> recv_msg;
    static uint32_t len;
    uint32_t j;

    while (data_len != 0)
    {
        switch (state)
        {
        case 0:
            if (*p == (PROTOCOL_HEAD & 0xFF))
            {
                recv_msg.clear();
                recv_msg.push_back(PROTOCOL_HEAD & 0xFF);
                state = 1;
            }
            p++;
            data_len--;
            break;

        case 1:
            if (*p == ((PROTOCOL_HEAD >> 8) & 0xFF))
            {
                recv_msg.push_back(((PROTOCOL_HEAD >> 8) & 0xFF));
                p++;
                data_len--;
                state = 2;
            }
            else
            {
                state = 0;
            }
            break;

        case 2: // len
            recv_msg.push_back(*p);
            len = *p;
            p++;
            data_len--;
            state = 3;
            break;

        case 3: // len
            recv_msg.push_back(*p);
            len += (*p) * 256;
            if (len > 1024 * 10)
            {
                state = 0;
                break;
            }
            p++;
            data_len--;
            state = 4;
            break;

        case 4: // pack_type
            recv_msg.push_back(*p);
            p++;
            data_len--;
            len--;
            state = 5;
            break;

        case 5: // pack_type
            recv_msg.push_back(*p);
            p++;
            data_len--;
            len--;
            state = 6;
            break;

        case 6: //
            if (len--)
            {
                recv_msg.push_back(*p);
                p++;
                data_len--;
            }
            else
            {
                state = 7;
            }
            break;

        case 7:
        {
            int i;
            uint8_t bcc = 0;
            recv_msg.push_back(*p);
            p++;
            data_len--;
            state = 0;

            for (i = 4; i < recv_msg.size(); i++)
            {
                bcc ^= recv_msg[i];
            }

            if (bcc == 0)
            {
                tianbotDataProc(&recv_msg[0], recv_msg.size()); // process recv msg
                communication_timer_.stop(); // restart timer for communication timeout
                communication_timer_.start();
            }
            else
            {
                ROS_INFO("BCC error");
            }
            state = 0;
        }
        break;

        default:
            state = 0;
            break;
        }
    }
}

void TianbotCore::communicationErrorCallback(const ros::TimerEvent &)
{
    ROS_ERROR_THROTTLE(5, "Communication with base error");
}

void TianbotCore::heartCallback(const ros::TimerEvent &)
{
    vector<uint8_t> buf;
    uint16_t dummy = 0;

    buildCmd(buf, PACK_TYPE_HEART_BEAT, (uint8_t *)&dummy, sizeof(dummy));
    serial_.send(&buf[0], buf.size());
}

void TianbotCore::debugcmdCallback(const std_msgs::String::ConstPtr &msg)
{
    vector<uint8_t> buf;
    buildCmd(buf, PACK_TYPE_DEBUG, (uint8_t *)msg->data.c_str(), msg->data.length());
    serial_.send(&buf[0], buf.size());
}

TianbotCore::TianbotCore(ros::NodeHandle *nh) : nh_(*nh)
{
    std::string param_serial_port;
    int32_t param_serial_baudrate;
    nh_.param<std::string>("serial_port", param_serial_port, DEFAULT_SERIAL_DEVICE);
    nh_.param<int>("serial_baudrate", param_serial_baudrate, DEFAULT_SERIAL_BAUDRATE);
    debug_pub_ = nh_.advertise<std_msgs::String>("debug_result", 1);
    debug_sub_ = nh_.subscribe("debug_cmd", 1, &TianbotCore::debugcmdCallback, this);
    heartbeat_timer_ = nh_.createTimer(ros::Duration(0.2), &TianbotCore::heartCallback, this);
    communication_timer_ = nh_.createTimer(ros::Duration(0.2), &TianbotCore::communicationErrorCallback, this);
    heartbeat_timer_.stop();
    communication_timer_.stop();
    while (serial_.open(param_serial_port.c_str(), param_serial_baudrate, 0, 8, 1, 'N',
                     boost::bind(&TianbotCore::serialDataProc, this, _1, _2)) != true)
    {
        ROS_ERROR_THROTTLE(5.0, "Device %s open failed", param_serial_port.c_str());
        ros::Duration(0.5).sleep();
    }
    ROS_INFO("Device %s open successfully", param_serial_port.c_str());
    heartbeat_timer_.start();
    communication_timer_.start();
}