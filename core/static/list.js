class Periods extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            error: null,
            isLoaded: false,
            periods: [],
            selected: null,
            day: 1
        }

        this.setPeriods = this.setPeriods.bind(this)
    }

    async setPeriods(day) {
        this.setState({
            day
        })

        try {
            const call = await fetch(`/api/periods/${day}`)

            if (!call.ok) {
                this.setState({
                    isLoaded: true,
                    error: call.statusText
                })
            }

            const result = await call.json()

            this.setState({
                isLoaded: true,
                periods: result
            })
        } catch (error) {
            this.setState({
                isLoaded: true,
                error
            })
        }
    }

    reload() {
        console.log(this.state)
        this.setPeriods(this.state.day);
    }

    async componentDidMount() {
        const d = new Date()
        let day = Math.min(Math.max(d.getDay(), 1), 5)

        this.setPeriods(day)
    }

    onNextClicked() {
        if (this.state.day + 1 > 5) {
            this.setPeriods(1)
        } else {
            this.setPeriods(this.state.day + 1)
        }

        this.setState({
            selected: null
        });
    }

    onPrevClicked() {
        if (this.state.day - 1 < 1) {
            this.setPeriods(5)
        } else {
            this.setPeriods(this.state.day - 1)
        }

        this.setState({
            selected: null
        });
    }

    render() {
        const { error, isLoaded, periods, day } = this.state
        if (error) {
            return <div>Error: {error.message}</div>
        } else if (!isLoaded) {
            return <div>Loading...</div>
        } else {
            return (
                <React.Fragment>
                    <nav className="align-items-center d-flex justify-content-center">
                        <ul className="pagination m-2">
                            <li className="page-item" onClick={() => this.onPrevClicked()}>
                                <a className="page-link user-select-none" aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            <li className="page-item"><a className="page-link user-select-none">{day}</a></li>
                            <li className="page-item" onClick={() => this.onNextClicked()}>
                                <a className="page-link user-select-none" aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                    <div className="background">
                        {periods.map((item, i) => (
                            <div onClick={() => this.setState({ selected: i })} key={i}>
                                <Period onClick selected={i === this.state.selected} {...item} reload={this.reload.bind(this)} isTeacher={this.props.isTeacher} />
                            </div>
                        ))}
                    </div>
                </React.Fragment>
            )
        }
    }
}


function Period(props) {
    function delPeriod() {
        fetch(`/api/delete-period/${props.id}`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
            mode: 'same-origin'
        }).then(() => {
            props.reload()
        })
    }

    return (
        <div className="period align-items-center d-flex justify-content-center user-select-none"
            style={{ backgroundColor: props.color, height: props.duration * 99, top: (props.time - 1) * 100 }}>

            <div>
                <div className="period-name">{props.name}</div>
                <div className="sub">{props.room}</div>
                <div className="sub">{props.teacher}</div>
            </div>

            {props.selected && props.teacher && props.isTeacher && (
                <div className="m-2" onClick={delPeriod}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-trash-fill" viewBox="0 0 16 16">
                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z" />
                    </svg>
                </div>
            )}
        </div>
    )
}

ReactDOM.render(<Periods isTeacher={document.querySelector('#periods').dataset.teacher === 'true'} />, document.querySelector('#periods'))