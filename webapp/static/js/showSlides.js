let slideIndex = 0;
let slideIndex_1 = 0;

showSlides();

// let slideIndex_1 = 0;
// showSlides_1();
function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
    // setTimeout(showSlides, 2000); // Change image every 2 seconds

    // let j;
    // let slides_1 = document.getElementsByClassName("mySlides_1");
    // let dots_1 = document.getElementsByClassName("dot_1");
    // for (i = 0; i < slides_1.length; i++) {
    // slides_1[i].style.display = "none";  
    // }
    // slideIndex_1++;
    // if (slideIndex_1 > slides_1.length) {slideIndex_1 = 1}    
    // for (j = 0; j < dots_1.length; j++) {
    // dots_1[j].className = dots_1[j].className.replace(" active", "");
    // }
    // slides_1[slideIndex_1-1].style.display = "block";  
    // dots_1[slideIndex_1-1].className += " active";
    setTimeout(showSlides, 2000); // Change image every 2 seconds
}
