from gameobject import GameObject

# лестница располагается в последней комнате для перехода на следующий уровень
class Stairs(GameObject):

    def start(self):
        self.drop_in_room(9)
