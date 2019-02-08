$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result1').text('');
        $('#result2').text('');
        $('#result3').text('');
        $('#result4').text('');
        $('#result5').text('');
        $('#result1').hide();
        $('#result2').hide();
        $('#result3').hide();
        $('#result4').hide();
        $('#result5').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result1').fadeIn(600);
                $('#result1').text('No.1: ' + data[0]);
                $('#result2').fadeIn(600);
                $('#result2').text('No.2: ' + data[1]);
                $('#result3').fadeIn(600);
                $('#result3').text('No.3: ' + data[2]);
                $('#result4').fadeIn(600);
                $('#result4').text('No.4: ' + data[3]);
                $('#result5').fadeIn(600);
                $('#result5').text('No.5: ' + data[4]);
                $('.choose_result').show();

            },
        });
    });

});
