from controllers import merge_controller
from utils import Directory


def main():
    data_folder = Directory("../data")
    merge_controller.start_merging(data_folder)


if __name__ == '__main__':
    main()
