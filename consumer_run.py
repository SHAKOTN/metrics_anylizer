import logging
from consumer import consume_messages

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    consume_messages()
