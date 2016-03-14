$(document).ready(function() {
    console.log('wassup lol');

    function doTracerAnalysis(labeled, unlabeled) {
        formData = $('#tracerForm').serialize()
        $.post('/api/tracer', formData).then(function(data) {
            var arrays = JSON.parse(data);
            var lines = []
            arrays.forEach(function(row) {
                lines.push(row.join('\t'));
            });
            $('#results').val(lines.join('\n'));
        });
    }
    
    $('#computePercentages').click(doTracerAnalysis);
});
