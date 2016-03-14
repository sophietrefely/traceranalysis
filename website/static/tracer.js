$(document).ready(function() {
    console.log('wassup lol');

    function doTracerAnalysis(labeled, unlabeled) {
        formData = $('#tracerForm').serialize()
        $.post('/api/tracer', formData).done(function(data) {
            var arrays = JSON.parse(data);
            var lines = []
            arrays.forEach(function(row) {
                lines.push(row.join('\t'));
            });
            $('#results').val(lines.join('\n'));
        }).fail(function() {
            alert('Something went wrong! Contact s.trefely@gmail.com with the data you tried to use.');
        });
    }
    
    $('#computePercentages').click(doTracerAnalysis);
});
