
import rclpy
from rclpy.node import Node

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
        
        super().__init__(self.name)

        self.create_service(..., f"{self.name}/permission", self.__handle_permission)
    #
    # ROS Messaging
    # 

    def __handle_permission(self, res):
        pass

    def __cb_receiver(self, msg):
        pass

    def send_msg(self, index: int):
        pass

    #
    #
    #

    def record_msg(self):
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