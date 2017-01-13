function makeDroppable(element, callback) {

  var input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('multiple', true);
  input.style.display = 'none';

  input.addEventListener('change', triggerCallback);
  element.appendChild(input);

  element.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    element.classList.add('dragover');
  });

  element.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    element.classList.remove('dragover');
  });

  element.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    element.classList.remove('dragover');
    triggerCallback(e);
  });

  element.addEventListener('click', function() {
    input.value=null;
    input.click();
  });

  function triggerCallback(e) {
    var files;
    if(e.dataTransfer) {
      files = e.dataTransfer.files;
    } else if(e.target) {
      files=e.target.files;
    }
    callback.call(null,files);
  }
}

var element = document.querySelector('.droppable');

function callback(files) {
  //log the array of files to the console:
  console.log(files);
}

makeDroppable(element, callback);

window.onload = myf;
