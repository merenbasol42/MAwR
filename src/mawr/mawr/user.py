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
        def cmd():
            self.name = self.gui.text_box.get()
            print(self.name)
            self.__run_node()

        self.gui.submit_button.configure(
            command = cmd
        )

    def __run_node(self):
        def node_run():
            rclpy.init()
            self.node = Node(self.name)
            rclpy.spin(self.node)
            rclpy.shutdown()
        
        Thread(
            target = node_run,
            daemon = True
        ).start()
        

    def run(self):
        self.bind()
        self.gui.run()

def main(name: str = "ahmed"):
    User(name).run()

if __name__ == "__main__":
    main()