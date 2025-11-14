from .serializer import serialize_game, deserialize_game
from .file_storage import write_file, read_file

def save_game(game, filename):
    data = serialize_game(game)
    write_file(filename, data)

def load_game(filename):
    data = read_file(filename)
    return deserialize_game(data)