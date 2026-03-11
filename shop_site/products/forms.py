from django import forms


class CSVImportForm(forms.Form):
    """Форма для ипорта CSV в админ панели"""
    csv_file: forms.FileField = forms.FileField(
        label="CSV файл",
        help_text="Загрузите CSV файл с категориями"
    )

    def clean_csv_file(self):
        """
        Валидация импортируемого файла
        - Нельзя загрузить никакие форматы кроме CSV
        - Нельзя загрузить больше 5mb
        """
        csv_file = self.cleaned_data["csv_file"]

        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError("Файл должен быть в формате CSV")

        if csv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Файл слишком большой (макс 5MB)")

        return csv_file
