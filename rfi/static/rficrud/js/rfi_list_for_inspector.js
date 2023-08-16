console.log('Test message');

const csrfToken = document.getElementById('csrfToken').value;

document.getElementById('toggleFormButton').addEventListener('click', function() {
  console.log('DOMContentLoaded fired');
  var formContainer = document.getElementById("filterForm");
  formContainer.classList.toggle('hidden');
});

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOMContentLoaded fired');
  // First part
  var objectNameSelect = document.getElementById("id_object_name");
  var projectNameInput = document.getElementById("id_project_name");

  function updateProjectList() {
    var objectNameId = objectNameSelect.value;
    if (objectNameId) {
      $.ajax({
        url: '/get_projects_by_object/' + objectNameId + '/',
        type: 'GET',
        success: function(data) {
          projectNameInput.empty();
          $.each(data, function(index, project) {
            projectNameInput.append($('<option>', {
              value: project.id,
              text: project.name
            }));
          });
        },
        error: function(xhr, textStatus, errorThrown) {
          console.log('Error:', errorThrown);
        }
      });
    } else {
      projectNameInput.empty();
    }
  }

  objectNameSelect.addEventListener('change', updateProjectList);

  // Second part
  const statusDropdowns = $('.status-dropdown');

  statusDropdowns.on('change', function(event) {
    const rfiId = $(this).data('rfiId');
    const newStatus = $(this).val();
    const updateUrl = updateUrlTemplate.replace('/0/', `/${rfiId}/`).replace('placeholder', newStatus);
;
    $.ajax({
      url: updateUrl,
      type: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      success: function(data) {
        if (data.status === 'success') {
          const rfiRow = $(`#rfi-row-${rfiId}`);

          const newClasses = getTableRowClass(newStatus);

          rfiRow.attr('class', newClasses);
        } else {
          alert(data.message);
          $(this).val('{{ rfi.status }}');
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        console.error('Error updating status:', errorThrown);
        $(this).val('{{ rfi.status }}');
      },
    });
  });

  function getTableRowClass(status) {
    if (status === 'rejected') {
      return 'table-danger';
    } else if (status === 'accepted') {
      return 'table-success';
    } else if (status === 'in process') {
      return 'table-warning';
    } else if (status === 'canceled') {
      return 'table-secondary';
    } else {
      return '';
    }
  }
});
