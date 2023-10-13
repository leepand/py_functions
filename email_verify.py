import re

emailRegex = re.compile(
    r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", re.IGNORECASE
)


def verifyEmailAddy(x):
    return emailRegex.match(x) is not None


verifyEmailAddy("padd@163.com")
