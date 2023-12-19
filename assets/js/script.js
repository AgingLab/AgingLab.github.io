(function() {
    var slider = document.getElementById('image-slider');
    var images = slider.getElementsByTagName('img');
    var currentIndex = 0;
    var interval = 3000; // Duration in milliseconds between image changes

    function changeImage() {
        images[currentIndex].classList.remove('visible');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('visible');
    }

    setInterval(changeImage, interval);
})();


function openTab(evt, tabId) {
  const tabs = document.getElementsByClassName("tab");
  for (let i = 0; i < tabs.length; i++) {
    tabs[i].style.display = "none";
  }

  const tabButtons = document.getElementsByClassName("tab-btn");
  for (let i = 0; i < tabButtons.length; i++) {
    tabButtons[i].classList.remove("active");
  }

  document.getElementById(tabId).style.display = "block";
  evt.currentTarget.classList.add("active");
}
