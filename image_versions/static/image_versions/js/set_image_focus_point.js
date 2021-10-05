(window.jQuery || window.django.jQuery)(document).ready(function($) {
  /*
  * Focus point implementation is based on https://github.com/jonom/jquery-focuspoint
  * */
  var $helperToolImage;
  var faceSelector = 0;
  var detailsUrl;

  //This stores focusPoint's data-attribute values
  var focusPointAttr = {
    path: '',
    token: '',
    x: 0,
    y: 0,
    w: 0,
    h: 0
  };

  //Initialize Helper Tool
  (function () {

    //Initialize Variables
    $helperToolImage = $('img.helper-tool-img, img.target-overlay');

    var $imagePreview = $('#image_preview');
    detailsUrl = $imagePreview.data('focus-point-details-url');

    focusPointAttr.path = $imagePreview.data('path');
    focusPointAttr.token = $imagePreview.data('token');

    if (focusPointAttr.path) {
      var imageURL = window.settings.MEDIA_URL + focusPointAttr.path;

      $.get(detailsUrl + '?path=' + focusPointAttr.path + '&token=' + focusPointAttr.token, function(data) {
          focusPointAttr.x = parseFloat(data.result.x);
          focusPointAttr.y = parseFloat(data.result.y);
          //Set the default source image
          if (imageURL) {
            setImage(imageURL);
          }
      });
    }
  })();

  function setImage(imgURL) {
    //Get the dimensions of the image by referencing an image stored in memory
    var img = new Image();
    img.src = imgURL;
    img.onload = function () {
      focusPointAttr.w = this.width;
      focusPointAttr.h = this.height;

      //Set src on the thumbnail used in the GUI
      $helperToolImage.attr('src', imgURL);

      //Calculate CSS Percentages
      var percentageX = (focusPointAttr.x + 1) / 2 * 100;
      var percentageY = (1 - focusPointAttr.y) / 2 * 100;

      //Leave a sweet target reticle at the focus point.
      $('.reticle').addClass('no-transition').css({
        'top': percentageY + '%',
        'left': percentageX + '%'
      });
      $('#focus_face').removeClass('d-none');
      $('#reset_focus_point').removeClass('d-none');
      //Update the data attributes shown to the user
      printDataAttr();

    };
  }

  function printDataAttr() {
    console.log(
      focusPointAttr.path,
      focusPointAttr.token,
      focusPointAttr.x.toFixed(2),
      focusPointAttr.y.toFixed(2),
      focusPointAttr.w,
      focusPointAttr.h
    );
  }

  $helperToolImage.on('click', function (e) {
    var imageW = $(this).width();
    var imageH = $(this).height();

    //Calculate FocusPoint coordinates
    var offsetX = e.pageX - $(this).offset().left;
    var offsetY = e.pageY - $(this).offset().top;
    var focusX = (offsetX / imageW - .5) * 2;
    var focusY = (offsetY / imageH - .5) * -2;
    focusPointAttr.x = focusX;
    focusPointAttr.y = focusY;

    //Write values to input
    printDataAttr();

    //Update focus point
    updateFocusPoint();

    //Calculate CSS Percentages
    var percentageX = (offsetX / imageW) * 100;
    var percentageY = (offsetY / imageH) * 100;

    //Leave a sweet target reticle at the focus point.
    $('.reticle').removeClass('no-transition').css({
      'top': percentageY + '%',
      'left': percentageX + '%'
    });
  });

  function updateFocusPoint() {
    $.post(detailsUrl, {
      'path': focusPointAttr.path,
      'token': focusPointAttr.token,
      'x': focusPointAttr.x,
      'y': focusPointAttr.y
    }, function(data) {
      if (data.errors) {
        console.error(data.errors);
      } else {
        console.info('Focus point saved successfully.');
      }
    });
  }

  $('#focus_face').on('click', function() {
    var tracker = new tracking.ObjectTracker(['face']);
    tracker.setStepSize(1.7);
    var $img = $('img.helper-tool-img');
    tracking.track('img.helper-tool-img', tracker);

    tracker.on('track', function(event) {
      if (event.data.length) {
        var rect = event.data[faceSelector];
        faceSelector = (faceSelector + 1) % event.data.length;
        focusPointAttr.x = (rect.x + rect.width / 2) / $img.width() * 2 - 1;
        focusPointAttr.y = 1 - (rect.y + rect.height / 2) / $img.height() * 2;
        var imageURL = window.settings.MEDIA_URL + focusPointAttr.path;
        setImage(imageURL);
        updateFocusPoint();
      }
    });
  });

  $('#reset_focus_point').on('click', function() {
    focusPointAttr.x = 0;
    focusPointAttr.y = 0;
    var imageURL = window.settings.MEDIA_URL + focusPointAttr.path;
    setImage(imageURL);
    updateFocusPoint();
  });
});
