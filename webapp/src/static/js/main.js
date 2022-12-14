// import 'htmx.org';

var alertList = document.querySelectorAll('.alert')
alertList.forEach(function (alert) {
new bootstrap.Alert(alert)
})

function send_data(url, type, sendData) {
    console.log("Sending data...")
    $.ajax({
        url : url, // the endpoint, example "/update_profile/"
        type : type, // http method
        data : sendData, 
        cache: false,
        contentType: false,
        processData: false,
        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            $('#messages').html('<div class="alert alert-success alert-dismissible fade show" role="alert"> \
                Changes saved! \
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> \
            </div>');

        },
        // handle a non-successful response
        error : function(json) {
            
            $('#messages').html('<div class="alert alert-danger alert-dismissible fade show" role="alert"> \
                Oops! We have encountered an error! \
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> \
            </div>');
        }
    });
};