    document.getElementById('toggleCommentFormButton').addEventListener('click', function() {
        var formContainer = document.getElementById('commentFormContainer');
        formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
    });


    document.addEventListener('DOMContentLoaded', function() {
        const statusDropdowns = document.querySelectorAll('.status-dropdown');
        statusDropdowns.forEach(dropdown => {
            dropdown.addEventListener('change', function(event) {
                const rfiId = event.target.dataset.rfiId;
                const newStatus = event.target.value;
                const updateUrl = `{% url 'rficrud:update_rfi_status' 0 'placeholder' %}`.replace('/0/', `/${rfiId}/`).replace('placeholder', newStatus);

                fetch(updateUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'error') {
                        alert(data.message);
                        event.target.value = '{{ rfi.status }}';
                    }
                })
                .catch(error => {
                    console.error('Error updating status:', error);
                    event.target.value = '{{ rfi.status }}';
                });
            });
        });
    });