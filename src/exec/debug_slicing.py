from controllers import slice_controller
from utils import Directory


if __name__ == '__main__':
    data_folder = Directory("../data")
    slice_controller.start_slice(data_folder)
