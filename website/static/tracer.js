$(document).ready(function() {
    function showAlert() {
        alert('Something went wrong! Check your data. If you cannot fix the problem contact sjt65+fluxfix@drexel.edu with the data you tried to use.');
    }

    // TODO also pass the column in here, not computed correctly ATM
    function knownBadData(where) {
        message = 'Your data is not consistent! Check row: ' + where.row + '. ' +
                  'Look for trailing tabs or lines and make sure each row and column is the same length';
        alert(message);
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

    function findRowsAndColumns(data) {
        console.log('raw data:', data);
        // First, remove any trailling or preceding newlines
        var data = data.trim();

        // Replace \r with \n in case that is an issue
        // Fuck you microsoft
        data = data.replace(/\r\n/g, '\n');
        data = data.replace(/\r/g, '\n');

        // Split by newline to count number of rows
        var rows = data.split('\n');

        var numberOfColumns = null;
        rows.forEach(function(row, index) {
            // Trim any trailing tabs or other whitespace
            row = row.trim();

            // Split row to get the length and to check column consistency
            var rowSplit = row.split('\t');
            var length = rowSplit.length;

            // If numberOfColumns is defined, we have already seen a row length
            // Check it is the same as the one before with compound if statement
            if (numberOfColumns && numberOfColumns !== length) {
                var where = {
                    row: index + 1,
                    column: length + 1
                };
                knownBadData(where);
            }

            // Assign to numberOfColumns so we can check consistency as we go
            numberOfColumns = length;
        })

        return {
            rows: rows.length,
            columns: numberOfColumns
        };
    }

    function formatSizeStr(size) {
        return 'Data is ' + size.columns + ' columns by ' + size.rows + ' rows ';
    }

    function getMetadataForUnlabeled(e) {
        var input = e.originalEvent.clipboardData.getData('Text');
        console.log('compute metadata for:', input);
        size = findRowsAndColumns(input);

        var sizeStr = formatSizeStr(size);
        $('#unlabeledDataSize').text(sizeStr);
    }

    function getMetadataForLabeled(e) {
        var input = e.originalEvent.clipboardData.getData('Text');
        console.log('compute metadata for:', input);
        size = findRowsAndColumns(input);

        var sizeStr = formatSizeStr(size);
        $('#labeledDataSize').text(sizeStr);
    }

    function checkCleared() {
        // If either of the boxes are empty, then remove the message
        var unlabeledData = $('#unlabeledData').val();
        if (unlabeledData.trim() === '') {
            $('#unlabeledDataSize').empty();
        }

        var labeledData = $('#labeledData').val();
        if (labeledData.trim() === '') {
            $('#labeledDataSize').empty();
        }
    }

    $('#computePercentages').click(doTracerAnalysis);

    $('#unlabeledData').on('paste', getMetadataForUnlabeled);
    $('#labeledData').on('paste', getMetadataForLabeled);
});
