followbtn = document.querySelector('#follow');

if (followbtn) {
    followbtn.addEventListener('click', event => {
        fetch(`/follow/${event.target.dataset.profile}`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: !(event.target.dataset.following === "true")
            }),
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
    
        }).then(() => {
            location.reload();
        }).catch(error => {
            console.log(error);
        });
    });
}
