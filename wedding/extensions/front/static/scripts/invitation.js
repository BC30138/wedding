var lastScrollTop = $.cookie('last-scroll-top');
if (lastScrollTop) {
    $(window).scrollTop(lastScrollTop);
    $.removeCookie('last-scroll-top');
}

function toggle_modal_loading() {
  $("body").toggleClass("loading")
}

$("input:checkbox").on('click', function() {
  // позволяет создать чекбокс с одним ответом
  var $box = $(this);
  if ($box.is(":checked")) {
    var group = "input:checkbox[name='" + $box.attr("name") + "']";
    $(group).prop("checked", false);
    $box.prop("checked", true);
  } else {
    $box.prop("checked", false);
  }
});

var form_wrapper = $('.guest_form');
$(form_wrapper).on('click', '#submit-form', function (e) {
  path_parts = window.location.pathname.split('/')
  group_id = path_parts.pop()

  var form_answer = {
    "group_id": parseInt(group_id),
    "attend": null,
    "plus": null,
    "transfer": null,
    "sleepover": null,
  }

  // заполнение присутствия
  if (form_wrapper.find('#attend_yes').is(":checked")) {
    form_answer["attend"] = true
  } else if (form_wrapper.find('#attend_no').is(":checked")) {
    form_answer["attend"] = false
  }
  // заполнение плюса
  var plus_name = form_wrapper.find('#plus_name').val()
  if (plus_name) {
    form_answer.plus = plus_name
  }
  // заполнение трансфера
  if (form_wrapper.find('#transfer_yes').is(":checked")) {
    form_answer.transfer = true
  } else if (form_wrapper.find('#transfer_no').is(":checked")) {
    form_answer.transfer = false
  }
  // заполнение ночевки
  if (form_wrapper.find('#sleepover_yes').is(":checked")) {
    form_answer.sleepover = true
  } else if (form_wrapper.find('#sleepover_no').is(":checked")) {
    form_answer.sleepover = false
  }

  // проверка заполнения обязательных полей
  is_required_unanswered = [
    form_answer.attend,
    form_answer.transfer,
    form_answer.sleepover,
  ].some((value) => value === null)
  if (is_required_unanswered){
    if (!($('.guest_form_error').length)) {
      form_wrapper.append(
          '<p class="guest_form_error"> Пожалуйста, заполните все поля помеченные *</p>'
      )
    }
    return false
  }

  url = window.location.origin + "/public/forms/"


  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState === this.DONE) {
        if (this.status === 200) {
            $.cookie('last-scroll-top', $(window).scrollTop());
            window.location = window.location.href.split("?")[0];
        } else {
            alert('Ошибка, свяжитесь с Антоном!');
        }
      toggle_modal_loading()
    }
    return false;
  }

  xhr.open("PUT", url);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  toggle_modal_loading()
  xhr.send(JSON.stringify(form_answer));
});

$(form_wrapper).on('click', '#restart-form-button', function (e) {
    $.cookie('last-scroll-top', $(window).scrollTop());
    window.location = window.location.href.split("?")[0] + "?update_form=true";
});
