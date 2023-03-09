from ._utils import Directory
from ._controllers import slice_controller, merge_controller
from ._emdat import emdat_controller

__all__ = ['set_data_dir', 'process']

_data_dir = None


def set_data_dir(data_dir):
    """Set the data directory to be used by the processor."""
    global _data_dir
    _data_dir = Directory(data_dir)


def process(option):
    """Process the data in the data directory."""
    if _data_dir is None:
        raise ValueError('No data directory set.')
    if option['desinventar']['merge']:
        merge_controller.start_merging(_data_dir)
    if option['desinventar']['slice']:
        slice_controller.start_slice(_data_dir)
    if option['emdat']['process']:
        emdat_controller.start_emdat(_data_dir)
