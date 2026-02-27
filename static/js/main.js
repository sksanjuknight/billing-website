// Main JavaScript for Snacks Billing Application

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} fixed top-4 right-4 max-w-md z-50`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

// Open Modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

// Close Modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// Form submission with AJAX
function submitForm(formId, url, callback) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const formData = new FormData(form);
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Operation successful!', 'success');
            if (callback) callback(data);
        } else {
            showNotification(data.error || 'An error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}

// Delete confirmation
function confirmDelete(message = 'Are you sure?') {
    return confirm(message);
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2,
    }).format(value);
}

// Add row to dynamic table
function addTableRow(tableId, rowHTML) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = rowHTML;
    tbody.appendChild(tr);
}

// Remove table row
function removeTableRow(rowElement) {
    rowElement.closest('tr').remove();
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
    console.log('Snacks Billing App loaded');
});

// Export functions for global use
window.showNotification = showNotification;
window.openModal = openModal;
window.closeModal = closeModal;
window.submitForm = submitForm;
window.confirmDelete = confirmDelete;
window.formatCurrency = formatCurrency;
window.addTableRow = addTableRow;
window.removeTableRow = removeTableRow;
