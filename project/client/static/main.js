// custom javascript

$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('.btn').on('click', function() {
  $.ajax({
    url: '/tasks',
    data: { type: $(this).data('type') },
    method: 'POST'
  })
  .done((res) => {
    getStatus(res.data.task_id);
  })
  .fail((err) => {
    console.log(err);
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`
    $('#tasks').prepend(html);
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err);
  });
}

function copyToClipboard(text) {
  if (window.clipboardData && window.clipboardData.setData) {
      // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
      return window.clipboardData.setData("Text", text);

  }
  else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
      var textarea = document.createElement("textarea");
      textarea.textContent = text;
      textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
      document.body.appendChild(textarea);
      textarea.select();
      try {
          return document.execCommand("copy");  // Security exception may be thrown by some browsers.
      }
      catch (ex) {
          console.warn("Copy to clipboard failed.", ex);
          return prompt("Copy to clipboard: Ctrl+C, Enter", text);
      }
      finally {
          document.body.removeChild(textarea);
      }
  }
}
document.querySelector("#copy").onclick = function() {
  element = document.getElementById("code-gen")
  var text = element.innerText || element.textContent;
  var result = copyToClipboard(text);
  console.log("copied?", result);
};


$(document).on('click', '.edit', function() {
  $(this).parent().siblings('td.data').each(function() {
    var content = $(this).html();
    $(this).html('<input value="' + content + '" />');
  });
  
  $(this).siblings('.save').show();
  $(this).siblings('.delete').hide();
  $(this).hide();
});

$(document).on('click', '.save', function() {
  
  $('input').each(function() {
    var content = $(this).val();
    $(this).html(content);
    $(this).contents().unwrap();
  });
  $(this).siblings('.edit').show();
  $(this).siblings('.delete').show();
  $(this).hide();
  
});


$(document).on('click', '.delete', function() {
  $(this).parents('tr').remove();
});

$('.add').click(function() {
  $(this).parents('table').append('<tr><td class="data"></td><td class="data"></td><td class="data"></td><td><button class="save">Save</button><button class="edit">Edit</button> <button class="delete">Delete</button></td></tr>');
});