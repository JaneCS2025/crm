import { useState } from 'preact/hooks'
import './app.css'
import User from './componennts/User'

export function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <User/>
    </>
  )
}
