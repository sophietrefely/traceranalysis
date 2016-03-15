$(document).ready(function() {
    function showAlert() {
        alert('Something went wrong! Contact s.trefely@gmail.com with the data you tried to use.');
    }

    function doTracerAnalysis(labeled, unlabeled) {
        formData = $('#tracerForm').serialize()
        $.post('/api/tracer', formData).done(function(data) {
            try {
                var arrays = JSON.parse(data);
                var lines = []
                arrays.forEach(function(row) {
                    lines.push(row.join('\t'));
                });
                $('#results').val(lines.join('\n'));
            }
            catch (err) {
                showAlert();
            }
        }).fail(function() {
            showAlert();
        });
    }
    
    $('#computePercentages').click(doTracerAnalysis);
});
