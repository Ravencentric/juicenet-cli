class JuicenetError(Exception):
    """Base exception for all juicenet API errors"""

    pass


class JuicenetInputError(JuicenetError):
    """Invalid Input"""

    pass
