$('#auth_login, #auth_register').submit((e) => {
    e.preventDefault();
    let form = $(e.target)
    let url = window.location.href + 'api/v1'
    let csrf_token = ''
    if (form.attr('id') == 'auth_login') {
        url += '/login';
        csrf_token = $('#login-csrf > csrf_token').val();
    } else if (form.attr('id') == 'auth_register') {
        url += '/register';
        let password = $('#passwordRegInput').val();
        let repeat_password = $('#repeatPasswordInput').val();
        if (!valid_password(password, repeat_password))
            return false;
        csrf_token = $('#register-csrf > csrf_token').val();
    } else window.location.reload();
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {

            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }
    })
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: (data, status, xhr) => {
            if (data['error']) {
                if (form.attr('id') == 'auth_register') {
                    $('#reg-alert').addClass('alert-danger').removeClass('alert-success');
                    $('#reg-alert').text(data['message']);
                    $('#reg-alert').show();
                } else {
                    $('#login-alert').text(data['message']);
                    $('#login-alert').show();
                }
            } else {
                if (form.attr('id') == 'auth_register') {
                    $('#reg-alert').text(data['message']);
                    $('#reg-alert').addClass('alert-success').removeClass('alert-danger');
                    $('#reg-alert').show();
                }
                window.location.replace('/panel');
            }
        }
    });
    return false;
});


function valid_password(password, repeat_password) {
    if (/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/.test(password)) {
        if (password != repeat_password) {
            $('#reg-alert').addClass('alert-danger').removeClass('alert-success');
            $('#reg-alert').text('Пароли не совпадают');
            $('#reg-alert').show();
            return false;
        }
        return true;
    } else {
        $('#reg-alert').addClass('alert-danger').removeClass('alert-success');
        $('#reg-alert').text('Пароль не соответствует требованиям');
        $('#reg-alert').show();
        return false;
    }
};