import time
from threading import Thread

import rclpy
from rclpy.node import Node

from mawr_interfaces.msg import Voice
from mawr_interfaces.srv import Permission

from ..message import Message
from ..message import DirectionalMessage as DMsg

from ..stream import Recorder

#
# Constants
#

#
# Logic
#

class SendCommand:
    '''
    Gönderilecek olan mesajların emri. 
    Kime göndereliceği ve hangi mesaj gönderileceğini kapsar
    '''
    def __init__(self, to: str, index: int):
        self.to: str = to
        self.index: int = index

class User(Node):
    def __init__(self, name: str):
        self.name = name
        self.received_msgs: list[DMsg] = []
        self.recorded_msgs: list[Message] = []
        
        self.receive_flag: bool = False
        self.receiver_name: str = None

        self.recorder: Recorder = Recorder()

        self.send_cmds: list[SendCommand] = []
        self.sender_th: Thread | None = None

        super().__init__(self.name)

        self.create_service(Permission, f"{self.name}/permission", self.__handle_permission)
    
        self.subber_receiver = None
        self.pubber_receiver = None
        self.client_permission = None

    #
    # ROS Messaging
    # 

    def __handle_permission(self, req: Permission.Request, res: Permission.Response):
        if self.receive_flag:
        
            if req.name == self.receiver_name:
        
                if req.target:
                    self.get_logger().error(f"Already receiving from {req.name}")
                    res.success = False
                
                else:
                    self.get_logger().info(f"Receiving from {req.name} has been end")
                    self.receive_flag = False
                    self.receiver_name = None
                    res.success = True
                    self.__delete_receiver_sub()

            else:
             
                if req.target:
                    self.get_logger().warn(f"Receiver is full. So decline {req.name} query")
                    res.success = False
                
                else:
                    self.get_logger().error(f"Already not receiving from {req.name}. Receiving from another")
                    res.success = False

        else:

            if req.target:
                self.get_logger().error(f"Already not receiving from {req.name}")
                res.success = False
            
            else: 
                self.get_logger().info(f"Setting up for receive from {req.name}")
                self.receive_flag = True
                self.receiver_name = req.name
                res.success = True
                self.__create_receiver_sub(req.name)
                self.received_msgs.append(DMsg(req.name, self.name))
        
        return res

    def __call_permission(self, name: str, target: bool):
        '''Synchronus'''
        self.get_logger().info("... calling for permission")
        self.client_permission = self.create_client(
            Permission, f"{name}/permission"
        )
        
        return self.client_permission.call(
            Permission.Request(
                name = self.name,
                target = bool
            )
        ).success 

    def __cb_receiver(self, msg: Voice):
        self.received_msgs[-1].add_part(
            list(msg.data)
        )

    def __create_receiver_sub(self, postfix: str):
        self.subber_receiver = self.create_subscription(
            Voice,
            f"{self.name}/receiver/{postfix}",
            self.__cb_receiver,
            10
        )

    def __delete_receiver_sub(self):
        self.destroy_subscription(self.subber_receiver)
        self.subber_receiver = None

    def __create_receiver_pub(self, name: str):
        self.pubber_receiver = self.create_publisher(
            msg_type = Voice,
            topic = f"{name}/receiver/{self.name}",
            qos_profile = 10
        )
    
    #
    #
    #
    
    def __send(self, index: int, name: str) -> bool:
        success = self.__call_permission(name, True)
        if not success:
            self.get_logger().error(f"... permission denied from {name}")
            self.client_permission.destroy()
            return False
        
        self.__create_receiver_pub(name)
        
        self.get_logger().info(f"... publishing voice start")
        for part in self.recorded_msgs[index].audio:
            self.pubber_receiver.publish(
                Voice(data = part)
            )
            time.sleep(0.05)
        self.get_logger().info(f"... publishing voice end")
        
        self.client_permission.destroy()
        self.client_permission = None

    def __sender_work(self):
        while rclpy.ok() and len(self.send_cmds):
            for cmd in self.send_cmds:
                if self.__send(
                    index = cmd.index,
                    name = cmd.to
                ): self.send_cmds.remove(cmd)
        
        self.sender_th = None

    def start_record_msg(self):
        self.recorder.start()
        self.get_logger().info("recording start")

    def stop_record_msg(self):
        self.recorder.stop()
        self.get_logger().info("recording end")
        m = Message()
        m = self.recorder.get_audio()
        self.recorded_msgs.append(m)
        self.get_logger().info("record saved")

    def send_msg(self, index: int, name: str):
        self.send_cmds.append(
            SendCommand(
                index = index,
                to = name
            )
        )
        if self.sender_th is None:
            self.sender_th = Thread(
                target = self.__sender_work,
                daemon = True
            )
            self.sender_th.start()
        
    def play_msg(self, index: int):
        pass

#
# Entry Point
#

def main():
    rclpy.init()
    node = User("__def__")
    rclpy.spin()
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()