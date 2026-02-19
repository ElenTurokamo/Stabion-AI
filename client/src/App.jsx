import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        text: input
      })

      const botMessage = { role: 'bot', content: response.data.reply }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error(error)
      setMessages(prev => [...prev, { role: 'bot', content: 'Ошибка сервера' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Corporate AI (MVP)</h1>

      <div style={{ 
        height: '400px', 
        border: '1px solid #ccc', 
        overflowY: 'scroll', 
        padding: '10px',
        marginBottom: '10px',
        borderRadius: '8px'
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ 
            textAlign: msg.role === 'user' ? 'right' : 'left',
            margin: '5px 0' 
          }}>
            <span style={{ 
              background: msg.role === 'user' ? '#007bff' : '#f1f1f1',
              color: msg.role === 'user' ? '#fff' : '#000',
              padding: '8px 12px',
              borderRadius: '12px',
              display: 'inline-block'
            }}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && <div>Думаю...</div>}
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          style={{ flex: 1, padding: '10px' }}
          placeholder="Спроси про заявки или клиентов..."
        />
        <button onClick={sendMessage} style={{ padding: '10px 20px' }}>
          Send
        </button>
      </div>
    </div>
  )
}

export default App