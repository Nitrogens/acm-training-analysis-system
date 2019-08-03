$(document).ready(function () {
    $.ajax({
        url: '/api/stat/submission/',
        dataType: 'json',
        async: true,
        type: 'GET',
        success: function (data) {
            $("#submission-today").text(data.data.submission_today.toString());
            $("#accepted-submission-today").text(data.data.accepted_submission_today.toString());
            $("#submission-total").text(data.data.submission_total.toString());
            $("#accepted-submission-total").text(data.data.accepted_submission_total.toString());
        },
    });
    $.ajax({
        url: '/api/submission/',
        dataType: 'json',
        async: true,
        type: 'GET',
        data: {
            page_size: 8,
            verdict: 0,
        },
        success: function (data) {
            for (var i = 0; i < data.data.length; i++) {
                var htmlElement = '<span class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">\n' +
                    '                            <span class="problem-id">' + data.data[i].oj_name + '-' + data.data[i].problem_id + '</span>\n' +
                    '                            <span class="text-right problem-id badge badge-pill badge-warning">' + data.data[i].time + '</span>\n' +
                    '                        </span>';
                $("#accepted-submission-list").append(htmlElement);
            }
        },
    });
    $.ajax({
        url: '/api/stat/most_popular_problem/',
        dataType: 'json',
        async: true,
        type: 'GET',
        success: function (data) {
            for (var i = 0; i < data.data.length; i++) {
                var htmlElement = '<span class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">\n' +
                    '                            <span class="problem-id">' + data.data[i].oj_name + '-' + data.data[i].problem_id + '</span>\n' +
                    '                            <span class="text-right problem-id badge badge-pill badge-dark">' + data.data[i].count + ' 次</span>\n' +
                    '                        </span>';
                $("#most-popular-problem-list").append(htmlElement);
            }
        },
    });
});