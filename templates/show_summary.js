/**
 * Displays the Script Summary modal with the given content using simple class manipulation.
 * @param {string} summaryText - The text content for the script summary.
 */
function showScriptSummaryModal(summaryText) {
    const titleElement = document.getElementById('modal-summary-title');
    const bodyElement = document.getElementById('modal-summary-body');
    const modalElement = document.getElementById('script-summary-modal'); // 🌟 Updated ID

    titleElement.textContent = "Script Summary";

    // Inject content. Use whitespace-pre-wrap to respect line breaks in the LONGTEXT field.
    bodyElement.innerHTML = `<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400 whitespace-pre-wrap">${summaryText}</p>`;
    
    // 🌟 Show the modal by removing the 'hidden' class
    modalElement.classList.remove('hidden');

    // Simple fix to center the modal and add a dark background overlay
    modalElement.classList.add('flex'); 
    document.body.style.overflow = 'hidden'; 
}

// Function to hide the modal (for header button if Flowbite JS is absent)
function hideScriptSummaryModal() {
    const modalElement = document.getElementById('script-summary-modal');
    modalElement.classList.add('hidden');
    modalElement.classList.remove('flex');
    document.body.style.overflow = 'auto';
}