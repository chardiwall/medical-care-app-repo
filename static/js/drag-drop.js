function readURL(input) {
    if (input.files && input.files[0]) {

    reader = new FileReader();

    reader.onload = function(e) {
        $('.image-upload-wrap').hide();

        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
        $('.file-upload-btn').hide()

        $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

    } else {
    removeUpload();
    }
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
    $('.file-upload-btn').show();
}


$('.image-upload-wrap').bind('dragover', function () {
        $('.image-upload-wrap').addClass('image-dropping');
    });
    $('.image-upload-wrap').bind('dragleave', function () {
        $('.image-upload-wrap').removeClass('image-dropping');
});
