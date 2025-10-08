function showAddSOPModal() {
  populateServicesDropdown(); // Populate services dynamically
  document.getElementById('add-sop-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function hideAddSOPModal() {
  document.getElementById('add-sop-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

async function populateServicesDropdown() {
  const dropdown = document.getElementById('add-sop-service');

  try {
    const response = await fetch("http://192.168.64.1:5000/services"); // Replace with your actual backend URL
    if (!response.ok) throw new Error("Failed to fetch services");

    const services = await response.json();

    // Clear existing options except the placeholder
    dropdown.innerHTML = '<option value="">Select a service</option>';

    // Add options dynamically
   services.forEach(service => {
  const option = document.createElement("option");
  option.value = service.id; // Store service ID
  
  // 1. Check if the version is the string "0"
  const versionText = (service.version === "0") 
                      ? "" // If it's "0", use an empty string
                      : ` (v${service.version})`; // Otherwise, use the standard version format
  
  // 2. Set the text content
  option.textContent = `${service.name}${versionText}`; // Combine name and the conditionally formatted version
  
  dropdown.appendChild(option);
});

  } catch (error) {
    console.error("Error fetching services:", error);
  }
}
async function populateCreatedByDropdown() {
  const dropdown = document.getElementById("add-sop-created-by");

  try {
    const response = await fetch("http://192.168.64.1:5000/users"); // Replace with your actual backend URL
    if (!response.ok) throw new Error("Failed to fetch users");

    const users = await response.json();

    // Clear existing options except the placeholder
    dropdown.innerHTML = '<option value="">Select a user</option>';

    // Add options dynamically
    users.forEach(user => {
      const option = document.createElement("option");
      option.value = user.id;          // Store user ID
      option.textContent = user.username; // Show username
      dropdown.appendChild(option);
    });

  } catch (error) {
    console.error("Error fetching users:", error);
  }
}

// Call the function when the Add SOP modal is opened
function showAddSOPModal() {
  populateServicesDropdown(); // Populate services dynamically
  populateCreatedByDropdown(); // Populate created by dropdown dynamically
  document.getElementById('add-sop-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

async function submitAddSOP(event) {
  event.preventDefault();

  const serviceId = document.getElementById('add-sop-service').value;
  const alertName = document.getElementById('add-sop-alert').value.trim();
  const title = document.getElementById('add-sop-title').value.trim();
  const description = document.getElementById('add-sop-description').value.trim();
  const link = document.getElementById('add-sop-link').value.trim();
  
  // 🌟 READ NEW FIELD VALUES
  const daemonToolService = document.getElementById('add-sop-daemon-tool-service').value.trim();
  const scriptSummary = document.getElementById('add-sop-script-summary').value.trim();
  
  const createdBy = document.getElementById('add-sop-created-by').value;

  // Note: daemonToolService and scriptSummary are NOT required fields in your model (based on the Flask route),
  // so the validation check remains the same.
  if (!serviceId || !alertName || !title || !description || !createdBy) {
    alert('Please fill in all required fields.');
    return;
  }

  try {
    const response = await fetch('http://192.168.64.1:5000/sops', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        service_id: serviceId,
        alert: alertName,
        sop_title: title,
        sop_description: description,
        sop_link: link,
        
        // 🌟 INCLUDE NEW FIELDS IN PAYLOAD
        daemon_tool_service: daemonToolService,
        script_summary: scriptSummary,
        
        created_by: createdBy,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.error || 'Failed to add SOP'}`);
      return;
    }

    alert('SOP added successfully! 🎉');
    hideAddSOPModal();
    location.reload(); // Reload the page to reflect the new SOP
  } catch (error) {
    console.error('Error adding SOP:', error);
    alert('Something went wrong. Please try again.');
  }
}
