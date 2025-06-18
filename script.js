document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('button[data-type]');
    const modal = new bootstrap.Modal(document.getElementById('uploadModal'));

    buttons.forEach(button => {
        const type = button.getAttribute('data-type');
        button.addEventListener('click', function () {
            document.getElementById('fileAction').value = type;
            then(data => {
                document.getElementById("submitBtn").disabled = false;
                 document.getElementById("loader").classList.add("d-none");
            
    if (data.error) {
        alert(data.error);
        return;
    }
            runValidation(type).then(() => modal.show());
        });
    });

    document.getElementById('uploadForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
             document.getElementById("successMessage").classList.remove("d-none");

            if (response.ok && result.download1 && result.download2) {
                document.getElementById('download1').href = data.output_file_1;
                document.getElementById('download2').href = data.output_file_2;
                document.getElementById('downloadLinks').classList.remove("d-none");

            } else {
                console.error("Upload failed", result);
                alert(result.message || 'Unknown error occurred.');
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('An error occurred while uploading.');
        }

    });
}
