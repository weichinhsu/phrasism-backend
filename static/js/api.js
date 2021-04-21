$('.translate').submit(function (e) {
  e.preventDefault()
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/translator/translate",
    data: '[{"src": "' + $('#src').val() + '", "id": 100}]',
    success: function (data) {
      $('#tgt').val(data[0][0].tgt)
    }
  });
})