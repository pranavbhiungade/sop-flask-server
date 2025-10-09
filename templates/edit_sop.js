function enableInlineEditing(rowId, sopId) {
    const row = document.getElementById(`row-${rowId}`);
    if (!row) return;

    // Find the SOP object by ID from your global SOP array
    let sop = null;
    for (const serviceObj of allSOPData) {
        for (const versionObj of serviceObj.versions) {
            sop = versionObj.sops.find(s => s.id === sopId);
            if (sop) break;
        }
        if (sop) break;
    }
    if (!sop) return;

    // Fetch users for the "Modified By" dropdown
    fetch("http://192.168.64.1:5000/users")
        .then(response => response.json())
        .then(users => {
            let modifiedByOptions = users.map(user =>
                `<option value="${user.id}"${user.id === sop.last_modified_by ? " selected" : ""}>${user.username}</option>`
            ).join("");

            row.innerHTML = `
        <td><input type="text" value="${escapeHtml(sop.alert_name || '')}" id="edit-alert-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent"></td>
        <td><input type="text" value="${escapeHtml(sop.sop_title || '')}" id="edit-title-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent"></td>
        <td><textarea id="edit-description-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent" rows="2">${escapeHtml(sop.sop_description || '')}</textarea></td>
        <td><input type="text" value="${escapeHtml(sop.daemon_tool_service || '')}" id="edit-daemon-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent"></td>
        <td><textarea id="edit-script-summary-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent" rows="2">${escapeHtml(sop.script_summary || '')}</textarea></td>
        <td><input type="text" value="${escapeHtml(sop.sop_link || '')}" id="edit-link-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent" style="min-width:100px;" ></td>

        <td>${escapeHtml(sop.created_by || '-')}</td>
        <td>
          <select id="edit-modified-by-${rowId}" class="w-full text-sm border border-gray-100 rounded bg-transparent" style="min-width:80px;">
            ${modifiedByOptions}
          </select>
        </td>
        <td>${escapeHtml(sop.created_at || '-')}</td>
        <td>${escapeHtml(sop.updated_at || '-')}</td>
        <td>
          <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 12px; height: 100%;">
            <button class="action-btn save-btn bg-green-500 text-white" onclick="saveRow('${rowId}', ${sop.id})">
              <svg class="w-4 h-4 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 11.917 9.724 16.5 19 7.5"/>
              </svg>
            </button>
            <button class="action-btn cancel-btn bg-gray-500 text-white" onclick="cancelEdit('${rowId}', ${sop.id})">
              <svg class="w-4 h-4 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="m6 6 12 12m3-6a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
              </svg>
            </button>
          </div>
        </td>
      `;
        });
}

function saveRow(rowId, sopId) {
    const alertName = document.getElementById(`edit-alert-${rowId}`).value.trim();
    const title = document.getElementById(`edit-title-${rowId}`).value.trim();
    const description = document.getElementById(`edit-description-${rowId}`).value.trim();
    const daemonToolService = document.getElementById(`edit-daemon-${rowId}`).value.trim();
    const scriptSummary = document.getElementById(`edit-script-summary-${rowId}`).value.trim();
    const link = document.getElementById(`edit-link-${rowId}`).value.trim();
    const modifiedBy = document.getElementById(`edit-modified-by-${rowId}`).value;

    const payload = {
        alert: alertName,
        sop_title: title,
        sop_description: description,
        daemon_tool_service: daemonToolService,
        script_summary: scriptSummary,
        sop_link: link,
        last_modified_by: modifiedBy
    };

    fetch(`http://192.168.64.1:5000/sops/${sopId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    })
        .then(async response => {
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to update SOP');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || 'SOP updated successfully!');
            fetchGroupedSOPs(); // Refresh the SOP list
        })
        .catch(err => {
            console.error('Error updating SOP:', err);
            alert('Failed to update SOP. Please try again.');
        });
}

function cancelEdit(rowId, sopId) {
    const row = document.getElementById(`row-${rowId}`);
    if (!row) return;

    // Find the SOP object by ID from allSOPData
    let sop = null;
    for (const serviceObj of allSOPData) {
        for (const versionObj of serviceObj.versions) {
            sop = versionObj.sops.find(s => s.id === sopId);
            if (sop) break;
        }
        if (sop) break;
    }
    if (!sop) return;

    // Restore the original row content
    row.innerHTML = `
    <td>${escapeHtml(sop.alert_name || '-')}</td>
    <td>${escapeHtml(sop.sop_title || '-')}</td>
    <td>${escapeHtml(sop.sop_description || '-')}</td>
    <td>${escapeHtml(sop.daemon_tool_service || '-')}</td>
    <td style="white-space: pre-line; text-align: justify; word-break: break-word;">
  ${escapeHtml(sop.script_summary || 'No summary provided')}
        </td>
    <td>${sop.sop_link ? `<a href="${escapeHtml(sop.sop_link)}" target="_blank" class="open-sop-link flex items-center gap-1 text-blue-600 hover:underline">Open</a>` : '-'}</td>
    <td>${escapeHtml(sop.created_by || '-')}</td>
    <td>${escapeHtml(sop.last_modified_by || '-')}</td>
    <td>${escapeHtml(sop.created_at || '-')}</td>
    <td>${escapeHtml(sop.updated_at || '-')}</td>
    <td>
            <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 12px; height: 100%;">
              <button class="action-btn edit-btn" title="Edit" style="display: flex; align-items: center; justify-content: center;" onclick='enableInlineEditing("${rowId}", ${sop.id})'>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M4 21h17v2H3a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h2v2H4v17zm16.7-13.3a1 1 0 0 0 0-1.4l-2-2a1 1 0 0 0-1.4 0l-9.6 9.6a1 1 0 0 0-.3.6l-.7 4.2a1 1 0 0 0 1.2 1.2l4.2-.7a1 1 0 0 0 .6-.3l9.6-9.6zm-3.3-1.3 2 2-1.3 1.3-2-2L17.4 6.4zm-9 9 6.6-6.6 2 2-6.6 6.6-2.5.4.5-2.4z"/></svg>
              </button>
              <button class="action-btn delete-btn" title="Delete" style="display: flex; align-items: center; justify-content: center;" onclick="deleteSOP(${sop.id})">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M5 6h14v2H5V6zm2 3h10l-1.5 12.5a1 1 0 0 1-1 .5h-5a1 1 0 0 1-1-.5L7 9zm3 2v7h2v-7h-2z"/></svg>
              </button>
            </div>
          </td>
  `;
}
