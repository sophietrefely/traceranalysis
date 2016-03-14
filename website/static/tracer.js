$(document).ready(function() {
    console.log('wassup lol');

    function doTracerAnalysis(labeled, unlabeled) {
        formData = $('#tracerForm').serialize()
        $.post('/api/tracer', formData).then(function(a, b, c) {
            console.log('did request:', a, b, c);
        });
    }
 
    function onClickComputePercentages() {

    } 
    
    $('#computePercentages').click(doTracerAnalysis);

});
