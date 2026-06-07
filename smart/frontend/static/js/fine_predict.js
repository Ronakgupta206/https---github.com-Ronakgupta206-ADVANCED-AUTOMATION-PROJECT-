document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('fineForm');

    form.addEventListener('submit', function(e) {
        const days = form.days_late.value;
        if(days <= 0){
            alert("Days late must be greater than 0!");
            e.preventDefault();
        }
    });
});
