import { Link, useNavigate } from "react-router-dom";
import React, { useState } from "react";
import axios from "axios";
import "./Chat.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import Sender from "../sender/Sender";
import Bot from "../bot/Bot";

const Chat = () => {
  const [queries, setQueries] = useState([]);
  const [typing, setTyping] = useState(false);

  const addUserMessage = async (message) => {
    setQueries([...queries, message]);
    setTyping(true);
    const response = await axios.post("http://localhost:80/cypher", {
      query: message,
    });
    const reply = JSON.stringify(`(${response.data.role}) ` + response.data.message);
    setQueries([...queries, message, reply]);
    setTyping(false);
  };
  return (
    <div className="chatContainer">
      <ChatContainer>
        <div className="newChat" as="ConversationHeader">
          Chat with Oracle
        </div>
      </ChatContainer>

      <div style={{ position: "relative", height: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList>

              <Message
                model={{
                  message:
                    "Hello! I am your AI assistant for this session. How can I help you today?",
                }}
              />
              {queries.map((query) => (
                query[1] == "(" ? (
                  <Message
                    model={{
                      message: query.slice(12),
                    }}
                  />
                ) : (
                  <Sender message={query} />
                )
              ))}
            </MessageList>
            {typing ? (
              <MessageInput
                placeholder="Waiting for response..."
                sendDisabled={typing}
                disabled
              />
            ) : (
              <MessageInput
                placeholder="Type message here"
                sendDisabled={typing}
                sendOnReturnDisabled={typing}
                onSend={(e) => addUserMessage(e)}
              />
            )}
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
};
export default Chat;
