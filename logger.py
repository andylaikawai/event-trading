import json
import logging
import time

def setup_logger(log_file='logs/ws_messages.log'):
    # Custom log formatter
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            log_msg = super().format(record)
            # If the message is JSON, try to parse it and extract relevant fields
            if hasattr(record, 'json_message'):
                try:
                    message = json.loads(record.json_message)
                    title = message.get("title", "N/A")
                    body = message.get("body", "N/A")
                    time_ms = message.get("time", 0)
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_ms / 1000))
                    return f"{timestamp} - Title: '{title}' | Body: '{body}'"
                except json.JSONDecodeError:
                    return log_msg  # Fallback to the original log message
            return log_msg

    # Logger Configuration
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Apply custom formatter to the root logger
    for handler in logging.getLogger().handlers:
        handler.setFormatter(CustomFormatter('%(message)s'))