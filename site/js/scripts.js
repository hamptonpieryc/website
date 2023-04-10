function expand(btn,content) {
  document.getElementById(content).style.display = "block";
  document.getElementById(btn).style.display = "none";
}

function collapse(btn,content) {
  document.getElementById(content).style.display = "none";
  document.getElementById(btn).style.display = "inline";
}

function copyInputClipboard(element) {
  // Get the text field
  var copyText = document.getElementById(element);

  // Select the text field
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices

   // Copy the text inside the text field
  navigator.clipboard.writeText(copyText.value);

  // Alert the copied text
  alert("Copied the text: " + copyText.value);
}

function copyTextToClipboard(theText) {
  // Get the text field


   // Copy the text inside the text field
  navigator.clipboard.writeText(theText);


}

//function showmenu() {
//  document.getElementById("nav").style.display = "none";
//  //document.getElementById(btn).style.display = "inline";
//}