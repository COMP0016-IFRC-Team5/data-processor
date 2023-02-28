from emdat import emdat_controller
from utils import Directory


if __name__ == '__main__':
    data_folder = Directory("../data")
    emdat_controller.start(data_folder)
