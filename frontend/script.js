function upload() {
    const files = document.getElementById("pdfFiles").files;
    const formData = new FormData();

    for (let file of files) {
        formData.append("files", file);
    }

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").textContent =
            JSON.stringify(data, null, 2);
    })
    .catch(err => console.error(err));
}