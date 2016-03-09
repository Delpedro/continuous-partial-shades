$('.drop-zone')
  .on('dragenter', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).addClass('hover');
  })
  .on('dragover', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).addClass('hover');
  })
  .on('dragleave', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).removeClass('hover');
  })
  .on('drop', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).removeClass('hover');

    if (!event.originalEvent.dataTransfer) {
      return;
    }

    var spinner = new Spinner().spin();
    $('.output').empty().append(spinner.el);

    var file = event.originalEvent.dataTransfer.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload');
    xhr.responseType = 'blob';
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          console.log('success! %s bytes returned', xhr.response.size);
          var url = URL.createObjectURL(xhr.response);
          var image = document.createElement('img');
          image.src = url;
          $('.output').empty().append(image);
        } else {
          if (xhr.response) {
            var reader = new FileReader();
            reader.addEventListener("loadend", function() {
               console.error(reader.result)
            });
            reader.readAsText(xhr.response);
          }
        }
      }
    };
    xhr.send(formData);
  });
