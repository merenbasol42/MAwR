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
        self.gui.e_name.subscribe(
            self.__cb_name_entered
        )
        self.gui.e_play.subscribe(
            self.__cb_play
        )
        self.gui.e_record.subscribe(
            self.__cb_record
        )

    def __cb_record(self, target: bool):
        if target:
            print("recording on")
        else:
            print("recording off")

    def __cb_play(self, index: int):
        print(f"played: {index}")

    def __cb_name_entered(self, name: str):
        self.name = name
        self.__run_node()
        self.gui.switch_page()

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