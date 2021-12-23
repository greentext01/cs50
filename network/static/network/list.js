function Post(props) {
    const [state, setState] = React.useState({
        editing: false,
        content: props.content,
        likes: props.likes
    })

    function edit() {
        setState({
            ...state,
            editing: true,
        })
    }

    function saveEdit() {
        setState({
            ...state,
            editing: false
        })

        fetch(`/edit/${props.id}`, {
            method: 'POST',
            body: JSON.stringify({
                content: state.content
            }),
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
        })
    }

    function updateEdit(event) {
        setState({
            ...state,
            content: event.target.value
        })
    }

    function renderEditBtn() {
        if (props.editable == "true") {
            if (state.editing) {
                return <button className="btn btn-primary" onClick={saveEdit}>Save</button>
            } else {
                return <button className="btn btn-primary" onClick={edit}>Edit</button>
            }
        }
    }

    function renderContent() {
        if (state.editing) {
            return <textarea className="form-control" onChange={updateEdit} value={state.content}></textarea>
        } else {
            return <pre>{state.content}</pre>
        }
    }

    return (
        <div>
            <div className="container-fluid">
                <div className="row">
                    <div className="col p-0">
                        <a href={"/profile/" + props.owner}>
                            <h4 className="d-inline">{props.owner}</h4>
                        </a>
                    </div>
                    <div className="col p-0">
                        <div className="float-right">
                            {renderEditBtn()}
                        </div>
                    </div>
                </div>
            </div>
            <div className="text-secondary">{props.timestamp}</div>
            <div className="content">
                {renderContent()}
            </div>
            <LikeCounter liked={props.likes.includes(props.user)} likecount={props.likes.length} id={props.id} user={props.user} />
        </div>
    )
}


function LikeCounter(props) {
    const [state, setState] = React.useState({
        liked: props.liked,
        likecount: props.likecount
    })

    function setLiked(liked) {
        fetch(`/like/${props.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: liked
            }),
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(() => {
            fetch(`/get-likes/${props.id}`).then(result => result.text()).then(response => {
                setState({
                    ...state,
                    liked: liked,
                    likecount: parseInt(response)
                })
            })
        })
    }

    function like() {
        setLiked(true)
    }
    
    function unlike() {        
        setLiked(false)
    }

    if (props.user) {
        if (state.liked) {
            return <button type="button" className="btn btn-primary mt-2" onClick={unlike}>{state.likecount}❤</button>
        } else {
            return <button type="button" className="btn btn-outline-primary mt-2" onClick={like}>{state.likecount}❤</button>
        }
    } else {
        return <div>{state.likecount}❤</div>
    }

}


document.querySelectorAll('.post').forEach(item => {
    ReactDOM.render(<Post {...JSON.parse(item.dataset.post)} editable={item.dataset.editable} user={item.dataset.user} id={item.dataset.id} />, item)
})