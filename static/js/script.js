$(document).ready(function () {
    // Toggle antara input teks dan file
    $('input[name="keyInputModeSign"]').on('change', function () {
        if (this.value === 'file') {
            $('#privateKeyTextContainer').hide();
            $('#privateKeyFileContainer').show();
            $('#privateKeyTextContainer textarea').prop('required', false);
            $('#privateKeyFileContainer input[type="file"]').prop('required', true);
        } else {
            $('#privateKeyFileContainer').hide();
            $('#privateKeyTextContainer').show();
            $('#privateKeyTextContainer textarea').prop('required', true);
            $('#privateKeyFileContainer input[type="file"]').prop('required', false);
        }
    });

    // Validasi file .pem
    $('input[name="privateKeyFile"]').on('change', function () {
        const file = this.files[0];
        if (file && !file.name.endsWith('.pem')) {
            alert('Hanya file dengan ekstensi .pem yang diperbolehkan!');
            this.value = '';
        }
    });

    // Submit form tanda tangan
    $('#Sign_Generic_File').submit(function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        $.ajax({
            url: '/sign_generic_file',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhrFields: { responseType: 'blob' },
            success: function (blob) {
                const url = URL.createObjectURL(blob);

                const downloadBtn = document.createElement('a');
                downloadBtn.href = url;
                downloadBtn.download = 'signature.sig';
                downloadBtn.textContent = 'Unduh Signature';
                downloadBtn.classList.add('btn', 'btn-success');
                downloadBtn.style.display = 'inline-block';

                const container = document.getElementById('signatureDownloadContainer');
                container.innerHTML = ''; // bersihkan sebelumnya
                container.appendChild(downloadBtn);
            },
            error: function () {
                alert('Gagal menandatangani file.');
            }
        });
    });

    // VERIFY PAGE LOGIC
    $('input[name="keyInputModeVerify"]').on('change', function () {
        if (this.value === 'file') {
            $('#publicKeyTextContainer').hide();
            $('#publicKeyFileContainer').show();
            $('#publicKeyTextContainer textarea').prop('required', false);
            $('#publicKeyFileContainer input[type="file"]').prop('required', true);
        } else {
            $('#publicKeyFileContainer').hide();
            $('#publicKeyTextContainer').show();
            $('#publicKeyTextContainer textarea').prop('required', true);
            $('#publicKeyFileContainer input[type="file"]').prop('required', false);
        }
    });

    $('input[name="publicKeyFile"]').on('change', function () {
        const file = this.files[0];
        if (file && !file.name.endsWith('.pem')) {
            alert('Hanya file dengan ekstensi .pem yang diperbolehkan!');
            this.value = '';
        }
    });

    // Submit: Verify
$('#Verify_Generic_File').submit(function (e) {
    e.preventDefault();
    let formData = new FormData(this);

    $.ajax({
        url: '/verify_generic_file',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            const resultDiv = document.getElementById('verifyResult');
            if (response.success) {
                resultDiv.textContent = "Signature Verified: PASSED";
                resultDiv.style.color = "green";
            } else {
                resultDiv.textContent = "Signature Verified: FAILED";
                resultDiv.style.color = "red";
            }
        },
        error: function () {
            alert('Verifikasi gagal.');
        }
    });
});

});

$(document).ready(function() {
    $('#menuToggle').on('click', function () {
        $('#sidebar').toggleClass('show');
        $('body').toggleClass('sidebar-open');
    });

    
    document.getElementById('Generate_Key').addEventListener('submit', function(event) {
        event.preventDefault(); 
        const key_Size = document.getElementById('key_Size').value;
    
        $.ajax({
            url: '/generate_keys', 
            method: 'POST',
            data: JSON.stringify({ key_size: key_Size }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
    
                    const publicKey = response.publicKey;
                    const privateKey = response.privateKey;
    
                    document.getElementById('publicKey').value = publicKey;
                    document.getElementById('privateKey').value = privateKey;
    
                    // Buat link download public key
                    const pubBlob = new Blob([publicKey], { type: 'application/x-pem-file' });
                    const pubUrl = URL.createObjectURL(pubBlob);
                    const pubLink = document.getElementById('downloadPublicKey');
                    pubLink.href = pubUrl;
                    pubLink.style.display = 'inline';
    
                    // Buat link download private key
                    const privBlob = new Blob([privateKey], { type: 'application/x-pem-file' });
                    const privUrl = URL.createObjectURL(privBlob);
                    const privLink = document.getElementById('downloadPrivateKey');
                    privLink.href = privUrl;
                    privLink.style.display = 'inline';
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Terjadi kesalahan!');
            }
        });
    });


});
