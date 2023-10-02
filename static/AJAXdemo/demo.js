function loaddoc(){
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        document.getElementById("randint").innerHTML = this.responseText;
    }
    xhttp.open("GET", "/random", true);
    xhttp.send();
}