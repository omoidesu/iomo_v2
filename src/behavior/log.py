from khl import Message
from src.service import log_service
from src.dao.models import OsuLog


def save_log(msg: Message, *args):
    kook_id = msg.author.id
    command = msg.content.split(' ')[0]
    new_log = OsuLog(kook_id=kook_id, kook_name=msg.author.username, kook_num=msg.author.identify_num,
                     command=command[1:], args=' '.join(args))
    log_service.insert(new_log)

    return kook_id
