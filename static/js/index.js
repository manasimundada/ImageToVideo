const text = "Home Page!";
const delay = 80; // Delay in milliseconds between each character

let index = 0;

function typeText(){
  if (index < text.length) {
    document.getElementById("homepage").textContent += text.charAt(index);
    index++;
    setTimeout(typeText, delay);
  }
}
function reboundText(event) {
    const button = event.target;
    const bounds = button.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;
    
    const span = document.createElement('span');
    span.textContent = button.textContent;
    span.style.position = 'absolute';
    span.style.left = `${x}px`;
    span.style.top = `${y}px`;
    span.style.transition = 'all 0.3s ease';
    span.style.pointerEvents = 'none';
    
    button.appendChild(span);
    
    setTimeout(() => {
        span.style.transform = 'translate(-50%, -50%)';
        span.style.opacity = '0';
    }, 20);
    
    setTimeout(() => {
        span.remove();
    }, 300);
}


window.onload = function (){
    document.getElementById('sign_up').addEventListener('mouseenter', reboundText);
    document.getElementById('sign_in').addEventListener('mouseenter', reboundText);
    typeText();
};