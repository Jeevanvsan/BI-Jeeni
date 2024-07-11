
function morefn(){
  const hiddenParagraph = document.querySelector('.hidden');
    hiddenParagraph.style.display = (hiddenParagraph.style.display === 'none' || hiddenParagraph.style.display === '') ? 'block' : 'none';
  
    this.innerText = (hiddenParagraph.style.display === 'none') ? 'Read More' : 'Read Less';
}