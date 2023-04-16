document.addEventListener('DOMContentLoaded', () => {
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('video-preview');
    const menuItems = document.querySelectorAll('.menu-item');
    const applyChangesButton = document.getElementById('apply-changes');

    videoInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            videoPreview.src = url;
        }
    });

    menuItems.forEach((menuItem) => {
        menuItem.addEventListener('click', (event) => {
            const clickedSubmenu = event.target.nextElementSibling;
            clickedSubmenu.hidden = !clickedSubmenu.hidden;

            // Collapse other submenus
            menuItems.forEach((otherMenuItem) => {
                if (otherMenuItem !== event.target) {
                    const otherSubmenu = otherMenuItem.nextElementSibling;
                    otherSubmenu.hidden = true;
                }
            });
        });
    });

  applyChangesButton.addEventListener("click", async () => {
    if (!videoInput.files[0]) {
      alert("Please upload a video file.");
      return;
    }

    const trimOptions = document.querySelectorAll(".trim-option");
    const textOptions = document.querySelectorAll(".text-option");
    const filterOptions = document.querySelectorAll(".filter-option");

    const formData = new FormData();
    formData.append("video", videoInput.files[0]);
    formData.append("trim_start", trimOptions[0].checked);
    formData.append("trim_end", trimOptions[1].checked);
    formData.append("add_title", textOptions[0].checked);
    formData.append("add_subtitles", textOptions[1].checked);
    formData.append("black_and_white", filterOptions[0].checked);
    formData.append("sepia", filterOptions[1].checked);
    
    try {
      const response = await fetch("http://localhost:8001/process", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result);
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
});

document.getElementById("toggle-result").addEventListener("click", () => {
  const resultMessage = document.getElementById("result-message");
  resultMessage.hidden = !resultMessage.hidden;
});