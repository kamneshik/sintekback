console.log('Test message');

document.getElementById('toggleFormButton').addEventListener('click', function() {
    console.log('DOMContentLoaded fired'); // Add this line
    var formContainer = document.getElementById("filterForm");
    formContainer.classList.toggle('hidden');
});



document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired'); // Add this line
    // First part
    var objectNameSelect = document.getElementById("id_object_name");
    var projectNameInput = document.getElementById("id_project_name");

    function updateProjectList() {
        var objectNameId = objectNameSelect.value;
        if (objectNameId) {
            console.log('Dropdowns found:', statusDropdowns.length); // Add this line
            fetch(`/get_projects_by_object/${objectNameId}/`)
                .then(response => response.json())
                .then(projects => {
                    projectNameInput.innerHTML = "";
                    projects.forEach(project => {
                        var option = document.createElement("option");
                        option.value = project.id;
                        option.textContent = project.name;
                        projectNameInput.appendChild(option);
                    });
                });
        } else {
            projectNameInput.innerHTML = "";
        }
    }

    objectNameSelect.addEventListener('change', updateProjectList);

});