// variables declaration
var train_data = {
    name: "",
    file: null
};

var recognize_data = {
    file: null
};

var message = null;
var active_section = 'null';


// functions declaration
function render() {
    // clear form data
    $('.form-item input').val('');
    $('.tabs li').removeClass('active');
    $('.tabs li:first').addClass('active');
    active_section = 'train-content';
    $('#'+active_section).show();
}

function update() {

    if(message){
        // render message
        $('.message').html('<p class="'+_.get(message, 'type')+'">'+_.get(message, 'message')+'</p>');
    }
    $('#train-content, #recognize-content').hide();
    $('#'+active_section).show();
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

    //listen tab items when clicked
    $('.tabs li').on('click', function(e){
        var $this = $(this);
        console.log(" You clicked on tab", $this.data('section'));
        active_section = $this.data('section');

        // remove all active class
        $('.tabs li').removeClass('active');
        $this.addClass('active');

        update();
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
                message = {type: 'success', message: 'Training has been done, user with id: ' +_.get(response, 'data.id')};
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

    // listen for file field change
    $('#recognize-input-file')

    // listen for recognition form submit
    $('#recognize').submit(function (e) {
        console.log("Form is submitted", recognize_data);
       e.preventDefault();
    });


    // render the app
    render();
});