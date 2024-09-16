import json


def get_parsed_config():
    with open('test_config.json', 'r') as file:
        config = json.load(file)

    if config['msg_size'] == 'mala':
        config['msg_path'] = f'messages/10kb_message.txt'
    elif config['msg_size'] == 'srednja':
        config['msg_path'] = f'messages/1mb_message.txt'
    else:
        config['msg_path'] = f'messages/10mb_message.txt'

    return config