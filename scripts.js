function expand(btn,content) {
  document.getElementById(content).style.display = "block";
  document.getElementById(btn).style.display = "none";
}

function collapse(btn,content) {
  document.getElementById(content).style.display = "none";
  document.getElementById(btn).style.display = "inline";
}