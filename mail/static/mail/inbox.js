document.addEventListener('DOMContentLoaded', function() {
    
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').addEventListener('submit', send_email);
    
    // By default, load the inbox
    load_mailbox('inbox');
});

function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  return false;
}

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none'
    document.querySelector('#compose-view').style.display = 'none';
    
    // Show the mailbox name
    var html = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            html += `    
                <div class="card m-1 ${email.read ? 'bg-lightgray' : ''}" onclick="load_mail(${email.id})">
                    <div class="card-body">
                        <div class="container-fluid">
                            <div class="row">
                                <div class="col"><b>${email.sender}</b></div>
                                <div class="col">${email.subject}</div>
                                <div class="col">
                                    <div class="float-right text-secondary">${email.timestamp}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`
        })
        document.querySelector('#emails-view').innerHTML = html
    })
}

function toggle_archive(id, archived) {
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !archived
        })
    }).then(() => {
        load_mailbox('inbox')
    })
    
}

function load_mail(id) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    
    var html = ''

    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        document.querySelector('#em-reply').addEventListener('click', () => {
            compose_email()
            document.querySelector('#compose-recipients').value = email.sender;
            document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
            document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n------\n`;
        });

        document.querySelector('#em-archive').addEventListener('click', () => {
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !email.archived
                })
            }).then(() => {
                load_mailbox('inbox')
            })
        })
        
        document.querySelector('#em-from').innerHTML = email.sender
        document.querySelector('#em-to').innerHTML = email.recipients
        document.querySelector('#em-subject').innerHTML = email.subject
        document.querySelector('#em-timestamp').innerHTML = email.timestamp
        document.querySelector('#em-archive').innerHTML = email.archived ? 'Unarchive' : 'Archive'
        document.querySelector('#em-body').innerHTML = email.body
    });
}
