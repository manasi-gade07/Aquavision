// Script for future dropdown functionality (if needed for more interaction)
document.querySelector('.dropdown').addEventListener('click', function() {
    var dropdownContent = this.querySelector('.dropdown-content');
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
});
let slideIndex = 0;
showSlides();

function showSlides() {
    let slides = document.getElementsByClassName("slide");
    
    // Hide all slides initially
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    
    slideIndex++;
    
    // Reset index if it exceeds the number of slides
    if (slideIndex > slides.length) { 
        slideIndex = 1; 
    }
    
    // Show the current slide
    slides[slideIndex-1].style.display = "block";  
    
    // Automatically change slide every 5 seconds
    setTimeout(showSlides, 2000); 
}

function plusSlides(n) {
    let slides = document.getElementsByClassName("slide");
    slideIndex += n;

    // Ensure the index stays within the bounds of available slides
    if (slideIndex > slides.length) { 
        slideIndex = 1;
    } else if (slideIndex < 1) {
        slideIndex = slides.length;
    }
    
    // Hide all slides and show the current one
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    
    slides[slideIndex-1].style.display = "block";
}
