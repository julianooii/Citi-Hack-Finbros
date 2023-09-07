import React from 'react'
import './Sender.css'

const Sender = (props) => {
    return (
        <>
            <div className="chat-bubble">
                <div className="chat-bubble-text">
                    <p>{props.message}</p>
                </div>
            </div>
        </>
    )
}

export default Sender