export default function onload(func) {
  document.addEventListener('turbolinks:load', func);
}
