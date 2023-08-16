$(document).ready(function () {
    const objectName = $("#id_object_name");
    const fieldsToFilter = [
        $("#id_project_name"),
        $("#id_akkuyu_signer"),
        $("#id_independent_control"),
        $("#id_qc_signer"),
        $("#id_design_supervision_signer"),
        $("#id_contractor"),
    ];

    objectName.on("change", function () {
        const selectedObject = $(this).val();
        filterFields(selectedObject);
    });

    function filterFields(selectedObject) {
        fieldsToFilter.forEach(function (field) {
            const currentValue = field.val();
            field.find("option").each(function () {
                const option = $(this);
                const optionObject = option.data("object");
                if (optionObject && optionObject !== selectedObject) {
                    option.hide();
                } else {
                    option.show();
                }
            });

            field.val(
                field
                    .find("option")
                    .filter(function () {
                        return $(this).css("display") !== "none";
                    })
                    .first()
                    .val()
            );
        });
    }

    fieldsToFilter.forEach(function (field) {
        field.find("option").each(function () {
            const option = $(this);
            option.data("object", option.val().split("-")[0]);
        });
    });

    filterFields(objectName.val());
});
