function showAddServiceModal() {
  document.getElementById('add-service-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function hideAddServiceModal() {
  document.getElementById('add-service-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

async function submitAddService(event) {
  event.preventDefault();

  const serviceName = document.getElementById('service-name').value.trim();
  const serviceVersion = document.getElementById('service-version').value.trim();

  if (!serviceName || !serviceVersion) {
    alert('Please fill in all fields.');
    return;
  }

  try {
    const response = await fetch('http://192.168.64.1:5000/services', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: serviceName, version: serviceVersion }),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.message || 'Failed to add service'}`);
      return;
    }

    alert('Service added successfully!');
    hideAddServiceModal();
    location.reload(); // Reload the page to reflect the new service
  } catch (error) {
    console.error('Error adding service:', error);
    alert('Something went wrong. Please try again.');
  }
}