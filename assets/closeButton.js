function addCloseButton(element) {
  const closeButton = document.createElement('span');
  closeButton.className = 'close-button ' + element.className;
  closeButton.addEventListener('click', function() {
    const parent = closeButton.parentNode;
    parent.parentNode.removeChild(parent);
  });
  element.parentNode.replaceChild(closeButton, element);
}

export default function closeButton() {
  document.querySelectorAll('[data-close-button]')
    .forEach(addCloseButton);
}
