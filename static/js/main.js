$(document).ready(function () {
    // Init
    $('#correct_result').hide();

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
        $('.choose_result').hide();
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

    //only show choose correct result when none of the result given is correct
    $('#result').change(function () {
        if ($('#result option:selected').text() == "none"){
            $('#correct_result').show();
        }
         else { 
              $('#correct_result').hide();
         }
    });

    //get data for chart
    var getData = $.get('/data');
    
    getData.done(function(results_count) {
        //bar chart
        new Chart(document.getElementById("bar-chart"), {
            type: 'bar',
            data: {
                labels: ["No.1", "No.2", "No.3", "No.4", "No.5", "None"],
                datasets: [
                {
                    label: "Count",
                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#3b1245"],
                    data: results_count
                }
                ]
            },
            options: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Correctly Predict In Result No.#'
                }
            }
        });

        //pie chart
        new Chart(document.getElementById("pie-chart"), {
            type: 'pie',
            data: {
            labels: ["No.1", "No.2", "No.3", "No.4", "No.5", "None"],
            datasets: [{
                label: "Count",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#3b1245"],
                data: results_count
            }]
            },
            options: {
            title: {
                display: true,
                text: 'Correctly Predict In Result No.#'
            }
            }
        });
    });
    

});
