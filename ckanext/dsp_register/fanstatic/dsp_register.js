// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('dsp_register', function ($, _) {
  return {
    initialize: function () {
      console.log("I've been initialized for element: ", this.el);

      $('#dsp-register').submit(function(event){
         var username = $('#field-username').val();
         var fullname = $('#field-fullname').val();
         var email = $('#field-email').val();
         var password = $('#field-password').val();
         var confirm = $('#field-confirm-password').val();

         if(!(password == confirm)){
                $('#registerModalErr ul').append('<li>兩次密碼不同！</li>');

         }

         var data = {
            name: username,
            password: password,
            email: email
         };


//        $.ajax({
//            url: 'http://data.dsp.im/api/3/action/user_create',
//            data: data,
//            type: 'POST',
//            dataType: 'jsonp',
//            crossDomain: true,
//        success: function(data) {
//          alert('申請成功！')
//        }
//        });

        $.ajax({
            type: "POST",
            url: "http://data.dsp.im/api/3/action/user_create",
            crossDomain: true,
            data: JSON.stringify(data),
            dataType: "json",
            success: function (data) {
                // do something with server response data
                $('#registerModal').modal('hide');
                $('#username').val(data.result.name);
                $('#api_key').val(data.result.apikey);
            },
            error: function (err) {
                // handle your error logic here
                // console.log(err.responseJSON.error);

                $('#registerModalErr').show();

                $('#registerModalErr ul').html('');

                if(err.responseJSON.error.name){
                    $('#registerModalErr ul').append('<li>' + "Username: " + err.responseJSON.error.name + '</li>');
                }
                if(err.responseJSON.error.email){
                    $('#registerModalErr ul').append('<li>' + "Email: " + err.responseJSON.error.email + '</li>');
                }
                if(err.responseJSON.error.password){
                    $('#registerModalErr ul').append('<li>' + "Password: " + err.responseJSON.error.password + '</li>');
                }
            }
        });


         event.preventDefault();
      });
    }
  };
});
