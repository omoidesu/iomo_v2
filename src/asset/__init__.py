import os


def get_assets():
    folder = os.path.dirname(__file__)
    return {file[:-4]: os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.png')}


def get_user_not_found():
    path = get_assets().get('userNotFound')
    with open(path, 'rb') as f:
        return f.read()
