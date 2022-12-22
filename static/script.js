const container = document.querySelector(".container");
const loginBtn = document.querySelector("button");
const signupBtn = document.querySelector("button");

function DisplayProgressMessage(ctl, msg) {
  event.preventDefault()
  // Turn off the "Save" button and change text
  $(ctl).prop("disabled", true).text(msg);
  // Gray out background on page
  $("body").addClass("submit-progress-bg");
   
  // Wrap in setTimeout so the UI can update the spinners
  $(".submit-progress").removeClass("hidden");
  setTimeout(function () {
    $('form').submit()
  }, 2000);
   
  return true;
}


$(".dropdown-menu a").click(function () {
  var selText = $(this).text();
  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
});


loginBtn.addEventListener("click", () => {
  container.classList.toggle("change");
});

function myFunc() {
        window.location.href = "./templates/signup2.html";
}


