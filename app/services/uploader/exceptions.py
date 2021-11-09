
class TelegraphError(Exception):
    __subclasses = []
    match = None
    text = None

    @classmethod
    def get_text(cls):
        if cls.text is None and cls.match is not None:
            return cls.match.replace('_', ' ').capitalize() + '!'
        return cls.text

    def __init_subclass__(cls, match=None, **kwargs):
        super(TelegraphError, cls).__init_subclass__(**kwargs)
        if match is not None:
            cls.match = match.upper()
            cls.__subclasses.append(cls)

    @classmethod
    def detect(cls, description):
        """
        Automation detect error type.
        :param description:
        :raise: TelegramError
        """
        match = description.upper()
        for err in cls.__subclasses:
            if err is cls:
                continue
            if err.match in match:
                raise err(err.get_text() or description)
        raise cls(description)


class NoFilesPassed(TelegraphError):
    def __init__(self):
        super(NoFilesPassed, self).__init__('No files has been uploaded.')
