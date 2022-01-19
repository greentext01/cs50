class Homework extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            error: null,
            isLoaded: false,
            assignments: []
        }
    }

    async componentDidMount() {
        const call = await fetch('/api/assignments/')

        try {
            if (!call.ok) {
                this.setState({
                    isLoaded: true,
                    error: call.statusText
                })
            }

            const result = await call.json()

            this.setState({
                isLoaded: true,
                assignments: result
            })
        } catch (error) {
            this.setState({
                isLoaded: true,
                error
            })
        }
    }

    render() {
        const { error, isLoaded, assignments, day } = this.state
        if (error) {
            return <div>Error: {error.message}</div>
        } else if (!isLoaded) {
            return <div>Loading...</div>
        } else {
            return (
                <React.Fragment>
                    {assignments.map((assignment, i) => (
                        <Assignment {...assignment} teacher="" key={i} />
                    ))}
                </React.Fragment>
            )
        }
    }
}


class Assignment extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            checked: props.finished,
        }

        this.onCheck = this.onCheck.bind(this);
    }

    onCheck(e) {
        this.setState({
            checked: e.target.checked
        })

        fetch('/api/finish/', {
            method: 'POST',
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
            body: JSON.stringify({
                finished: e.target.checked,
                assignment: this.props.id,
            }),
            mode: 'same-origin'
        }).catch(error => {
            console.log(error)
        })
    }

    render() {
        const assignment = this.props
        const date = new Date(assignment.due).toDateString()

        return (
            <div className="card my-3">
                <h5 className="card-header">{assignment.subject}</h5>
                <div className="card-body">
                    <p className="text-secondary">Due: {date}</p>
                    <p className="card-text">{assignment.instructions}</p>
                    <div className="form-check">
                        <input onChange={this.onCheck} checked={this.state.checked} className="form-check-input" type="checkbox" id="flexCheckDefault" />
                        <label className="form-check-label">
                            Done
                        </label>
                    </div>
                </div>
            </div>
        )
    }
}

ReactDOM.render(<Homework />, document.querySelector('#homework'))
