import random

import rclpy
from rclpy.node import Node

from mawr_interfaces.srv import Register

#
# Constants
#

NODE_NAME_PREFIX: str = "new_user"
SRV_NAME_REGISTER: str = "register"
RANDOM_RANGE: tuple[int] = (0, 999)
SPIN_TIMEOUT: float = 0.05
SERVICE_WAIT_TIMEOUT: float = 0.5

#
# Logic
#

class NewUser(Node):
    def __init__(self):
        __flag: bool = True
        while rclpy.ok() and __flag: 
            __post_fix: int = random.randint(
                *RANDOM_RANGE
            )
            try: 
                super().__init__(
                    f"{NODE_NAME_PREFIX}_{__post_fix}"
                )
            except:
                self.get_logger().warn(
                    "post fix taken. retrying"
                )
        
        self.__success: bool | None = None
        
        self.client_register = self.create_client(
            Register, SRV_NAME_REGISTER 
        )

    def __call_register(self, name: str):
        self.client_register.call_async(
            Register.Request(
                name = name
            )
        ).add_done_callback(
            self.__call_register_done
        )

    def __call_register_done(self, response: Register.Response):
        self.__success = response.success

    def __wait_for_services(self):
        while not self.client_register.wait_for_service(
            SERVICE_WAIT_TIMEOUT
        ):
            self.get_logger().warn(
                "pending register service ..."
            )

    def register(self, name: str) -> bool:
        self.__success = None
        self.__wait_for_services()
        self.get_logger().info("registering ...")
        self.__call_register(name)
        while self.__success is None:
            rclpy.spin_once(self, SPIN_TIMEOUT)
        self.get_logger().info("registering successfull")
        return self.__success
        
    def kill(self):
        self.destroy_node()

#
# Entry Point
#

def main():
    rclpy.init()
    node = NewUser()
    id = node.register()
    print(f"id is {id}")
    node.kill()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()