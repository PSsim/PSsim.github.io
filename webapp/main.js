// -----------------------------------------------------------------------------
// Borra Contenido de div clase 'PlotErase'
function borrarContenido() {
  const elementos = document.getElementsByClassName("PlotErase");
  for (let i = 0; i < elementos.length; i++) {
    elementos[i].innerHTML = "";
  }
}
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------
// Oculta Data Boxes
var miSection = document.getElementById("mi-div");
miSection.addEventListener("transitionend", function (event) {
    if (event.propertyName === "height") {
        if (miSection.classList.contains("oculto")) {
            miSection.style.display = "none";
        } else {
            miSection.style.height = "auto";
        }
    }
});

function toggleSection() {
    var miSection = document.getElementById("mi-div");
    miSection.classList.toggle("oculto");
    if (miSection.classList.contains("oculto")) {
        miSection.style.height = 0;
    } else {
        var height = miSection.scrollHeight;
        miSection.dataset.height = height;
        miSection.style.height = height + "px";
    }
}
// -----------------------------------------------------------------------------