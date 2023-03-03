import re


class PrePro:
    @staticmethod
    def filter(code: str) -> str:
        try:
            return re.match("(.*?)#", code).group()[:-1]
        except:
            return code
