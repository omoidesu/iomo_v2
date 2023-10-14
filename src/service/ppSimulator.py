import asyncio
import json

from src.config import osu_tools_path


async def simulate_pp_with_accuracy(beatmap_id: int, accuracy: float, mode: str, mods: list):
    if mode == 'mania':
        return '-'

    mode = 'catch' if mode == 'fruits' else mode
    cmd = f'dotnet run --project {osu_tools_path} -- simulate {mode} {beatmap_id} -j -a {accuracy}'
    if mods:
        for mod in mods:
            cmd += ' -m ' + mod

    pp, _, _, _, _ = await do_simulate(cmd)
    return pp


async def simulate_pp_if_fc(beatmap_id: int, mode: str, mods: list, statistics: dict):
    mode = 'catch' if mode == 'fruits' else mode
    cmd = f'dotnet run --project {osu_tools_path} -- simulate {mode} {beatmap_id} -j'
    if mods:
        for mod in mods:
            cmd += ' -m ' + mod

    if mode == 'osu':
        cmd += f' -M {statistics.get("count_50")} -G {statistics.get("count_100")}'
    elif mode == 'taiko':
        cmd += f' -G {statistics.get("count_100")}'
    elif mode == 'catch':
        cmd += f' -T {statistics.get("count_katu")} -D {statistics.get("count_100")}'
    else:
        cmd += ' -s 1000000'

    return await do_simulate(cmd)


async def do_simulate(cmd: str):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()

    if stdout:
        out = stdout.decode()
        if out.startswith('Downloading'):
            out = out.split('...\r\n')[1]
        data = json.loads(out)
        pp = round(data.get('performance_attributes').get('pp'))
        difficulty_attributes = data.get('difficulty_attributes')
        star_rating = round(difficulty_attributes.get('star_rating'), 2)
        ar = round(difficulty_attributes.get('approach_rate'), 2)
        od = round(difficulty_attributes.get('overall_difficulty'), 2)
        acc = round(data.get('score', {}).get('accuracy', 0), 2)
        return pp, star_rating, ar, od, acc
    else:
        return '-'
