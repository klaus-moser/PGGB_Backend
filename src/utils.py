from re import fullmatch


class Utils:
    """
    Class with useful functions
    """

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate a given email for its format: {String}+@{String}.{String}

        :param email: Email to be validated by RegEx.
        """

        regex = '^[^@]+@{1}[^@]+[.]{1}[^@]+$'

        if not fullmatch(regex, email):
            return False
        return True
