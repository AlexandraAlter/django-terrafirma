from django import forms


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({
            'list': 'list__{}'.format(self._name),
            'autocomplete': 'off',
        })

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs=attrs)
        data_list = '<datalist id="list__{}">'.format(self._name)
        items = self._list() if callable(self._list) else self._list
        for item in items:
            data_list += '<option value="{}">'.format(item)
        data_list += '</datalist>'

        return (text_html + data_list)

