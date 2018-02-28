// variables declaration
var train_data = {
    name: "",
    file: null
}

var message = null;


// functions declaration
function render() {
    // clear form data
    $('.form-item input').val('');
}

function update() {

    if(message){
        // render message
        $('.message').html('<p class="'+_.get(message, 'type')+'">'+_.get(message, 'message')+'</p>');
    }
}


// queries declaration
$(document).ready(function () {
    //file added function
    $('#train #input-file').on('change', function (event) {
       //set file object to train_data
        train_data.file = _.get(event, 'target.files[0]', null);
    });

    // listen for name change
    $('#name-field').on('change', function (event) {
       train_data.name = _.get(event, 'target.value', '');
    });

    // form submission event
    $('#train').submit(function (event) {

        message = null;

        if(train_data.name && train_data.file){
            // send data to backend api
            var train_form_data = new FormData();
            train_form_data.append('name', train_data.name);
            train_form_data.append('file', train_data.file);
            axios.post('/api/train', train_form_data).then(function(response){
                message = {type: 'success', message: 'Training has been done, user with id is: ' +_.get(response, 'data.id')};
                update();
            }).catch(function (error) {

                message = {type: 'error', message: _.get(error, 'response.data.error.message', 'Unknown Error.')}

                update();
            });

        }else {
            message = {type: "error", message: "Name and image is required."}
        }
        update();
        event.preventDefault();
    });

    // render the app
    render();
});