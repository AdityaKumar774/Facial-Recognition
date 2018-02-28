var train_data = {
    name: "",
    file: null
}


function render() {
    // clear form data
    $('.form-item input').val('');
}


$(document).ready(function () {
    //file added function
    $('#train #input-file').on('change', function (event) {
       //set file object to train_data
        train_data.file = _.get(event, 'target.files[0]', null);

    });

    // form submission event
    $('#train').submit(function (event) {
        console.log("Form is submited", train_data);
       event.preventDefault();
    });

    // render the app
    render();
});