$(document).ready(function() {
  // Hide project field initially
  $('#id_project_name').parent().hide();

  // Trigger project field update on object selection change
  $('#id_object_name').on('change', function() {
    var objectID = $(this).val();
    if (objectID) {
      // Make AJAX request to fetch available projects
      $.ajax({
        url: '/get_projects_by_object/' + objectID + '/',
        type: 'GET',
        success: function(data) {
          // Clear project field options
          $('#id_project_name').empty();

          // Add available projects as options
          $.each(data, function(index, project) {
            $('#id_project_name').append($('<option>', {
              value: project.id,
              text: project.name
            }));
          });

          // Show project field
          $('#id_project_name').parent().show();

          // Update Akkuyu signer field
          updateAkkuyuSignerField(objectID);
        },
        error: function(xhr, textStatus, errorThrown) {
          console.log('Error:', errorThrown);
        }
      });
    } else {
      // Clear project field options and hide it
      $('#id_project_name').empty().parent().hide();
    }
  });

  function updateAkkuyuSignerField(objectId) {
    $.ajax({
      url: '/api/defualt-signers/' + objectId + '?format=json',
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        console.log(data.object_name.id);
        console.log(objectId);
        console.log(data.akkuyy_signer.name);
        console.log(data.independent_signer);
        console.log(data.titan2_qc_signer);
        if (objectId == data.object_name.id) {
          $('#id_akkuyu_signer').val(data.akkuyy_signer.id);
          $('#id_independent_control').val(data.independent_signer.id);
          $('#id_qc_signer').val(data.titan2_qc_signer.id);
          $('#id_design_supervision_signer').val(data.supervision_signer.id);
          $('#id_contractor').val(data.titan2_contractor_signer.id);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log('Error:', errorThrown);
      }
    });
  }

  // Add row functionality
  $('#add-row').on('click', function() {
    var row = $('.work-row').first().clone();
    row.find('input').val('');
    row.insertAfter('.work-row:last');
  });

  // Show/hide work section based on type selection
  $('#id_type').on('change', function() {
    var selectedType = $(this).val();
    if (selectedType === 'СМР' || selectedType === 'АКЗ' || selectedType === 'СТР') {
      $('#work-section').show();
    } else {
      $('#work-section').hide();
    }
  });

  // Add elevation row functionality
  $(document).on('click', '#add_elevation_row', function() {
    var rowHtml = `
      <div class="form-group">
        <div class="row">
          <div class="col-md-4">
            <label for="id_axes">Оси:</label>
            <input type="text" name="axes" class="form-control">
          </div>
          <div class="col-md-4">
            <label for="id_from_elevation">От отметки:</label>
            <input type="text" name="from_elevation" class="form-control">
          </div>
          <div class="col-md-4">
            <label for="id_to_elevation">До отметки:</label>
            <input type="text" name="to_elevation" class="form-control">
          </div>
        </div>
      </div>
    `;

    $('#additional_elevation_section').append(rowHtml);
  });

  // Add construction element section functionality
  $(document).on('click', '#add_construction_element_section', function() {
    var sectionHtml = `
      <div class="form-section">
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="id_construction_element">Конструктивный элемент:</label>
              <input type="text" name="construction_element" class="form-control">
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="id_axes">Оси:</label>
          <input type="text" name="axes" class="form-control">
        </div>
        <div class="row">
          <div class="col-md-4">
            <label for="id_from_elevation">От отметки:</label>
            <input type="text" name="from_elevation" class="form-control">
          </div>
          <div class="col-md-4">
            <label for="id_to_elevation">До отметки:</label>
            <input type="text" name="to_elevation" class="form-control">
          </div>
        </div>
      </div>
    `;

    $('#additional_elevation_section').after(sectionHtml);
  });

  // Submit form
  $('form').on('submit', function(e) {
    e.preventDefault();

    // Get form data
    var formData = $(this).serialize();
    console.log(formData);

    // Send AJAX request or perform form submission
    // ...
  });
});
