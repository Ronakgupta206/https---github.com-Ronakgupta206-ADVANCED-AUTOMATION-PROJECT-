document.addEventListener("DOMContentLoaded", function() {
    const list = document.getElementById('notificationsList');
    if(list.children.length === 0){
        list.innerHTML = "<li>No notifications at the moment.</li>";
    }
});
