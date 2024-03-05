class ClientError(Exception):
    """Base class for client exceptions."""

    pass


class ClientRequestError(ClientError):
    """Exception for problems with the Request."""

    pass
