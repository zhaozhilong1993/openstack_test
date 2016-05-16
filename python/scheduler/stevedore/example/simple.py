from stevedore.example import base


class Simple(base.FormatterBase):
    def format(self, data):
        for name, value in sorted(data.items()):
            line = '{name} = {value}\n'.format(
                name=name,
                value=value,
            )
            yield line