import string


class ConfirmCode:
    def get_encode_string(self, obj):
        symbol_list = string.digits + string.ascii_letters
        encoding_str = list(obj)
        result = []
        for symbol in encoding_str:
            for index, sign in enumerate(symbol_list):
                if symbol == sign:
                    result.append(str(index))
        return ''.join(result)

    def is_same(self, obj, encode_str):
        encoding_str = self.get_encode_string(obj)
        return encoding_str == encode_str


confirmation_code = ConfirmCode()
