
function openItemAltModal(event, register_id) {
  // Simple function which opens a modal on click.
  // Also makes sure the default submit behaviour of the buttons is
  // overridden.
    var modal = $('#alternativesModal');
    var url = $(event.target).closest('a').attr('href');
    $.ajax({
        type: "GET",
        url: url
    }).done(function(data, textStatus, jqXHR) {
        $('#alternativesModal').find('.modal-body').html(data);
        $('#alternativesModal').modal('show');
        formAjaxSubmit(modal, url);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        alert(errorThrown);
    });
}

function submitForm(){
  // making sure that the id of the item is submitted as well
    var id = (event.currentTarget.id);
    $('#modal_form').attr('data-index-number', id)
    $('#modal_form').submit();
}

function openItemEditModal(event, register_id) {
  // A function similar to the openItemAltModal function.
  // Opens the modal for editing an item instead.
    var modal = $('#editModal');
    var url = $(event.target).closest('a').attr('href');
    $.ajax({
        type: "GET",
        url: url
    }).done(function(data, textStatus, jqXHR) {
        $('#editModal').find('.modal-body').html(data);
        $('#editModal').modal('show');
        formEditAjaxSubmit(modal, url);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        alert(errorThrown);
    });
}
