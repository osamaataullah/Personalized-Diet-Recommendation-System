var create_acc=document.querySelector(".create_acc");
var login_acc=document.querySelector(".login_acc");
var s_form=document.querySelectorAll(".s_form");
var login_button=document.querySelector(".login_button");
var signin_form_input=document.querySelectorAll(".signin_form input");

var signin_eye_click = document.querySelector(".fa-eye-slash");
var signin_type = document.querySelector(".signin_pass");
var set_signin_eye = document.querySelector(".fa-eye-slash");

var signup_eye_click = document.querySelector(".signup_eye");
var signup_type = document.querySelector(".signup_pass");
var set_signup_eye = document.querySelector(".signup_eye");

var signup_form_input=document.querySelectorAll(".signup_form input");
var signup_button=document.querySelector(".signup_button");


let formnumber=0;

create_acc.addEventListener('click',function(){
   formnumber++;
   create();
});

login_acc.addEventListener('click',function(){
   formnumber--;
   create();
});



function create(){
    s_form.forEach((form_num)=>{
       form_num.classList.add('d-none');
   });
   s_form[formnumber].classList.remove('d-none'); 
};


login_button.onclick=function(){
    // signin_form_input.forEach((e)=>{
    //     if(e.value.length<1){
    //         e.classList.add('signin_warn');
    //     }
          
    // });
    const name = document.getElementById("username").innerHTML
    const pwd = document.getElementById("pwd").innerHTML

        $.ajax({
            url: "{{ url_for('result') }}",
            type: 'POST',
            data: {
                name: name,
                pass:pwd
            },
            success: function (response) {
            },
            error: function (response) {
            }
        });
};

signin_form_input.forEach((e)=>{
    e.addEventListener('keyup',function(){
       if(e.value.length<1){
           e.classList.add('signin_warn');
          
       } 
      
       else{
           e.classList.remove('signin_warn');
       }
    });
});



signup_button.onclick=function(){
    signup_form_input.forEach((signup_e)=>{
        if(signup_e.value.length<1){
            signup_e.classList.add('signup_warn');
        }
    });
};

signup_form_input.forEach((signup_e)=>{
    signup_e.addEventListener('keyup',function(){
       if(signup_e.value.length<1){
           signup_e.classList.add('signup_warn');
          
       } 
        else{
               signup_e.classList.remove('signup_warn');
           }
    });
});


signin_eye_click.addEventListener('click',function(){
   if(signin_type.type=="password"){
       signin_type.type="text";
       set_signin_eye.classList.remove('fa-eye-slash');
       set_signin_eye.classList.add('fa-eye');
       signin_type.classList.add('signin_eye_wrn');
   } 
   else{
       signin_type.type="password";
       set_signin_eye.classList.add('fa-eye-slash');
       set_signin_eye.classList.remove('fa-eye');
       signin_type.classList.remove('signin_eye_wrn');
   }
});

signup_eye_click.addEventListener('click',function(){ 
   if(signup_type.type=="password"){
       signup_type.type="text";
       set_signin_eye.classList.remove('fa-eye-slash');
       set_signup_eye.classList.add('fa-eye');
       signup_type.classList.add('signup_eye_wrn');
   }
   else{
       signup_type.type="password";
       set_signin_eye.classList.add('fa-eye-slash');
       set_signup_eye.classList.remove('fa-eye');
       signup_type.classList.remove('signup_eye_wrn');
       
   }
});