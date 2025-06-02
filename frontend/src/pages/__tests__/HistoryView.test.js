import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom'; // Needed because HistoryView uses <Link>
import HistoryView from '../HistoryView';
import { server } from '../../mocks/server';
import { handlers } from '../../mocks/handlers'; // Default handlers
import { http, HttpResponse } from 'msw';

// MSW server setup is in setupTests.js

describe('HistoryView Page', () => {
  beforeEach(() => {
    server.resetHandlers(...handlers); // Reset to default handlers
  });

  test('renders loading state initially', () => {
    render(
      <MemoryRouter>
        <HistoryView />
      </MemoryRouter>
    );
    expect(screen.getByText(/Loading history.../i)).toBeInTheDocument();
  });

  test('displays list of prompts after successful fetch', async () => {
    render(
      <MemoryRouter>
        <HistoryView />
      </MemoryRouter>
    );

    // Wait for mock API call to resolve and component to update
    await waitFor(() => {
      expect(screen.getByText('History prompt 1')).toBeInTheDocument();
      expect(screen.getByText('History prompt 2')).toBeInTheDocument();
    });

    // Check links
    expect(screen.getByText('History prompt 1').closest('a')).toHaveAttribute('href', '/history/1');
  });

  test('displays error message if API call fails', async () => {
    server.use(
      http.get('http://localhost:8000/history/prompts', () => {
        return HttpResponse.json({ detail: 'Failed to fetch (mocked)' }, { status: 500 });
      })
    );

    render(
      <MemoryRouter>
        <HistoryView />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Error loading history:/i)).toBeInTheDocument();
      expect(screen.getByText(/Failed to fetch history. Details: Failed to fetch \(mocked\)/i)).toBeInTheDocument();
    });
  });

  test('displays "No history found" message if API returns empty list', async () => {
    server.use(
      http.get('http://localhost:8000/history/prompts', () => {
        return HttpResponse.json([]); // Empty list
      })
    );

    render(
      <MemoryRouter>
        <HistoryView />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/No history found./i)).toBeInTheDocument();
      expect(screen.getByRole('link', { name: /Go to Forge/i})).toBeInTheDocument();
    });
  });
});
