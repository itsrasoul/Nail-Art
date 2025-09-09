from django import forms
from .models import Profile, Contact, OrderPayment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'phone', 'avatar', 'welcome_text')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = OrderPayment
        fields = ('method', 'card_name', 'card_last4', 'bank_name', 'paypal_email', 'cashapp_tag', 'crypto_address')
        widgets = {
            'card_name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'paypal_email': forms.EmailInput(attrs={'placeholder': 'your.email@example.com'}),
            'cashapp_tag': forms.TextInput(attrs={'placeholder': '$yourusername or +1234567890'}),
            'crypto_address': forms.TextInput(attrs={'placeholder': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'Bank name, account number, routing number'}),
        }

    # Add realistic card fields for UI; we will only persist last4
    card_number = forms.CharField(max_length=19, required=False, widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_expiry = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvv = forms.CharField(max_length=4, required=False, widget=forms.PasswordInput(attrs={'placeholder': '123'}))

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('method')
        if method == 'card':
            if not cleaned.get('card_number'):
                raise forms.ValidationError('Card number is required for card payments')
            # basic numeric check for last4
            num = ''.join(filter(str.isdigit, cleaned.get('card_number')))
            if len(num) < 12:
                raise forms.ValidationError('Enter a valid card number')
        elif method == 'paypal':
            if not cleaned.get('paypal_email'):
                raise forms.ValidationError('PayPal email is required for PayPal payments')
        elif method == 'cashapp':
            if not cleaned.get('cashapp_tag'):
                raise forms.ValidationError('Cash App tag is required for Cash App payments')
        elif method == 'crypto':
            if not cleaned.get('crypto_address'):
                raise forms.ValidationError('Crypto address is required for cryptocurrency payments')
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        card_number = self.cleaned_data.get('card_number')
        if card_number:
            digits = ''.join(filter(str.isdigit, card_number))
            instance.card_last4 = digits[-4:]
        # do not save full card number or CVV
        if commit:
            instance.save()
        return instance
