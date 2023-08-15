def set_skill_lvl(avg_att):
    if avg_att >= 15:
        return 'baby'
    elif avg_att >= 10 and avg_att < 15:
        return 'children'
    elif avg_att >= 7 and avg_att < 10:
        return 'student'
    elif avg_att >= 5 and avg_att < 7:
        return 'smart guy'
    elif avg_att >= 3 and avg_att < 5:
        return 'intellectual'
    elif avg_att >= 2 and avg_att < 3:
        return 'genius'
    elif avg_att >= 1 and avg_att < 2:
        return 'AI'
    elif avg_att >= 0 and avg_att < 1:
        return 'you hacked the game?'
    else:
        return 'human'