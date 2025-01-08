
import rclpy
from rclpy.node import Node

from mawr_interfaces.msg import Voice
from mawr_interfaces.srv import Permission

from ..message import Message
from ..message import DirectionalMessage as DMsg

#
# Constants
#

NODE_NAME_PREFIX: str = "user_"

#
# Logic
#

class User(Node):
    def __init__(self, id: int):
        self.id : int = id
        self.name = f"{NODE_NAME_PREFIX}{self.id}"
        self.received_msgs: list[DMsg] = []
        self.recorded_msgs: list[Message] = []
        
        self.receive_flag: bool = False
        self.receiver_name: str = None

        super().__init__(self.name)

        self.create_service(Permission, f"{self.name}/permission", self.__handle_permission)
    
        self.receiver_sub = None

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
                    self.__delete_receiver_topic()

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
                self.__create_receiver_topic(req.name)
                self.received_msgs.append(DMsg(req.name, self.name))
        
        return res

    def __cb_receiver(self, msg: Voice):
        self.received_msgs[-1].add_part(
            list(msg.data)
        )

    def __create_receiver_topic(self, postfix: str):
        self.receiver_sub = self.create_subscription(
            Voice,
            f"{self.name}/receiver/{postfix}",
            self.__cb_receiver
        )

    def __delete_receiver_topic(self):
        self.destroy_subscription(self.receiver_sub)

    #
    #
    #

    def record_msg(self):
        pass

    def send_msg(self, index: int):
        pass
    
    def play_msg(self, index: int):
        pass

#
# Entry Point
#

def main():
    rclpy.init()
    node = User()
    try: rclpy.spin(node)
    except: pass
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()