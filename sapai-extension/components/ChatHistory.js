const ChatHistory = ({ messages }) => {
  const chatEndRef = React.useRef(null);
  
  React.useEffect(() => {
    // Scroll to bottom whenever messages change
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);
  
  return (
    <div className="chat-history">
      {messages.map(message => (
        <ChatMessage key={message.id} message={message} />
      ))}
      <div ref={chatEndRef} />
    </div>
  );
}; 