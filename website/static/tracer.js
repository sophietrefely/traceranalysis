$(document).ready(function() {
    var cachedLabeled = null;
    var cachedUnlabeled = null;

    function showAlert() {
        alert('Something went wrong! Check your data. If you cannot fix the problem contact sjt65+fluxfix@drexel.edu with the data you tried to use.');
    }

    // google 'check number javascript'
    function isNumber(n) {
          return (Object.prototype.toString.call(n) === '[object Number]' || Object.prototype.toString.call(n) === '[object String]') &&!isNaN(parseFloat(n)) && isFinite(n.toString().replace(/^-/, ''));
    }

    // TODO also pass the column in here, not computed correctly ATM
    function knownBadData(where) {
        message = 'Your data is not consistent! Check row: ' + where.row + '. ' +
                  'Look for trailing tabs or lines and make sure each row and column is the same length';
        alert(message);
    }

    function alertNonNumericData(where) {
        message = 'Your data contains non-numeric characters. Check that you did ' +
                  'not include any row or column header text at row ' + where.row + ', col ' + where.column;
        alert(message)
    }

    function cleanPastedData(data) {
        // First, remove any trailling or preceding newlines
        var data = data.trim();

        // Replace \r with \n in case that is an issue
        // Fuck you microsoft
        data = data.replace(/\r\n/g, '\n');
        data = data.replace(/\r/g, '\n');

        return data;
    }

    function onClickComputePercentages(e) {
        doTracerAnalysis();
    }

    function doTracerAnalysis(callback) {
        formData = $('#tracerForm').serialize()
        $.post('/api/tracer', formData).done(function(data) {
            try {
                var arrays = JSON.parse(data);
                var lines = []
                arrays.forEach(function(row) {
                    lines.push(row.join('\t'));
                });

                var result = lines.join('\n');
                $('#results').val(result);
                if (callback) {
                    callback(lines.join(result));
                }
            }
            catch (err) {
                console.log('Got error:', err)
                showAlert();
            }
        }).fail(function() {
            showAlert();
        });
    }

    function downloadResultTsv() {
        function cb(results) {
            var downloadLink = document.createElement("a");
            downloadLink.style.width = 0;
            var blob = new Blob([results]);
            var url = URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = "result.tsv";
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        }
        doTracerAnalysis(cb);
    }

    function findRowsAndColumns(data) {
        console.log('raw data:', data);

        // Split by newline to count number of rows
        var rows = data.split('\n');

        var numberOfColumns = null;
        rows.forEach(function(row, index) {
            // Trim any trailing tabs or other whitespace
            row = row.trim();

            // Split row to get the length and to check column consistency
            var rowSplit = row.split('\t');
            var length = rowSplit.length;

            for (var colIndex = 0; colIndex < rowSplit.length; colIndex++) {
                var elem = rowSplit[colIndex];
                if (!isNumber(elem.trim())) {
                    var where = {
                        row: index + 1,
                        column: colIndex + 1
                    }
                    alertNonNumericData(where);
                    return {
                        rows: 0, columns: 0 
                    };
                    //throw 'Failed to parse data (non-numeric)';
                }
            }
            /*
            rowSplit.forEach(function(elem, colIndex) {
                if (elem.match(/[a-z]/i)) {
                    var where = {
                        row: index + 1,
                        column: colIndex + 1
                    }
                    alertNonNumericData(where);
                    throw 'Failed to parse data (non-numeric)';
                }
            })
            */

            // If numberOfColumns is defined, we have already seen a row length
            // Check it is the same as the one before with compound if statement
            if (numberOfColumns && numberOfColumns !== length) {
                var where = {
                    row: index + 1,
                    column: length + 1
                };
                knownBadData(where);
                throw 'Failed to parse data (imbalanced structure)';
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
        var input = cleanPastedData(e.originalEvent.clipboardData.getData('Text'));

        var unchanged = cachedUnlabeled && cachedUnlabeled === input;
        cachedUnlabeled = input;
        if (unchanged) {
            console.log('data unchanged');
            return;
        }

        console.log('compute metadata for:', input);
        size = findRowsAndColumns(input);

        var sizeStr = formatSizeStr(size);
        $('#unlabeledDataSize').text(sizeStr);
    }

    function getMetadataForLabeled(e) {
        var input = cleanPastedData(e.originalEvent.clipboardData.getData('Text'));

        var unchanged = cachedLabeled && cachedLabeled === input;
        cachedLabeled = input;
        if (unchanged) {
            console.log('data unchanged');
            return;
        }
 
        console.log('compute metadata for:', input);
        size = findRowsAndColumns(input);

        var sizeStr = formatSizeStr(size);
        $('#labeledDataSize').text(sizeStr);
    }

    function getTextareaValueFromUnlabeled() {
        var input = cleanPastedData($('#unlabeledData').val());

        var unchanged = cachedUnlabeled && cachedUnlabeled === input;
        cachedUnlabeled = input;
        if (unchanged) {
            console.log('data unchanged');
            return;
        }

        // Check input is not null
        if (!input || input.length === 0) {
            // do nothing
            return;
        }

        console.log('compute metadata for:', input);
        size = findRowsAndColumns(input);

        var sizeStr = formatSizeStr(size);
        $('#unlabeledDataSize').text(sizeStr);
    }

    function getTextareaValueFromLabeled() {
        var input = cleanPastedData($('#labeledData').val());

        var unchanged = cachedLabeled && cachedLabeled === input;
        cachedLabeled = input;
        if (unchanged) {
            console.log('data unchanged');
            return;
        }

        if (!input || input.length === 0) {
            // do nothing
            return;
        }
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

    function uploadUnlabeledTsv(e) {
        var file = document.getElementById('unlabeledTsv').files[0];

        var reader = new FileReader();
        reader.onload = function (e) {
            text = e.target.result;
            $('#unlabeledData').val(text);
            // Hack to trigger checking of data (as though edited)
            $('#unlabeledData').trigger('blur');
        };
        reader.readAsText(file);
    }

    function uploadLabeledTsv(e) {
        var file = document.getElementById('labeledTsv').files[0];

        var reader = new FileReader();
        reader.onload = function (e) {
            text = e.target.result;
            $('#labeledData').val(text);
            // Hack to trigger checking of data (as though edited)
            $('#labeledData').trigger('blur');
        };
        reader.readAsText(file);
    }

    $('#computePercentages').click(onClickComputePercentages);

    $('#unlabeledData').on('paste', getMetadataForUnlabeled);
    $('#unlabeledData').on('blur', getTextareaValueFromUnlabeled);
    
    $('#labeledData').on('paste', getMetadataForLabeled);
    $('#labeledData').on('blur', getTextareaValueFromLabeled);

    $('#downloadTsv').on('click', downloadResultTsv);

    $('#labeledTsv').on('change', uploadLabeledTsv);
    $('#unlabeledTsv').on('change', uploadUnlabeledTsv);
});
