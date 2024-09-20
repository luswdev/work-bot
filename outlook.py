import logging
import win32com.client
import pythoncom
import re

class outlook:
    def __init__(self, keyword):
        self.keyword = keyword

    def search(self, date):
        try:
            pythoncom.CoInitialize()
            outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
            inbox = outlook.GetDefaultFolder(6)
            messages = inbox.Items
            found = False
            for message in messages:
                if re.search(date, message.Subject, re.IGNORECASE) and self.keyword in message.Subject:
                    logging.info(f'match email: {message.Subject}')
                    found = self.parse_body(message.Body)
            return found
        except pythoncom.com_error as e:
            logging.error(f'COM error: {e}')
            return False
        except Exception as ex:
            logging.error(f'unexpected error: {ex}')
            return False
        finally:
            pythoncom.CoUninitialize()

    def parse_body(self, body):
        time_pattern = r'\b\d{2}:\d{2}:\d{2}\b' # HH:MM:SS
        time_matches = re.findall(time_pattern, body)
        return time_matches[0]
