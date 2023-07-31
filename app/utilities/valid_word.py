import enchant

dictionary = enchant.Dict("en_US")


def word_valid(user_word):
    """check if user word exist or it is just random word"""
    user_word = user_word

    if dictionary.check(user_word):
        return True
    return False