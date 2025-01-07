
import rclpy
from rclpy.node import Node

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
        super().__init__(f"{NODE_NAME_PREFIX}{self.id}")
        self.received: list
        self.sended: list

    def query_message_list(self):
        pass

    def send_message(self, index: int, user: str):
        pass

    def receive_message(self, index: int):
        pass

    def record_message(self):
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