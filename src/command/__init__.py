from .bindCommand import bind_command
from .bpCommand import bp_command, bp_today_command
from .infoCommand import info_command
from .mapInfoCommand import beatmap_command, beatmap_set_command
from .mpCommand import MultiPlayCommand
from .rankingCommand import ranking_command
from .recationCallback import reaction_callback
from .recentCommand import recent_command
from .scoreCommand import score_command
from .searchCommand import SearchQueue, upload_assets_and_generate_search_card

mp_command = MultiPlayCommand.instance()
search_command = SearchQueue.get_instance()
