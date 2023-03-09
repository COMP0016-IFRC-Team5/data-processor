# data-processor

A simple data processor for the [DesInventar](https://www.desinventar.net) and 
[EM-DAT](https://www.emdat.be/).

## Installation

```bash
git clone https://github.com/COMP0016-IFRC-Team5/data-processor.git
cd data-processor
```

## Requirements

1. Install dependencies in any preferred way

- Using conda
```bash
conda env create -f conda_env.yml
conda activate data-processor
```

- Using pip
```bash
pip install -r requirements.txt
```
2. Get data using data-downloader module

## Usage

This module provides functionality for processing data from a data directory.

### Functions:
    set_data_dir(data_dir)
        Set the data directory to be used by the processor.

    process(option)
        Process the data in the data directory.

### Usage:
To use this module, first call `set_data_dir()` to set the data directory to be
used by the processor. Then call `process()` with a dictionary `option`
containing the following keys:

    * 'desinventar': A dictionary containing the following keys:
        - 'merge': A boolean indicating whether to merge data.
        - 'slice': A boolean indicating whether to slice data.
    * 'emdat': A dictionary containing the following key:
        - 'process': A boolean indicating whether to process EMDAT data.

### Example:
See `example.py` for detail.

```bash
python3 example.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- Dekun Zhang    [@DekunZhang](https://www.github.com/DekunZhang)
- Hardik Agrawal [@Hardik2239](https://www.github.com/Hardik2239)
- Yuhang Zhou    [@1756413059](https://www.github.com/1756413059)
- Jucheng Hu     [@smgjch](https://www.github.com/smgjch)