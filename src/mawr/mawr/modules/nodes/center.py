
import rclpy
from rclpy.node import Node

from mawr_interfaces.srv import Register

#
# Constants
#

SERVICE_NAME_REGISTER: str = "register"

#
# Logic
#

class Center(Node):
    def __init__(self):
        super().__init__("my_node")
        self.users: list[str] = []
        self.register_server = self.create_service(
            Register, SERVICE_NAME_REGISTER, self.handle_register
        )

    def handle_register(self, req: Register.Request, res: Register.Response):
        
        if self.users.count(req.name) > 0:
            res.id = -1
            return res
        
        else:
            res.id = len(self.users)
            self.users.append(req.name)
            return res

#
# Entry Point
#

def main():
    rclpy.init()
    node = Center()
    try: rclpy.spin(node)
    except: pass
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()