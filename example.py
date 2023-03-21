import processor

processor.set_data_dir('../data-visualiser/data')

option = {
    'desinventar': {
        'merge': True,
        'slice': True,
    },
    'emdat': {
        'process': False,
    },
}

processor.process(option)
