class ChallengeBaseError(Exception):
    pass


class FileNotFoundError(ChallengeBaseError):
    pass


class UnableToMapRecordError(ChallengeBaseError):
    pass


class UndefinedValueInRecord(ChallengeBaseError):
    pass
