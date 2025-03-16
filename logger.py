import logging


def setup_logger(log_file='logs/ws_messages.log'):
    # Logger Configuration
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
