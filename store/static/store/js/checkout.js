// Checkout payment method toggle
document.addEventListener('DOMContentLoaded', function() {
    const paymentOptions = document.querySelectorAll('.payment-option');
    const paymentFields = document.querySelectorAll('.payment-fields');

    function toggleFields() {
        const selectedMethod = document.querySelector('input[name="method"]:checked').value;
        paymentFields.forEach(field => {
            if (field.dataset.method === selectedMethod) {
                field.classList.add('show');
            } else {
                field.classList.remove('show');
            }
        });
    }

    // Handle payment option clicks
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            radio.checked = true;
            toggleFields();
        });
    });

    // Initial toggle
    if (document.querySelector('input[name="method"]:checked')) {
        toggleFields();
    }
});
