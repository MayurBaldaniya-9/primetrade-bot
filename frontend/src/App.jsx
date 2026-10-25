import { useMemo, useState } from 'react'
import './App.css'

const initialForm = {
  market: 'FUTURES',
  symbol: 'BTCUSDT',
  side: 'BUY',
  type: 'MARKET',
  quantity: '0.001',
  price: '',
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function validateForm(form) {
  const errors = {}

  if (!form.symbol.trim()) {
    errors.symbol = 'Symbol is required'
  }

  if (!['BUY', 'SELL'].includes(form.side)) {
    errors.side = 'Side must be BUY or SELL'
  }

  if (!['MARKET', 'LIMIT'].includes(form.type)) {
    errors.type = 'Order type must be MARKET or LIMIT'
  }

  const quantity = Number(form.quantity)
  if (Number.isNaN(quantity) || quantity <= 0) {
    errors.quantity = 'Quantity must be a valid number greater than zero'
  }

  if (form.type === 'LIMIT') {
    const price = Number(form.price)
    if (form.price === '' || Number.isNaN(price) || price <= 0) {
      errors.price = 'Price must be a valid number greater than zero for LIMIT orders'
    }
  }

  return errors
}

function App() {
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [history, setHistory] = useState([])

  const showPrice = useMemo(() => form.type === 'LIMIT', [form.type])

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const nextErrors = validateForm(form)
    setErrors(nextErrors)
    setResult(null)
    setErrorMessage('')

    if (Object.keys(nextErrors).length > 0) {
      return
    }

    setLoading(true)
    try {
      const payload = {
        market: form.market,
        symbol: form.symbol,
        side: form.side,
        type: form.type,
        quantity: Number(form.quantity),
      }

      if (form.type === 'LIMIT') {
        payload.price = Number(form.price)
      }

      const response = await fetch(`${apiBaseUrl}/api/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        const message = data?.error?.message || 'Order request failed'
        setErrorMessage(message)
        return
      }

      setResult(data.data)
      setHistory((prev) => [
        {
          id: Date.now(),
          status: data.data.status,
          symbol: data.data.symbol,
          side: data.data.side,
          type: data.data.type,
          quantity: data.data.origQty,
        },
        ...prev,
      ].slice(0, 5))
    } catch {
      setErrorMessage('Unable to reach backend service')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      <h1>Primetrade Order Console</h1>
      <p className="subtitle">API: {apiBaseUrl}</p>

      <form className="order-form" onSubmit={handleSubmit}>
        <label>
          Market
          <select name="market" value={form.market} onChange={handleChange}>
            <option value="FUTURES">FUTURES</option>
            <option value="SPOT">SPOT</option>
          </select>
        </label>

        <label>
          Symbol
          <input name="symbol" value={form.symbol} onChange={handleChange} />
          {errors.symbol && <span className="error">{errors.symbol}</span>}
        </label>

        <label>
          Side
          <select name="side" value={form.side} onChange={handleChange}>
            <option value="BUY">BUY</option>
            <option value="SELL">SELL</option>
          </select>
        </label>

        <label>
          Type
          <select name="type" value={form.type} onChange={handleChange}>
            <option value="MARKET">MARKET</option>
            <option value="LIMIT">LIMIT</option>
          </select>
        </label>

        <label>
          Quantity
          <input name="quantity" type="number" step="any" value={form.quantity} onChange={handleChange} />
          {errors.quantity && <span className="error">{errors.quantity}</span>}
        </label>

        {showPrice && (
          <label>
            Price
            <input name="price" type="number" step="any" value={form.price} onChange={handleChange} />
            {errors.price && <span className="error">{errors.price}</span>}
          </label>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Placing order...' : 'Place order'}
        </button>
      </form>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {result && (
        <section>
          <h2>Latest response</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </section>
      )}

      <section>
        <h2>Recent activity</h2>
        {history.length === 0 ? (
          <p>No activity yet.</p>
        ) : (
          <ul>
            {history.map((entry) => (
              <li key={entry.id}>
                {entry.side} {entry.quantity} {entry.symbol} ({entry.type}) - {entry.status}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}

export default App
