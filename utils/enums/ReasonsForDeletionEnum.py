from enum import Enum


class DeletionReasons(Enum):
    BANNED_LANGUAGE = "banned_language"
    ADVERTISING = "advertising"
    SPAM = "spam"
    HATE = "hate"
    OFFENSIVE = "offensive"
