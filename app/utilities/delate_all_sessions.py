from flask import session

def delete_sessions():
        session.pop('client_word', None)
        session.pop('find_word', None)
        session.pop('global_direct', None)
        session.pop('global_indirect', None)
        session.pop('word_history', None)
        session.pop('attempt_number', None)
        session.pop('last_time_win', None)
        session.pop('client_word', None)
        session.pop('indirect_match', None)
        session.pop('direct_match', None)