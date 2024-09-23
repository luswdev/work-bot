import os
import logging
import logging.handlers

def init_logging(type = 'console'):
    match type:
        case 'file':
            base_path = os.getenv('APPDATA')
            log_path = os.path.join(base_path, 'work-bot', 'logs')
            os.makedirs(log_path, exist_ok=True)

            log_file = 'work-bot.log'
            logging.basicConfig(
                format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level    = logging.INFO,
                datefmt  = '%Y-%m-%dT%H:%M:%S',
                filename = os.path.join(log_path, log_file),
                filemode ='a',
            )

            file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when = 'd', interval = 7, backupCount=7)
            file_handler.suffix = '%Y-%m-%dT%H-%M-%S.log'
            logging.getLogger().addHandler(file_handler)

        case 'console':
            logging.basicConfig(
                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level  = logging.INFO,
            )
