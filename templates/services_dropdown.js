// Wait until the HTML document is fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
  
  // Find the <ul> element in the HTML where we'll insert the services
  const servicesList = document.getElementById('services-list');

  // Define an async function to fetch data from the API
  async function fetchServices() {
    try {
      // Make a GET request to your Flask endpoint
      const response = await fetch('http://192.168.64.1:5000/services');
      
      // Check if the request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      // Parse the JSON data from the response
      const services = await response.json();
      
      // Clear the "Loading..." text from the list
      servicesList.innerHTML = '';
      
      // Loop through each service object in the data array
      services.forEach(service => {
        // 1. Create a new list item (<li>)
        const listItem = document.createElement('li');
        
        // 2. Create a new link (<a>)
        const link = document.createElement('a');
        link.href = '#'; // Set a placeholder link
        link.className = 'block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white';
        
        // 🌟 CONDITIONAL LOGIC ADDED HERE 🌟
        // Determine the version text: if version is "0", use an empty string, otherwise format it with "(v...)"
        const versionText = (service.version === "0") 
                            ? "" 
                            : ` (v${service.version})`;
        
        // 3. Set the text content with the service name and the conditional version text
        link.textContent = `${service.name}${versionText}`;
        
        // 4. Put the link inside the list item, and the list item inside the <ul>
        listItem.appendChild(link);
        servicesList.appendChild(listItem);
      });

    } catch (error) {
      // If something goes wrong, log the error and show a message in the UI
      console.error('Failed to fetch services:', error);
      servicesList.innerHTML = '<li><a href="#" class="block px-4 py-2 text-red-500">Failed to load services</a></li>';
    }
  }
  
  // Call the function to start the process
  fetchServices();

});