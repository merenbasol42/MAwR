import random

import rclpy
from rclpy.node import Node

#
# Constants
#

NODE_NAME_PREFIX: str = "new_user"
RANDOM_RANGE: tuple[int] = (0, 999)
SRV_NAME_REGISTER: str = "register"
SPIN_TIMEOUT: float = 0.05

#
# Logic
#

class NewUser(Node):
    def __init__(self):
        __flag: bool = True
        while rclpy.ok() and __flag: 
            __post_fix: int = random.randint(*RANDOM_RANGE)
            try: 
                super().__init__(f"{NODE_NAME_PREFIX}_{__post_fix}")
            except:
                self.get_logger().warn("post fix taken. retrying")
        
        self.id: int | None = None
        
        self.client_register = self.create_client(
            ..., SRV_NAME_REGISTER 
        )

    def __call_register(self):
        msg = ...
        self.client_register.call_async(
            msg
        ).add_done_callback(
            self.__call_register_done
        )

    def __call_register_done(self, response: ...):
        pass

    def register(self) -> int:
        self.__call_register()
        while self.id is None:
            rclpy.spin_once(self, SPIN_TIMEOUT)
        return self.id

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