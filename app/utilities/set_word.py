from random import choice

all_5_noun = ['Brief', 'Bread', 'Heart']
all_6_noun = ['people', 'family', 'health', 'system', 'thanks', 'person', 'method', 'theory', 'nature', 'safety', 'player', 'policy', 'series', 'camera', 'growth', 'income', 'energy', 'nation', 'moment', 'office', 'driver', 'flight', 'length', 'dealer', 'debate', 'member', 'advice', 'effort', 'wealth', 'county', 'estate', 'recipe', 'studio', 'agency', 'memory', 'aspect', 'cancer', 'region', 'device', 'engine', 'height', 'sample', 'boring', 'cousin', 'editor', 'extent', 'guitar', 'leader', 'singer', 'tennis', 'basket', 'church', 'coffee', 'dinner', 'orange', 'poetry', 'police', 'sector', 'volume', 'farmer', 'injury', 'speech', 'winner', 'worker', 'writer', 'breath', 'cookie', 'drawer', 'insect', 'ladder', 'potato', 'sister', 'tongue', 'affair', 'client', 'throat', 'number', 'market', 'course', 'school', 'amount', 'answer', 'matter', 'access', 'garden', 'reason', 'future', 'demand', 'action', 'record', 'result', 'period', 'chance', 'figure', 'source', 'design', 'object', 'profit', 'inside', 'stress', 'review', 'screen', 'medium', 'bottom', 'choice', 'impact', 'career', 'credit', 'square', 'effect', 'friend', 'couple', 'living', 'summer', 'button', 'desire', 'notice', 'damage', 'target', 'animal', 'author', 'budget', 'ground', 'lesson', 'minute', 'bridge', 'letter', 'option', 'plenty', 'weight', 'factor', 'master', 'muscle', 'appeal', 'mother', 'season', 'signal', 'spirit', 'street', 'status', 'ticket', 'degree', 'doctor', 'father', 'stable', 'detail', 'shower', 'window', 'corner', 'finger', 'garage', 'manner', 'winter', 'battle', 'bother', 'horror', 'phrase', 'relief', 'string', 'border', 'branch', 'breast', 'expert', 'league', 'native', 'parent', 'salary', 'silver', 'tackle', 'assist', 'closet', 'collar', 'jacket', 'reward', 'bottle', 'candle', 'flower', 'lawyer', 'mirror', 'purple', 'stroke', 'switch', 'bitter', 'carpet', 'island', 'priest', 'resort', 'scheme', 'script', 'public', 'common', 'change', 'simple', 'second', 'single', 'travel', 'excuse', 'search', 'remove', 'return', 'middle', 'charge', 'active', 'visual', 'affect', 'report', 'beyond', 'junior', 'unique', 'listen', 'handle', 'finish', 'normal', 'secret', 'spread', 'spring', 'cancel', 'formal', 'remote', 'double', 'attack', 'wonder', 'annual', 'nobody', 'repeat', 'divide', 'survey', 'escape', 'gather', 'repair', 'strike', 'employ', 'mobile', 'senior', 'strain', 'yellow', 'permit', 'abroad', 'prompt', 'refuse', 'regret', 'reveal', 'female', 'invite', 'resist', 'stupid']
all_7_noun = ['Feature', 'Contact', 'Cabinet']
#len(all_words) == 246
all_6_noun_len = 246 


count = 0
def set_word(word_len):
    """take word in turn, if count == last index -> reset it"""
    wd_list = all_5_noun if word_len == 5 else all_6_noun if word_len == 6 else all_7_noun
    word = choice(wd_list)
    return word.strip().lower()