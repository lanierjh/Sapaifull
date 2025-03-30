const App = () => {
  const [messages, setMessages] = React.useState([
    {
      id: 1,
      content: "Hello! I'm your Super Auto Pets Coach. I'll provide advice as you play.",
      timestamp: new Date().toISOString(),
      isUser: false
    }
  ]);
  
  // Function to add a new message
  const addMessage = (content) => {
    const newMessage = {
      id: Date.now(),
      content: content,
      timestamp: new Date().toISOString(),
      isUser: false
    };
    
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };
  
  // Function to request next action
  const requestNextAction = () => {
    // Send a message to the Python backend
    fetch('http://localhost:3000/request_action', {
      method: 'POST',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log("Action requested successfully:", data);
      // Add a user message indicating action was requested
      const userMessage = {
        id: Date.now(),
        content: "Next action please.",
        timestamp: new Date().toISOString(),
        isUser: true
      };
      setMessages(prevMessages => [...prevMessages, userMessage]);
    })
    .catch(error => {
      console.error("Error requesting action:", error);
    });
  };
  
  React.useEffect(() => {
    // Check for messages in localStorage every second
    const checkLocalStorage = () => {
      const storedMessage = localStorage.getItem('sapai-message');
      if (storedMessage) {
        try {
          addMessage(storedMessage);
          // Clear the message after reading it
          localStorage.removeItem('sapai-message');
        } catch (e) {
          console.error("Error processing stored message:", e);
        }
      }
    };
    
    // Check immediately on mount
    checkLocalStorage();
    
    // Then check periodically
    const interval = setInterval(checkLocalStorage, 1000);
    
    return () => {
      // Clean up
      clearInterval(interval);
    };
  }, []);
  
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>SAPAI Coach</h1>
      </header>
      <main className="app-main">
        <ChatHistory messages={messages} />
      </main>
      <footer className="app-footer">
        <button 
          className="action-button" 
          onClick={requestNextAction}
        >
          Get Next Action
        </button>
      </footer>
    </div>
  );
}; 