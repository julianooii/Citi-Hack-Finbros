import React from 'react'
import './Bot.css'

const Bot = (props) => {
    return (
        <>
            <div className="chat-bubble-bot">
                <div className="chat-bubble-text-bot">
                    <p>{props.message}</p>
                </div>
            </div>
        </>
    )
}

export default Bot