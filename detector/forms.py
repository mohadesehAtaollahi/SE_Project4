from django import forms

class FormOne(forms.Form):
    q1 = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Do you prefer facts, data, and evidence?"
    )

    q2 = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Do you prefer tangible and concrete things over abstract ideas?"
    )

    q3 = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Do you usually rely more on logic than intuition when making decisions?"
    )


class FormTwo(forms.Form):
    h = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Is your height approximately above 175 cm?"
    )

    shoe = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Is your shoe size generally above 42?"
    )

    beard = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Does your facial hair grow more than 0.5 cm per week?"
    )

    voice = forms.ChoiceField(
        choices=[("yes","Yes"),("no","No")],
        widget=forms.RadioSelect,
        label="Do you have a deep and low-pitched voice?"
    )