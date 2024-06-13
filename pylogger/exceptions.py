class UnknownError(Exception):
    """Raised when an unknown error is raised"""

    def __init__(self, data: str):
        """Raised when an unknown error is raised

        :param data: Additional error data, tipically ``format_exc()``
        :type data: str
        """

        super().__init__(data)
