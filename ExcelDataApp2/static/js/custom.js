document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom JS çalıştı!');
});

// Örnek bir fonksiyon
function greetUser(name) {
    console.log('Merhaba, ' + name + '!');
}
// Kullanıcıyı selamla
greetUser('Ziyaretçi');
// Bir tıklama olayını dinle

document.getElementById('myButton').addEventListener('click', function() {
    alert('Butona tıklandı!');
}
);

// Form gönderimini engelleyen bir fonksiyon
function preventFormSubmission(event) {
    event.preventDefault();
    console.log('Form gönderimi engellendi!');
}