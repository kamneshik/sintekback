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
      url:  `/api/defualt-signers/${objectId}/?format=json`,
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        console.log(data.object_name);
        console.log(data.akkuyy_signer.name);
        console.log(data.independent_signer);
        console.log(data.titan2_qc_signer);

        $('#id_akkuyu_signer').val(data.akkuyy_signer.id);
        $('#id_independent_control').val(data.independent_signer.id);
        $('#id_qc_signer').val(data.titan2_qc_signer.id);
        $('#id_design_supervision_signer').val(data.supervision_signer.id);
        $('#id_contractor').val(data.titan2_contractor_signer.id);
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log('Error:', errorThrown);
      }
    });
  }
});
