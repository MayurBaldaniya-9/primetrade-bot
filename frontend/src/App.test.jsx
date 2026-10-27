import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { vi } from 'vitest'

import App from './App'

describe('App order form', () => {
  it('submits order and shows response and activity', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        success: true,
        data: {
          orderId: 101,
          status: 'FILLED',
          symbol: 'BTCUSDT',
          type: 'MARKET',
          side: 'BUY',
          origQty: '0.001',
          executedQty: '0.001',
          avgPrice: '62000',
        },
      }),
    })

    vi.stubGlobal('fetch', fetchMock)

    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: 'Place order' }))

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
    expect(await screen.findByText(/Latest response/i)).toBeInTheDocument()
    expect(screen.getByText(/Recent activity/i)).toBeInTheDocument()
    expect(screen.getAllByText(/FILLED/i).length).toBeGreaterThan(0)

    vi.unstubAllGlobals()
  })
})
