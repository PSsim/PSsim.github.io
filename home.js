// -----------------------------------------------------------------------------
function verPDF(linkPDF) {
  var url = "https://drive.google.com/file/d/" + encodeURIComponent(linkPDF) + "/preview";
  window.open(url, '_blank');
}
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------
// Cambia el backgroundColor o borderColor de la clase 'classname'
function JSfcnHighlight(color, classname) {
  var aux = document.getElementsByClassName(classname);
  for (var i = 0; i < aux.length; i++) {
    aux[i].style.backgroundColor = color;
    // aux[i].style.borderColor = color;
  }
}

// Al pasar (o quitar) el mouse por 'id' llama a JSfcnHighlight y modifica elementos 'class'
function JSfcnEventMouse(buttonId, className, color) {
  document.getElementById(buttonId).addEventListener("mouseover", function () {
    JSfcnHighlight(color, className);
  });

  document.getElementById(buttonId).addEventListener("mouseout", function () {
    JSfcnHighlight("var(--color-oscuro)", className);
  });
}

// Eventos de JS
JSfcnEventMouse("NetworkButton", "Network", "#0d6efd");
JSfcnEventMouse("CONVgenButton", "CONVgen", "#dc3545");
JSfcnEventMouse("RESgenButton", "RESgen", "#28a745");
JSfcnEventMouse("UP", "PowerConverter", "#6610f2");
JSfcnEventMouse("ControlButton", "Control", "#d63384");
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------

// Obtener los elementos <a> por su identificador
const patron1 = document.getElementById('patron1');
const patron2 = document.getElementById('patron2');
const patron3 = document.getElementById('patron3');

// Agregar un evento 'click' a cada elemento <a>
patron1.addEventListener('click', () => {
  document.body.style.backgroundImage = "url('imgs/background-electrical.svg')";
  document.documentElement.style.setProperty('--colorbase-claro', 'rgb(239, 240, 241)');
  document.documentElement.style.setProperty('--colorbase-oscuro', 'rgb(96, 205, 242)');
  document.documentElement.style.setProperty('--color-oscuro', 'rgba(49, 54, 59, 0.4)');
  document.documentElement.style.setProperty('--color-medio', 'rgb(239, 240, 241)');
  document.documentElement.style.setProperty('--colortexto-claro', 'rgb(49, 54, 59)');
  document.documentElement.style.setProperty('--colorXXXXXX', 'rgba(32, 38, 57, 0.5)');
});

patron2.addEventListener('click', () => {
  document.body.style.backgroundImage = "url('imgs/background-electronics.svg')";
  document.documentElement.style.setProperty('--colorbase-claro', 'rgb(218, 203, 198)');
  document.documentElement.style.setProperty('--colorbase-oscuro', 'goldenrod');
  document.documentElement.style.setProperty('--color-oscuro', 'black');
  document.documentElement.style.setProperty('--color-medio', 'white');
  document.documentElement.style.setProperty('--colortexto-claro', '#20222a');
  document.documentElement.style.setProperty('--colorXXXXXX', 'rgb(30, 30, 30)');
});

patron3.addEventListener('click', () => {
  document.body.style.backgroundImage = "url('imgs/background-neither.svg')";
  document.documentElement.style.setProperty('--colorbase-claro', 'rgb(239, 240, 241)');
  // document.documentElement.style.setProperty('--colorbase-oscuro', 'rgb(169, 96, 242)');
  document.documentElement.style.setProperty('--colorbase-oscuro', '#dc3545');
  document.documentElement.style.setProperty('--color-oscuro', 'rgba(49, 54, 59, 0.4)');
  document.documentElement.style.setProperty('--color-medio', 'rgb(239, 240, 241)');
  document.documentElement.style.setProperty('--colortexto-claro', 'rgb(49, 54, 59)');
  document.documentElement.style.setProperty('--colorXXXXXX', 'rgba(32, 38, 57, 0.5)');
});
// -----------------------------------------------------------------------------


//  220  53  69  #dc3545 (RED)
//   13 110 253  #0d6efd (BLUE)
//   40 167  69  #28a745 (GREEN)
//  255 193   7  #ffc107 (YELLOW)
//   23 162 184  #17a2b8 (CYAN)
//  102  16 242  #6610f2 (INDIGO)
//  253 126  20  #fd7e14 (ORANGE)
//  111  66 193  #6f42c1 (PURPLE)
//  214  51 132  #d63384 (PINK)
//   32 201 151  #20c997 (TEAL)


// -----------------------------------------------------------------------------
// XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
const aux = document.getElementById("CONVgenButton");
aux.addEventListener("click", function () {
  aux.classList.toggle("clicked");
});
// -----------------------------------------------------------------------------



