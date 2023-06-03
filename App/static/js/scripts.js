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

    function updatePageWithResults(result) {
      const resultMessage = document.getElementById('result-text');
      if (result['result']['summarized_text'] != null){
      resultMessage.innerHTML = `<b>Summary</b>: ${JSON.stringify(result['result']['summarized_text'])}`;
      }

      resultMessage.hidden = false;
      const video = document.getElementById('video-preview');
      video.src = result['video_url'];
  }

    const trimOptions = document.querySelectorAll(".trim-option");
    const textOptions = document.querySelectorAll(".text-option");
    const filterOptions = document.querySelectorAll(".filter-option");
    const summarizeOptions = document.querySelectorAll(".summarize-option");
    const audioOptions = document.querySelectorAll(".audio-option");


    const formData = new FormData();
    formData.append("video", videoInput.files[0]);
    formData.append("trim_start", trimOptions[0].checked);
    formData.append("trim_end", trimOptions[1].checked);
    formData.append("add_subtitles", textOptions[0].checked);
    formData.append("translate_subtitles", textOptions[1].checked);
    formData.append("summarize", summarizeOptions[0].checked);
    formData.append("news_letter", summarizeOptions[1].checked);
    formData.append("blur_faces", filterOptions[0].checked);
    formData.append("blur_license_plates", filterOptions[1].checked);
    formData.append("audio_clean", audioOptions[0].checked);

    
    try {
      const response = await fetch("http://localhost:8001/request", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        updatePageWithResults(result, videoInput.files[0].fil);
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