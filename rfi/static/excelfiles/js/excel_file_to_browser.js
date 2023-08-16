document.getElementById("input-excel").addEventListener("change", handleFile, false);

function handleFile(e) {
  const files = e.target.files;
  const f = files[0];

  const reader = new FileReader();

  reader.onload = function (e) {
    const data = e.target.result;
    const workbook = XLSX.read(data, { type: "binary" });

    // Assuming the first sheet contains the data you want to display
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];

    // Convert the sheet to an HTML table
    const html = XLSX.utils.sheet_to_html(sheet, { id: "excel-table", editable: false });

    // Display the table
    document.getElementById("excel-data").innerHTML = html;

    // Add Bootstrap classes to the table
    const table = document.getElementById("excel-table");
    table.classList.add("table", "table-striped", "table-bordered");
  };

  reader.readAsBinaryString(f);
}
