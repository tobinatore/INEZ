'use strict';

function formAjaxSubmit(modal, action) {
    var form = modal.find('.modal-body form');
    var footer = $(modal).find('.modal-footer');

    // bind to the form’s submit event
    $(form).on('submit', function(event) {
        var id = event.currentTarget.dataset.indexNumber
        var token = $('[name="csrfmiddlewaretoken"]').val();

        // prevent the form from performing its default submit action
        event.preventDefault();
        footer.addClass('loading');

        // either use the action supplied by the form, or the original rendering url
        var url = $(this).attr('action') || action;

        // get the item id and the csrf-token and send them via an AJAX call
        // using the form’s defined method
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: {id : id,
                    csrfmiddlewaretoken: token},
            success: function(xhr, ajaxOptions, thrownError) {

                // If the server sends back a successful response,
                // we need to further check the HTML received

                // If xhr contains any field errors, the form did not
                // validate successfully, so we update the modal body
                // with the new form and its error
                if ($(xhr).find('.has-error').length > 0) {
                    $(modal).find('.modal-body').html(xhr);
                    formAjaxSubmit(modal, url);
                } else {
                    // otherwise, close the modal and refresh the site
                    $(modal).modal('hide');
                    window.location.href = window.location.href;
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
            },
            complete: function() {
                footer.removeClass('loading');
            }
        });
    });
}

function formEditAjaxSubmit(modal, action) {
    var form = modal.find('.modal-body form');
    var footer = $(modal).find('.modal-footer');

    var btn_save = modal.find('.modal-footer #btn-save');
    if (btn_save) {
      btn_save.off().on('click', function(event) {
      modal.find('.modal-body form').submit();
      });
    }

    // bind to the form’s submit event
    $(form).on('submit', function(event) {
        var token = $('[name="csrfmiddlewaretoken"]').val();

        // prevent the form from performing its default submit action
        event.preventDefault();
        footer.addClass('loading');

        // either use the action supplied by the form, or the original rendering url
        var url = $(this).attr('action') || action;

        // serialize the form’s content and send it via an AJAX call
        // using the form’s defined method
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: $(this).serialize(),
            success: function(xhr, ajaxOptions, thrownError) {

                // If the server sends back a successful response,
                // we need to further check the HTML received

                // If xhr contains any field errors, the form did not
                // validate successfully, so we update the modal body
                // with the new form and its error
                if ($(xhr).find('.has-error').length > 0) {
                    $(modal).find('.modal-body').html(xhr);
                    formEditAjaxSubmit(modal, url);
                } else {
                    // close modal and refresh the site
                    $(modal).modal('hide');
                    window.location.href = window.location.href;
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
            },
            complete: function() {
                footer.removeClass('loading');
            }
        });
    });
}
