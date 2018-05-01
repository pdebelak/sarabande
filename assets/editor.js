import ClassicEditor from '@ckeditor/ckeditor5-build-classic';


function createEditor(element) {
  return ClassicEditor.create(element,
    {
        ckfinder: {
          uploadUrl: '/images'
        }
    });
}

export default function initEditor(selector) {
  document.querySelectorAll(selector)
    .forEach(createEditor);
}
