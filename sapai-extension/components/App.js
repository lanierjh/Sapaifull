const App = () => {
  const [messages, setMessages] = React.useState([
    {
      id: 1,
      content: "Hello! I'm your Super Auto Pets Coach.",
      timestamp: new Date().toISOString(),
      isUser: false
    }
  ]);
  
  // Function to add a new message
  const addMessage = (content) => {
    const newMessage = {
      id: messages.length + 1,
      content: content,
      timestamp: new Date().toISOString(),
      isUser: false
    };
    
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };
  
  React.useEffect(() => {
    // For demo purposes, add a new message every few seconds
    const interval = setInterval(() => {
      const demoResponses = [
        "Here's some information you requested...",
        "I've analyzed the data and found interesting patterns.",
        "Based on the latest research, I can tell you that...",
        "The results of your query show the following trends..."
      ];
      
      addMessage(demoResponses[Math.floor(Math.random() * demoResponses.length)]);
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  // This function would be called when receiving messages from your LLM service
  const handleLLMResponse = (response) => {
    addMessage(response);
  };
  
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>SAPAI Coach</h1>
      </header>
      <main className="app-main">
        <ChatHistory messages={messages} />
      </main>
    </div>
  );
}; 