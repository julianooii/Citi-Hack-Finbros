import { Link, useNavigate } from "react-router-dom";
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

const Chat = () => {
  return (
    // <div style={{ position: "relative" }}>
    //   <ChatContainer>
    //     {/* <div class = "cs-chat-container my-chat-container"> */}
    //     <div as="ConversationHeader">New Chat</div>
    //     {/* <MessageInput/> */}
    //     {/* <button>Custom button</button> */}
    //     {/* </div> */}
    //   </ChatContainer>
    //   <div style={{ position: "relative", height: "500px" }}>
    //     <MainContainer>
    //       <ChatContainer>
    //         <MessageList>
    //           <Message
    //             model={{
    //               message: "Hello",
    //               sentTime: "just now",
    //               sender: "Joe",
    //             }}
    //           />
    //         </MessageList>
    //         <MessageInput placeholder="Type message here" />
    //       </ChatContainer>
    //     </MainContainer>
    //   </div>
    // </div>

    <div className="chatContainer">
      <ChatContainer>
        <div className="newChat" as="ConversationHeader">New Chat</div>
      </ChatContainer>

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
  );
};
export default Chat;
