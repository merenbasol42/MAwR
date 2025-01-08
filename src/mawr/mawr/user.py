import rclpy
from threading import Thread
from .modules.gui.user import GUI
from .modules.nodes.user import User as Node

class User:
    def __init__(self, name: str):
        self.name = name
        self.node: Node
        self.gui: GUI = GUI()
        self.gui.init()

    def bind(self):
        self.gui.record_button.configure(
            command = lambda: print("record") 
        )

        self.gui.play_button.configure(
            command = lambda: print("play")
        )

    def run(self):
        print(f"my name is {self.name}")
        def node_run():
            rclpy.init()
            self.node = Node(self.name)
            self.bind()
            rclpy.spin(self.node)
            rclpy.shutdown()
        
        Thread(
            target = node_run,
            daemon = True
        ).start()
        
        self.gui.run()

def main(name: str = "ahmed"):
    User(name).run()

if __name__ == "__main__":
    main()