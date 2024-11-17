const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const squad = document.querySelector(".squad");
const joephoto = document.querySelector(".joephoto");
const joephoto2 = document.querySelector(".joephoto2");
const formcont = document.querySelector(".formcont");
const formcont2 = document.querySelector(".formcont2");


sign_up_btn.addEventListener("click", () => {
  squad.classList.add("squadmov");
  squad.classList.add("transition");
  joephoto.classList.add("photomov");
  joephoto.classList.add("transition");
  joephoto2.classList.add("photomov");
  joephoto2.classList.add("transition");
  formcont.classList.remove("index");
  formcont.classList.add("transition");
  formcont.classList.add("formmov");
  formcont2.classList.add("formmov");
  formcont2.classList.add("transition");
  setTimeout(() =>{
    squad.classList.remove("transition");
    joephoto.classList.remove("transition");
    joephoto2.classList.remove("transition");
    formcont2.classList.add("index");
    formcont.classList.remove("transition");
    formcont2.classList.remove("transition");
  },1000);
});

sign_in_btn.addEventListener("click", () => {
  squad.classList.remove("squadmov");
  squad.classList.add("transition");
  joephoto.classList.remove("photomov");
  joephoto.classList.add("transition");
  joephoto2.classList.remove("photomov");
  joephoto2.classList.add("transition");
  formcont2.classList.remove("index");
  formcont.classList.add("transition");
  formcont.classList.remove("formmov");
  formcont2.classList.remove("formmov");
  formcont2.classList.add("transition");
  setTimeout(() =>{
    squad.classList.remove("transition");
    joephoto.classList.remove("transition");
    joephoto2.classList.remove("transition");
    formcont.classList.add("index");
    formcont.classList.remove("transition");
    formcont2.classList.remove("transition");
  },1000);
});
