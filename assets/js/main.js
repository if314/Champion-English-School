(function () {
"use strict";
var toggle = document.querySelector(".menu-toggle");
var mobileNav = document.querySelector(".mobile-nav");
if (toggle && mobileNav) {
var closeMenu = function () {
toggle.setAttribute("aria-expanded", "false");
mobileNav.classList.remove("is-open");
document.body.style.overflow = "";
};
var openMenu = function () {
toggle.setAttribute("aria-expanded", "true");
mobileNav.classList.add("is-open");
document.body.style.overflow = "hidden";
};
toggle.addEventListener("click", function () {
var isOpen = toggle.getAttribute("aria-expanded") === "true";
if (isOpen) {
closeMenu();
} else {
openMenu();
}
});
mobileNav.querySelectorAll("a").forEach(function (link) {
link.addEventListener("click", closeMenu);
});
document.addEventListener("keydown", function (e) {
if (e.key === "Escape") closeMenu();
});
}
var forms = document.querySelectorAll(".js-form");
forms.forEach(function (form) {
form.addEventListener("submit", function (e) {
e.preventDefault();
var valid = true;
form.querySelectorAll("[required]").forEach(function (input) {
var field = input.closest(".field");
var value = (input.value || "").trim();
var ok = value.length > 0;
if (ok && input.type === "email") {
ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}
if (ok && input.type === "tel") {
ok = /^[0-9+()\s-]{6,}$/.test(value);
}
if (input.type === "checkbox") {
ok = input.checked;
}
if (field) field.classList.toggle("has-error", !ok);
if (!ok) valid = false;
});
var honeypot = form.querySelector('input[name="website"]');
if (honeypot && honeypot.value) {
valid = false;
}
if (!valid) {
var firstError = form.querySelector(".has-error input, .has-error select, .has-error textarea");
if (firstError) firstError.focus();
return;
}
fakeSubmit(form);
});
});
function fakeSubmit(form) {
form.setAttribute("data-submitted", "true");
var success = form.querySelector(".form-success");
if (success) {
success.classList.add("is-visible");
success.setAttribute("tabindex", "-1");
success.focus();
}
}
})();