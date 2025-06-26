const inside = document.getElementById("in");
const fileEl = document.getElementById("fileElem")
const fileP = document.getElementById("file");
const form = document.getElementById("form");

form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const fileInput = document.getElementById('fileElem');
      const file = fileInput.files[0];

      if (!file) {
        alert("Διάλεξε ένα αρχείο πρώτα!");
        return;
      }

      const formData = new FormData();
      formData.append("fileElem", file);

      try {
        const response = await fetch("http://127.0.0.1:8000/process", {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          throw new Error(`Σφάλμα ${response.status}`);
        }

        const result = await response.json();
        console.log("Απάντηση από server:", result);
        alert("Επιτυχία! Δες κονσόλα.");
      } catch (err) {
        alert("Σφάλμα σύνδεσης: " + err.message);
      }
});

inside.addEventListener('click', () => {
    inside.classList.add('dragover');
    fileEl.click();
});

fileEl.addEventListener('change', () => {
    if (fileEl.files.length > 0) {
      fileP.textContent = fileEl.files[0].name;
    }
    else{
      fileP.textContent = "";
      inside.classList.remove('dragover');
    }
});

inside.addEventListener('dragover', (e) => {
    e.preventDefault();
    inside.classList.add('dragover');
  });

inside.addEventListener('dragleave', () => {
    inside.classList.remove('dragover');
});


inside.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;

    if (files.length > 0) {
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(files[0]);
      fileEl.files = dataTransfer.files;
      fileP.textContent = fileEl.files[0].name;
    }
  });