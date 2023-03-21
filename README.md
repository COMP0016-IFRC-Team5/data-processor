# data-processor

A simple data processor for the [DesInventar](https://www.desinventar.net) and 
[EM-DAT](https://www.emdat.be/).

This tool is a part of a UCL IXN project: "[Define return periods for low-impact 
hazardous events](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/README.md#project-introduction)" with IFRC. 

## Installation

```bash
git clone https://github.com/COMP0016-IFRC-Team5/data-processor.git
cd data-processor
```

## Requirements

1. Install dependencies in any preferred way

- Using conda ([Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
```bash
conda env create -f conda_env.yml
conda activate data-processor
```

- Using pip ([Python 3.10+](https://www.python.org/downloads/))
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

## Customise

### Merge
When implementing the algorithm for merging the records to events, we referred 
[THE HYBRID LOSS EXCEEDANCE CURVE](https://www.preventionweb.net/english/hyogo/gar/2011/en/bgdocs/ERN-AL_2011.pdf). 
In section _4.2.1 Algorithm for grouping events together_. The code related to 
the implementation is located in `processor/_models/_event_builder.py` and 
`processor/_apps/_combiner.py`.

### Slice
The slicing algorithm is `__slice_for_one_event()` in 
`processor/_apps/_slicer.py`. Currently, we just slice out the first 5% of the 
events.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- Dekun Zhang    [@DekunZhang](https://www.github.com/DekunZhang)
- Hardik Agrawal [@Hardik2239](https://www.github.com/Hardik2239)
- Yuhang Zhou    [@1756413059](https://www.github.com/1756413059)
- Jucheng Hu     [@smgjch](https://www.github.com/smgjch)
