import processor

processor.set_data_dir('./data')

option = {
    'desinventar': {
        'merge': True,
        'slice': True,
    },
    'emdat': {
        'process': True,
    },
}

processor.process(option)
