const ChatMessage = ({ message }) => {
  const messageClass = message.isUser ? "user-message" : "ai-message";
  
  return (
    <div className={`message ${messageClass}`}>
      <div className="message-content">{message.content}</div>
      <div className="message-timestamp">
        {new Date(message.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}; 