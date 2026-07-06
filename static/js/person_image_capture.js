(function () {
  function setFile(input, blob, name) {
    const file = new File([blob], name || 'person.jpg', { type: blob.type || 'image/jpeg' });
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
  }

  function compressFile(input, file, preview) {
    if (!file || !file.type || !file.type.startsWith('image/')) return;
    const reader = new FileReader();
    reader.onload = function (event) {
      const img = new Image();
      img.onload = function () {
        const maxSize = 900;
        let width = img.width;
        let height = img.height;
        if (width > height && width > maxSize) {
          height = Math.round(height * (maxSize / width));
          width = maxSize;
        } else if (height > maxSize) {
          width = Math.round(width * (maxSize / height));
          height = maxSize;
        }
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(img, 0, 0, width, height);
        canvas.toBlob(function (blob) {
          if (!blob) return;
          setFile(input, blob, 'person.jpg');
          if (preview) {
            preview.src = URL.createObjectURL(blob);
            preview.style.display = 'block';
          }
        }, 'image/jpeg', 0.72);
      };
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }

  document.querySelectorAll('[data-person-image-input]').forEach(function (input) {
    input.accept = 'image/*';
    input.setAttribute('capture', 'environment');
    const box = input.closest('[data-person-image-box]') || input.parentElement;
    const preview = box ? box.querySelector('[data-person-image-preview]') : null;
    const video = box ? box.querySelector('[data-person-image-video]') : null;
    const startBtn = box ? box.querySelector('[data-person-camera-start]') : null;
    const shotBtn = box ? box.querySelector('[data-person-camera-shot]') : null;
    let stream = null;

    input.addEventListener('change', function () {
      compressFile(input, input.files && input.files[0], preview);
    });

    if (startBtn && video && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      startBtn.addEventListener('click', async function () {
        try {
          stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
          video.srcObject = stream;
          video.style.display = 'block';
          if (shotBtn) shotBtn.style.display = 'inline-block';
        } catch (err) {
          alert('Camera access not available. Use upload/camera file picker instead.');
        }
      });
    }

    if (shotBtn && video) {
      shotBtn.addEventListener('click', function () {
        if (!video.videoWidth) return;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        canvas.toBlob(function (blob) {
          if (!blob) return;
          setFile(input, blob, 'camera-person.jpg');
          if (preview) {
            preview.src = URL.createObjectURL(blob);
            preview.style.display = 'block';
          }
          if (stream) stream.getTracks().forEach(function (track) { track.stop(); });
          video.style.display = 'none';
          shotBtn.style.display = 'none';
        }, 'image/jpeg', 0.72);
      });
    }
  });
})();
