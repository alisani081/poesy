$(document).ready( function () {

  const user_input = $(".searchInp")
  const search_icon = $('.search_input')
  const results_div = $('.segment')
  const endpoint = '/search/'
  const delay_by_in_ms = 750
  let scheduled_function = false

  let ajax_call = function (endpoint, request_parameters) {
    $.ajaxSetup({ cache: true });
    $.getJSON(endpoint, request_parameters)
      .done(response => {
        results_div.removeClass('hidden').fadeTo('slow', 0).promise().then(() => {
          // replace the HTML contents
          results_div.html(response['html_view'])
          // fade-in the div with new contents
          results_div.fadeTo('slow', 1)
          // stop animating search icon
          search_icon.removeClass('loading')
        })
      })
  }

  user_input.on('keyup', function () {

    const request_parameters = {
      q: $(this).val()
    }

    search_icon.addClass('loading')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
      clearTimeout(scheduled_function)
    }
    
    if (request_parameters.q.length > 0) {
      // setTimeout returns the ID of the function to be executed
      scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    } else {
      search_icon.removeClass('loading')
      results_div.addClass('hidden')
    }

  });

});