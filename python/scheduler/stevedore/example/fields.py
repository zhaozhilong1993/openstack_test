from stevedore.example import base
import textwrap


class FieldList(base.FormatterBase):
    def format(self, data):
        for name, value in sorted(data.items()):
            full_text = ': {name} : {value}'.format(
                name=name,
                value=value,
            )
            wrapped_text = textwrap.fill(
                full_text,
                initial_indent='',
                subsequent_indent='    ',
                width=self.max_width,
            )
            yield wrapped_text + '\n'
