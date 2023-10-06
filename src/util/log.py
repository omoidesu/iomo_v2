from khl import Message

from src.dao.models import OsuLog
from src.service import log_service


def save_log(msg: Message, *args, command: str = ''):
    kook_id = msg.author.id
    if not command:
        command = msg.content.split(' ')[0][1:]
    new_log = OsuLog(kook_id=kook_id, kook_name=msg.author.username, kook_num=msg.author.identify_num,
                     command=command, args=' '.join(args))
    log_service.insert(new_log)

    return kook_id
