function Quiz() {
    const [state, setState] = React.useState({
        questions: [],
        title: '',
        subjects: [],
        divisions: [],
        subject: '',
        division: '',
        due: undefined,
    })


    function addTextQuestion() {
        setState({
            ...state,
            questions: [
                ...state.questions,
                {
                    type: 'text',
                    title: '',
                    answer: ''
                }
            ]
        })
    }


    function addMCQuestion() {
        setState({
            ...state,
            questions: [
                ...state.questions,
                {
                    type: 'multi',
                    title: '',
                    answer: -1,
                    options: []
                }
            ]
        })
    }


    function addOption(question) {
        let questions = state.questions
        questions[question].options.push('')
        setState({
            ...state,
            questions: questions
        })
    }


    function delOption(question, option) {
        let questions = state.questions
        questions[question].options.splice(option, 1)
        setState({
            ...state,
            questions: questions
        })
    }


    function onQuestionChange(event, question, option) {
        let options = state.questions[question].options
        options.splice(option, 1, event.target.value)
        setState({
            ...state,
            questions: [
                ...state.questions
            ]
        })
    }


    function onMultiTitleChange(event, question) {
        let questions = state.questions
        questions[question].title = event.target.value
        setState({
            ...state,
            questions: questions
        })
    }


    function delQuestion(question) {
        let questions = state.questions
        questions.splice(question, 1)
        setState({
            ...state,
            questions: questions
        })
    }


    function changeTextQuestion(event, question) {
        let questions = state.questions
        questions[question].title = event.target.value
        setState({
            ...state,
            questions: questions
        })
    }


    function changeTextAnswer(event, question) {
        let questions = state.questions
        questions[question].answer = event.target.value
        setState({
            ...state,
            questions: questions
        })
    }


    function onSelectAnswer(question, option) {
        let questions = state.questions
        questions[question].answer = option
        setState({
            ...state,
            questions: questions
        })
    }


    function error(message) {
        setState({
            ...state,
            error: message
        })
    }


    React.useEffect(() => {
        fetch('/api/subjects/', {
            credentials: "include"
        })
            .then(res => res.json())
            .then(subjects => {
                fetch('/api/divisions/', {
                    credentials: "include"
                })
                    .then(res => res.json())
                    .then(divisions => setState({
                        ...state,
                        divisions: divisions,
                        subjects: subjects
                    }))
            })
    }, []);




    function save() {
        if (!state.title) {
            error('Quiz does not have a title.')
            return
        }

        if (state.questions.length === 0) {
            error('Quiz does not have any questions.')
            return
        }

        if (!state.subject) {
            error('Please select a subject for this quiz.')
            return
        }

        if (!state.division) {
            error('Please select a division to assign this quiz to.')
            return
        }

        if (!state.due) {
            error('Please select a due date.')
            return
        }

        const duedate = new Date(state.due)

        if (duedate < new Date()) {
            error('Please select a valid due date.')
            return
        }

        for (const [index, question] of state.questions.entries()) {
            if (!question.title) {
                error(`Question ${index + 1} does not have a title.`)
                return
            } else if (question.answer === -1 || question.answer === '') {
                error(`Question ${index + 1} does not have an answer.`)
                return
            }

            if (question.type === 'multi') {
                if (question.options.length === 0) {
                    error(`Question ${index + 1} does not have any options.`)
                    return
                }

                for (const [option_index, option] of question.options.entries()) {
                    if (!option) {
                        error(`Question ${index + 1} > Option ${option_index + 1} does not have an answer.`)
                        return
                    }
                }
            }
        }

        setState({
            ...state,
            error: null
        })

        fetch('/api/createquiz/', {
            method: 'POST',
            headers: {
                'Content-type': 'applicaiton/json',
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            body: JSON.stringify({
                questions: state.questions,
                title: state.title,
                subject: state.subject,
                division: state.division,
                due: duedate.toISOString(),
            }),
            mode: 'same-origin'
        }).then(res => {
            if (res.ok) {
                setState({
                    ...state,
                    success: `${state.title} has been saved!`,
                    error: ''
                })
            } else {
                res.text().then(text => {
                    setState({
                        ...state,
                        error: text,
                    })
                })
            }
        })
    }


    return (
        <div className="m-3">
            <h3>Create quiz</h3>
            {state.error &&
                <div className="alert alert-danger" role="alert">
                    {state.error}
                </div>
            }

            {state.success &&
                <div className="alert alert-success" role="alert">
                    {state.success}
                </div>
            }

            <label className="form-label">Title</label>

            <input type="text" value={state.title}
                onChange={(event) => setState({ ...state, title: event.target.value })}
                className="form-control mb-3" />

            <label className="form-label">Division</label>
            {state.divisions &&
                <select value={state.division} className="form-select mb-3" aria-label="Select division"
                    onChange={(event) => setState({ ...state, division: event.target.value })}>

                    <option disabled value="">----------</option>
                    {state.divisions.map((d) =>
                        <option value={d.key} key={d.key}>{d.name}</option>
                    )}
                </select>
            }

            <label className="form-label">Subject</label>
            {state.subjects &&
                <select value={state.subject} className="form-select mb-3" aria-label="Select division"
                    onChange={(event) => setState({ ...state, subject: event.target.value })}>

                    <option disabled value="">----------</option>
                    {state.subjects.map((d) =>
                        <option value={d.key} key={d.key}>{d.name}</option>
                    )}
                </select>
            }

            <label className="form-label">Due date</label>
            <input type="datetime-local" className="form-control"
                defaultValue={state.due}
                onChange={event => setState({ ...state, due: event.target.value })} />

            {state.questions.map(((question, question_index) => {
                if (question.type === 'text') {
                    return (
                        <div key={question_index}>
                            <hr />
                            <h5>
                                Question {question_index + 1}
                                <button className="btn btn-outline-danger float-end btn-sm" onClick={() => delQuestion(question_index)}>
                                    <TrashSVG size={13} />
                                </button>
                            </h5>
                            <div className="mt-3">
                                <input type="text" className="form-control" id="question" aria-describedby="question" placeholder="Question"
                                    value={question.title} onChange={(event) => changeTextQuestion(event, question_index)} />
                            </div>
                            <div className="mt-3">
                                <input type="text" className="form-control" id="answer" aria-describedby="answer" placeholder="Answer"
                                    value={question.answer} onChange={(event) => changeTextAnswer(event, question_index)} />
                            </div>
                        </div>
                    )
                } else if (question.type === 'multi') {
                    return (
                        <div key={question_index}>
                            <hr />
                            <h5>
                                Question {question_index + 1}
                                <button className="btn btn-outline-danger float-end btn-sm" onClick={() => delQuestion(question_index)}>
                                    <TrashSVG size={13} />
                                </button>
                            </h5>

                            <div className="mt-3">
                                <div className="mt-3">
                                    <input type="text" className="form-control mb-3"
                                        id="question" aria-describedby="question" placeholder="Title" value={question.title}
                                        onChange={(event) => onMultiTitleChange(event, question_index)} />
                                </div>
                                {question.options.map((option, option_index) => (
                                    <div key={option_index}>
                                        <div className="d-flex flex-row bd-highlight mb-3 align-items-center d-flex">
                                            <input type="radio" className="form-check-input me-2" name="answer"
                                                onChange={() => onSelectAnswer(question_index, option_index)}
                                                checked={question.answer === option_index} value={option_index} />

                                            <div className="input-group">
                                                <input type="text" className="form-control" value={option} name={option_index}
                                                    placeholder={'Option ' + (option_index + 1)}
                                                    onChange={(event) => onQuestionChange(event, question_index, option_index)} />
                                                <button className="btn btn-outline-danger" onClick={() => delOption(question_index, option_index)}>
                                                    <TrashSVG size={15} />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                <button className="btn btn-sm btn-primary" onClick={() => addOption(question_index)}>
                                    Add option
                                </button>
                            </div>
                        </div>
                    )
                }
            }))}
            <div>
                <hr />
                <div className="mt-3">
                    <button className="btn btn-primary dropdown-toggle me-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Add question
                    </button>
                    <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                        <li><button className="dropdown-item" onClick={addTextQuestion}>Text question</button></li>
                        <li><button className="dropdown-item" onClick={addMCQuestion}>Multiple choice question</button></li>
                    </ul>
                </div>
            </div>
            <button className="btn btn-primary mt-1" onClick={save}>
                Save
            </button>
        </div>
    )
}


function TrashSVG(props) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" width={props.size} height={props.size} fill="currentColor" className="bi bi-trash-fill" viewBox="0 0 16 16">
            <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z" />
        </svg>
    )
}

ReactDOM.render(<Quiz />, document.querySelector('#quiz'))
