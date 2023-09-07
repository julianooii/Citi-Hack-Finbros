import { Link, useNavigate } from "react-router-dom";
import "./Chat.css"
 import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
 import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";

 const Chat = () => {

    return(
        <div style={{ position: "relative", height: "500px" }}>
            {/* <ChatContainer> */}
{/* 
            <div class = "cs-chat-container my-chat-container">
                <div as = "ConversationHeader">My custom conversation header</div>
                <MessageInput/>
                <button>Custom button</button>
                </div> */}
            {/* </ChatContainer> */}
  {/* <MainContainer>
    <ChatContainer>
      <MessageList>
        <Message
          model={{
            message: "Hello my friend",
            sentTime: "just now",
            sender: "Joe",
          }}
        />
      </MessageList>
      <MessageInput placeholder="Type message here" />
    </ChatContainer>
  </MainContainer> */}
  <div style={{ position: "relative", height: "500px" }}>
  <MainContainer>
    <ChatContainer>
      <MessageList>
        <Message
          model={{
            message: "Hello",
            sentTime: "just now",
            sender: "Joe",
          }}
        />
      </MessageList>
      <MessageInput placeholder="Type message here" />
    </ChatContainer>
  </MainContainer>
</div>
</div>
    )
}
export default Chat